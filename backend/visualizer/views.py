# backend/visualizer/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from django.http import FileResponse
from io import BytesIO, StringIO  # <-- StringIO added

from .models import Dataset


# =========================
# CSV UPLOAD API
# =========================
class CSVUploadView(APIView):
    authentication_classes = []          # 🔥 NO AUTH
    permission_classes = [AllowAny]      # 🔥 PUBLIC API

    def post(self, request):
        file = request.FILES.get("file")

        if not file:
            return Response(
                {"error": "CSV file not provided"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # -------------------------
        # Robust read: decode bytes -> StringIO -> pandas
        # -------------------------
        try:
            raw_bytes = file.read()
            try:
                decoded = raw_bytes.decode("utf-8")
            except UnicodeDecodeError:
                # fallback if file is not UTF-8
                decoded = raw_bytes.decode("latin-1")

            # pass text stream to pandas; use engine='python' to allow sep=None auto-detection
            df = pd.read_csv(StringIO(decoded), sep=None, engine="python")
        except Exception as e:
            return Response(
                {"error": "Unable to read CSV", "details": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 🔹 Validate columns
        required_columns = ["Flowrate", "Pressure", "Temperature", "Type"]
        missing = [c for c in required_columns if c not in df.columns]

        if missing:
            return Response(
                {
                    "error": "Invalid CSV format",
                    "missing_columns": missing,
                    "available_columns": list(df.columns)
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # 🔹 Convert numeric columns
        for col in ["Flowrate", "Pressure", "Temperature"]:
            df[col] = pd.to_numeric(df[col], errors="coerce")

        # 🔹 Build summary
        summary = {
            "total_equipment": int(len(df)),
            "avg_flowrate": float(df["Flowrate"].mean()),
            "avg_pressure": float(df["Pressure"].mean()),
            "avg_temperature": float(df["Temperature"].mean()),
            "type_distribution": df["Type"].value_counts().to_dict()
        }

        # 🔹 Save to DB
        Dataset.objects.create(
            filename=file.name,
            summary=summary
        )

        # 🔹 Keep only last 5 uploads
        if Dataset.objects.count() > 5:
            Dataset.objects.order_by("uploaded_at").first().delete()

        return Response(summary, status=status.HTTP_201_CREATED)


# =========================
# DATASET HISTORY API
# =========================
class DatasetHistoryView(APIView):
    authentication_classes = []
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
    authentication_classes = []
    permission_classes = [AllowAny]

    def get(self, request):
        latest = Dataset.objects.order_by("-uploaded_at").first()

        if not latest:
            return Response(
                {"error": "No data available"},
                status=status.HTTP_404_NOT_FOUND
            )

        buffer = BytesIO()
        pdf = canvas.Canvas(buffer, pagesize=A4)
        width, height = A4

        y = height - 50
        pdf.setFont("Helvetica-Bold", 16)
        pdf.drawString(50, y, "Chemical Equipment Report")

        pdf.setFont("Helvetica", 11)
        y -= 40

        for key, value in latest.summary.items():
            pdf.drawString(50, y, f"{key}: {value}")
            y -= 20

        pdf.showPage()
        pdf.save()
        buffer.seek(0)

        return FileResponse(
            buffer,
            as_attachment=True,
            filename="chemical_equipment_report.pdf"
        )