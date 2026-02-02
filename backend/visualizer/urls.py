from django.urls import path
from .views import CSVUploadView, DatasetHistoryView, PDFReportView

urlpatterns = [
    path('upload/', CSVUploadView.as_view(), name='upload'),
    path('history/', DatasetHistoryView.as_view(), name='history'),
    path('report/', PDFReportView.as_view(),name ="report"),
]
