import time
from absl import app, logging
from flask import Flask, request, Response, jsonify, send_from_directory, abort
from flask_cors import CORS
import gpt_2_simple as gpt2
import os, sys, traceback
import tensorflow as tf
import requests

# Initialize Flask application
app = Flask(__name__)

CORS(app)

# load in weights and classes
sess = gpt2.start_tf_sess()
gpt2.load_gpt2(sess, run_name='play')

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

@app.route('/gen_text', methods=['POST','OPTIONS'])
def generate_story():
    global sess
    # input text is request.form['input']

    try:
        tf.reset_default_graph()
        sess.close()
        sess = gpt2.start_tf_sess()
        gpt2.load_gpt2(sess, run_name=request.form['genre'])
        print("GENRE")
        print(request.form['genre'])
        generated_text = gpt2.generate(sess,
              run_name=request.form['genre'],
              length=200,
              temperature=0.8,
              prefix=str(request.form['input']),
              nsamples=1,
              batch_size=1,
              return_as_list=True
              )[0]
        return Response(response=generated_text, status=200)

    except:
        traceback.print_exc(file=sys.stdout)
        print('aborting gen text')
        abort(404)
    generate_count = generate_count + 1

if __name__ == '__main__':
    app.run(debug=True, host = '0.0.0.0', port=8080)