import csv, io
from datetime import datetime

from django.shortcuts import render
from django.contrib import messages
from django.conf import settings

from .anomalies_finder_utils import parse_io_string_to_list_of_lists

def anomalies_finder_main(request):
    if request.method == 'POST':
        file = request.FILES['file']
        if not file.name.endswith('.csv'):
            messages.error(request, 'This is not a CSV file.')

        # Parse and save CSV as file in MEDIA_ROOT dir
        data = file.read().decode('UTF-8')
        io_string = io.StringIO(data)
        file_name = "{}csv_data_{}.csv".format(settings.MEDIA_ROOT, datetime.now().strftime("%Y-%m-%d_%H:%M:%S"))
        with open(file_name, mode='w') as f:
            csv_writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for row in csv.reader(io_string, delimiter=','):
                csv_writer.writerow(row)

    context = {}
    return render(request, 'index.html', context=context)
