import os
import json

from flask import Flask
from .gallery.probability import prob_pee_sea

# from dash import Dash
# from werkzeug.wsgi import DispatcherMiddleware
# from werkzeug.serving import run_simple
# import dash_html_components as html


# dash_app1 = Dash(__name__, server = app, url_base_pathname='/dashboard/')
# dash_app2 = Dash(__name__, server = server, url_base_pathname='/reports/')
# dash_app1.layout = html.Div([html.H1('Hi there, I am Dash1')])
# dash_app2.layout = html.Div([html.H1('Hi there, I am Dash2')])

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        # DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # # root
    # @app.route('/home')
    from . import home
    app.register_blueprint(home.bp_home)
    app.add_url_rule('/', endpoint='home')

    from . import gallery
    app.register_blueprint(gallery.bp_gal)

    app.register_blueprint(gallery.bp_demo)
    app = prob_pee_sea(app)


    return app




