from django.shortcuts import render
from django.contrib import messages

from algos.twitter_algo import FindAnomaliesDriver
from .anomalies_finder_utils import parse_and_write_uploaded_csv

def anomalies_finder_main(request):
    fad = FindAnomaliesDriver()
    if request.method == 'POST':
        file = request.FILES['file']
        if not file.name.endswith('.csv'):
            messages.error(request, 'This is not a CSV file.')

        # Parse and save CSV as file in MEDIA_ROOT dir
        data = file.read().decode('UTF-8')
        csv_file_path = parse_and_write_uploaded_csv(data)
        df = fad.get_df_from_csv(csv_file_path)
        columns_mapping = fad.get_df_headers_dtypes(df)
        fad.run_twitter_algo(csv_file_path)

    context = {}
    return render(request, 'index.html', context=context)
