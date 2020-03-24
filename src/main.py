"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap, sha256
from models import db
from models import Person
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)


app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
app.config['JWT_SECRET_KEY'] = 'Panda_bubu'  
jwt = JWTManager(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/myLogin', methods=['POST'])
def myLogin_handle():
    body = request.get_json()
    email = request.json.get('email', None)

    user = Person.query.filter_by(email=body['email'], password=sha256(body['password'])).first()
    access_token = create_access_token(identity=email)
    msg = "hey" + user.firstname + "you are logged in! :)"
    return jsonify({
        "token":access_token,
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "firstname": user.firstname,
        "lastname": user.lastname,
        "password": user.password,
        "zipcode": user.zipcode,
        "address": user.address,
        "msg": msg
    })

@app.route('/login', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    username = request.json.get('username', None)
    password = request.json.get('password', None)
    if not username:
        return jsonify({"msg": "Missing username parameter"}), 400
    if not password:
        return jsonify({"msg": "Missing password parameter"}), 400

    if username != 'test' or password != 'test':
        return jsonify({"msg": "Bad username or password"}), 401

    # Identity can be any data that is json serializable
    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token), 200


@app.route('/protected', methods=['GET'])
@jwt_required
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200
@app.route('/register', methods=['POST'])
def registration():
    body = request.get_json()

    db.session.add(Person(
        username = body['username'],
        email = body['email'],
        firstname = body['firstname'],
        lastname = body['lastname'],
        zipcode = body['zipcode'],
        address = body['address'],
        password = sha256(body['password'])
    ))

    db.session.commit()

    return jsonify({
        'register': 'success',
        'msg': 'your account has been made'
    })



@app.route('/hello', methods=['POST', 'GET'])
def handle_hello():

    response_body = {
        "hello": "world"
    }

    return jsonify(response_body), 200

@app.route('/person', methods=['POST'])
def handle_person():

    # First we get the payload json
    body = request.get_json()

    user1 = Person(username=body['username'], email=body['email'])
    db.session.add(user1)
    db.session.commit()
    return "ok", 200

@app.route('/users', methods=['GET'])
def handle_users():

    if request.method == 'GET':
        users = Person.query.all()

        if not users:
            return jsonify({'msg':'User not found'}), 404

        return jsonify( [x.serialize() for x in users] ), 200

    return "Invalid Method", 404


@app.route('/person/<int:person_id>', methods=['PUT', 'GET'])
def get_single_person(person_id):
    """
    Single person
    """
    body = request.get_json() #{ 'username': 'new_username'}
    if request.method == 'PUT':
        user1 = Person.query.get(person_id)
        user1.username = body.username
        db.session.commit()
        return jsonify(user1.serialize()), 200
    if request.method == 'GET':
        user1 = Person.query.get(person_id)
        return jsonify(user1.serialize()), 200

    return "Invalid Method", 404



# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
