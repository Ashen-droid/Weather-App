import sys
import requests
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QComboBox, QPushButton, QGraphicsDropShadowEffect, QSizePolicy
)
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve, QSize
from PyQt5.QtGui import QFont, QColor, QLinearGradient, QPalette, QIcon


class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("⛅ Weather App")
        self.setFixedSize(480, 620)

        # ── Widgets ──────────────────────────────────────────────
        # Title / header
        self.header_emoji = QLabel("🌤️", self)
        self.header_title = QLabel("Weather", self)
        self.header_subtitle = QLabel("Search any city to get the current weather", self)

        # City input area
        self.city_input = QComboBox()
        self.city_input.setEditable(True)
        self.city_input.lineEdit().setPlaceholderText("Search for a city…")
        cities = [
            "Colombo", "Kandy", "Galle", "Ampara", "Anuradhapura", "Badulla", "Mathugama", "Homagama",
            "Batticaloa", "Chilaw", "Dambulla", "Dehiwala", "Gampaha", "Gampola",
            "Hambantota", "Haputale", "Hatton", "Horana", "Ja-Ela", "Jaffna",
            "Kalmunai", "Kalutara", "Katunayake", "Kegalle", "Kelaniya",
            "Kilinochchi", "Kurunegala", "Maharagama", "Malabe", "Mannar",
            "Matale", "Matara", "Minuwangoda", "Monaragala", "Moratuwa",
            "Mount Lavinia", "Mullaitivu", "Negombo", "Nugegoda", "Nuwara Eliya",
            "Panadura", "Peliyagoda", "Point Pedro", "Polonnaruwa", "Puttalam",
            "Ratmalana", "Ratnapura", "Sri Jayawardenepura Kotte", "Tangalle",
            "Trincomalee", "Valvettithurai", "Vavuniya", "Wattala", "Weligama",
            "Akurana", "Balangoda", "Bandarawela", "Beruwala", "Chavakachcheri",
            "Embilipitiya", "Eravur", "Kattankudy", "Kinniya", "Kuliyapitiya",
            "Kadugannawa", "Nawalapitiya", "Piliyandala", "Sigiriya", "Talawakele",
            "Wattegama", "Arugam Bay", "Ella", "Hikkaduwa", "Mirissa", "Unawatuna",
            "Pasikudah", "Koggala", "Bentota", "Kataragama", "Mihintale",
            # International Cities
            "London", "New York", "Tokyo", "Paris", "Berlin", "Sydney", "Moscow",
            "Beijing", "Mumbai", "Delhi", "Toronto", "Los Angeles", "Chicago",
            "Dubai", "Singapore", "Hong Kong", "Seoul", "Rome", "Madrid",
            "Barcelona", "Amsterdam", "Vienna", "Istanbul", "Bangkok", "Jakarta",
            "Rio de Janeiro", "Buenos Aires", "Cape Town", "Cairo", "Johannesburg",
            "Nairobi", "Lagos", "Mexico City", "Sao Paulo", "Lima", "Bogota",
            "Santiago", "Melbourne", "Brisbane", "Auckland", "Wellington",
            "Stockholm", "Oslo", "Copenhagen", "Helsinki", "Warsaw", "Prague",
            "Budapest", "Athens", "Dublin", "Lisbon", "Geneva", "Zurich", "Brussels"
        ]
        self.city_input.addItems(sorted(cities))
        self.city_input.setCurrentText("")

        self.get_weather_button = QPushButton("  Get Weather", self)

        # Result widgets
        self.temperature_label = QLabel("Temperature: ", self)
        self.emoji_label = QLabel(self)
        self.description_label = QLabel("sunny", self)

        self.initUI()

    # ─── UI Setup ────────────────────────────────────────────────
    def initUI(self):
        # ── Main Layout ──
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(36, 40, 36, 36)
        main_layout.setSpacing(0)

        # ── Header Section ──
        self.header_emoji.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.header_emoji)
        main_layout.addSpacing(8)

        self.header_title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.header_title)
        main_layout.addSpacing(4)

        self.header_subtitle.setAlignment(Qt.AlignCenter)
        self.header_subtitle.setWordWrap(True)
        main_layout.addWidget(self.header_subtitle)

        main_layout.addSpacing(32)

        # ── Input Section (inside a "card") ──
        card = QWidget()
        card.setObjectName("card")
        card_layout = QVBoxLayout()
        card_layout.setContentsMargins(24, 28, 24, 28)
        card_layout.setSpacing(16)

        input_label = QLabel("📍  City")
        input_label.setObjectName("input_label")
        card_layout.addWidget(input_label)

        self.city_input.setObjectName("city_input")
        self.city_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.city_input.setMinimumHeight(46)
        card_layout.addWidget(self.city_input)

        card_layout.addSpacing(4)

        self.get_weather_button.setObjectName("get_weather_button")
        self.get_weather_button.setMinimumHeight(48)
        self.get_weather_button.setCursor(Qt.PointingHandCursor)
        card_layout.addWidget(self.get_weather_button)

        card.setLayout(card_layout)

        # Card shadow
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(30)
        shadow.setOffset(0, 8)
        shadow.setColor(QColor(0, 0, 0, 60))
        card.setGraphicsEffect(shadow)

        main_layout.addWidget(card)
        main_layout.addSpacing(28)

        # ── Result Section ──
        self.temperature_label.setAlignment(Qt.AlignCenter)
        self.emoji_label.setAlignment(Qt.AlignCenter)
        self.description_label.setAlignment(Qt.AlignCenter)

        main_layout.addWidget(self.temperature_label)
        main_layout.addSpacing(4)
        main_layout.addWidget(self.emoji_label)
        main_layout.addSpacing(4)
        main_layout.addWidget(self.description_label)

        main_layout.addStretch()

        # ── Footer credit ──
        footer = QLabel("Powered by Open-Meteo")
        footer.setObjectName("footer")
        footer.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(footer)

        self.setLayout(main_layout)

        # ── Object Names ──
        self.setObjectName("WeatherApp")
        self.header_emoji.setObjectName("header_emoji")
        self.header_title.setObjectName("header_title")
        self.header_subtitle.setObjectName("header_subtitle")
        self.temperature_label.setObjectName("temperature_label")
        self.emoji_label.setObjectName("emoji_label")
        self.description_label.setObjectName("description_label")

        # ── Signals ──
        self.get_weather_button.clicked.connect(self.get_weather)
        self.city_input.lineEdit().returnPressed.connect(self.get_weather_button.click)

        # ── Stylesheet ──
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.base_bg = "qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #0f0c29, stop:0.5 #302b63, stop:1 #24243e)"
        self.base_stylesheet = f"""
            /* ── Window ── */
            QWidget#WeatherApp {{
                background: {self.base_bg};
            }}

            /* ── Header ── */
            QLabel#header_emoji {{
                font-size: 52px;
                padding: 0;
                background: transparent;
                font-family: "Segoe UI Emoji", "Apple Color Emoji", "Noto Color Emoji", sans-serif;
            }}
            QLabel#header_title {{
                font-size: 32px;
                font-weight: 700;
                color: #ffffff;
                letter-spacing: 1px;
                background: transparent;
                font-family: "Segoe UI", "Helvetica Neue", Arial, sans-serif;
            }}
            QLabel#header_subtitle {{
                font-size: 13px;
                color: rgba(255, 255, 255, 0.55);
                background: transparent;
                font-family: "Segoe UI", "Helvetica Neue", Arial, sans-serif;
            }}

            /* ── Card ── */
            QWidget#card {{
                background: rgba(255, 255, 255, 0.07);
                border: 1px solid rgba(255, 255, 255, 0.12);
                border-radius: 18px;
            }}

            /* ── Input Label ── */
            QLabel#input_label {{
                font-size: 13px;
                font-weight: 600;
                color: rgba(255, 255, 255, 0.65);
                background: transparent;
                font-family: "Segoe UI", "Helvetica Neue", Arial, sans-serif;
            }}

            /* ── ComboBox ── */
            QComboBox#city_input {{
                font-size: 15px;
                font-family: "Segoe UI", "Helvetica Neue", Arial, sans-serif;
                padding: 10px 14px;
                background: rgba(255, 255, 255, 0.08);
                border: 1px solid rgba(255, 255, 255, 0.15);
                border-radius: 12px;
                color: #ffffff;
                selection-background-color: rgba(99, 102, 241, 0.5);
            }}
            QComboBox#city_input:focus {{
                border: 1.5px solid rgba(129, 140, 248, 0.7);
            }}
            QComboBox#city_input QAbstractItemView {{
                background: #1e1b4b;
                border: 1px solid rgba(255, 255, 255, 0.12);
                border-radius: 8px;
                color: #e0e7ff;
                padding: 4px;
                selection-background-color: rgba(99, 102, 241, 0.45);
                font-size: 14px;
                outline: none;
            }}
            QComboBox#city_input::drop-down {{
                subcontrol-origin: padding;
                subcontrol-position: center right;
                width: 32px;
                border: none;
                background: transparent;
            }}
            QComboBox#city_input::down-arrow {{
                image: none;
                width: 0; height: 0;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 6px solid rgba(255,255,255,0.4);
            }}

            /* ── Button ── */
            QPushButton#get_weather_button {{
                font-size: 15px;
                font-weight: 600;
                font-family: "Segoe UI", "Helvetica Neue", Arial, sans-serif;
                padding: 12px;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #6366f1, stop:1 #8b5cf6);
                color: #ffffff;
                border: none;
                border-radius: 12px;
                letter-spacing: 0.5px;
            }}
            QPushButton#get_weather_button:hover {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #818cf8, stop:1 #a78bfa);
            }}
            QPushButton#get_weather_button:pressed {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #4f46e5, stop:1 #7c3aed);
            }}

            /* ── Results ── */
            QLabel#temperature_label {{
                font-size: 26px;
                font-weight: 700;
                color: #ffffff;
                background: transparent;
                font-family: "Segoe UI", "Helvetica Neue", Arial, sans-serif;
            }}
            QLabel#emoji_label {{
                font-size: 72px;
                background: transparent;
                font-family: "Segoe UI Emoji", "Apple Color Emoji", "Noto Color Emoji", sans-serif;
            }}
            QLabel#description_label {{
                font-size: 18px;
                color: rgba(255, 255, 255, 0.7);
                background: transparent;
                font-family: "Segoe UI", "Helvetica Neue", Arial, sans-serif;
            }}

            /* ── Footer ── */
            QLabel#footer {{
                font-size: 11px;
                color: rgba(255, 255, 255, 0.25);
                background: transparent;
                font-family: "Segoe UI", "Helvetica Neue", Arial, sans-serif;
            }}
        """
        self.setStyleSheet(self.base_stylesheet)

        # Hide result widgets until weather is fetched
        self.temperature_label.hide()
        self.emoji_label.hide()
        self.description_label.hide()

    # ─── Weather Fetch ───────────────────────────────────────────
    def get_weather(self):
        city = self.city_input.currentText().strip()
        if not city:
            self.description_label.setStyleSheet(
                "font-size: 14px; color: #fca5a5; background: transparent;"
            )
            self.description_label.setText("⚠  Please enter a city name.")
            self.description_label.show()
            self.temperature_label.hide()
            self.emoji_label.hide()
            return

        # Reset description style
        self.description_label.setStyleSheet("")

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
            country = geo_data["results"][0].get("country", "")
            country_code = geo_data["results"][0].get("country_code", "")

            # Fetch the current weather
            weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
            weather_response = requests.get(weather_url)
            weather_response.raise_for_status()
            weather_data = weather_response.json()

            current_weather = weather_data.get("current_weather", {})
            temp = current_weather.get("temperature")
            weather_code = current_weather.get("weathercode", 0)

            if temp is None:
                self.description_label.setText("Weather data currently unavailable.")
                self.description_label.show()
                self.temperature_label.hide()
                self.emoji_label.hide()
                return

            weather_desc = self.get_weather_description(weather_code)

            country_str = f" ({country} {self.get_flag_emoji(country_code)})" if country else ""
            self.temperature_label.setText(f"{temp}°C{country_str}")

            # Determine temperature-related emoji and background gradient
            if temp <= 0:
                temp_emoji = "🥶"
                bg = "qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #0c1445, stop:0.5 #1a3a5c, stop:1 #0f2847)"
            elif 0 < temp <= 10:
                temp_emoji = "🧣"
                bg = "qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #0f1b4d, stop:0.5 #1e3a5f, stop:1 #162d50)"
            elif 10 < temp <= 20:
                temp_emoji = "🧥"
                bg = "qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #0f0c29, stop:0.5 #302b63, stop:1 #24243e)"
            elif 20 < temp <= 30:
                temp_emoji = "🌤️"
                bg = "qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #2d1b69, stop:0.5 #5b3a8c, stop:1 #44337a)"
            elif 30 < temp <= 40:
                temp_emoji = "🥵"
                bg = "qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #4a1942, stop:0.5 #7b2d5f, stop:1 #5c2249)"
            else:
                temp_emoji = "🔥"
                bg = "qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #5c1018, stop:0.5 #8b2030, stop:1 #6b1525)"

            updated_stylesheet = self.base_stylesheet.replace(
                f"background: {self.base_bg};",
                f"background: {bg};"
            )
            self.setStyleSheet(updated_stylesheet)

            weather_emoji = self.get_weather_emoji(weather_code)

            self.emoji_label.setText(f"{weather_emoji} {temp_emoji}")
            self.description_label.setText(weather_desc)

            self.temperature_label.show()
            self.emoji_label.show()
            self.description_label.show()

        except Exception:
            self.description_label.setText("Error fetching weather data.")
            self.description_label.show()
            self.temperature_label.hide()
            self.emoji_label.hide()

    # ─── Helpers ─────────────────────────────────────────────────
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

    def get_flag_emoji(self, country_code):
        if not country_code or len(country_code) != 2:
            return ""
        return chr(ord(country_code[0].upper()) + 127397) + chr(ord(country_code[1].upper()) + 127397)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    weather_app = WeatherApp()
    weather_app.show()
    sys.exit(app.exec_())
