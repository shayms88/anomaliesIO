import pandas as pd

from utils.logger import Log
logger = Log(module_name='anomaly_detection_main')

from utils.pythonic_utils import generate_subset_df_from_fields_list
from algos.find_anomalies import FindAnomaliesFactory


MAX_DIMENSION_FIELD_UNIQUE_VALUES = 4
RESULTS_FIELDS_ORDER = ['dimension_name', 'measure_name', 'dimension_value', 'anomalies', 'anomalies_expected_results', 'series_statistics']


class OutputFormats:
    LIST = 'list'
    DF = 'df'


class AnomaliesFinder:
    def __init__(self, data, csv_columns_schema: dict, output_format: str = OutputFormats.LIST):
        self.data = data
        self.csv_columns_schema = csv_columns_schema
        self.output_format = output_format

    @staticmethod
    def get_column_unique_values(df, column_name):
        column_df = df[column_name]
        unique_values_list = column_df.unique()
        if len(unique_values_list) > MAX_DIMENSION_FIELD_UNIQUE_VALUES:
            return False
        else:
            return unique_values_list

    @staticmethod
    def _enrich_anomalies_results(anomalies_found, dimension_name, measure_name):
        for a in anomalies_found:
            a['dimension_name'] = dimension_name
            a['measure_name'] = measure_name

        return anomalies_found

    @staticmethod
    def get_df_from_csv(file_path):
        df = pd.read_csv(file_path)
        return df

    @staticmethod
    def get_df_headers_dtypes(df):
        headers_dtypes_raw = df.columns.to_series().groupby(df.dtypes).groups
        headers_dtypes = {k.name: v for k, v in headers_dtypes_raw.items()}
        return headers_dtypes

    def _format_results(self, final_list_of_anomalies):
        if self.output_format == OutputFormats.LIST:
            return final_list_of_anomalies
        elif self.output_format == OutputFormats.DF:
            return pd.DataFrame(final_list_of_anomalies)
        else:
            logger.log_error(f'output format: `{self.output_format}` is not supported')

    @staticmethod
    def _print_final_results(results):
        beautified_results = results.reindex(columns=RESULTS_FIELDS_ORDER)
        print(f'Total anomalies found: {len(beautified_results)}')
        return beautified_results

    def run(self):
        # Load DF
        logger.log_info("Reading CSV file")
        initial_csv_df = pd.read_csv(self.data)

        # For each dimension and each measure, find anomalies
        final_list_of_anomalies = []
        dimensions = self.csv_columns_schema.get('dimensions')
        measures = self.csv_columns_schema.get('measures')

        for dimension in dimensions:
            logger.log_info(f'---- RUNNING FOR DIMENSION: `{dimension}`')
            dimension_name = dimension

            for measure in measures:
                measure_name = measure
                dim_and_measure_subset_df = generate_subset_df_from_fields_list(initial_csv_df,
                                                                                fields_list=['timestamp',
                                                                                             dimension_name,
                                                                                             measure_name])

                anomaly_factory = FindAnomaliesFactory(dim_and_measure_subset_df)
                anomalies_found = anomaly_factory.run()
                logger.log_info(f'{len(anomalies_found)} anomalies found for measure `{measure}`')
                anomalies_found_enriched = self._enrich_anomalies_results(anomalies_found, dimension_name, measure_name)
                final_list_of_anomalies.extend(anomalies_found_enriched)

        results = self._format_results(final_list_of_anomalies)
        self._print_final_results(results)
        return results
