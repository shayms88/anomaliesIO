import datetime

from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponse, JsonResponse

from rest_framework.views import APIView
from rest_framework.response import Response

def financial_calculator_main(request):
    context = {}
    if request.method == 'POST':
        return HttpResponse(status=204)


    return render(request, 'financial_calculator/index.html', context=context)
