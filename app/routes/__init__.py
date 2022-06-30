from flask import (
    Blueprint, render_template
)

import app.db as db

bp_home = Blueprint('home', __name__, url_prefix='/')
bp_contact = Blueprint('contact', __name__, url_prefix='/')
bp_todo = Blueprint('not-implemented', __name__)


@bp_home.route('/')
def home():
    return render_template(
                'home.html',
                links=db.get_tags(),
                )

@bp_contact.route('/contact')
def contact():
    return render_template(
                'contact.html',
                links=db.get_tags(),
                )

@bp_todo.route('/not-implemented')
def todo():
    return render_template(
                'todo.html',
                links=db.get_tags(),
                )               
