from flask import Flask, render_template, request, jsonify, json, Response, redirect, url_for
from twitter_api_requests import TwitterAPI
from twitter_svm import TwitterSVM
from twitter_naive_bay import TwitterBayes


app = Flask(__name__)
svm = TwitterSVM()
bay = TwitterBayes()
-app.config.from_pyfile('flaskapp.cfg')
from site_conf import SiteConfig
import os
import csv

SiteConfig(app)
api = TwitterAPI(svm, bay)

region_codes = {}


def init_geo_codes():
    file_path = os.path.join(os.path.dirname(__file__), "./state_twitter_place_id.csv")
    with open(file_path, 'rb') as csvfile:
        filereader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in filereader:
            if "USA" in row[3]:
                region_codes["US-" + row[0]] = {'lat': row[1], 'lng': row[2]}
            else:
                region_codes[row[0]] = {'lat': row[1], 'lng': row[2]}


init_geo_codes()


def get_geo_string(code):
    loc = region_codes[code]
    return loc["lat"] + "," + loc["lng"] + ",250mi"


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
    place_id = get_geo_string(code)

    return api.search_twitter('linearsvc',search_term, place_id, code, 100, 400)

@app.route('/bayes')
def predict_bayes():
    search_term = request.args.get('q')
    code = request.args.get('code')
    place_id = get_geo_string(code)

    return api.search_twitter('bayes',search_term, place_id, code, 100, 400)

@app.route('/accuracy')
def accuracy_al():
    algorithm = request.args.get('algorithm')
    output = {'accuracy' : 0}
    if algorithm == "linearsvc":
      output['accuracy'] = svm.calculate_accuracy()
    elif algorithm == "bayes":
        output['accuracy'] = bay.calculate_accuracy()

    return jsonify(output)


app.secret_key = 'gg_secret_cw'
app.debug = True

if __name__ == '__main__':
    app.run()
