import sys
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton
from PyQt5.QtCore import Qt

class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.city_label = QLabel("Enter city name : ",self)
        self.city_input = QLineEdit()
        self.get_weather_button = QPushButton("Get Weather", self)
        self.temperature_label = QLabel("Temperature: ", self)
        self.emoji_label = QLabel(self)
        self.description_label = QLabel("sunny",self)
        self.initUI()

    def initUI(self):
        vbox = QVBoxLayout()
        vbox.addWidget(self.city_label)
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.get_weather_button)
        vbox.addWidget(self.temperature_label)
        vbox.addWidget(self.emoji_label)
        vbox.addWidget(self.description_label)
        self.setLayout(vbox)

        self.city_label.setAlignment(Qt.AlignCenter)
        self.city_input.setAlignment(Qt.AlignCenter)
        self.temperature_label.setAlignment(Qt.AlignCenter)
        self.emoji_label.setAlignment(Qt.AlignCenter)
        self.description_label.setAlignment(Qt.AlignCenter)

        self.city_label.setObjectName("city_label")
        self.city_input.setObjectName("city_input")
        self.get_weather_button.setObjectName("get_weather_button")
        self.temperature_label.setObjectName("temperature_label")
        self.emoji_label.setObjectName("emoji_label")
        self.description_label.setObjectName("description_label")
        
        self.get_weather_button.clicked.connect(self.get_weather)
        
        # Adding some basic styling matching the object names
        self.setStyleSheet("""
            QLabel#city_label {
                font-size: 20px;
                font-weight: bold;
            }
            QLineEdit#city_input {
                font-size: 20px;
                padding: 5px;
            }
            QPushButton#get_weather_button {
                font-size: 18px;
                padding: 8px;
                background-color: #4CAF50;
                color: white;
                border-radius: 4px;
            }
            QPushButton#get_weather_button:hover {
                background-color: #45a049;
            }
            QLabel#temperature_label {
                font-size: 28px;
                font-weight: bold;
                color: #2196F3;
            }
            QLabel#emoji_label {
                font-size: 80px;
                font-family: "Segoe UI Emoji", "Apple Color Emoji", "Noto Color Emoji", sans-serif;
            }
            QLabel#description_label {
                font-size: 22px;
                color: #555;
            }
        """)

        self.temperature_label.hide()
        self.emoji_label.hide()
        self.description_label.hide()

    def get_weather(self):
        city = self.city_input.text().strip()
        if not city:
            self.description_label.setText("Please enter a city name.")
            self.description_label.show()
            self.temperature_label.hide()
            self.emoji_label.hide()
            return

        # Fetch coordinates for the city
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1&language=en&format=json"
        try:
            geo_response = requests.get(geo_url)
            geo_response.raise_for_status()
            geo_data = geo_response.json()

            if not geo_data.get("results"):
                self.description_label.setText(f"City '{city}' not found.")
                self.description_label.show()
                self.temperature_label.hide()
                self.emoji_label.hide()
                return

            lat = geo_data["results"][0]["latitude"]
            lon = geo_data["results"][0]["longitude"]

            # Fetch the current weather
            weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
            weather_response = requests.get(weather_url)
            weather_response.raise_for_status()
            weather_data = weather_response.json()

            current_weather = weather_data.get("current_weather", {})
            temp = current_weather.get("temperature")
            weather_code = current_weather.get("weathercode", 0)

            weather_desc = self.get_weather_description(weather_code)

            self.temperature_label.setText(f"Temperature: {temp}°C")
            
            # Determine temperature-related emoji
            if temp <= 0:
                temp_emoji = "🥶"
            elif 0 < temp <= 10:
                temp_emoji = "🧣"
            elif 10 < temp <= 20:
                temp_emoji = "🧥"
            elif 20 < temp <= 30:
                temp_emoji = "🌤️"
            elif 30 < temp <= 40:
                temp_emoji = "🥵"
            else:
                temp_emoji = "🔥"
                
            weather_emoji = self.get_weather_emoji(weather_code)
            
            self.emoji_label.setText(f"{weather_emoji} {temp_emoji}")
            self.description_label.setText(weather_desc)
            
            self.temperature_label.show()
            self.emoji_label.show()
            self.description_label.show()

        except requests.exceptions.RequestException:
            self.description_label.setText("Error fetching weather data.")
            self.description_label.show()
            self.temperature_label.hide()
            self.emoji_label.hide()

    def get_weather_description(self, code):
        weather_codes = {
            0: "Clear sky", 1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
            45: "Fog", 48: "Depositing rime fog",
            51: "Light drizzle", 53: "Moderate drizzle", 55: "Dense drizzle",
            56: "Light freezing drizzle", 57: "Dense freezing drizzle",
            61: "Slight rain", 63: "Moderate rain", 65: "Heavy rain",
            66: "Light freezing rain", 67: "Heavy freezing rain",
            71: "Slight snow fall", 73: "Moderate snow fall", 75: "Heavy snow fall",
            77: "Snow grains",
            80: "Slight rain showers", 81: "Moderate rain showers", 82: "Violent rain showers",
            85: "Slight snow showers", 86: "Heavy snow showers",
            95: "Thunderstorm", 96: "Thunderstorm with slight hail", 99: "Thunderstorm with heavy hail"
        }
        return weather_codes.get(code, "Unknown weather")
        
    def get_weather_emoji(self, weather_code):
        weather_codes = {
            0: "☀️", 1: "🌤️", 2: "⛅", 3: "☁️",
            45: "🌫️", 48: "🌫️",
            51: "🌧️", 53: "🌧️", 55: "🌧️",
            56: "🌧️", 57: "🌧️",
            61: "🌧️", 63: "🌧️", 65: "🌧️",
            66: "🌧️", 67: "🌧️",
            71: "❄️", 73: "❄️", 75: "❄️",
            77: "❄️",
            80: "🌦️", 81: "🌦️", 82: "🌦️",
            85: "🌨️", 86: "🌨️",
            95: "⛈️", 96: "⛈️", 99: "⛈️"
        }
        return weather_codes.get(weather_code, "🌡️")



if __name__ == "__main__":      
    app = QApplication(sys.argv)
    weather_app = WeatherApp()
    weather_app.show()
    sys.exit(app.exec_())         
        
