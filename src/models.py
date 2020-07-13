# -*- coding: utf-8 -*-

from flask_sqlalchemy import SQLAlchemy
from random import randint

db = SQLAlchemy()


class Petition(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(10), nullable=False)
    asked_number = db.Column(db.Integer, nullable=False)
    phone_number = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(50), nullable=True)
    change_or_return = db.Column(db.Boolean, nullable=False)
    Boughtproduct = db.relationship('Boughtproduct', backref='Petition', lazy=True)
    Change = db.relationship('Change', backref='Petition', lazy=True)
    Return = db.relationship('Return', backref='Petition', lazy=True)

    def serialize(self):
        return{
            "id": self.id,
            "email": self.email,
            "phone_number": self.phone_number,
            "description": self.description,
            "change_or_return": self.change_or_return,
        }
    
    def _generateId(self):
        return randint(0, 99999999)


class Boughtproduct(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    selected = db.Column(db.Boolean, nullable=False)
    description = db.Column(db.String(50), nullable=True)
    petition_id = db.Column(
        db.Integer, db.ForeignKey('petition.id'), nullable=True)

    def serialize(self):
        return{
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "selected": self.selected,
            "description": self.description,
        }
    
    def _generateId(self):
        return randint(0, 99999999)


class Change(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    change_product = db.Column(db.String(50), nullable=True)
    state = db.Column(db.String(50), nullable=True)
    city = db.Column(db.String(50), nullable=True)
    address = db.Column(db.String(50), nullable=True)
    commune = db.Column(db.String(50), nullable=True)
    petition_id = db.Column(db.Integer, db.ForeignKey('petition.id'), nullable=True)

    def serialize(self):
        return{
            "id": self.id,
            "change_product": self.change_product,
            "state": self.state,
            "city": self.city,
            "address": self.address,
            "commune": self.commune
        }
    
    def _generateId(self):
        return randint(0, 99999999)


class Return(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bank = db.Column(db.String(50), nullable=True)
    account_type = db.Column(db.String(50), nullable=True)
    account_number = db.Column(db.Integer, nullable=True)
    petition_id = db.Column(
        db.Integer, db.ForeignKey('petition.id'), nullable=True)

    def serialize(self):
        return{
            "id": self.id,
            "bank": self.bank,
            "account_type": self.account_type,
            "account_number": self.account_number
        }
    
    def _generateId(self):
        return randint(0, 99999999)


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_name = db.Column(db.String(50), nullable=False) #se agrega ya que está en el formulario de "create order".
    streetAddress = db.Column(db.String(50), nullable=False)
    commune = db.Column(db.String(50), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    invoice_id = db.Column(db.Integer, nullable=False)
    office_id = db.Column(db.Integer, nullable=False)
    products = db.Column(db.String(50), nullable=False)
    courrier = db.Column(db.String(50), nullable=False) #se agrega courrier.
    client_email = db.Column(db.String(50), nullable=False)
    cellphone = db.Column(db.Integer, nullable=False)
    confirmed = db.Column(db.Boolean, nullable=False)
    #user_email = db.Column(db.String(255), db.ForeignKey('user.email'), nullable=True)

    def serialize(self):
        return{
            "id": self.id,
            "client_name": self.client_name,
            "streetAddress": self.streetAddress,
            "commune": self.commune,
            "city": self.city,
            "invoice_id": self.invoice_id,
            "office_id": self.office_id,
            "products": self.products,
            "courrier": self.courrier,
            "client_email": self.client_email,
            "cellphone": self.cellphone,
            "confirmed": self.confirmed,
            #"user_email": self.user_email,
        }
    
    def _generateId(self): 
        return randint(0, 99999999)

class Billing_details(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cardNumber = db.Column(db.Integer, nullable=False)
    cvv = db.Column(db.Integer, nullable=False)
    month = db.Column(db.String(50), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    user_email = db.Column(db.String(255), db.ForeignKey('user.email'), nullable=True)

    def serialize(self):
        return{
            "id": self.id,
            "cardNumber": self.cardNumber,
            "cvv": self.cvv,
            "month": self.month,
            "year":self.year,
         

        }
    
    def _generateId(self):
        return randint(0, 99999999)


class Sender_details(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    storeName = db.Column(db.String(20), nullable=False)
    contactName = db.Column(db.String(20), nullable=False)
    companyName = db.Column(db.String(20), nullable=False)
    contactPhone = db.Column(db.Integer, nullable=False)
    industry = db.Column(db.String(20),nullable=False)
    address = db.Column(db.String(10), nullable=False)
    city = db.Column(db.String(30), nullable=False)
    emailContact = db.Column(db.String(20), nullable=False)
   # user_email = db.Column(db.String(255), db.ForeignKey('user.email'), nullable=True)

    def serialize(self):
        return{
            "id": self.id,
            "storeName": self.storeName,
            "contactName": self.contactName,
            "companyName": self.companyName,
            "contactPhone": self.contactPhone,
            "industry":self.industry,
            "address":self.address,
            "city":self.city,
            "emailContact": self.emailContact,
        
        }
    
    def _generateId(self):
        return randint(0, 99999999)

class User(db.Model):
    __tablename__="user"
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), nullable=False, unique=True)
    firstname = db.Column(db.String(150), nullable=False)
    lastname = db.Column(db.String(150), nullable=False)
    #person_id = db.Column(db.Integer, db.ForeignKey("person.id"), nullable=True)
    #orders = db.relationship("Order", backref="user", lazy=True)
    #employee = db.relationship("Employee", backref="user", lazy=True)

    def __repr__(self):
        return "<User %r>" % self.email

    def serialize(self):
        return{
            "id": self.id,
            "email": self.email,
            "firstname": self.firstname,
            "lastname": self.lastname
        }

    def update_user(self, id,):
        obj = self.get.User(id)
        obj.update()
        return obj
    
    def _generateId(self):
        return randint(0, 99999999)



class Employee(db.Model):
    __tablename__="employee"
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(150), nullable=False)
    #confirmPassword = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), nullable=False, unique=True)
    firstName = db.Column(db.String(150), nullable=False) #tiene el mismo nombre que aparece en el store.
    lastName = db.Column(db.String(150), nullable=False) #tiene el mismo nombre que aparece en el store.

    def __repr__(self):
        return "<Employee %r>" % self.email

    def serialize(self):
        return{
            "id": self.id,
            "email": self.email,
            "firstName": self.firstName,
            "lastName": self.lastName
        }

    def update_user(self, id,):
        obj = self.get.Employee(id)
        obj.update()
        return obj
    
    def _generateId(self):
        return randint(0, 99999999)