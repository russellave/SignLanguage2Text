import time
from absl import app, logging
import cv2
import numpy as np
import tensorflow as tf
from flask import Flask, request, Response, jsonify, send_from_directory, abort
from flask_cors import CORS
import os
from eval_i3d import run 


# load in weights and classes
physical_devices = tf.config.experimental.list_physical_devices('GPU')
if len(physical_devices) > 0:
    tf.config.experimental.set_memory_growth(physical_devices[0], True)

# Initialize Flask application
app = Flask(__name__)

CORS(app)

@app.route('/gen_text', methods=['POST','OPTIONS'])
def generate_story():
    # input text is request.form['input']
    try:
        return Response(response='ABCD '+request.form['input'], status=200)
    except:
        print('aborting gen text')
        abort(404)

@app.route('/w2s', methods=['POST','OPTIONS'])
def generate_sentence():
    # input text is request.form['input']
    try:
        return Response(response='ABCD '+request.form['input'], status=200)
    except:
        print('aborting w2s text')
        abort(404)

@app.route('/vid2text', methods=['POST','OPTIONS'])
def video_to_text():
    print('in video to text')
    print('**************************************************')
    print("Here is the request: ", request)
    print('**************************************************')
    print("Here is request.files:", request.files)
    # input video is request.files['video']
    video = request.files['video']
    video_name = video.filename

    for f in os.listdir(os.path.join(os.getcwd(), 'eval_vids')):
        os.remove(os.path.join(os.getcwd(), 'eval_vids', f))
    video.save(os.path.join(os.getcwd(), 'eval_vids', video_name))


    mode = 'rgb'
    num_classes = 1042 #look at preprocess ms-asl class list
    save_model = './checkpoints/' #doesn't matter

    root = 'eval_vids' #where data is

    train_split =  'preprocess/eval.json' #doesn't matter
    weights = 'weights/unproc_bs4_456225.pt' #where weights are

    pred = '0'
    pred = run(mode=mode, root=root, save_model=save_model, train_split=train_split, weights=weights, num_classes = num_classes)
    print ('prediction received in app.py: ', pred)
    print(type(pred))
    try:
        return Response(response= pred, status=200)
    except:
        print('aborting vid2text')
        abort(404)


if __name__ == '__main__':
    app.run(debug=True, host = '0.0.0.0', port=5000)