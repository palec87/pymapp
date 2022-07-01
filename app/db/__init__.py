import json
import random
from collections import defaultdict as ddc

from flask import current_app
from werkzeug.exceptions import abort

def read_json(path):
    '''instead of sqlite I store data simply in json file'''
    with open(path) as f:
        return json.load(f)

def get_demo(id:str):
    '''read dict related to one specific demo'''
    if id == 'random':
        content = read_json(current_app.root_path
                            + '/data/db.json')
        name = random.choice(list(content.keys()))
        # this might link to the same tutorial again.
        demo = content[name]
    else:
        demo = read_json(current_app.root_path
                         + '/data/db.json')[id]
    
    if demo is None:
        abort(404, 'Demo does not exist.')
    return demo


def get_tags():
    '''
    count tag occurances
    create list of strings (tag #occurances)
    TODO: Once I have many, I have to pick some
     subset of those
    '''
    dm, dp, dt = ddc(lambda:0), ddc(lambda:0), ddc(lambda:0)  # tags for math, python and topic separated
    all = set()
    content = read_json(current_app.root_path
                        + '/data/db.json')

    # counting tag occurances for math/python/main topics 
    for _, value in content.items():
        for tag in value['tags_math']:
            dm[tag] += 1
            all.add(tag)
        for tag in value['tags_python']:
            dp[tag] += 1
            all.add(tag)
        for tag in value['tags_topic']:
            dt[tag] += 1
            all.add(tag)

    # creating string, tag name + #occurances
    lm = [key + ': ' + str(value) + 'x' for key, value in dm.items()]
    lp = [key + ': ' + str(value) + 'x' for key, value in dp.items()]
    lt = [key + ': ' + str(value) + 'x' for key, value in dt.items()]
    return (lm, lp, lt, all)

def get_demos_by_tag(tag:str):
    '''search all demos containng particular tag
    '''
    demos_tagged = {}
    content = read_json(current_app.root_path+'/data/db.json')

    for key, value in content.items():
        if tag in value['tags_math']:
            demos_tagged[key] = value
        elif tag in value['tags_python']:
            demos_tagged[key] = value
        elif tag in value['tags_topic']:
            demos_tagged[key] = value
        else:
            # TODO, handle error
            pass
    return demos_tagged