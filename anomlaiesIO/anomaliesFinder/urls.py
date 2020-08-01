from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include

from .views import anomalies_finder_main, SaveUploadedFile

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^main$', anomalies_finder_main, name='main_page'),
    # Ajax URLS
    url(r'^save_uploaded_file', SaveUploadedFile.as_view(), name='save_uploaded_file'),
]
