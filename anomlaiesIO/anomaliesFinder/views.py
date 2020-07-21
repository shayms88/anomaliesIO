import csv, io

from django.shortcuts import render
from django.contrib import messages



def anomalies_finder_main(request):
    if request.method == 'POST':
        file = request.FILES['file']
        if not file.name.endswith('.csv'):
            messages.error(request, 'This is not a CSV file.')

        data = file.read().decode('UTF-8')
        io_string = io.StringIO(data)
        # Get file column names
        for row in csv.reader(io_string, delimiter=','):
            print(row)


    context = {}
    return render(request, 'index.html', context=context)
