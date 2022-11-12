import pandas as pd
from pathlib import Path
import logging

from utils.logger import Log
from utils.pythonic_utils import change_dict_keys_to_str_type, generate_subset_df_from_fields_list, \
    generate_unique_list_values
from algos.find_anomalies import FindAnomaliesFactory


TEST_DATA_DIR = Path('test_data')
# logging.getLogger('anomaly_detection').setLevel(logging.DEBUG)
logger = Log(module_name='anomaly_detection_main')

CSV_FIELDS_SCHEMA = {
    'dimensions': ['platform', 'browser', 'country', 'continent', 'user_type', 'is_new_user', 'used_web'],
    'measures': ['visits', 'registrations', 'purchases', 'messages']
}
MAX_DIMENSION_FIELD_UNIQUE_VALUES = 4


class FindAnomalyDetectionEngine:
    def __init__(self):
        pass

    def get_column_unique_values(self, df, column_name):
        column_df = df[column_name]
        unique_values_list = column_df.unique()
        if len(unique_values_list) > MAX_DIMENSION_FIELD_UNIQUE_VALUES:
            return False
        else:
            return unique_values_list

    def generate_dimensions_and_measures(self):
        '''
        :param df:
        :return: {dict} dimension and measures column that we get on the CSV.
                        dimension will be all string (`object` in df) & BOOLEAN field types
                        measure will be all the INT/FLOAT field types
        '''

        return CSV_FIELDS_SCHEMA

    def modify_series_index_to_datetime(self, df):
        logger.log_debug("Modifying series index to datetime64")
        valid_datetime_str_formats = ['%Y-%m-%d', '%Y-%m-%d %H:%M:%S', '%Y-%m-%dt%H:%M:%S', '%Y-%m-%d %H:%M:%S UTC']
        for datetime_format in valid_datetime_str_formats:
            try:
                df.index = pd.to_datetime(df.index, format=datetime_format)
                logger.log_debug("Found index datetime_format match: {}".format(datetime_format))
            except ValueError:
                pass

        return df

    @staticmethod
    def _enrich_anomalies_results(anomalies_found, dimension_name, measure_name):
        for a in anomalies_found:
            a['dimension_name'] = dimension_name
            a['measure_name'] = measure_name

        return anomalies_found

    def get_df_from_csv(self, file_path):
        df = pd.read_csv(file_path)
        return df

    def get_df_headers_dtypes(self, df):
        headers_dtypes_raw = df.columns.to_series().groupby(df.dtypes).groups
        headers_dtypes = {k.name: v for k, v in headers_dtypes_raw.items()}
        return headers_dtypes

    def run_twitter_algo(self, file_path):
        #######################
        ####   Prepare DF  ####
        #######################
        logger.log_info("Reading CSV file")
        initial_csv_df = pd.read_csv(file_path)

        final_list_of_anomalies = []
        list_of_skipped_dimensions = []

        # Get only 3 fields (timestamp, dimension, measure)
        for dimension in CSV_FIELDS_SCHEMA.get('dimensions'):
            dimension_anomalies_counter = 0
            logger.log_info("    ----  RUNNING FOR DIMENSION: {}  ----    ".format(dimension))
            dimension_name = dimension

            for measure in CSV_FIELDS_SCHEMA.get('measures'):
                measure_name = measure
                dim_and_measure_subset_df = generate_subset_df_from_fields_list(initial_csv_df,
                                                                 fields_list=['timestamp', dimension_name, measure_name])
                anomaly_factory = FindAnomaliesFactory(dim_and_measure_subset_df)
                anomalies_found = anomaly_factory.run()
                print(f"LEN ANOMS FOUND {len(anomalies_found)}")
                anomalies_found_enriched = self._enrich_anomalies_results(anomalies_found, dimension_name, measure_name)
                final_list_of_anomalies.extend(anomalies_found_enriched)

        print(f"Total anomalies found: {len(final_list_of_anomalies)}")

driver = FindAnomalyDetectionEngine()
driver.run_twitter_algo('/Users/shay.misgav/Documents/Shay Projects/anomaliesIO/algos/test_data/simple_data.csv')
