import csv, io
from datetime import datetime

from django.conf import settings


def parse_and_write_uploaded_csv(csv_data):
    try:
        io_string = io.StringIO(csv_data)
        file_name = "{}csv_data_{}.csv".format(settings.MEDIA_ROOT, datetime.now().strftime("%Y-%m-%d_%H:%M:%S"))
        with open(file_name, mode='w') as f:
            csv_writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for row in csv.reader(io_string, delimiter=','):
                csv_writer.writerow(row)
        return file_name

    except Exception as err:
        print("Error when parsing CSV:\n{}".format(err))