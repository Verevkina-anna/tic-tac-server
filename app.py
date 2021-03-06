"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/

This file creates your application.
"""

import os
from flask import Flask, render_template, request, redirect, url_for
from flask_cors import CORS
from flask_socketio import SocketIO, send, emit
from flask_pymongo import PyMongo
from flask import jsonify
from flask import request
from pymongo import MongoClient
from flask import request
import gameService
import datetime

import json
from bson import ObjectId
import jwt

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

app.config["MONGO_URI"] = "mongodb+srv://vlad123:qwerty123@tic-tac-toe-jtwsd.mongodb.net/scoreboard?retryWrites=true&w=majority"
# app.config['MONGO_DBNAME'] = 'scoreboard'
app.config['SECRET_KEY'] = 'hero'


###
# Routing for your application.
###

@app.route('/')
def home():
    """Render website's home page."""
    return '<h1> Deployed </h1>'

@app.route("/login")
def login():
    userName = request.args.get('userName')
    token = encode_auth_token(userName)
    return jsonify({"token": token})

@app.route("/checkLogin")
def checkLogin():
    bearer = request.headers['Authorization']
    userId = get_user_name(bearer)
    return userId

# returns created instance
@app.route("/create-score", methods=["POST"])
def createScore():
    bearer = request.headers['Authorization']
    userId = get_user_name(bearer)
    id = ObjectId()
    mongo.db.scoreboard.insert({"_id": id, "userName": userId, "winCount": 1})
    output = []
    for s in mongo.db.scoreboard.find({"_id": id}):
        output.append({'userName': s['userName'], 'winCount': s['winCount'], "_id": str(id)})
    return jsonify({'result': output})


@app.route('/set-score', methods=["PUT"])
def setScore():
    id = request.args.get("id")
    value = request.args.get('value')
    mongo.db.scoreboard.update({"_id": ObjectId(id)}, {"$set": {"winCount": int(value)}})
    return "done"

@app.route("/get-score")
def getScore():
    scores = mongo.db.scoreboard
    output = []
    for s in scores.find({}):
        output.append({'userName': s['userName'],'winCount': s['winCount'], "_id": str(s['_id'])})
    return jsonify({'result': output})



@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html')


###
# The functions below should be applicable to all Flask apps.
###

# @app.route('/<file_name>.txt')
# def send_text_file(file_name):
#     """Send your static text file."""
#     file_dot_text = file_name + '.txt'
#     return app.send_static_file(file_dot_text)
#
#
# @app.after_request
# def add_header(response):
#     """
#     Add headers to both force latest IE rendering engine or Chrome Frame,
#     and also to cache the rendered page for 10 minutes.
#     """
#     response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
#     response.headers['Cache-Control'] = 'public, max-age=600'
#     return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


@socketio.on('message')
def handle_message(data):
    print('received message: ', data)

@socketio.on('json')
def handle_json(json):
    print json['token']
    userName = decode_auth_token(json['token'])
    print userName
    result = gameService.checkStepAvailable(json)
    send(result)

@socketio.on('connect')
def test_connect():
    send('Connected from server')


mongo = PyMongo(app)

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

def encode_auth_token(user_id):
    """
    Generates the Auth Token
    :return: string
    """
    try:
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
            'iat': datetime.datetime.utcnow(),
            'sub': user_id
        }
        return jwt.encode(
            payload,
            app.config.get('SECRET_KEY'),
            algorithm='HS256'
        )
    except Exception as e:
        return e

def decode_auth_token(auth_token):
    """
    Decodes the auth token
    :param auth_token:
    :return: integer|string
    """
    try:
        payload = jwt.decode(auth_token, app.config.get('SECRET_KEY'))
        return payload['sub']
    except jwt.ExpiredSignatureError:
        return 'Signature expired. Please log in again.'
    except jwt.InvalidTokenError:
        return 'Invalid token. Please log in again.'


def get_user_name(bearer):
    if bearer:
        token = bearer.split("Bearer ")[1]
        return decode_auth_token(token)

if __name__ == '__main__':
    socketio.run(app, cors_allowed_origins="*")
