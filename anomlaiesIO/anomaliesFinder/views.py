import datetime

from django.shortcuts import render
from django.contrib import messages

from rest_framework.views import APIView
from rest_framework.response import Response

from algos.twitter_algo import FindAnomaliesDriver
from .anomalies_finder_utils import parse_and_write_uploaded_csv

def anomalies_finder_main(request):
    context = {}
    if request.method == 'POST':
        file = request.FILES['file']

    return render(request, 'index.html', context=context)



class SaveUploadedFile(APIView):
    '''
        This class is responsible to save a CSV/JSON uploaded data
        And then run the Twitter anomaly-detection algo
    '''
    def __init__(self):
        self.start_timestamp = datetime.datetime.utcnow()
        self.resource = 'release_notes'
        self.fad = FindAnomaliesDriver()

    def post(self, request, *args, **kwargs):
        context = {}
        try:
            file = request.FILES['file']
            if not file.name.endswith('.csv'):
                messages.error(request, 'This is not a CSV file.')

            # Parse and save CSV as file in MEDIA_ROOT dir
            data = file.read().decode('UTF-8')
            csv_file_path = parse_and_write_uploaded_csv(data)
            print(csv_file_path)
            context = {'csv_file_path':csv_file_path}
            # df = self.fad.get_df_from_csv(csv_file_path)
            # columns_mapping = self.fad.get_df_headers_dtypes(df)
            # self.fad.run_twitter_algo(csv_file_path)
            # context = {'columns_mapping':columns_mapping}

        except Exception as err:
            print("Error occured while trying to upload CSV:\n{}".format(err))

        return Response(context)