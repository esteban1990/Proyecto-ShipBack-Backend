 #-*- coding: utf-8 -*-

from flask_sqlalchemy import SQLAlchemy
from random import randint

db = SQLAlchemy()

#Me traje la clase person y user del ejemplo visto en el curso por si se utiliza para generar el log in.
class Petition(db.Model):
      id = db.Column(db.Integer, primary_key=True)
      email = db.Column(db.String(10), nullable=False)
      asked_number = db.Column(db.Integer, nullable=False)
      phone_number = db.Column(db.Integer, nullable=False)
      description = db.Column(db.String(50), nullable=True)
      change_or_return = db.Column(db.Boolean, nullable=False) #Si es falso es porque es devolución.
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

class Boughtproduct(db.Model):
     id = db.Column(db.Integer, primary_key=True)
     name = db.Column(db.String(50), nullable=False)
     price = db.Column(db.Integer, nullable=False)
     selected = db.Column(db.Boolean, nullable=False)
     description = db.Column(db.String(50), nullable=True)
     petition_id = db.Column(db.Integer, db.ForeignKey('petition.id'), nullable=True)

     def serialize(self):
        return{
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "selected": self.selected,
            "description": self.description,
          
     }

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

class Return(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bank = db.Column(db.String(50), nullable=True)
    account_type = db.Column(db.String(50), nullable=True)
    account_number = db.Column(db.Integer, nullable=True)
    petition_id = db.Column(db.Integer, db.ForeignKey('petition.id'), nullable=True)

    def serialize(self):
        return{
            "id": self.id,
            "bank": self.bank,
            "account_type": self.account_type,
            "account_number": self.account_number
        }

class Order(db.Model): 
     id = db.Column(db.Integer, primary_key=True)
     streetAddress = db.Column(db.String(50), nullable=False)
     commune=db.Column(db.String(50), nullable=False)
     city=db.Column(db.String(50), nullable=False)
     invoice_id=db.Column(db.Integer, nullable=False)
     office_id=db.Column(db.Integer, nullable=False)
     products=db.Column(db.String(50), nullable=False)
     client_email=db.Column(db.String(50), nullable=False)
     cellphone=db.Column(db.Integer, nullable=False)
     user_email = db.Column(db.String(255), db.ForeignKey('user.email'), nullable=True)

     def serialize(self):
        return{
            "id": self.id,
            "streetAddress": self.id,
            "commune": self.id,
            "city": self.city,
            "invoice_id": self.invoice_id,
            "office_id": self.office_id,
            "products": self.products,
            "email": self.email,
            "cellphone": self.cellphone,
            "user_email": self.user_email,
        }

class Billing_details(db.Model):
     id = db.Column(db.Integer, primary_key=True)
     cardNumber = db.Column(db.Integer, nullable=False)
     cvv = db.Column(db.Integer, nullable=False)
     expiration_date = db.Column(db.String(50), nullable=False)
     user_email = db.Column(db.String(255), db.ForeignKey('user.email'), nullable=True)

     def serialize(self):
        return{
        "id": self.id,
        "cardNumber": self.cardNumber,
        "cvv": self.cvv,
        "expiration_date": self.expiration_date
       
        }

class Sender_details(db.Model):
     id = db.Column(db.Integer, primary_key=True)
     storeName = db.Column(db.String(10), nullable=False)
     contactName = db.Column(db.String(10), nullable=False)
     companyName = db.Column(db.String(10), nullable=False)
     emailContact = db.Column(db.String(10), nullable=False)
     user_email = db.Column(db.String(255), db.ForeignKey('user.email'), nullable=True)
     PickUpAddress = db.relationship('PickUpAddress', backref='sender_details', lazy=True)

     def serialize(self):
        return{
        "id": self.id,
        "storeName": self.storeName,
        "contactName": self.contactName,
        "companyName": self.companyName,
        "emailContact": self.emailContact,
        }

class Support(db.Model):
     id = db.Column(db.Integer, primary_key=True)
     reason = db.Column(db.String(10), nullable=False)
     attached_file = db.Column(db.Boolean, nullable=False)
     description = db.Column(db.String(300), nullable=False)
     user_email = db.Column(db.String(), db.ForeignKey('user.email'), nullable=True)

     def serialize(self):
        return{
        "id": self.id,
        "reason": self.reason,
        "attached_file": self.attached_file,
        "description": self.description
       
        }

class PickUpAddress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(50), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    Sender_details_id = db.Column(db.Integer, db.ForeignKey('sender_details.id'), nullable=True)

    def serialize(self):
        return{
        "id": self.id,
        "address": self.address,
        "city": self.city,
        }

class Person(db.Model):
    __tablename__ = 'person'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)
    users = db.relationship("User", backref="person", lazy=True)

    def serialize(self):
        return{
            "id": self.id,
            "name": self.name,
            "lastname": self.lastname,
            
        }
    def _generateId(self): # devuelve un numero aleatorio entre 0 y el numero que se ve
        return randint(0, 99999999)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), nullable=False)
    password= db.Column(db.String(255), nullable=False)
    person_id = db.Column(db.Integer, db.ForeignKey("person.id"), nullable=True)
    orders = db.relationship("Order", backref="user", lazy=True)

    def serialize(self):
        return{
            "id":self.id,
            "email":self.email,
            "password":self.password
        
        }
    

    def update_user(self, id,):
        obj = self.get.User(id)
        obj.update()
        return obj
    

    