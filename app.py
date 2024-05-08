from flask import Flask, jsonify
import requests
import os

app = Flask(__name__)

NWS_API_URL = "https://api.weather.gov/stations/KNYC/observations/latest"
API_KEY = os.environ.get("SECURE_WEATHER_API_KEY")  # Use get() to avoid KeyError if environment variable is missing

@app.route("/weather")
def get_weather():
    if not API_KEY:
        return jsonify({"error": "SECURE_WEATHER_API_KEY environment variable not set"}), 500

    response = requests.get(NWS_API_URL, headers={"X-API-KEY": API_KEY})

    if response.status_code != 200:
        return jsonify({"error": "Failed to get weather data"}), response.status_code

    data = response.json()
    latest_observation = data.get("properties", {})

    temperature = latest_observation.get("temperature", {}).get("value")
    description = latest_observation.get("textDescription")
    pressure = latest_observation.get("barometricPressure", {}).get("value", "N/A")
    humidity = latest_observation.get("relativeHumidity", {}).get("value", "N/A")

    if temperature is not None:
        temperature = temperature * 9 / 5 + 32
        temperature = f"{temperature:.2f}°F"

    weather = {
        "city": "New York City",
        "temperature": temperature,
        "description": description,
        "pressure": pressure,
        "humidity": humidity
    }

    return jsonify(weather)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 80))
    app.run(debug=True, host="0.0.0.0", port=port)
