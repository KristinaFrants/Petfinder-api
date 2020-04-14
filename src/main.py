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
from models import Person, Alert, Pet
from twilio.rest import Client
from sendsms import first_function
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
    
    msg = "hey " + user.firstname + " you are logged in! :)"
   
    return jsonify({
        "token":access_token,
        "id": user.id,
        "email": user.email,
        "firstname": user.firstname,
        "lastname": user.lastname,
        "zipcode": user.zipcode,
        "address": user.address,
        "msg": msg
    })


@app.route('/protected', methods=['GET'])
@jwt_required
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

# --------------------signup/userPostandGet------------------------------------------------------

##########################make a user#################################
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
        'register': 'success'
    })


##############################get all users###################################
@app.route('/users', methods=['GET'])
def handle_users():

    if request.method == 'GET':
        users = Person.query.all()

        if not users:
            return jsonify({'msg':'User not found'}), 404

        return jsonify( [x.serialize() for x in users] ), 200

    return "Invalid Method", 404

###############################getputdel single user########################################
@app.route('/users/<int:person_id>', methods=['PUT','GET', 'DELETE'])
def get_single_user(person_id):
    #put request
    if request.method == 'PUT':
        body = request.get_json()
        if body is None:
            raise APIException("Specify JSON body", status_code=400)
        
        user1 = Person.query.get(person_id)
        if "email" in body:
            user1.email= body["email"]
        if "firstname" in body:
            user1.firstname= body["firstname"]
        if "lastname" in body:
            user1.lastname= body["lastname"]
        if "username" in body:
            user1.username= body["username"]
        if "zipcode" in body:
            user1.zipcode= body["zipcode"]
        if "address" in body:
            user1.address= body["address"]
        if "image" in body:
            user1.image= body["image"]
        db.session.commit()
        
        return jsonify(user1.serialize()), 200
    
    #get request
    if request.method == "GET":
        user1 = Person.query.get(person_id)
        if user1 is None:
            raise APIException("User Not Found", status_code=404)
        return jsonify(user1.serialize()), 200

    #delete request
    if request.method == 'DELETE':
        user1 = Person.query.get(person_id)
        if user1 is None:
            raise APIException("User Not Found", status_code=404)
        db.session.delete(user1)
        db.session.commit()
        return "person deleted", 200

    return "invalid method", 404





# @app.route('/person', methods=['POST'])
# def handle_person():

#     # First we get the payload json
#     body = request.get_json()

#     user1 = Person(username=body['username'], email=body['email'])
#     db.session.add(user1)
#     db.session.commit()
#     return "ok", 200

# @app.route('/person/<int:person_id>', methods=['PUT', 'GET'])
# def get_single_person(person_id):
#     """
#     Single person
#     """
#     body = request.get_json() #{ 'username': 'new_username'}
#     if request.method == 'PUT':
#         user1 = Person.query.get(person_id)
#         user1.username = body.username
#         db.session.commit()
#         return jsonify(user1.serialize()), 200
#     if request.method == 'GET':
#         user1 = Person.query.get(person_id)
#         return jsonify(user1.serialize()), 200

#     return "Invalid Method", 404

#########################################################################
#ALERT
#########################################################################
@app.route('/alert', methods=['POST','GET'])
def get_alert():
    # get request
    if request.method == 'GET':
        all_alerts = Alert.query.all()
        all_alerts = list(map(lambda x : x.serialize(), all_alerts))
        
        return jsonify(all_alerts), 200

    if request.method == 'POST':
        body = request.get_json() 
        if body is None:
            raise APIException("Specify JSON body", status_code=400)
        if "message" not in body:
            raise APIException("Specify Message", status_code=400)
        if "email" not in body:
            raise APIException("Specify Email", status_code=400)

        alert1 = Alert(message = body['message'], email = body['email'], name = body['name'], petname = body['petname'], phone = body['phone'])
        db.session.add(alert1)
        db.session.commit()


        # print('kevin', alert1.__repr__())
        return "ok", 200

    return "invalid method", 404

@app.route('/alert/<int:alert_id>', methods=['PUT','GET', 'DELETE'])
def get_single_alert(alert_id):
    #put request
    if request.method == 'PUT':
        body = request.get_json()
        if body is None:
            raise APIException("Specify JSON body", status_code=400)
        
        alert1 = Alert.query.get(alert_id)
        if "message" in body:
            alert1.message = body["message"]
        db.session.commit()
        
        return jsonify(alert1.serialize()), 200
    
    #get request
    if request.method == "GET":
        alert1 = Alert.query.get(alert_id)
        if alert1 is None:
            raise APIException("Alert Not Found", status_code=404)
        return jsonify(alert1.serialize()), 200

    #delete request
    if request.method == 'DELETE':
        alert1 = Alert.query.get(alert_id)
        if alert1 is None:
            raise APIException("Alert Not Found", status_code=404)
        db.session.delete(alert1)
        db.session.commit()
        return "alert deleted", 200

    return "invalid method", 404
    

#########################################################################
#PET
#########################################################################

@app.route('/pets', methods=['POST','GET'])
def get_pet():
    # get request
    if request.method == 'GET':
        all_pets = Pet.query.all()
        all_pets = list(map(lambda x : x.serialize(), all_pets))
        
        return jsonify(all_pets), 200

    if request.method == 'POST':
        body = request.get_json() 
        if body is None:
            raise APIException("Specify JSON body", status_code=400)
        if "name" not in body:
            raise APIException("Specify Date", status_code=400)
        if "description" not in body:
            raise APIException("Specify Description", status_code=400)
        if "animal" not in body:
            raise APIException("Specify Animal", status_code=400)
            
        pet1 = Pet(name = body['name'], image = body['image'], description = body['description'], breed = body['breed'], age = body['age'], eyecolor = body['eyecolor'],  furcolor = body['furcolor'], animal = body['animal'], gender = body['gender'], person_id = body['person_id'])
        db.session.add(pet1)
        db.session.commit()
        
        # print('kevin', pet.__repr__())
        return "ok", 200

    return "invalid method", 404

############################singlepetuser###################
@app.route('/pets/<int:pet_id>', methods=['PUT','GET', 'DELETE'])
def get_single_pet(pet_id):
    #put request
    if request.method == 'PUT':
        body = request.get_json()
        if body is None:
            raise APIException("Specify JSON body", status_code=400)
        
        pet1 = Pet.query.get(pet_id)
        if "name" in body:
            pet1.name= body["name"]
        if "animal" in body:
            pet1.animal= body["animal"]
        if "breed" in body:
            pet1.breed= body["breed"]
        if "gender" in body:
            pet1.gender= body["gender"]
        if "eyecolor" in body:
            pet1.eyecolor= body["eyecolor"]
        if "furcolor" in body:
            pet1.furcolor= body["furcolor"]
        if "description" in body:
            pet1.description= body["description"]
        if "age" in body:
            pet1.age= body["age"]
        if "image" in body:
            pet1.image= body["image"]
        if "person_id" in body:
            pet1.person_id= body["person_id"]
        db.session.commit()
        
        return jsonify(pet1.serialize()), 200
    
    #get request
    if request.method == "GET":
        pet1 = Pet.query.get(pet_id)
        if pet1 is None:
            raise APIException("User Not Found", status_code=404)
        return jsonify(pet1.serialize()), 200

    #delete request
    if request.method == 'DELETE':
        pet1 = Pet.query.get(pet_id)
        if pet1 is None:
            raise APIException("User Not Found", status_code=404)
        db.session.delete(pet1)
        db.session.commit()
        return "pet deleted", 200

    return "invalid method", 404
# -------------------------------------------sms fetching and end point---------------------
@app.route('/alert/<int:alert_id>/sendmsg', methods=['GET'])
def first_msg(alert_id):
 
    body = request.get_json() 
    
    # body = request.form()
    alert2 = Alert.query.get(alert_id)
    number = "+17865662238"
    mess = "Hi " + alert2.name + ", There's a lead on your alert!"

    first_function(number, mess)
    print('ok')
    return jsonify({'msg':'message sent!' }), 200

# @app.route('/newmsg', methods=['POST'])
# def new_message():

#     body = request.form()
    
#     name = body['Body']
#     number = body['From']
#     message =  body[name + ", you are now in the queue."]

#     Alert.enqueue(name, number)
    
#     resp = MessagingResponse()
#     resp.message("Hello " + message_body + " you have been added."  " There are " + repr(len(Queue()._queeue)-1) + " person in front of you.")
#     return  str(resp)

# @app.route('/all_msgs', methods=['GET'])
# def getting_all_messages():
#     return jsonify(Alert(), Person()), 200


# this only runs if `$ python src/main.py` is executed


# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
