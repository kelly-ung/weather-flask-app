import requests 
import os 
from flask import Flask, render_template, request, url_for 

# initialize Flask app
app = Flask(__name__)

# route for the home page
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST": # when the form is submitted
        API_KEY = os.environ.get("OPENWEATHER_API_KEY")
        city = str(request.form["city"]) # get the city name from the form
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&APPID={API_KEY}"
        response = requests.get(url).json() # make a request to the OpenWeatherMap API

        # error like unknown city name or invalid api key
        if response.get('cod') != 200:
            return render_template("error.html", city=city.title()) # render error page 

        # get current temperature and convert it into fahrenheit
        current_temperature = response.get("main", {}).get("temp")
        country = response.get("sys", {}).get("country")
        main = response.get("weather")[0].get("main") # get the main weather condition

        # determine the icon based on the main weather condition
        icon = None
        if main == "Clouds":
            icon = "icon1.png"
        elif main == "Clear":
            icon = "icon2.png"
        elif main == "Thunderstorm":
            icon = "icon3.png"
        elif main == "Rain" or "Drizzle":
            icon = "icon4.png"
        elif main == "Snow":
            icon = "icon5.png"
        elif main == "Mist" or "Smoke" or "Haze" or "Dust" or "Fog" or "Sand" or "Ash" or "Squall" or "Tornado":
            icon = "icon6.png"

        # check if current temperature is available and render the result page
        if current_temperature:
            current_temperature_fahrenheit = round((current_temperature - 273.15) * 1.8 + 32, 2)
            return render_template("result.html", city=city.title(), 
            current_temperature_fahrenheit=current_temperature_fahrenheit,
            country=country, main=main, icon=icon)   
        else: # if current temperature is not available, render error page
            return render_template("error.html", city=city.title())
    return render_template("home.html")

# create the Flask app
def create_app():
    return app

if __name__ == "__main__":
    app.run()