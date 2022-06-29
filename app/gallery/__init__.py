from flask import (
    Blueprint, g, render_template, request, url_for,current_app
)
from werkzeug.exceptions import abort
import json

import app.db as db
from .fft import fft_intro
from .sets import sets_intro
from .probability import prob_pee_sea
from .quadratic import quad_pizza
from collections import defaultdict as ddc
# from flaskr.auth import login_required
# from flaskr.db import get_db

# with open(current_app.root_path+'/data/db.json') as f:
#     global DB
#     DB = json.load(f)

bp_gal = Blueprint('gallery', __name__, url_prefix='/gallery')
bp_demo = Blueprint('demo', __name__, url_prefix='/demo')


@bp_gal.route('/')
@bp_gal.route('/<string:include_tags>',methods= ['GET'])
def index(include_tags='all'):
    if include_tags=='all':
        content = db.read_json(current_app.root_path+'/data/db.json')
    else:
        content = db.get_tag_content(include_tags)

    return render_template(
                'gallery/index.html',
                demos=content,
                links=db.get_tags()
                )


@bp_demo.route('/<string:id>', methods=['GET'])
def demo(id):
    demo = db.get_demo(id)
    if demo['type']=='dash':
        return render_template(
            'gallery/dash_item.html', 
            demo=demo,
            dash_url=demo['url']
            )
    else:
        plot = globals()[demo['pipe_name']]()
        return render_template(
            'gallery/item.html', 
            demo=demo,
            plot=plot
            )

