from django.urls import path
from .views import CSVUploadView, DatasetHistoryView, PDFReportView

urlpatterns = [
    path("upload/", CSVUploadView.as_view(), name="csv-upload"),
    path("history/", DatasetHistoryView.as_view(), name="dataset-history"),
    path("report/", PDFReportView.as_view(), name="pdf-report"),
]
