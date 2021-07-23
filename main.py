# Created by kor_a at 23/07/2021
from flask import Flask, render_template, request, jsonify
import requests
import pyshorteners
from covid import Covid
import random
import string

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/links")
def links():
    return render_template("links.html")

@app.route("/apod")
def apod():
    apod = requests.get("https://api.nasa.gov/planetary/apod?api_key=aBqBMm12sPeFWcVTnoiDMeqcGJx3kMe7WF33Fgvw")
    apod_json = apod.json()
    title = apod_json['title']
    explanation = apod_json['explanation']
    media_type = apod_json['media_type']
    if(media_type == 'image'):
        media = apod_json['hdurl']
    else:
        media = apod_json['url']

    return render_template("apod.html", title=title, explanation=explanation, media=media, media_type=media_type)

@app.route("/urlshort")
def urlshort():
    return render_template("urlshort.html")

@app.route("/urlshort", methods=['POST'])
def urlshorten():
    shortener = pyshorteners.Shortener()
    url = request.form['text']
    processed = shortener.tinyurl.short(url)
    return processed

@app.route("/covid")
def getCovid():
    return render_template("covid.html")

@app.route("/covid", methods=['POST'])
def getCoviddd():
    country = request.form['covid']
    covid = Covid()
    data = covid.get_status_by_country_name(country)
    cadr = {
        key: data[key]
        for key in data.keys() & {"confirmed", "active", "deaths", "recovered"}
    }
    return cadr


@app.route("/get_my_ip", methods=["GET"])
def get_my_ip():
    return jsonify({'ip': request.environ.get('HTTP_X_REAL_IP', request.remote_addr)}), 200


@app.route("/randpassgen")
def randpassgen():
    return render_template("randpassgen.html")

@app.route("/randpassgen", methods=['POST'])
def generate():
    length = int(request.form['password'])

    lower = string.ascii_lowercase
    upper = string.ascii_uppercase
    num = string.digits
    symbols = string.punctuation

    all = lower + upper + num + symbols

    password = ''.join([random.choice(all) for _ in range(length)])

    return password



if __name__ == "__main__":
    app.run()
