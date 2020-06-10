from flask import Flask, jsonify, request
import json
from flask_jwt_extended import(
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from models import db, Person, User, Billing_details, Order,Petition, boughtProduct, Change

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] ="postgresql://postgres:123.admin@localhost/ejemplo"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'KS+.:GMk^+ gO,5.#y6c%?SmYE^5+_2P ao)Etk4AA'
jwt = JWTManager(app)
bcrypt = Bcrypt(app)
migrate = Migrate(app, db)
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
def billingDetailsGet():
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
  client_email=newOrder["client_email"],booked_date=newOrder["booked_date"],city=newOrder["city"], state=newOrder["state"],
  courrier=newOrder["courrier"], cost=newOrder["cost"], number_of_packages=newOrder["number_of_packages"],invoice_number=newOrder["invoice_number"],
  postCode=newOrder["postCode"],user_id=newOrder["user_id"])

  db.session.add(order)
  db.session.commit

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
  change_or_return=newPetition["change_or_return"],bought_product=newPetition["bought_product"],change_product=newPetition["change_product"],
  return_product=newPetition["return_product"])

  db.session.add(petition)
  db.session.commit()

  return jsonify(list(map(lambda item: item.serialize(),Petition.query.all())))


@app.route("/boughtproducts", methods = ["GET"])
def getBoughtProducts():
  boughtProducts = boughtProduct.query.all()
  boughtProducts_json = list(map(lambda item: item.seralize(), boughtProducts))

  return jsonify(boughtProducts_json)


@app.route("/boughtproducts", methods = ["POST"])
def postBoughtProducts():
  newBoughtProduct = json.loads(request.data)
  bought_Product = boughtProduct(id=newBoughtProduct["id"], name=newBoughtProduct["name"],price=newBoughtProduct["price"],
  selected=newBoughtProduct["selected"],description=newBoughtProduct["description"],petition_id=newBoughtProduct["petition_id"])

  db.session.add(bought_Product)
  db.session.commit()


@app.route("/changes", methods = ["GET"])
def getChanges():
  changes = Change.query.all()
  changes_json = list(map(lambda item: item.serialize(),changes))

  return jsonify(changes_json)

@app.route("/changes", methods =["POST"])
def postChanges():
  newChange = json.loads(request.data)
  change = Change(id=newChange["id"], change_product=newChange["change_product"], state=newChange["state"], city=newChange["city"],
  address=newChange["address"], commune=newChange["commune"], petition_id=newChange["petition_id"])

  db.session.add(change)
  db.session.commit()

  

if __name__ == '__main__':
  app.run(host='127.0.0.1', port=3245, debug=True)