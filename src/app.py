from flask import Flask, jsonify, request
import json
import os#librebria de pyhton para comunicarme con mi sistemas de archivos
from flask_jwt_extended import(
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)
from flask_bcrypt import Bcrypt
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from models import db, Person, User, Billing_details, Order,Petition, Boughtproduct, Change, Return

BASEDIR = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(BASEDIR, "test.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'KS+.:GMk^+ gO,5.#y6c%?SmYE^5+_2P ao)Etk4AA'
jwt = JWTManager(app)
bcrypt = Bcrypt(app)
migrate = Migrate(app, db)
db.init_app(app)
Manager = Manager(app)
Manager.add_command("db",MigrateCommand)


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
  db.session.commit()

 
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
   
  

  access_token = create_access_token(identity=email)
  return jsonify(access_token=access_token),200

@app.route("/login", methods=["POST"])
def login():
  if not request.is_json:
    return jsonify({"msge": "Missing Json in request"}),400
  email = request.json.get("email",None)
  password = request.json.get("password", None)
  if not email:
    return jsonify({"msge": "Misssing email parameter"}),400
  if not password:
    return({"msge":"Missing password parameter"}),400
  
  user = User.query.filter_by(email=email).first()
  if user is None:
    return jsonify({"msge":"user dosent exist"}),400

  if user.password != password:
    return jsonify({"msge": "password dont match"}),400

  access_token = create_access_token(identity=email)
  return jsonify(access_token=access_token),200



@app.route("/users", methods= ["GET"])
def getUsers():
  users = User.query.all()
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
def billingDetailsGet():
  billingDetails = Billing_details.query.all()
  billingDetails_json = list(map(lambda item: item.serialize(),billingDetails))

  return (billingDetails_json)


@app.route("/billingdetails", methods = ["POST"])
def billingDetailsPost():
  newInfo = json.loads(request.data)
  info = Billing_details(id=newInfo["id"], cvv=newInfo["cvv"],cardNumber=newInfo["cardNumber"],expiration_date=newInfo["expiration_date"])
  db.session.add(info)
  db.session.commit()

  return jsonify(list(map(lambda item : item.serialize(),Billing_details.query.all())))

@app.route("/orders", methods=["GET"])
def getOrders():
  orders = Order.query.all()
  orders_json = list(map(lambda item: item.serialize(), orders))

  return jsonify(orders_json)

@app.route("/orders", methods=["POST"])
def ordersPost():
  newOrder = json.loads(request.data)
  order = Order(id=newOrder["id"],entrepreneur_name=newOrder["entrepreneur_name"], entrepreneur_lastname=newOrder["entrepreneur_lastname"],
  entrepreneur_email=newOrder["entrepreneur_email"], client_name=newOrder["client_name"], client_lastname=newOrder["client_lastname"],
  client_email=newOrder["client_email"],booked_date=newOrder["booked_date"], city=newOrder["city"], state=newOrder["state"],
  courrier=newOrder["courrier"], cost=newOrder["cost"], number_of_packages=newOrder["number_of_packages"],invoice_number=newOrder["invoice_number"],
  postCode=newOrder["postCode"])

  db.session.add(order)
  db.session.commit()

  return jsonify(list(map(lambda item: item.serialize(), Order.query.all())))


@app.route("/petitions", methods = ["GET"])
def getPetitions():
  petitions = Petition.query.all()
  petitions_json = list(map(lambda item: item.serialize(), petitions))

  return jsonify(petitions_json)


@app.route("/petitions", methods = ["POST"])
def postPetitions():
  newPetition = json.loads(request.data)
  petition = Petition(id=newPetition["id"], email=newPetition["email"], phone_number=newPetition["phone_number"],description=newPetition["description"],
  change_or_return=newPetition["change_or_return"])

  db.session.add(petition)
  db.session.commit()

  return jsonify(list(map(lambda item: item.serialize(),Petition.query.all())))


@app.route("/boughtproducts", methods = ["GET"])
def getBoughtProducts():
  boughtProducts = Boughtproduct.query.all()
  boughtProducts_json = list(map(lambda item: item.seralize(), boughtProducts))

  return jsonify(boughtProducts_json)


@app.route("/boughtproducts", methods = ["POST"])
def postBoughtProducts():
  newBoughtProduct = json.loads(request.data)
  bought_Product = Boughtproduct(id=newBoughtProduct["id"], name=newBoughtProduct["name"],price=newBoughtProduct["price"],
  selected=newBoughtProduct["selected"],description=newBoughtProduct["description"])

  db.session.add(bought_Product)
  db.session.commit()

  return jsonify(list(map(lambda item: item.serialize(),Boughtproduct.query.all())))




@app.route("/changes", methods = ["GET"])
def getChanges():
  changes = Change.query.all()
  changes_json = list(map(lambda item: item.serialize(),changes))

  return jsonify(changes_json)

@app.route("/changes", methods =["POST"])
def postChanges():
  newChange = json.loads(request.data)
  change = Change(id=newChange["id"], change_product=newChange["change_product"], state=newChange["state"], city=newChange["city"],
  address=newChange["address"], commune=newChange["commune"])

  db.session.add(change)
  db.session.commit()
  return jsonify(list(map(lambda item: item.serialize(),Change.query.all())))


@app.route("/returns", methods = ["GET"])
def getReturn():
  returns = Return.query.all()
  return_json =  list(map(lambda item: item.serialize(), returns))

  return jsonify(return_json)


@app.route("/returns", methods = ["POST"])
def postReturn():
  newReturn = json.loads(request.data)
  return_  = Return(id=newReturn["id"], bank=newReturn["bank"],account_type=newReturn["account_type"],account_number=newReturn["account_number"])
  db.session.add(return_)
  db.session.commit()

  return jsonify(list(map(lambda item: item.serialize(), Return.query.all())))

if __name__ == '__main__':
  Manager.run()