import sys
import requests
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel,
                             QLineEdit, QPushButton, QVBoxLayout)
from PyQt5.QtCore import Qt

class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        # Define UI components
        self.city_label = QLabel("Enter city name:", self)
        self.city_input = QLineEdit(self)
        self.get_weather_button = QPushButton("Get Weather", self)
        self.temperature_label = QLabel(self)
        self.emoji_label = QLabel(self)
        self.description_label = QLabel(self)
        
        # CRITICAL: Added initUI call so the interface actually displays!
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Weather App")
        self.setFixedSize(450, 550) # Set a comfortable, compact widget size

        # Fix: Add () to instantiate the layout class
        vbox = QVBoxLayout()

        vbox.addWidget(self.city_label)
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.get_weather_button)
        vbox.addWidget(self.temperature_label)
        vbox.addWidget(self.emoji_label)
        vbox.addWidget(self.description_label)

        self.setLayout(vbox)

        # Center alignments
        self.city_label.setAlignment(Qt.AlignCenter)
        self.city_input.setAlignment(Qt.AlignCenter)
        self.temperature_label.setAlignment(Qt.AlignCenter)
        self.emoji_label.setAlignment(Qt.AlignCenter)
        self.description_label.setAlignment(Qt.AlignCenter)

        # Object names for styling targeting
        self.city_label.setObjectName("city_label")
        self.city_input.setObjectName("city_input")
        self.get_weather_button.setObjectName("get_weather_button")
        self.temperature_label.setObjectName("temperature_label")
        self.emoji_label.setObjectName("emoji_label")
        self.description_label.setObjectName("description_label")

        # Stylesheet configurations
        self.setStyleSheet("""
            QWidget {
                background-color: #f4f4f6;
            }
            QLabel, QPushButton {
                font-family: calibri;               
            }               
            QLabel#city_label {
                font-size: 35px;
                font-style: italic;   
                color: #333333;
                padding-top: 10px;
            }   
            QLineEdit#city_input {
                font-size: 30px;           
                padding: 5px;
                border: 2px solid #bdc3c7;
                border-radius: 5px;
                background-color: white;
            }              
            QPushButton#get_weather_button {
                font-size: 24px;
                font-weight: bold;    
                background-color: #3498db;
                color: white;
                border-radius: 5px;
                padding: 8px;
            }
            QPushButton#get_weather_button:hover {
                background-color: #2980b9;
            }
            QLabel#temperature_label {
                font-size: 70px;    
                font-weight: bold;
                color: #2c3e50;                    
            }
            QLabel#emoji_label {
                font-size: 90px;
                font-family: "Segoe UI Emoji", "Apple Color Emoji";      
            }
            QLabel#description_label {
                font-size: 35px;
                color: #7f8c8d;
                text-transform: capitalize;
            }
        """)
        
        self.get_weather_button.clicked.connect(self.get_weather)

    def get_weather(self):
        # Fix variable declaration from api.key to api_key
        api_key = "4a01cc17862f3bb6759c0323273c688a"
        city = self.city_input.text().strip()
        
        if not city:
            self.display_error("Enter a city first!")
            return

        # Changed units=imperial to pull temperature directly in Fahrenheit (°F)
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=imperial"

        try:
            response = requests.get(url)
            data = response.json()
            
            # OpenWeatherMap returns code as int, or string in some error formats
            if str(data.get("cod")) == "200":
                self.display_weather(data)
            else:
                # Matches your third sketch state: "Not found! City not found"
                self.display_error(f"Not found!\nCity not found")
        except Exception:
            self.display_error("Connection Error!")

    def display_error(self, message):
        # Clear out current weather views and render the error message
        self.temperature_label.clear()
        self.emoji_label.clear()
        self.description_label.setText(message)
        self.description_label.setStyleSheet("color: #e74c3c; font-size: 30px; font-weight: bold;")

    def display_weather(self, data):
        # Reset text color properties back to normal in case an error happened before
        self.description_label.setStyleSheet("font-size: 35px; color: #7f8c8d;")
        
        # Extract properties
        temp = data["main"]["temp"]
        weather_id = data["weather"][0]["id"]
        description = data["weather"][0]["description"]
        
        # Render info
        self.temperature_label.setText(f"{temp:.1f}°F")
        self.description_label.setText(description)
        self.emoji_label.setText(self.get_weather_emoji(weather_id))

    def get_weather_emoji(self, weather_id):
        # Return an emoji icon matching weather condition codes
        if 200 <= weather_id <= 232:
            return "⛈️"
        elif 300 <= weather_id <= 321:
            return "🌧️"
        elif 500 <= weather_id <= 531:
            return "🌧️"
        elif 600 <= weather_id <= 622:
            return "❄️"
        elif 701 <= weather_id <= 781:
            return "🌫️"
        elif weather_id == 800:
            return "☀️"
        elif weather_id == 801:
            return "🌤️"
        elif 802 <= weather_id <= 804:
            return "☁️"
        return "✨"

# Fix spelling layout names in execution section
if __name__ == "__main__": 
    app = QApplication(sys.argv)
    weather_app = WeatherApp()
    weather_app.show()
    sys.exit(app.exec_())