from flask import Flask, render_template, request
import requests
import os

app = Flask(__name__)

# 🔑 Put your real OpenWeather API key here
API_KEY = "YOUR_API_KEY_HERE"

@app.route("/", methods=["GET", "POST"])
def home():
    weather = None
    error = None

    if request.method == "POST":
        city = request.form.get("city")

        if city:
            try:
                url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
                response = requests.get(url)
                data = response.json()

                if response.status_code == 200:
                    weather = {
                        "city": data["name"],
                        "temp": data["main"]["temp"],
                        "humidity": data["main"]["humidity"],
                        "wind": data["wind"]["speed"],
                        "desc": data["weather"][0]["description"]
                    }
                else:
                    error = data.get("message", "City not found")

            except Exception:
                error = "Something went wrong. Try again."

    return render_template("index.html", weather=weather, error=error)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)