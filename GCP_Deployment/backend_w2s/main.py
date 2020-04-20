import time
from absl import app, logging
from flask import Flask, request, Response, jsonify, send_from_directory, abort
from flask_cors import CORS
import os, sys, traceback
import requests
from w2s import init_and_load_model, translate_sentence

# Initialize Flask application
app = Flask(__name__)

CORS(app)

@app.route('/caroline', methods=['POST','OPTIONS'])
def hi_caroline():
    print('did I make it?')
    print(request)
    print("data:", request.data)
    print("values:", request.values)
    print("form:", request.form)
    try:
        return Response(response='Hi '+request.form['name'], status=200)
    except:
        abort(404)

@app.route('/w2s', methods=['POST','OPTIONS'])
def generate_sentence():
    # input text is request.form['input']
    model_path  = './cc_model_5p.pt'
    model = init_and_load_model(model_path)
    sentence, logits = translate_sentence(model, request.form['input'])

    try:
        return Response(response=sentence, status=200)
    except:
        print('aborting w2s text')
        abort(404)

if __name__ == '__main__':
    app.run(debug=True, host = '0.0.0.0', port=8080)