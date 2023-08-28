import sys
import requests
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPalette, QColor
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QMessageBox


class PogodynkaApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Pogodynka u Rikusia")
        self.setGeometry(100, 100, 1920, 1200)

        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(0, 0, 255))
        palette.setColor(QPalette.ColorRole.WindowText, QColor(255, 255, 255))
        palette.setColor(QPalette.ColorRole.Button, QColor(65, 105, 225))
        palette.setColor(QPalette.ColorRole.ButtonText, QColor(255, 255, 255))
        palette.setColor(QPalette.ColorRole.Base, QColor(0, 0, 255))
        self.setPalette(palette)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.city_label = QLabel("Wprowadź żądaną nazwę miasta poniżej:", self)
        font = QFont("Arial", 20)
        self.city_label.setFont(font)
        self.city_label.setStyleSheet("color: white;")
        layout.addWidget(self.city_label)

        self.city_entry = QLineEdit(self)
        self.city_entry.setFont(font)
        self.city_entry.setStyleSheet("color: Black; background-color: White")
        self.city_entry.setMaximumWidth(self.width() // 4)
        layout.addWidget(self.city_entry)

        self.przycisk_gowny = QPushButton("Sprawdź!", self)
        self.przycisk_gowny.setFont(font)
        self.przycisk_gowny.setStyleSheet("background-color: Royalblue; color: white;")
        self.przycisk_gowny.setMaximumWidth(self.width() // 4)
        self.przycisk_gowny.clicked.connect(self.sprawdz_pogode)
        layout.addWidget(self.przycisk_gowny)

        container = QWidget(self)
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.dane_pogody = None


    def bier_pogode(self, miasto):
        api_key = "d01a693948e4482124bcb57cc85406a1"
        base_url = "http://api.openweathermap.org/data/2.5/weather"
        params = {
            "q": miasto,
            "appid": api_key,
            "units": "metric"
        }
        try:
            response = requests.get(base_url, params=params)
            data = response.json()
            if response.status_code == 200:
                return data
            else:
                print("Błąd w odpowiedzi API:", data)
                return None
        except Exception as e:
            print("Błąd podczas wykonywania zapytania:", e)
            return None

    def sprawdz_pogode(self):
        miasto = self.city_entry.text()
        if miasto:
            try:
                dane_pogody = self.bier_pogode(miasto)
                if dane_pogody:
                    temperatura = dane_pogody.get("main", {}).get("temp")
                    opis = dane_pogody.get("weather", [{}])[0].get("description")
                    if temperatura is not None and opis:
                        QMessageBox.information(self, "Pogoda",
                                                f"Aktualna temperatura to {temperatura} stopni Celsjusza.\nOpis: {opis}")
                        self.dane_pogody = None
                    else:
                        QMessageBox.critical(self, "Błąd", "Nie znaleziono miasta.")
                        self.dane_pogody = None
                else:
                    QMessageBox.critical(self, "Błąd", "Nie znaleziono miasta.")
                    self.dane_pogody = None
            except Exception as er:
                print("Błąd w funkcji sprawdz_pogode:", er)
                QMessageBox.critical(self, "Błąd", "Nie można pobrać danych")
                self.dane_pogody = None
        else:
            QMessageBox.critical(self, "Błąd", "Wprowadź nazwę miasta.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PogodynkaApp()
    window.show()
    sys.exit(app.exec())
