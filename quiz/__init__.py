import json
from collections import OrderedDict
from flask import (
    Flask, 
    render_template, 
    jsonify,
)


app = Flask('HBR')


def load_quiz():
    with open('.quiz.json', 'r', encoding='UTF-8') as f:
        return json.load(f, object_pairs_hook=OrderedDict)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', quiz=load_quiz())


@app.route('/api/quiz', methods=['GET'])
def quiz():
    return jsonify(load_quiz())
