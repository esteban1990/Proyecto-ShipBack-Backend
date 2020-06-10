from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

#Me traje la clase person y user del ejemplo visto en el curso por si se utiliza para generar el log in.

class Petition(db.Model):
     id = db.Column(db.Integer, primary_key=True)
     email = db.Column(db.String(10), nullable=False)
     phone_number = db.Column(db.Integer, nullable=False)
     description = db.Column(db.String(50), nullable=True)
     change_or_return = db.Column(db.Boolean, nullable=False) #Si es falso es porque es devolución.
     bought_product = db.relationship('boughtProduct', backref='Petition', lazy=True)
     change_product = db.relationship('Change', backref='Petition', lazy=True)
     return_product = db.relationship('Return', backref='Petition', lazy=True)

class boughtProduct(db.Model):
     id = db.Column(db.Integer, primary_key=True)
     name = db.Column(db.String(50), nullable=False)
     price = db.Column(db.Integer, nullable=False)
     selected = db.Column(db.Boolean, nullable=False)
     description = db.Column(db.String(50), nullable=True)
     petition_id = db.Column(db.Integer, db.ForeignKey('Petition.id'), nullable=True)

class Change(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    change_product = db.Column(db.String(50), nullable=True)
    state = db.Column(db.String(50), nullable=True)
    city = db.Column(db.String(50), nullable=True)
    address = db.Column(db.String(50), nullable=True)
    commune = db.Column(db.String(50), nullable=True)
    petition_id = db.Column(db.Integer, db.ForeignKey('Petition.id'), nullable=True)

class Return(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bank = db.Column(db.String(50), nullable=True)
    account_type = db.Column(db.String(50), nullable=True)
    account_number = db.Column(db.Integer, nullable=True)
    petition_id = db.Column(db.Integer, db.ForeignKey('Petition.id'), nullable=True)

class Order(db.Model):
     id = db.Column(db.Integer, primary_key=True)
     entrepreneur_name = db.Column(db.String(10), nullable=False)
     entrepreneur_lastname = db.Column(db.String(10), nullable=False)
     entrepreneur_email = db.Column (db.String(10), nullable=False)
     client_name = db.Column(db.String(10), nullable=False) 
     client_lastname = db.Column(db.String(10), nullable=False)
     client_email = db.Column(db.String(10), nullable=False) 
     booked_date = db.Column(db.DateTime, nullable=False)
     city = db.Column(db.String(10), nullable=False)
     state = db.Column(db.String(10), nullable=False)
     courrier = db.Column(db.String(10), nullable=False)
     cost = db.Column(db.Integer, nullable=False)
     number_of_packages = db.Column(db.Integer, nullable=False)
     invoice_number = db.Column(db.Integer, nullable=False)
     postCode = db.Column(db.Integer, nullable=False)
     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)

class Billing_details(db.Model):
     id = db.Column(db.Integer, primary_key=True)
     cardNumber = db.Column(db.Integer, nullable=False)
     cvv = db.Column(db.Integer, nullable=False)
     expiration_date = db.Column(db.String(10), nullable=False)
     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)

class Person(db.Model):
    __tablename__ = 'person'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10), nullable=False)
    lastname = db.Column(db.String(10), nullable=False)
    users = db.relationship("User", backref="person", lazy=True)

    def serialize(self):
        return{
            "id": self.id,
            "name": self.name,
            "lastname": self.lastname,
            
        }


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), nullable=False)
    password= db.Column(db.String(255), nullable=False)
    person_id = db.Column(db.Integer, db.ForeignKey("person.id"), nullable=True)


    def serialize(self):
        return{
            "id":self.id,
            "email":self.email,
            "password":self.password,
        
        }
