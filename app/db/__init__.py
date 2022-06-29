import json
from collections import defaultdict as ddc

from flask import current_app
from werkzeug.exceptions import abort

def read_json(path):
    with open(path) as f:
        return json.load(f)


def get_demo(id):
    demo = read_json(current_app.root_path+'/data/db.json')[id]
    if demo is None:
        abort(404, 'Demo does not exist.')
    return demo


def get_tags():
    dm, dp, dt = ddc(lambda:0), ddc(lambda:0), ddc(lambda:0)  # tags for math, python and topic separated
    all = set()
    content = read_json(current_app.root_path+'/data/db.json')

    for _, value in content.items():
        for tag in value['tags_math']:
            dm[tag]+=1
            all.add(tag)
        for tag in value['tags_python']:
            dp[tag]+=1
            all.add(tag)
        for tag in value['tags_topic']:
            dt[tag]+=1
            all.add(tag)

    lm = [key + ': ' + str(value) + 'x' for key, value in dm.items()]
    lp = [key + ': ' + str(value) + 'x' for key, value in dp.items()]
    lt = [key + ': ' + str(value) + 'x' for key, value in dt.items()]
    return (lm, lp, lt, all)


def get_tag_content(tag):
    ans = {}
    content = read_json(current_app.root_path+'/data/db.json')
    # *_, tags = get_tags()
    for key, value in content.items():
        if tag in value['tags_math']:
            ans[key]=value
        elif tag in value['tags_python']:
            ans[key]=value
        elif tag in value['tags_topic']:
            ans[key]=value
        else:
            pass
    with open(current_app.root_path+'test.json','w') as f:
        json.dump(ans,f, indent=4)
    return ans