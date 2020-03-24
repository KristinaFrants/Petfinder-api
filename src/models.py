from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

db = SQLAlchemy()

# --------------user------------------
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
            "password": self.password
        }
   
    # ----------------------alert subclass---------------------------------
class Alert(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(80), unique=True, nullable=False)
    message = db.Column(db.String(80), nullable=False)
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'))
    person = relationship(Person)

    def __repr__(self):
        return "<Alert %r>" % self.message

    def serialize(self):
        return {
            "id": self.id,
            "date": self.date,
            "message": self.message
        }
    

# class Pet (db.Model)
# id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(80), unique=True, nullable=False)
#     email = db.Column(db.String(120), unique=True, nullable=False)
#     firstname = db.Column(db.String(120))
#     lastname = db.Column(db.String(120))
#     zipcode = db.Column(db.String(8))
#     address = db.Column(db.String(120))
#     password = db.Column(db.String(120), nullable=False)
    



