from models import db
from flask import Flask, jsonify, request
import json
from flask_jwt_extended import(
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from models import db, Person, User, Billing_details

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] ="postgresql://postgres:123.admin@localhost/ejemplo"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'KS+.:GMk^+ gO,5.#y6c%?SmYE^5+_2P ao)Etk4AA'
jwt = JWTManager(app)
bcrypt = Bcrypt(app)
MIGRATE = Migrate(app, db)
db.init_app(app)

@app.route("/persons", methods = ["GET"])
def getPersons():
  persons = Person.query.all()
  persons_json = list(map(lambda item: item.serialize(),persons))

  return jsonify(persons_json)


@app.route("/persons", methods = ["POST"])
def postPersons():
  newPerson = json.loads(request.data)
  person = Person(name=newPerson["name"], lastname=newPerson["lastname"])
  db.session.add(person)

  return jsonify(list(map(lambda item: item.serialize(), Person.query.all())))


@app.route("/signup", methods=["POST"])
def signUp():
  if not request.is_json:
    return jsonify({"msge": "Missing Json in request"}),400
  email = request.json.get("email",None)
  password = request.json.get("password", None)
  name =  request.json.get("name", None)
  lastname = request.json.get("lastname",None)
  if not email:
    return jsonify({"msge": "Misssing email parameter"}),400
  if not password:
    return({"msge":"Missing password parameter"}),400
  if not name:
    return({"msge":"Missing name parameter"}),400
  if not lastname:
    return({"msge":"Missing lastname parameter"}),400

  user = User.query.filter(email=email).first()
  if user is None:
    return jsonify({"msge": "User doesnt exist"}),400

  
  access_token = create_access_token(identity=email)
  return jsonify(access_token=access_token),200


@app.route("/login", methods=["GET"])
def login():
  if not request.is_json:
    return jsonify({"msge": "Missing Json in request"}),400
  email = request.json.get("email",None)
  password = request.json.get("password", None)
  if not email:
    return jsonify({"msge": "Misssing email parameter"}),400
  if not password:
    return({"msge":"Missing password parameter"}),400

  user = User.query.filter(email=email).first()
  if user is None:
    return jsonify({"msge": "User doesnt exist"}),400

  if user.password!=password:
    return jsonify({"msge": "password dont match"}) 
  access_token = create_access_token(identity=user.id)
  return jsonify(access_token=access_token),200



@app.route("/users", methods= ["GET"])
@jwt_required
def getUsers():
  users = User.query.get(get_jwt_identity())
  users_json = list(map(lambda item: item.serialize(),users))

  return jsonify(users_json)


@app.route("/users", methods = ["POST"])
def postUsers():
  newUser = json.loads(request.data)
  user = User(email=newUser["email"], password=newUser["password"])
  db.session.add(user)
  db.session.commit()


  return jsonify(list(map(lambda item: item.serialize(), User.query.all())))




@app.route("/billingdetails", methods=["GET"])
def billingDetailsPost():
  billingDetails = Billing_details.query.all()
  billingDetails_json = list(map(lambda item: item.serialize(),billingDetails))

  return (billingDetails_json)


@app.route("/billingdetails", methods = ["POST"])
def billingDetailsPost():
  newInfo = json.loads(request.data)
  info = Billing_details(id=newInfo["id"], cvv=newInfo["cvv"],cardNumber=newInfo["cardNumber"],expirationDate=newInfo["expirateDate"], user_id=newInfo["user_id"])
  db.session.add(info)
  db.session.commit

  return jsonify(list(map(lambda item : item.serialize(),Billing_details.query.all())))




if __name__ == '__main__':
  app.run(host='127.0.0.1', port=3245, debug=True)