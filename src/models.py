from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy import Table, Column, Integer, ForeignKey
# from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import datetime

db = SQLAlchemy()

# --------------Person = PetOwner = User------------------
class Person(db.Model):
    __tablename__ = "person"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    firstname = db.Column(db.String(120))
    lastname = db.Column(db.String(120))
    zipcode = db.Column(db.String(6))
    address = db.Column(db.String(120))
    password = db.Column(db.String(120), nullable=False)
    # alerts = db.relationship('Alert', backref='person', lazy=True)
    pets = db.relationship('Pet', backref='person', lazy=True)
    

    def __repr__(self):
        return '<Person %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "zipcode": self.zipcode,
            "address": self.address,
            # "alerts": list(map(lambda bubu : bubu.serialize(), self.alerts)),
            "pets": list(map(lambda x : x.serialize(), self.pets))
        }
   
    # ----------------------alert subclass---------------------------------
class Alert(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    name = db.Column(db.String(30), nullable=False)
    petname = db.Column(db.String(30), nullable=true)
    date = db.Column(db.DateTime, default=datetime.datetime.now(), nullable=True)
    message = db.Column(db.String(80), nullable=False)
    # person_id = db.Column(db.Integer, db.ForeignKey('person.id'))


    def __repr__(self):
        return "<Alert %r>" % self.message

    def serialize(self):
        return {
            "id": self.id,
            "date": self.date,
            "email": self.email,
            "name": self.name,
            "petname": self.petname,
            "phone": self.phone,
            "message": self.message
        }
    
# ----------------------------------Pet Subclass--------------------------------------
class Pet (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    animal = db.Column(db.String(20), nullable=False)
    breed = db.Column(db.String(40), nullable=True)
    age = db.Column(db.Integer, nullable=True)
    eyecolor = db.Column(db.String(20), nullable=True)
    furcolor = db.Column(db.String(20), nullable=True)
    gender = db.Column(db.String(20), nullable=True)
    description = db.Column(db.String(1000), nullable=False)
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'), nullable=False)
    image = db.Column(db.String(150), nullable=False)
   
    def __repr__(self):
        return '<Pet %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "animal": self.animal,
            "breed": self.breed,
            "age": self.age,
            "eyecolor": self.eyecolor,
            "furcolor": self.furcolor,
            "description": self.description,
            "gender": self.gender,
            "image": self.image
        }
   



