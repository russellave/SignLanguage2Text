# Disclaimers:
This may be in more detail/have more explanation than you need, but I went for more just in case anyone needs it (I would have needed it).  Also, some of the terminology could be wrong or imprecise - this is my best guess at the right words based on a few days of learning this stuff.  

I have a PC.  I think things should be the same for Mac, but I make no promises.

# Word to Sentences extra steps:
`python -m spacy download en_core_web_sm`
added spacy and torchtext to requirements.txt

# How I get it to run on my laptop:

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

`npm install`

`npm run `

A tab should automatically open up in your browser, and you'll be able to see and play around with the frontend interface.  

Note: if `npm run` doesn't work, try `npm start` - worked for me


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
To add new backend functionality (add a python function of some sort that you want to run when something happens on the website - like a person clicking a button), the main file you need to work with is backend/app.py.  

Debugging:
- Postman 
- Print statements - will print to the console that you run the backend from 

Adding a function:
- Write the Python function that you want to call, in mostly normal Python syntax, with these exceptions:
  -  The function will automatically receive an argument called 'request' which is the JSON file that gets sent to whatever was sent to the route that you specify for this function.  You can print the request to see what's in it.  To get the dictionary of files in it, do request.files.  To get the dictionary of text in it, do request.form.  You can index into those dictionaries using the keys you put into the JSON file.  
  - Put a decorator on the line above the function definition that is in a format like this: `@app.route('/caroline', methods=['POST','OPTIONS'])` where `/caroline` is replaced by whatever route you want to be attached to this function and `methods` has whatever API call methods are allowed for it.  So, when I put this decorator above the `hi_caroline` function in app.py, I made it so that when a `POST` or `OPTIONS` API request is sent to `hostaddress/caroline`, `hi_caroline` is called.  The names `/caroline` and `hi_caroline` don't have to be related to each other; the placement of the decorator is what connects the route to the function.  
- You can call functions from other files within the one in app.py as long as you import them 

## Adding to frontend 
Debugging: 
- In your browser, right click, click inspect, and then click console.  You can use console.log to print stuff to here.

Using React 
- For most things you can think of that you need, you can google "(thing that you need) react" and find an existing component that pretty much does it.  You'll probably need to use npm to install things to get it to work, but that's easy.  
- Within html tags, you can use curly braces { } to use javascript.  A simple example where this is useful is if you want to make a header that displays the content of some variable "num_clicks"; you would do `<h1> {num_clicks} </h1>`.  
- You can add and update key value pairs to the component's state (this.state).  This is super useful.  You can look through uploader.jsx to see a few examples of it.  
- You can import components from other components.  This lets you make more complex things while keeping it modular.  One common place where this is done is in making different pages of a website; you could have a home page component that has multiple other components in it.  
- Components can have css files to set the styling.  
- Please make sure to add the `--save` keyword when you `npm install` anything - that makes sure to add the dependency to the package info so that when somebody runs `npm install` initially, they also install the package.

Sending requests to backend 
- We saw before how we can send requests to the backend using Postman.  All we need to be able to do from the frontend is to send the requests that we already tested and sent in Postman.  Axios lets us do this.  

Here's some code using axios to send requests from frontend/uploader.jsx:
- `const data = new FormData();` - This line creates a new FormData instance; FormData is what we need to add to and send as our request.  

- `data.append('name', this.state.name)` - This line shows how to add an entry into the request.  If the value is text, it will automatically go to the text (form) dictionary.  If it's a file, it will automatically go to the file dictionary.  
-     axios.post("http://localhost:5000/caroline", data). then(res => {
        console.log(res);
        this.setState({
        display_str: res.data
        })
      })
 There are two important things going on with this:
  1. The `axios.post` part - here's where you specify where to send the request and what to send. 
  2. The `.then()` part - Anything inside of the .then function will wait to run until the request is sent and the response is received.  Whatever is received will go into the variable `res` (or whatever other name you give a variable in the same position).  You can then do whatever you need to with that response: in this case, print it to the console and set the state to hold the data field.  

There are a lot more things to be said about React/Javscript/HTML/CSS that I'm not the best person to tell you, but there are tons of useful tutorials and things like that available, and hopefully this is enough to explain most of the connecting frontend to backend stuff and some basics of how to read what's here so far and add new components.  

# Link to original backend git repo (where some of the stuff above comes from):
[Here](https://github.com/theAIGuysCode/Object-Detection-API) is the original backend repo that I added to a little bit. Their readme has a lot of information, so if something that you need isn't here, it might be there.  
