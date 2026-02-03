from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from django.http import FileResponse
from io import BytesIO

from .models import Dataset


# =========================
# CSV UPLOAD API  (🔥 FIXED)
# =========================
class CSVUploadView(APIView):
    authentication_classes = []   # 🔥 YAHI LINE 401 FIX KARTI HAI
    permission_classes = [AllowAny]

    def post(self, request):
        file = request.FILES.get("file")

        if not file:
            return Response(
                {"error": "CSV file not provided"},
                status=status.HTTP_400_BAD_REQUEST
            )

        df = pd.read_csv(file)

        summary = {
            "total_equipment": len(df),
            "avg_flowrate": float(df["Flowrate"].mean()),
            "avg_pressure": float(df["Pressure"].mean()),
            "avg_temperature": float(df["Temperature"].mean()),
            "type_distribution": df["Type"].value_counts().to_dict()
        }

        Dataset.objects.create(
            filename=file.name,
            summary=summary
        )

        # keep only last 5 uploads
        if Dataset.objects.count() > 5:
            Dataset.objects.order_by("uploaded_at").first().delete()

        return Response(summary, status=status.HTTP_201_CREATED)


# =========================
# HISTORY API
# =========================
class DatasetHistoryView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        data = Dataset.objects.order_by("-uploaded_at")[:5]
        return Response([
            {
                "filename": d.filename,
                "uploaded_at": d.uploaded_at,
                "summary": d.summary
            }
            for d in data
        ])


# =========================
# PDF REPORT API
# =========================
class PDFReportView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        latest = Dataset.objects.order_by("-uploaded_at").first()
        if not latest:
            return Response({"error": "No data available"}, status=404)

        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=A4)
        width, height = A4

        y = height - 50
        p.setFont("Helvetica-Bold", 16)
        p.drawString(50, y, "Chemical Equipment Report")

        p.setFont("Helvetica", 11)
        y -= 40

        for key, value in latest.summary.items():
            p.drawString(50, y, f"{key}: {value}")
            y -= 20

        p.showPage()
        p.save()
        buffer.seek(0)

        return FileResponse(
            buffer,
            as_attachment=True,
            filename="chemical_equipment_report.pdf"
        )
