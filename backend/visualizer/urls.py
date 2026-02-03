from django.urls import path
from .views import CSVUploadView, DatasetHistoryView, PDFReportView

urlpatterns = [
    path("upload/", CSVUploadView.as_view()),
    path("history/", DatasetHistoryView.as_view()),
    path("report/", PDFReportView.as_view()),
]
