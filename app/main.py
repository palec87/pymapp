import os

from flask import Flask
from gallery.probability import prob_pee_sea
from gallery.quadratic import quad_pizza
from gallery.fft_compression import compress_fourier
from gallery.newton_disc import nd
import routes
import gallery


# def create_app(test_config=None):
app = Flask(__name__)  # , instance_relative_config=True)
app.config.from_mapping(
    SECRET_KEY='dev')

# if test_config is None:
#     # load the instance config, if it exists, when not testing
#     app.config.from_pyfile('config.py', silent=True)
# else:
#     # load the test config if passed in
#     app.config.from_mapping(test_config)

# ensure the instance folder exists
try:
    os.makedirs(app.instance_path)
except OSError:
    pass

# # root
app.register_blueprint(routes.bp_home)
app.add_url_rule('/', endpoint='home')

app.register_blueprint(routes.bp_contact)
app.add_url_rule('/contact', endpoint='contact')

app.register_blueprint(routes.bp_todo)
app.add_url_rule('/not-implemented', endpoint='not-implemented')

# gallery
app.register_blueprint(gallery.bp_gal)

app.register_blueprint(gallery.bp_demo)

# dash plotly apps
app = prob_pee_sea(app)
app = quad_pizza(app)
app = compress_fourier(app)
app = nd(app)

if __name__ == "__main__":
    # from waitress import serve
    # serve(app, host="127.0.0.1", port=5000)
    app.run()
