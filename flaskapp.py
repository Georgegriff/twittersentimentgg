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
    file_path = os.path.join(os.path.dirname(__file__), "./state_twitter_place_id.csv")
    with open(file_path, 'rb') as csvfile:
        filereader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in filereader:
            if "USA" in row[3]:
                region_codes["US-" + row[0]] = {'place_id': row[1]}
            else:
                region_codes[row[0]] = {'place_id': row[1]}



init_geo_codes()


def get_place_id(code):
    print code
    loc = region_codes[code]
    return loc["place_id"]


@app.route('/')
def home_page():
    return render_template('index.html')


@app.route('/trending')
def trending_topics():
    loc = request.args.get('loc')
    if loc is not None:
        return jsonify({'trending': api.find_trending(loc)})
    else:
        return jsonify({'trending': api.find_trending()})


@app.route('/linearsvc')
def predict_linear_svc():
    search_term = request.args.get('q')
    code = request.args.get('code')
    place_id = get_place_id(code)

    return api.search_twitter(search_term, place_id, code, 100, 400)


app.secret_key = 'gg_secret_cw'
app.debug = True

if __name__ == '__main__':
    app.run()
