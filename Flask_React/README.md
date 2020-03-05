# How I get it to run on my laptop:
This may be in more detail/have more explanation than you need, but I went for more just in case anyone needs it (I would have needed it).  

I have a PC.  I think things should be the same for Mac, but I make no promises.

## To install all the libraries and such that you'll need so far: 
`pip install -r requirements.txt` (only needs to be done the first time)

It's possible that I already had some things installed and didn't realize they were missing from requirements.txt, so if you get an error saying something wasn't found when you try to run things, just install it and add it to requirements.txt for other people's future use.  

## To download the weights of the object detection model:
These weights are too big to push to git, so they're git ignored and you'll need to download them yourself.  If you don't want to bother with this because we won't need these weights for the real project, you can just test with the "Say Hi" part instead of the person detection part.  

Open a terminal. 

`wget https://pjreddie.com/media/files/yolov3.weights -O weights/yolov3.weights`

You can also download the tiny yolo weights using this command: 

`wget https://pjreddie.com/media/files/yolov3-tiny.weights -O weights/yolov3-tiny.weights`

but unless you change the parameters that are set now you shouldn't need them. 

## Running backend 
Open a terminal.  cd into backend folder. 

`python app.py`

This will run the backend part.  From what I understand, flask makes it so that when this is running you can send API requests to the location specified in app.py.  The last line in app.py is currently "app.run(debug=True, host = '0.0.0.0', port=5000)", so you can send requests to localhost:5000 (based on the host and port arguments).  

## Running frontend 
Open another terminal.  cd into frontend folder. 

`npm run `

A tab should automatically open up in your browser, and you'll be able to see and play around with the frontend interface.  


# Things that I learned that might be useful / how to edit and add to what's here so far: 

## Using Postman to test backend 
If you want to be able to test that the backend is working without having the frontend piece of it up and running, you can use Postman.  Postman lets you send API requests to a host and port that you specify.  So you can mimic the requests that your frontend would make to check backend functionality.  It's pretty simple to use.  

Download Postman from https://www.postman.com/downloads/

Run the backend (open a terminal, cd into backend folder, `python app.py`)

Open Postman.  Click "Create a request" on the launchpad screen.  

Click on Body in the row of tabs under where it says Send.  Select the form-data option.  

Now you'll be able to make a request that matches what our frontend will send.  Requests are in JSON format, so they'll basically look like a collection of Python dictionaries.  There will be one dictionary of files and one of text.  Within each of those, every entry has a key and value (like in a normal dictionary).  

You can see how Postman lets you construct an entry that has this format - you can specify the key, value, and whether it's a File or Text (shows up when you hover over Key). So you can choose File vs. Text and type in your key and value.  

Then, at the top, you can enter the address that Postman should send the request to.  With everything how it's set up right now, you want it to be http://localhost:5000/whatever_backend_route_youre_testing.  Change the method type to the left of that to be whatever you're testing.  When you hit send, you'll see the response you get back underneath the place where you enter the key and value fields.  

Here's what you would enter into all of those places to get a response that says "Hi SignLanguage2Text":
- key: name
- Text, not File 
- value: SignLanguage2Text
- method: select POST from the dropdown menu 
- request URL: http://localhost:5000/caroline


## Adding to backend 
adding route
route decorator and how it relates to the function and how that gets used in the frontend to connect things together
can print to terminal to help debug 
### I'll finish this soon

## Adding to frontend 
axios - what it does, why, how it's similar to what postman is doing 
inspecting page and going to console, console.log 
files and form in request 
react components and pages 
finding react components to use online 
### I'll finish this soon 



# Instructions from original backend git repo (where some of the stuff above comes from):
[Here](https://github.com/theAIGuysCode/Object-Detection-API) is the original backend repo that I added to a little bit.
## Yolov3 Object Detection with Flask and Tensorflow 2.0 (APIs and Detections)
Yolov3 is an algorithm that uses deep convolutional neural networks to perform object detection. This repository implements Yolov3 using TensorFlow 2.0 and creates two easy-to-use APIs that you can integrate into web or mobile applications. <br>

![example](https://github.com/theAIGuysCode/Object-Detection-API/blob/master/detections/detection.jpg)

## Getting started

#### Conda (Recommended)

```bash
# Tensorflow CPU
conda env create -f conda-cpu.yml
conda activate yolov3-object-detection-cpu

# Tensorflow GPU
conda env create -f conda-gpu.yml
conda activate yolov3-object-detection-gpu
```

#### Pip
```bash
# TensorFlow CPU
pip install -r requirements.txt

# TensorFlow GPU
pip install -r requirements-gpu.txt
```

### Nvidia Driver (For GPU, if you haven't set it up already)
```bash
# Ubuntu 18.04
sudo apt-add-repository -r ppa:graphics-drivers/ppa
sudo apt install nvidia-driver-430
# Windows/Other
https://www.nvidia.com/Download/index.aspx
```
### Downloading official pretrained weights
For Linux: Let's download official yolov3 weights pretrained on COCO dataset. 

```
# yolov3
wget https://pjreddie.com/media/files/yolov3.weights -O weights/yolov3.weights

# yolov3-tiny
wget https://pjreddie.com/media/files/yolov3-tiny.weights -O weights/yolov3-tiny.weights
```
For Windows:
You can download the yolov3 weights by clicking [here](https://pjreddie.com/media/files/yolov3.weights) and yolov3-tiny [here](https://pjreddie.com/media/files/yolov3-tiny.weights) then save them to the weights folder.

### Using Custom trained weights
<strong> Learn How To Train Custom YOLOV3 Weights Here: https://www.youtube.com/watch?v=zJDUhGL26iU </strong>

Add your custom weights file to weights folder and your custom .names file into data/labels folder.
  
### Saving your yolov3 weights as a TensorFlow model.
Load the weights using `load_weights.py` script. This will convert the yolov3 weights into TensorFlow .ckpt model files!

```
# yolov3
python load_weights.py

# yolov3-tiny
python load_weights.py --weights ./weights/yolov3-tiny.weights --output ./weights/yolov3-tiny.tf --tiny
```

After executing one of the above lines, you should see .tf files in your weights folder.

## Running the Flask App and Using the APIs
Now you can run a Flask application to create two object detections APIs in order to get detections through REST endpoints.

If you used custom weights and classes then you may need to adjust one or two of the following lines within the app.py file before running it.
![app](https://github.com/theAIGuysCode/Object-Detection-API/blob/master/data/helpers/custom_app.PNG)

You may also want to configure IOU threshold (how close two of the same class have to be in order to count it as one detection), the Confidence threshold (minimum detected confidence of a class in order to count it as a detection), or the maximum number of classes that can be detected in one image and all three can be adjusted within the yolov3-tf2/models.py file.
![models](https://github.com/theAIGuysCode/Object-Detection-API/blob/master/data/helpers/model_config.PNG)

Initialize and run the Flask app on port 5000 of your local machine by running the following command from the root directory of this repo in a command prompt or shell.
```bash
python app.py
```

You should see the following appear in the command prompt if the app is successfully running.
![app](https://github.com/theAIGuysCode/Object-Detection-API/blob/master/data/helpers/app_running.PNG)

### Detections API (http://localhost:5000/detections)
While app.py is running the first available API is a POST routed to /detections on port 5000 of localhost. This endpoint takes in images as input and returns a JSON response with all the detections found within each image (classes found within the images and the associated confidence)

You can test out the APIs using Postman or through Curl commands (both work fine). You may have to download them if you don't already have them.

#### Accessing Detections API with Postman (RECOMMENDED)
Access the /detections API through Postman by doing the following.
![postman](https://github.com/theAIGuysCode/Object-Detection-API/blob/master/data/helpers/detections_api_config.PNG)
Note that the body has to have key "images of type "form-data" set to file. When uploading files hold CTRL button and click to choose multiple photos.

The response should look similar to this.
![response](https://github.com/theAIGuysCode/Object-Detection-API/blob/master/data/helpers/detections_api_response.PNG)

#### Accessing Detections API with Curl 
To access and test the API through Curl, open a second command prompt or shell (may have to run as Administrator). Then cd your way to the root folder of this repository (Object-Detection-API) and run the following command.
```bash
curl.exe -X POST -F images=@data/images/dog.jpg "http://localhost:5000/detections"
```
The JSON response should be outputted to the commmand prompt if it worked successfully.

### Image API (http://localhost:5000/image)
While app.py is running the second available API is a POST routed to /image on port 5000 of localhost. This endpoint takes in a single image as input and returns a string encoded image as the response with all the detections now drawn on the image.

#### Accessing Detections API with Postman (RECOMMENDED)
Access the /image API through Postman by configuring the following.
![postman](https://github.com/theAIGuysCode/Object-Detection-API/blob/master/data/helpers/image_api_config.PNG)

The uploaded image should be returned with the detections now drawn.
![postman](https://github.com/theAIGuysCode/Object-Detection-API/blob/master/data/helpers/image_api_response.PNG)

#### Accessing Detections API with Curl 
To access and test the API through Curl, open a second command prompt or shell (may have to run as Administrator). Then cd your way to the root folder of this repository (Object-Detection-API) and run the following command.
```bash
curl.exe -X POST -F images=@data/images/dog.jpg "http://localhost:5000/image" --output test.png
```
This will save the returned image to the current folder as test.png (can't output the string encoded image to command prompt)

<strong> NOTE: </strong> As a backup both APIs save the images with the detections drawn overtop to the /detections folder upon each API request.

These are the two APIs I currently have created for Yolov3 Object Detection and I hope you find them useful. Feel free to integrate them into your applications as needed.

## Running just the TensorFlow model
The tensorflow model can also be run not using the APIs but through using `detect.py` script. 

Don't forget to set the IoU (Intersection over Union) and Confidence Thresholds within your yolov3-tf2/models.py file

### Usage examples
Let's run an example or two using sample images found within the data/images folder. 
```bash
# yolov3
python detect.py --images "data/images/dog.jpg, data/images/office.jpg"

# yolov3-tiny
python detect.py --weights ./weights/yolov3-tiny.tf --tiny --images "data/images/dog.jpg"

# webcam
python detect_video.py --video 0

# video file
python detect_video.py --video data/video/paris.mp4 --weights ./weights/yolov3-tiny.tf --tiny

# video file with output saved (can save webcam like this too)
python detect_video.py --video path_to_file.mp4 --output ./detections/output.avi
```
Then you can find the detections in the `detections` folder.
<br>
You should see these two images saved for running the first command.
```
detection1.jpg
```
![demo](https://github.com/theAIGuysCode/Object-Detection-API/blob/master/detections/detection1.jpg)
```
detection2.jpg
```
![demo](https://github.com/theAIGuysCode/Object-Detection-API/blob/master/detections/detection2.jpg)

### Video example
![demo](https://github.com/heartkilla/yolo-v3/blob/master/data/detection_examples/detections.gif)

## Command Line Args Reference

```bash
load_weights.py:
  --output: path to output
    (default: './weights/yolov3.tf')
  --[no]tiny: yolov3 or yolov3-tiny
    (default: 'false')
  --weights: path to weights file
    (default: './weights/yolov3.weights')
  --num_classes: number of classes in the model
    (default: '80')
    (an integer)

detect.py:
  --classes: path to classes file
    (default: './data/labels/coco.names')
  --images: path to input images as a string with images separated by ","
    (default: 'data/images/dog.jpg')
  --output: path to output folder
    (default: './detections/')
  --[no]tiny: yolov3 or yolov3-tiny
    (default: 'false')
  --weights: path to weights file
    (default: './weights/yolov3.tf')
  --num_classes: number of classes in the model
    (default: '80')
    (an integer)

detect_video.py:
  --classes: path to classes file
    (default: './data/labels/coco.names')
  --video: path to input video (use 0 for webcam)
    (default: './data/video/paris.mp4')
  --output: path to output video (remember to set right codec for given format. e.g. XVID for .avi)
    (default: None)
  --output_format: codec used in VideoWriter when saving video to file
    (default: 'XVID)
  --[no]tiny: yolov3 or yolov3-tiny
    (default: 'false')
  --weights: path to weights file
    (default: './checkpoints/yolov3.tf')
  --num_classes: number of classes in the model
    (default: '80')
    (an integer)
```

## Acknowledgments
* [Yolov3 TensorFlow 2 Amazing Implementation](https://github.com/zzh8829/yolov3-tf2)
* [Another Yolov3 TensorFlow 2](https://github.com/heartkilla/yolo-v3)
* [Yolo v3 official paper](https://arxiv.org/abs/1804.02767)
* [A Tensorflow Slim implementation](https://github.com/mystic123/tensorflow-yolo-v3)
