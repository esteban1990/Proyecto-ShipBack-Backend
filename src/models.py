from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

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
    id = db.Column(db.Interger, primary_key=True)
    email = db.Column(db.String(255), nullable=False)
    password= db.Column(db.String(255), nullable=False)
    person_id = db.Column(db.Interger, db.ForeignKey("person.id"), nullable=True)


    def serialize(self):
        return{
            "id":self.id,
            "email":self.email,
            "password":self.password
        }