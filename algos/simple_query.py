import pandas as pd
from utils.logger import Log
logger = Log(module_name='anomaly_detection_main')

from algos.find_anomalies import FindAnomaliesFactory


class FindAnomalySimpleCase:
    def __init__(self, data):
        """

        Parameters
        ----------
        data {str} path to local csv/json file or a pandas.pd object
        """
        self.data = data

    def assert_df(self):
        df = self.convert_data_to_df()
        assert isinstance(df, pd.Series), 'data must be a series(Pandas.Series)'
        assert df.values.dtype in [int, float], 'Values of the series must be number'

    def _get_file_type(self):
        return type(self.data)

    def _generate_df_from_data_source(self, file_type):
        if file_type == 'df':
            df = self.data
        elif file_type == 'csv':
            df = pd.read_csv(self.data)
        elif file_type == 'json':
            df = pd.read_json(self.data)
        else:
            raise(f'file_type: `{file_type} is not supported`')
        return df

    def convert_data_to_df(self, file_type='csv'):
        if not file_type:
            try:
                file_type = self._get_file_type(self.data)
            except Exception as err:
                raise(f'Could not get file_type. Error: {err}')

        return self._generate_df_from_data_source(file_type)

    def find_columns_types(self):
        pass

    def find_anomaly(self):
        anomaly_factory = FindAnomaliesFactory(self.data)
        anomalies_found = anomaly_factory.run()

    def run(self):
        self.assert_df()


driver = FindAnomalySimpleCase(data='/Users/shay.misgav/Documents/Shay Projects/anomaliesIO/algos/test_data/simple_data.csv',)
driver.run()