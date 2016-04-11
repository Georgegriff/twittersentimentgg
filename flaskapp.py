from flask import Flask, render_template, request, jsonify, json, Response, redirect, url_for
from twitter_api_requests import TwitterAPI

import time
import itertools

app = Flask(__name__)
-app.config.from_pyfile('flaskapp.cfg')
from site_conf import SiteConfig
import os
import csv

SiteConfig(app)
api = TwitterAPI()

region_codes = {}


def init_geo_codes():
    file_path = os.path.join(os.path.dirname(__file__), "./state_latlon.csv")
    with open(file_path, 'rb') as csvfile:
        filereader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in filereader:
            region_codes["US-" + row[0]] = {'lat': row[1], 'lng': row[2]}


init_geo_codes()


def get_geo_string(code):
    loc = region_codes[code]
    return loc["lat"] + "," + loc["lng"] + ",250mi"


@app.route('/')
def home_page():
    return render_template('index.html')


@app.route('/trending')
def trending_topics():
    return jsonify({'trending': api.find_trending()})


@app.route('/linearsvc')
def predict_linear_svc():
    search_term = request.args.get('q')
    code = request.args.get('code')
    geo = get_geo_string(code)

    return api.search_twitter(search_term, geo, code, 100, 400)


app.secret_key = 'gg_secret_cw'
app.debug = True

if __name__ == '__main__':
    app.run()
