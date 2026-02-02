import sys
import requests
import matplotlib.pyplot as plt

from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton,
    QFileDialog, QLabel, QTableWidget, QTableWidgetItem
)

API_URL = "http://127.0.0.1:8000/api/upload/"

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Chemical Equipment Visualizer (Desktop)")
        self.setGeometry(200, 200, 700, 500)

        self.layout = QVBoxLayout()

        self.upload_btn = QPushButton("Upload CSV")
        self.upload_btn.clicked.connect(self.upload_csv)

        self.status = QLabel("Select a CSV file")
        self.table = QTableWidget()

        self.layout.addWidget(self.upload_btn)
        self.layout.addWidget(self.status)
        self.layout.addWidget(self.table)

        self.setLayout(self.layout)

    def upload_csv(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select CSV File", "", "CSV Files (*.csv)"
        )

        if not file_path:
            return

        self.status.setText("Uploading...")

        with open(file_path, 'rb') as f:
            response = requests.post(API_URL, files={"file": f})

        if response.status_code != 201:
            self.status.setText("Upload failed")
            return

        data = response.json()
        self.status.setText("Upload successful")

        self.show_table(data)
        self.show_chart(data)

    def show_table(self, data):
        rows = [
            ("Total Equipment", data["total_equipment"]),
            ("Avg Flowrate", round(data["avg_flowrate"], 2)),
            ("Avg Pressure", round(data["avg_pressure"], 2)),
            ("Avg Temperature", round(data["avg_temperature"], 2)),
        ]

        self.table.setRowCount(len(rows))
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Parameter", "Value"])

        for row, (key, value) in enumerate(rows):
            self.table.setItem(row, 0, QTableWidgetItem(key))
            self.table.setItem(row, 1, QTableWidgetItem(str(value)))

    def show_chart(self, data):
        labels = list(data["type_distribution"].keys())
        values = list(data["type_distribution"].values())

        plt.figure()
        plt.pie(values, labels=labels, autopct="%1.1f%%")
        plt.title("Equipment Type Distribution")
        plt.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec_())