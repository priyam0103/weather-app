from flask import Flask, render_template, request
import requests

app = Flask(__name__)

API_KEY = "YOUR_API_KEY_HERE"

@app.route("/", methods=["GET", "POST"])
def home():
    weather = None
    error = None

    if request.method == "POST":
        city = request.form.get("city")

        if city:
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

            try:
                response = requests.get(url)
                data = response.json()

                if data["cod"] == 200:
                    weather = {
                        "city": data["name"],
                        "temp": data["main"]["temp"],
                        "humidity": data["main"]["humidity"],
                        "wind": data["wind"]["speed"],
                        "desc": data["weather"][0]["description"]
                    }
                else:
                    error = "City not found!"
            except:
                error = "Something went wrong!"

    return render_template("index.html", weather=weather, error=error)

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)