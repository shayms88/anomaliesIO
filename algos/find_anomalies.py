import pandas as pd
import logging

from utils.logger import Log

logger = Log(module_name='find_anomalies')
logging.getLogger('algos.twitter_algo.anomaly_detect_ts').setLevel(logging.ERROR)

from algos.twitter_algo.anomaly_detect_ts import anomaly_detect_ts


class AnomalyDfFields:
    TIMESTAMP = 'timestamp'
    DIMENSION = 'dimension'
    MEASURE = 'measure'


VALID_DATETIME_STR_FORMATS = ['%Y-%m-%d', '%Y-%m-%d %H:%M:%S', '%Y-%m-%dt%H:%M:%S', '%Y-%m-%d %H:%M:%S UTC']


class FindAnomaliesFactory:
    def __init__(self, df, max_anoms=0.1, direction='both', alpha=0.05, only_last=None, plot=False):
        self.df = df
        self.max_anoms = max_anoms
        self.direction = direction
        self.alpha = alpha
        self.only_last = only_last
        self.plot = plot

        # longterm --> if number of dates > 1 months (30 days), set longterm=True

    def assert_df(self):
        if True:
            return True
        else:
            raise (f'DF assertion failed')

    def _get_column_unique_values(self, column_name):
        column_df = self.df[column_name]
        return column_df.unique()

    def _get_anomalies(self, anomaly_series):
        return anomaly_detect_ts(anomaly_series,
                                 direction='both', alpha=0.5,
                                 plot=False, longterm=True,
                                 resampling=True,
                                 max_anoms=self.max_anoms)

    @staticmethod
    def _modify_series_index_to_datetime(pd_series):
        for datetime_format in VALID_DATETIME_STR_FORMATS:
            try:
                pd_series.index = pd.to_datetime(pd_series.index, format=datetime_format)
                # logger.log_debug(f'Found index datetime_format match: {datetime_format}')
            except ValueError as err:
                # logger.log_warning(f'cannot modify {datetime_format} to any of valid formats')
                pass
        return pd_series

    def _group_df_by_dim_and_date(self):
        return self.df.groupby([AnomalyDfFields.TIMESTAMP, AnomalyDfFields.DIMENSION])[AnomalyDfFields.MEASURE] \
            .sum().reset_index()

    @staticmethod
    def _get_timestamps_indexes_for_dim(df, dimension_value):
        return df.loc[df[AnomalyDfFields.DIMENSION] == f'{dimension_value}', AnomalyDfFields.TIMESTAMP]

    @staticmethod
    def _get_values_for_dim(df, dimension_value):
        return df.loc[df[AnomalyDfFields.DIMENSION] == f'{dimension_value}', AnomalyDfFields.MEASURE]

    def generate_series_for_df_dimension_value(self, dimension_value):
        # TODO can improve performance by creating grouped_by_df only once
        grouped_by_df = self._group_df_by_dim_and_date()

        # Generate a pandas-series items per dimension_value
        timestamps_indexes = self._get_timestamps_indexes_for_dim(grouped_by_df, dimension_value)
        values = self._get_values_for_dim(grouped_by_df, dimension_value)

        # Create the pandas series
        anomaly_series = pd.Series(data=values.tolist(), index=timestamps_indexes)
        anomaly_series = self._modify_series_index_to_datetime(anomaly_series)
        return anomaly_series

    @staticmethod
    def _get_series_statistics(series):
        return {
            'total_values': len(series),
            'min_value': min(series),
            'max_value': max(series),
            'avg_value': series.mean(),
            'median_value': series.quantile(.5),
            'upper_90_value': series.quantile(.9)
        }

    def run(self):
        self.assert_df()
        list_of_anomalies = []

        # Rename fields to always be in same format
        self.df.columns = ('timestamp', 'dimension', 'measure')
        dimension_unique_values = self._get_column_unique_values(column_name='dimension')

        for dim_value in dimension_unique_values:
            specific_dim_series = self.generate_series_for_df_dimension_value(dimension_value=dim_value)
            try:
                anomalies = self._get_anomalies(specific_dim_series)
                list_of_anomalies.append(
                    {
                        'dimension_value': dim_value,
                        'anomalies': anomalies,
                        'series_statistics': self._get_series_statistics(specific_dim_series)
                    }
                )
            except AssertionError as assertion_err:
                logger.log_warning(
                    f'could not yield anomaly for dimension: `{dim_value}` due to anomaly_detect_ts assertion error: {assertion_err}')
            except Exception as err:
                logger.log_warning(f'could not yield anomaly for dimension: `{dim_value}`, due to Exception. Error:{err}')
        return list_of_anomalies
