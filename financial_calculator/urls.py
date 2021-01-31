from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include

from .views import financial_calculator_main

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^main$', financial_calculator_main, name='financial_calculator_main_page'),
]
