from flask import Flask, render_template, json, jsonify, request, current_app as app
from sense_hat import SenseHat
from datetime import date
from time import sleep
import webbrowser
import os
import requests

app = Flask(__name__, static_folder="static")

@app.route('/')
def index():
    return render_template('index.html')

running = "no"
localList = []
@app.route('/show', methods=['GET','POST'])
def display_sense():
    if request.method == 'POST':
        global running
        global localList
        if running == "no":
            show = request.form['show']
            sense = SenseHat()
            sense.set_rotation(180)
            sense.low_light = True
            running = "yes"
            sense.show_message(show)
            localList.append(" "+show)
            running = "no"

    return render_template("index.html")

@app.route('/runImg', methods=['GET'])
def display_Img():
    results = []
    global running
    if 'show' in request.args and running == "no":
        show = request.args['show']
        sense = SenseHat()
        running = "yes"
        sense.load_image(show)
        running = "no"

    return render_template("index.html")

@app.route('/logs', methods=['GET'])
def display_all():
    global running
    global localList
    if running == "no":
        sense = SenseHat()
        sense.set_rotation(180)
        sense.low_light = True
        running = "yes"
        sense.show_message("".join(localList))
        running = "no"

    return render_template("index.html")

@app.route('/reset', methods=['GET'])
def log_reset():
    global localList
    localList = []
    return render_template("index.html")

if __name__ == '__main__':
 app.run(debug=True, host='0.0.0.0') 