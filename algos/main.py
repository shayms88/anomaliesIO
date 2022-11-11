from algos.twitter_algo.anomaly_detect_ts import anomaly_detect_ts

import pandas as pd
from pathlib import Path
import logging

from utils.logger import Log
from utils.pythonic_utils import change_dict_keys_to_str_type, generate_subset_df_from_fields_list, \
    generate_unique_list_values

TEST_DATA_DIR = Path('test_data')
logging.getLogger('anomaly_detection').setLevel(logging.DEBUG)
logger = Log(module_name='faDriver')

CSV_FIELDS_SCHEMA = {
    'dimensions': ['platform', 'browser', 'country', 'continent', 'user_type', 'is_new_user', 'used_web'],
    'measures': ['visits', 'registrations', 'purchases', 'messages']
}
MAX_DIMENSION_FIELD_UNIQUE_VALUES = 4


class FindAnomaliesDriver(object):
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

    def generate_series_for_df_dimension_value(self, df, dimension_value):
        '''
        :param df:
        :param dimension_value:
        :return:
        '''
        # Aggregate data for dim_value
        df = df.groupby(['timestamp', 'dimension'])['measure'].sum().reset_index()
        # Generate a pandas-series items per dimension_value
        timestamps_indexes = df.loc[df['dimension'] == '{}'.format(dimension_value), 'timestamp']
        values = df.loc[df['dimension'] == '{}'.format(dimension_value), 'measure']
        # Create the pandas series
        anomaly_series = pd.Series(data=values.tolist(), index=timestamps_indexes)
        anomaly_series = self.modify_series_index_to_datetime(anomaly_series)
        return anomaly_series

    def generate_results_dict(self, results, anomaly_series,
                              dimension_name, dimension_value, measure_name):
        # Get anomalies results
        results_dict = dict(results.get('anoms'))
        results = results.get('anoms')

        results_dict = change_dict_keys_to_str_type(results_dict)

        anomalies_dict = {
            'dimension_name': dimension_name,
            'dimension_value': dimension_value,
            'measure_name': measure_name,

            'results_dict': results_dict,
            'results_statistics':
                {
                    'total_values': len(anomaly_series),
                    'min_value': min(anomaly_series),
                    'max_value': max(anomaly_series),
                    'avg_value': anomaly_series.mean(),
                    'median_value': anomaly_series.quantile(.5),
                    'upper_90_value': anomaly_series.quantile(.9)
                }
        }
        return anomalies_dict

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

        list_of_anomalies = []
        list_of_skipped_dimensions = []

        # Get only 3 fields (timestamp, dimension, measure)
        for dimension in CSV_FIELDS_SCHEMA.get('dimensions'):
            logger.log_info("    ----  RUNNING FOR DIMENSION: {}  ----    ".format(dimension))
            dimension_name = dimension

            for measure in CSV_FIELDS_SCHEMA.get('measures'):
                measure_name = measure
                anomaly_df = generate_subset_df_from_fields_list(initial_csv_df,
                                                                 fields_list=['timestamp', dimension_name,
                                                                              measure_name])
                # Rename fields
                anomaly_df.columns = ['timestamp', 'dimension', 'measure']
                # Get dimension unique values
                dimension_unique_values = self.get_column_unique_values(df=anomaly_df,
                                                                        column_name='dimension')
                # If `dimension_unique_values` is FALSE, skip this dimension
                # (that means its bigger then max unique values allowed)
                if dimension_unique_values is False:
                    logger.log_info("    ----  SKIPPING DIMENSION: {}    ----    ".format(dimension))
                    list_of_skipped_dimensions.append(dimension)
                    continue

                ########################
                ####   Run Anomaly  ####
                ########################
                for dimension_value in dimension_unique_values:
                    anomaly_series = self.generate_series_for_df_dimension_value(df=anomaly_df,
                                                                                 dimension_value=dimension_value)

                    # Run anomaly detection
                    try:
                        results = anomaly_detect_ts(anomaly_series,
                                                    direction='both', alpha=0.5,
                                                    plot=False, longterm=True,
                                                    resampling=True)

                        anomalies_dict = self.generate_results_dict(results, anomaly_series,
                                                                    dimension_name, dimension_value, measure_name)
                        print()
                        logger.log_info(
                            "####    DIMENSION: {}  |"
                            "  DIMENSION_VALUE: {}  |"
                            "  MEASURE: {}  |    ####".format(dimension_name, dimension_value, measure_name))
                        logger.log_info("Found {} anomalies".format(len(results['anoms'])))

                        list_of_anomalies.append(anomalies_dict)

                    except Exception as err:
                        print(err)

        list_of_skipped_dimensions = generate_unique_list_values(list_of_skipped_dimensions)
        logger.log_critical("Dimensions Skipped: [{} Total] {}".format(len(list_of_skipped_dimensions),
                                                                       list_of_skipped_dimensions))

        for anomaly in list_of_anomalies:
            print("###   DIMENSION: {}  |  DIMENSION VALUE: {}  |  MEASURE: {}  |"
                  "  Anomalies: {}   ###".format(anomaly.get('dimension_name'), anomaly.get('dimension_value'),
                                                 anomaly.get('measure_name'), len(anomaly.get('results_dict'))))

            print("Results Statistics:\n{}".format(anomaly.get('results_statistics')))
            print()
            print()


driver = FindAnomaliesDriver()
driver.run_twitter_algo('/Users/shay.misgav/Documents/Shay Projects/anomaliesIO/algos/test_data/simple_data.csv')
