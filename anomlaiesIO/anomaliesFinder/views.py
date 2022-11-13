import datetime

from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponse, JsonResponse

from rest_framework.views import APIView
from rest_framework.response import Response

from algos.complex_query import FindAnomaliesDriver
from .anomalies_finder_utils import parse_and_write_uploaded_csv

def anomalies_finder_main(request):
    context = {}
    if request.method == 'POST':
        return HttpResponse(status=204)


    return render(request, 'index.html', context=context)



class SaveUploadedFile(APIView):
    '''
        This class is responsible to save a CSV/JSON uploaded data
        And then run the Twitter anomaly-detection algo
    '''
    http_method_names = ['get', 'post']

    def __init__(self):
        self.start_timestamp = datetime.datetime.utcnow()
        self.event = 'save_uploaded_file'

    def post(self, request, *args, **kwargs):
        context = {}
        file = request.FILES['file']
        if not file.name.endswith('.csv'):
            messages.error(request, 'This is not a CSV file.')

        # Parse and save CSV as file in MEDIA_ROOT dir
        data = file.read().decode('UTF-8')
        file_path = parse_and_write_uploaded_csv(data)
        context = {'file_path':file_path}
        return Response(context)

class setFiledsSchema(APIView):
    http_method_names = ['get', 'post']

    def __init__(self):
        self.start_timestamp = datetime.datetime.utcnow()
        self.event = 'trigger_set_fields_schema'
        self.columns_mapping_strings = {'object':'Dimension', 'int64':'Measure', 'float64':'Measure', 'bool':'Boolean'}
        self.fad = FindAnomaliesDriver()

    def get(self, request, *args, **kwargs):
        file_path = request.GET['file_path']
        df = self.fad.get_df_from_csv(file_path)
        columns_mapping = self.fad.get_df_headers_dtypes(df)
        context = {'columns_mapping':columns_mapping}
        return Response(context)
