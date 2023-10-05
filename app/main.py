import os
from flask import Flask
import routes
import gallery


app = Flask(__name__)
app.config.from_mapping(
    SECRET_KEY='dev')

# ensure the instance folder exists
try:
    os.makedirs(app.instance_path)
except OSError:
    pass

print(app.instance_path)

from gallery.probability import prob_pee_sea
from gallery.quadratic import quad_pizza
from gallery.fft_compression import compress_fourier
from gallery.newton_disc import nd
from gallery.spectrometer import spectrometer

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
app = spectrometer(app)

if __name__ == "__main__":
    app.run()
