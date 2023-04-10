from algos.get_anomalies.get_anomalies_from_csv import AnomaliesFinder


CSV_FIELDS_SCHEMA = {
    'dimensions': ['platform', 'browser', 'country', 'continent', 'user_type', 'is_new_user', 'used_web'],
    'measures': ['visits', 'registrations', 'purchases', 'messages']
}

driver = AnomaliesFinder(data='/Users/shay.misgav/Documents/Shay Projects/anomaliesIO/algos/test_data/simple_data.csv',
                         csv_columns_schema=CSV_FIELDS_SCHEMA,
                         output_format='df')
anomalies = driver.run()
print(anomalies)
