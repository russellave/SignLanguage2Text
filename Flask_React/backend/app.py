import time
from absl import app, logging
import cv2
import numpy as np
import tensorflow as tf
from flask import Flask, request, Response, jsonify, send_from_directory, abort
from flask_cors import CORS
import os
from eval_i3d import run 
from w2s import init_and_load_model, translate_sentence
import gpt_2_simple as gpt2


# load in weights and classes
physical_devices = tf.config.experimental.list_physical_devices('GPU')
if len(physical_devices) > 0:
    tf.config.experimental.set_memory_growth(physical_devices[0], True)


# load in weights and classes
sess = gpt2.start_tf_sess()
gpt2.load_gpt2(sess, run_name='play')

# Initialize Flask application
app = Flask(__name__)

CORS(app)

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