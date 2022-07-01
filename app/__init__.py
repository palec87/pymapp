import os

from flask import Flask
from .gallery.probability import prob_pee_sea

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev')

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
    from . import routes
    app.register_blueprint(routes.bp_home)
    app.add_url_rule('/', endpoint='home')

    app.register_blueprint(routes.bp_contact)
    app.add_url_rule('/contact', endpoint='contact')

    app.register_blueprint(routes.bp_todo)
    app.add_url_rule('/not-implemented', endpoint='not-implemented')

    # gallery
    from . import gallery
    app.register_blueprint(gallery.bp_gal)

    app.register_blueprint(gallery.bp_demo)

    # dash plotly app
    app = prob_pee_sea(app)

    return app




