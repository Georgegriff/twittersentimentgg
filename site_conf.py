# myapp/util/assets.py
from flask_assets import Bundle, Environment
import os


class SiteConfig:
    def __init__(self, app):
        bundles = {

            'js': Bundle(
                'js/lib/jquery.min.js',
                'js/lib/d3.v3.min.js',
                'js/lib/nv.d3.min.js',
                'js/lib/jquery-jvectormap-2.0.3.min.js',
                'js/lib/jquery-jvectormap.js',
                'js/lib/jquery-uk-jvectormap.js',
                'js/main.js',
                'js/charting.js',
                output='gen/index.js'),

            'css': Bundle(
                'css/lib/normalize.css',
                'css/lib/nv.d3.min.css',
                'css/main.css',
                'css/lib/jquery-jvectormap-2.0.3.css',
                output='gen/style.css'
            ),
        }

        assets = Environment(app)

        assets.register(bundles)
