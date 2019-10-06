import os
import requests

import string
import random

from flask import Flask, jsonify, render_template, request, redirect, url_for
from flask_socketio import SocketIO, emit, join_room, leave_room, close_room, rooms

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)

votes = {}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/create")
def create_room():
    room_code = ''.join(random.choice(string.ascii_lowercase) for x in range(4))
    print(room_code)
    return redirect(url_for("room", room_code=room_code))

@app.route("/<string:room_code>")
def room(room_code):
    return render_template("vote.html", room_code=room_code)

###

@socketio.on('join', namespace='/test')
def on_join(data):
    room = data['room_code']
    join_room(room)
'''
@socketio.on('leave')
def on_leave(data):
    username = data['username']
    room = data['room']
    leave_room(room)
'''

@socketio.on("submit vote", namespace='/test')
def vote(data):
    room_code = data["room_code"]
    selection = data["selection"]
    try:
        votes[room_code]
    except KeyError:
        votes[room_code] = {"yes": 0, "no": 0, "maybe": 0}
    votes[room_code][selection] += 1
    emit("vote totals", votes[room_code], room_code=room_code)
    print(votes[room_code])
