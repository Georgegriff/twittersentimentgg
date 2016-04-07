from flask import Flask, render_template, request, jsonify, json, Response, redirect, url_for
from twitter_api_requests import TwitterAPI
from twitter_svm import TwitterSVM
import time
import itertools

app = Flask(__name__)
app.config.from_pyfile('flaskapp.cfg')

from site_conf import SiteConfig

SiteConfig(app)
api = TwitterAPI()
svm = TwitterSVM()


@app.route('/')
def home_page():
    return render_template('index.html')


@app.route('/trending')
def trending_topics():
    return jsonify({'trending': api.find_trending()})


@app.route('/linearsvc')
def predict_linear_svc():
    search_term = request.args.get('q')

    tweets = api.search_twitter(search_term, 1000)
    def events():
        for tweet in tweets:
            results = svm.predict([tweet.text])
            yield '{"data":{"result": %s}}' % (results[0])
            yield ','


    return Response(events(), mimetype='application/json')

app.secret_key = 'gg_secret_cw'
app.debug = True

if __name__ == '__main__':
    app.run()
