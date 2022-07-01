from flask import (
    Blueprint, render_template, current_app
)

import app.db as db
from .fft import fft_intro
from .sets import sets_intro
from .probability import prob_pee_sea
from .quadratic import quad_pizza


bp_gal = Blueprint('gallery', __name__, url_prefix='/gallery')
bp_demo = Blueprint('demo', __name__, url_prefix='/demo')


@bp_gal.route('/')
@bp_gal.route('/<string:include_tags>', methods=['GET'])
def index(include_tags='all'):
    '''rfenders Gallery index page with all
    TODO: paging for the case of many demos
    '''
    if include_tags == 'all':
        content = db.read_json(current_app.root_path
                               + '/data/db.json')
    else:
        content = db.get_demos_by_tag(include_tags)

    return render_template(
            'gallery/index.html',
            demos=content,
            links=db.get_tags())


@bp_demo.route('/<string:id>', methods=['GET'])
def demo(id='random'):
    ''' Renders demo page based on the
    info from the json file.s
    '''
    demo = db.get_demo(id)
    if demo['type'] == 'dash':
        return render_template(
            'gallery/dash_item.html',
            demo=demo,
            dash_url=demo['url']
            )
    elif demo['type'] == 'plotly':
        plot = globals()[demo['pipe_name']]()
        return render_template(
            'gallery/item.html',
            demo=demo,
            plot=plot)
    else:
        return render_template(
            'todo.html',
            links=db.get_tags(),
            demo=demo)
