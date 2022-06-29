from flask import (
    Blueprint, render_template
)

import app.db as db

bp_home = Blueprint('home', __name__, url_prefix='/')


@bp_home.route('/')
def home():
    return render_template(
                'home/home.html',
                links=db.get_tags(),
                )