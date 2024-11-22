import sys
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
from PIL import Image
from io import BytesIO

class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Weather Forecast App")
        self.setFixedSize(400, 600)

        self.setStyleSheet("background-color: #f0f0f0;")
        
        self.city_label = QLabel("Enter City Name:")
        self.city_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #333;")
        
        self.city_input = QLineEdit(self)
        self.city_input.setStyleSheet("font-size: 14px; padding: 10px;")
        
        self.get_weather_btn = QPushButton("Get Weather", self)
        self.get_weather_btn.setStyleSheet("background-color: #4CAF50; color: white; padding: 10px; font-size: 14px;")
        self.get_weather_btn.clicked.connect(self.get_weather_data)

        self.weather_info = QLabel("")
        self.weather_info.setStyleSheet("font-size: 14px; color: #333;")

        self.icon_label = QLabel(self)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.city_label)
        layout.addWidget(self.city_input)
        layout.addWidget(self.get_weather_btn)
        layout.addWidget(self.weather_info)
        layout.addWidget(self.icon_label)

        self.setLayout(layout)
        
        self.show()

    def get_weather_data(self):
        api_key = "your_own_api" # give your own api from the openweatherapp which you have to sign up for.  
        city = self.city_input.text()
        
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        
        try:
            response = requests.get(url)
            data = response.json()

            if data.get("cod") != 200:
                self.show_error("Error", f"City not found: {data.get('message', 'Unknown error')}")
                return

            main_data = data.get("main", {})
            weather_data = data.get("weather", [{}])[0]
            
            if main_data:
                temperature = main_data.get("temp", "N/A")
                pressure = main_data.get("pressure", "N/A")
                humidity = main_data.get("humidity", "N/A")

                weather_description = weather_data.get("description", "N/A")
                icon_code = weather_data.get("icon", "")

                self.weather_info.setText(f"Temperature: {temperature}°C\n"
                                          f"Pressure: {pressure} hPa\n"
                                          f"Humidity: {humidity}%\n"
                                          f"Condition: {weather_description.capitalize()}")

                icon_url = f"http://openweathermap.org/img/wn/{icon_code}.png"
                self.set_weather_icon(icon_url)

        except Exception as e:
            self.show_error("Error", f"Error retrieving data: {str(e)}")

    def set_weather_icon(self, icon_url):
        try:
            icon_response = requests.get(icon_url)
            icon_data = Image.open(BytesIO(icon_response.content))
            icon_data = icon_data.convert("RGBA")  # Ensure RGBA format
            icon_data = icon_data.resize((100, 100))

            # Convert PIL Image to QImage
            img_byte_arr = BytesIO()
            icon_data.save(img_byte_arr, format='PNG')
            img_byte_arr = img_byte_arr.getvalue()
            qimage = QImage.fromData(img_byte_arr)

            # Set the icon in the QLabel
            self.icon_label.setPixmap(QPixmap.fromImage(qimage))

        except Exception as e:
            print(f"Error displaying icon: {e}")

    def show_error(self, title, message):
        QMessageBox.critical(self, title, message)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = WeatherApp()
    sys.exit(app.exec_())
