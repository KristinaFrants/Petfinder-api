from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import datetime

db = SQLAlchemy()

# --------------Person = PetOwner------------------
class Person(db.Model):
    __tablename__ = "person"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    firstname = db.Column(db.String(120))
    lastname = db.Column(db.String(120))
    zipcode = db.Column(db.String(8))
    address = db.Column(db.String(120))
    password = db.Column(db.String(120), nullable=False)
    alerts = db.relationship('Alert', backref='person', lazy=True)
    pets = db.relationship('Pets', backref='person', lazy=True)
    

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
            "password": self.password,
            "alerts": list(map(lambda bubu : bubu.serialize(), self.alerts))
        }
   
    # ----------------------alert subclass---------------------------------
class Alert(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.datetime.now(), nullable=True)
    message = db.Column(db.String(80), nullable=False)
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'))


    def __repr__(self):
        return "<Alert %r>" % self.message

    def serialize(self):
        return {
            "id": self.id,
            "date": self.date,
            "message": self.message
        }
    
# ----------------------------------Pet Subclass--------------------------------------
class Pet (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    animal = db.Column(db.String(20), nullable=False)
    breed = db.Column(db.String(40), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    eyecolor = db.Column(db.String(20), nullable=False)
    furcolor = db.Column(db.String(20), nullable=False)
    gender = db.Column(db.String(20), nullable=False)
    description = db.Column(db.String(1000), nullable=False)
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'))
   
    def __repr__(self):
        return '<Pets %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "animal": self.animal,
            "breed": self.breed,
            "age": self.age,
            "eyecolor": self.eyecolor,
            "furcolor": self.eyecolor,
            "gender": self.gender,
            "pets": list(map(lambda x : x.serialize(), self.pets))
        }
   



