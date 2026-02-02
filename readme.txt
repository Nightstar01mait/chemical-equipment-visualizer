-> Chemical Equipment Parameter Visualizer
Hybrid Web + Desktop Application

Overview
This project is a hybrid application developed for an internship screening task.
It allows users to upload CSV files containing chemical equipment parameters,
analyze the data, visualize it, and generate PDF reports.

The application uses a common Django REST backend that is consumed by both
a Web application and a Desktop application.

---

Features
- Upload CSV files containing chemical equipment data
- Backend data analysis using Pandas
- Summary statistics (count, averages, type distribution)
- Data visualization
- PDF report generation
- Dataset history (last 5 uploads only)
- Same backend API used by Web and Desktop apps

---

Tech Stack
Backend:
- Python
- Django
- Django REST Framework
- Pandas
- SQLite
- ReportLab (PDF generation)

Web Frontend:
- React.js
- Chart.js

Desktop Frontend:
- PyQt5
- Matplotlib

Version Control:
- Git
- GitHub

---

CSV File Format
The uploaded CSV file must contain the following columns:

EquipmentName, Type, Flowrate, Pressure, Temperature

Example:
EquipmentName,Type,Flowrate,Pressure,Temperature
Pump A,Pump,10.5,5.2,80
Valve B,Valve,7.2,3.8,60

---

API Endpoints

Upload CSV
POST /api/upload/

Form-Data:
- key: file
- value: CSV file

Response:
- Summary statistics of uploaded data

---

Dataset History
GET /api/history/

Returns last 5 uploaded datasets.

---
PDF Report
GET /api/report/

- Generates a PDF report for the latest uploaded dataset
- Returns "No data available" if no CSV has been uploaded

---

## Project Structure

Chemical_equipment_visualizer/
├── backend/
│   ├── backend/
│   │   ├── settings.py
│   │   ├── urls.py
│   │   ├── wsgi.py
│   ├── visualizer/
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── serializers.py
│   │   ├── urls.py
│   ├── manage.py
│
├── web/
│   └── src/
│       ├── components/
│       ├── api.js
│       └── App.js
│
├── desktop/
│   └── app.py
│
└── README.md

---
Setup Instructions

Backend Setup
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver

Server runs at:
http://127.0.0.1:8000/

---

Web Application
cd web
npm install
npm start

---

Desktop Application
cd desktop
python app.py

---

Notes
- Only the latest 5 datasets are stored in the database
- PDF generation is handled on the backend
- CORS is enabled for frontend communication
- This project is intended for development and internship evaluation purposes

---

Author
Gaurav Raj  
B.Tech (Computer Science and Engineering)
  
---

License
This project is created for educational and internship screening purposes.
