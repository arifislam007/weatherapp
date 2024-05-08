from flask import Flask, jsonify
import requests
import os

app = Flask(__name__)

NWS_API_URL = "https://api.weather.gov/stations/KNYC/observations/latest"
API_KEY = os.environ["SECURE_WEATHER_API_KEY"]


@app.route("/weather")
def get_weather():
    response = requests.get(NWS_API_URL, headers={"X-API-KEY": API_KEY})

    data = response.json()

    if response.status_code != 200:
        return (jsonify({"error": "Failed to get weather data"}), response.status_code)

    latest_observation = data["properties"]

    pressure = (
        latest_observation["barometricPressure"]["value"]
        if latest_observation["barometricPressure"]["value"] is not None
        else "N/A"
    )

    humidity = (
        latest_observation["relativeHumidity"]["value"]
        if latest_observation["relativeHumidity"]["value"] is not None
        else "N/A"
    )

    weather = {
        "city": "New York City",
        "temperature": latest_observation["temperature"]["value"],
        "description": latest_observation["textDescription"],
        "pressure": pressure,
        "humidity": humidity,
    }

    if weather["temperature"] is not None:
        weather["temperature"] = weather["temperature"] * 9 / 5 + 32
        weather["temperature"] = f"{weather['temperature']:.2f}°F"

    return jsonify(weather)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 80))
    app.run(debug=True, port=port)
