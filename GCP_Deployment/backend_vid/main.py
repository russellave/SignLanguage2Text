import time
from absl import app, logging
import numpy as np
from flask import Flask, request, Response, jsonify, send_from_directory, abort
from flask_cors import CORS
import os
from eval_one_i3d import runx




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
    weights = 'weights/nslt_1042_007480_0.516498.pt' #where weights are

    pred = '0'
    spot = str(os.path.join(os.getcwd(), 'eval_vids', video_name))
    print(spot)
    pred = runx(spot, mode='rgb', weights=weights)
    # pred = runx(mode=mode, root=root, save_model=save_model, train_split=train_split, weights=weights, num_classes = num_classes)
    print ('prediction received in app.py: ', pred)
    print(type(pred))
    try:
        return Response(response= pred, status=200)

    except:
        print('aborting vid2text')
        abort(404)


if __name__ == '__main__':
    app.run(debug=True, host = '0.0.0.0', port=8080)