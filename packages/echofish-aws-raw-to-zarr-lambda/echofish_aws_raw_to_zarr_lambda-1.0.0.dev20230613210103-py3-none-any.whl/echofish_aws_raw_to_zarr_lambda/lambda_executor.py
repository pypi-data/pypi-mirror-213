import os
import glob
import shutil
import echopype as ep
import boto3
import botocore
import numpy as np
import pandas as pd
import geopandas
from datetime import datetime
from botocore.config import Config
from botocore.exceptions import ClientError


class LambdaExecutor:

    def __init__(self, s3_operations, dynamo_operations, input_bucket, output_bucket, table_name, output_bucket_access_key, output_bucket_secret_access_key):
        self.__s3 = s3_operations
        self.__dynamo = dynamo_operations
        self.__input_bucket = input_bucket
        self.__output_bucket = output_bucket
        self.__table_name = table_name
        self.__output_bucket_access_key = output_bucket_access_key
        self.__output_bucket_secret_access_key = output_bucket_secret_access_key

    def __delete_all_local_raw_and_zarr_files(self):
        # Used to cleanse the system of any ephemeral files
        for i in ['*.raw*', '*.zarr']:
            for j in glob.glob(i):
                f'Deleting {j}'
                if os.path.isdir(j):
                    shutil.rmtree(j, ignore_errors=True)
                elif os.path.isfile(j):
                    os.remove(j)


    def __set_processing_status(self, ship_name, cruise_name, sensor_name, file_name, new_status):
        # Updates PIPELINE_STATUS via new_status value
        # HASH: FILE_NAME, RANGE: SENSOR_NAME
        self.__dynamo.put_item(
            self.__table_name,
            {
                'FILE_NAME': {'S': file_name},  # HASH
                'SHIP_NAME': {'S': ship_name},
                'CRUISE_NAME': {'S': cruise_name},
                'SENSOR_NAME': {'S': sensor_name},  # RANGE
                'PIPELINE_TIME': {'S': datetime.now().isoformat(timespec="seconds") + "Z"},
                'PIPELINE_STATUS': {'S': new_status},  # TODO: change to enum
            }
        )

    def __update_processing_status(self, cruise_name, file_name, new_status):
        self.__dynamo.update_item(
            self.__table_name,
            {
                'FILE_NAME': {'S': file_name},  # Partition Key
                'CRUISE_NAME': {'S': cruise_name},  # Sort Key
            },
            {
                '#PS': 'PIPELINE_STATUS'
            },
            {
                ':ps': {
                    'S': new_status
                }
            },
            'SET #PS = :ps'
        )


    def __get_processing_status(self, file_name, cruise_name):
        # HASH: FILE_NAME, RANGE: SENSOR_NAME
        item = self.__dynamo.get_item(
            self.__table_name,
            {
                'FILE_NAME': {'S': file_name},  # Partition Key
                'CRUISE_NAME': {'S': cruise_name},  # Sort Key
            })
        if item is None:
            return 'NONE'
        return item['PIPELINE_STATUS']['S']

    def __zarr_info_to_table(self, cruise_name, file_name, zarr_path, min_echo_range, max_echo_range, num_ping_time_dropna, start_time, end_time, frequencies, channels):
        self.__dynamo.update_item(
            self.__table_name,
            {
                'FILE_NAME': {'S': file_name},  # Partition Key
                'CRUISE_NAME': {'S': cruise_name},  # Sort Key
            },
            {
                '#ZB': 'ZARR_BUCKET',
                '#ZP': 'ZARR_PATH',
                '#MINER': 'MIN_ECHO_RANGE',
                '#MAXER': 'MAX_ECHO_RANGE',
                '#P': 'NUM_PING_TIME_DROPNA',
                '#ST': 'START_TIME',
                '#ET': 'END_TIME',
                '#F': 'FREQUENCIES',
                '#C': 'CHANNELS',
            },
            {
                ':zb': {
                    'S': self.__output_bucket
                },
                ':zp': {
                    'S': zarr_path
                },
                ':miner': {
                    'N': str(np.round(min_echo_range, 4))
                },
                ':maxer': {
                    'N': str(np.round(max_echo_range, 4))
                },
                ':p': {
                    'N': str(num_ping_time_dropna)
                },
                ':st': {
                    'S': start_time
                },
                ':et': {
                    'S': end_time
                },
                ':f': {
                    'L': [{'N': str(i)} for i in frequencies]
                },
                ':c': {
                    'L': [{'S': i} for i in channels]
                }
            },
            'SET #ZB = :zb, #ZP = :zp, #MINER = :miner, #MAXER = :maxer, #P = :p, #ST = :st, #ET = :et, #F = :f, #C = :c'
        )


    def __create_local_zarr_store(self, raw_file_name, cruise_name, sensor_name, output_zarr_prefix, store_name):
        print(f'Opening raw: {raw_file_name}')
        echodata = ep.open_raw(raw_file_name, sonar_model=sensor_name)
        print('Compute volume backscattering strength (Sv) from raw data.')
        ds_Sv = ep.calibrate.compute_Sv(echodata)
        frequencies = echodata.environment.frequency_nominal.values
        assert(
            'latitude' in echodata.platform.variables and 'longitude' in echodata.platform.variables
        ), "GPS coordinates not found."
        latitude = echodata.platform.latitude.values
        longitude = echodata.platform.longitude.values  # len(longitude) == 14691
        # RE time coordinates: https://github.com/OSOceanAcoustics/echopype/issues/656#issue-1219104771
        nmea_times = echodata.platform.time1.values  # len(nmea_times) == 14691
        time1 = echodata.environment.time1.values  # len(sv_times) == 9776
        # Because of differences in measurement frequency, figure out where sv_times match up to nmea_times
        assert(
            np.all(time1[:-1] <= time1[1:]) and np.all(nmea_times[:-1] <= nmea_times[1:])
        ), "NMEA time stamps are not sorted."
        indices = nmea_times.searchsorted(time1, side="right") - 1
        lat = latitude[indices]
        lat[indices < 0] = np.nan  # values recorded before indexing are set to nan
        lon = longitude[indices]
        lon[indices < 0] = np.nan
        # https://osoceanacoustics.github.io/echopype-examples/echopype_tour.html
        gps_df = pd.DataFrame({'latitude': lat, 'longitude': lon, 'time1': time1}).set_index(['time1'])
        gps_gdf = geopandas.GeoDataFrame(
            gps_df,
            geometry=geopandas.points_from_xy(gps_df['longitude'], gps_df['latitude']),
            crs="epsg:4326"
        )
        # Returns a FeatureCollection with IDs as "time1"
        geo_json = gps_gdf.to_json()
        min_echo_range = float(np.nanmin(ds_Sv.echo_range.values[np.nonzero(ds_Sv.echo_range.values)]))
        max_echo_range = float(np.nanmax(ds_Sv.echo_range))
        num_ping_time_dropna = gps_df.dropna().shape[0]
        start_time = np.datetime_as_string(ds_Sv.ping_time.values[0], unit='ms') + "Z"
        end_time = np.datetime_as_string(ds_Sv.ping_time.values[-1], unit='ms') + "Z"
        channels = list(ds_Sv.channel.values)
        print('Creating Zarr')
        #
        # TODO: will this crash if it doesn't write to /tmp directory
        #
        ds_Sv.to_zarr(store=store_name)
        print('Note: Adding GeoJSON inside Zarr store')
        with open(os.path.join(store_name, 'geo.json'), "w") as outfile:
            outfile.write(geo_json)
        self.__zarr_info_to_table(cruise_name, raw_file_name, output_zarr_prefix, min_echo_range, max_echo_range, num_ping_time_dropna, start_time, end_time, frequencies, channels)

    def __remove_existing_s3_zarr_store(self, output_zarr_prefix):
        for key in self.__s3.list_objects(self, self.__output_bucket, output_zarr_prefix, access_key=self.__output_bucket_access_key, secret_access_key=self.__output_bucket_secret_access_key):
            self.__s3.delete(self.__output_bucket, key, access_key=None, secret_access_key=None)

    def __upload_files(self, local_directory, object_prefix):
        for subdir, dirs, files in os.walk(local_directory):
            for file in files:
                local_path = os.path.join(subdir, file)
                print(local_path)
                s3_key = os.path.join(object_prefix, local_path)
                self.__s3.upload_file(local_path, self.__output_bucket, s3_key, access_key=self.__output_bucket_access_key, secret_access_key=self.__output_bucket_secret_access_key)

    def execute(self, message):

        ship_name = message['shipName']
        cruise_name = message['cruiseName']
        sensor_name = message['sensorName']
        file_name = message['fileName']

        print(f"Processing: {file_name}")
        processing_status = self.__get_processing_status(file_name, cruise_name)
        if processing_status == 'SUCCESS':
            print('Already processed, skipping...')
        else:
            bucket_key = f'data/raw/{ship_name}/{cruise_name}/{sensor_name}/{file_name}'
            self.__set_processing_status(ship_name, cruise_name, sensor_name, file_name, "PROCESSING")
            self.__delete_all_local_raw_and_zarr_files()
            self.__s3.download_file(self.__input_bucket, bucket_key, file_name)
            store_name = f"{os.path.splitext(file_name)[0]}.zarr"
            output_zarr_prefix = f'level_1/{ship_name}/{cruise_name}/{sensor_name}/{store_name}/'
            self.__create_local_zarr_store(file_name, cruise_name, sensor_name, output_zarr_prefix, store_name)
            self.__remove_existing_s3_zarr_store(output_zarr_prefix)
            self.__upload_files(store_name, output_zarr_prefix)
            self.__update_processing_status(cruise_name, file_name, 'SUCCESS')
            self.__delete_all_local_raw_and_zarr_files()
        print(f'Done processing {file_name}')

