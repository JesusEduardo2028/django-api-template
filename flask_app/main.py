from flask import Flask, request, jsonify, json, make_response
import requests
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import jwt
import datetime
from functools import wraps

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
CORS(app)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

app.config['SECRET_KEY'] = 'secretkey'


def validationToken(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        #token = request.json['token']
        token = request.args.get('token')

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
        except:
            return jsonify({'message': 'Invalid token'}), 403

        return f(*args, **kwargs)

    return decorated


app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:12345678@localhost:3306/fadbdev'

db = SQLAlchemy(app)


class Users(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    user = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    urlPhoto = db.Column(db.String(300), nullable=False)
    facebook_id = db.Column(db.String(100), unique=True, nullable=True)
    google_id = db.Column(db.String(100), unique=True, nullable=True)

    def __init__(self, user, name, urlPhoto, facebookId, googleId):
        self.user = user
        self.name = name
        self.urlPhoto = urlPhoto
        self.facebook_id = facebookId
        self.google_id = googleId


@app.route('/register', methods=['POST'])
def createUser():
    try:
        user = request.json['user']
        name = request.json['name']
        urlPhoto = request.json['urlPhoto']
        facebookId = request.json['facebookId']
        googleId = request.json['googleId']
        print('Paso', request.get_json())
        newUser = Users(user, name, urlPhoto, facebookId, googleId)

        db.session.add(newUser)
        db.session.commit()
        token = jwt.encode({'user': user, 'exp': datetime.datetime.utcnow(
        )+datetime.timedelta(minutes=5)}, app.config['SECRET_KEY'])
    except:
        return jsonify({
            'responsePayload': {
                'code': 100,
                'message': 'An error was occurred'
            }
        }), 403
    responseData = {
        'responsePayload': {
            'code': 200,
            'message': 'User register correctly',
            'idToken': token.decode('UTF-8')
        }
    }
    return jsonify(responseData)


@app.route('/login', methods=['POST', 'GET'])
def login():
    email = request.json['email']
    password = request.json['password']

    existUser = db.session.query(Users).filter(
        Users.email == email, Users.password == password).first()
    if bool(existUser):
        token = jwt.encode({'user': email, 'exp': datetime.datetime.utcnow(
        )+datetime.timedelta(minutes=5)}, app.config['SECRET_KEY'])
        return jsonify({'token': token.decode('UTF-8')})

    return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="login Required"'})


@app.route('/test')
@validationToken
def test():
    return jsonify({
        'responsePayload': {
            'code': 200,
            'message': 'The token is valid'
        }
    }), 200


@app.route('/flights/search',  methods=['GET', 'POST'])
def searchFlights():
    try:
        url = "https://kiwicom-prod.apigee.net/v2/search"

        querystring = request.json['flightData']
        headers = {
            'apikey': "avjQA7qeTc1AE5NRNg5SHIbP2syojDXq",
            'Accept': "*/*",
            'Host': "kiwicom-prod.apigee.net",
            'accept-encoding': "gzip, deflate"
        }

        response = requests.request(
            "GET", url, headers=headers, params=querystring)
        # print(response.json())
        return jsonify(response.json())
    except:
        return jsonify({
            'responsePayload': {
                'code': 100,
                'message': 'An error was occurred'
            }
        }), 403


@app.route('/autocomplete/places',  methods=['GET', 'POST'])
def autocompletePlaces():
    try:
        url = "http://autocomplete.travelpayouts.com/places2"
        querystring = request.json['placesData']
        # {"term": "BCN", "locale": "en", "types[]": "city,airport"}
        headers = {}
        response = requests.request("GET", url, headers=headers, params=querystring)
        # print(response.text)
        return jsonify(response.json())
    except:
        return jsonify({
            'responsePayload': {
                'code': 100,
                'message': 'An error was occurred'
            }
        }), 403

if __name__ == '__main__':
    app.run()
