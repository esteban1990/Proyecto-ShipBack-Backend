import json
import os
import re
from flask import Flask, jsonify, request
from flask_bcrypt import Bcrypt
from flask_jwt_extended import (JWTManager, create_access_token,
                                get_jwt_identity, jwt_required)
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_cors import CORS

from models import (Billing_details, Boughtproduct, Change, Order,
                    Petition, Return, Sender_details,
                    User, Employee, db)

BASEDIR = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
CORS(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + \
    os.path.join(BASEDIR, "test.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'KS+.:GMk^+ gO,5.#y6c%?SmYE^5+_2P ao)Etk4AA'
jwt = JWTManager(app)
bcrypt = Bcrypt(app)
migrate = Migrate(app, db)
db.init_app(app)
Manager = Manager(app)
Manager.add_command("db", MigrateCommand)

@app.route("/signup", methods=["POST"])
def signUp():
        #Regular expression that checks a valid email
        ereg = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
        #Regular expression that checks a valid password
        preg = '^.*(?=.{8,})(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).*$'
        # Instancing the a new user
        user = User()
        #Checking email 
        if (re.search(ereg,request.json.get("email"))):
            user.email = request.json.get("email")
        else:
            return "Invalid email format", 400
        #Checking password
        if (re.search(preg,request.json.get('password'))):
            pw_hash = bcrypt.generate_password_hash(request.json.get("password"))
            user.password = pw_hash
        else:
            return "Invalid password format", 400
        #Ask for everything else
        user.firstname = request.json.get("firstname")
        user.lastname = request.json.get("lastname")
        
        db.session.add(user)

        db.session.commit()

        return jsonify({"success": True}), 201 

@app.route("/user/<int:id>", methods=["DELETE", "GET", "PUT"])
@app.route("/users", methods=["GET"])
def user(id=None):
    if request.method == "GET":
        if id is not None:
            user = User.query.get(id)
            return jsonify(user.serialize()), 200
        else:
            user = User.query.all()
            users = list(map(lambda user: user.serialize(), user))
            return jsonify(users), 200

    if request.method == "DELETE": 
        user = User.query.get(id)
        db.session.delete(user)
        db.session.commit()
        return "User has been deleted", 200

    if request.method == "PUT":
        if id is not None: 
            user = User.query.get(id)
            user.firstname = request.json.get("firstname")
            user.lastname = request-json.get("lastname")
            user.email =request.json.get("email")
            user.password = request.json.get("password")
            db.session.commit()
            return jsonify(user.serialize()), 201

@app.route("/login", methods=["POST"])
def login():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400
    email = request.json.get('email', None)
    password = request.json.get('password', None)
    if not email:
        return jsonify({"msg": "Missing email parameter"}), 400
    if not password:
        return jsonify({"msg": "Missing password parameter"}), 400
    
    user = User.query.filter_by(email=email).first()

    if user is None:
        return jsonify({"msg": "Email not found"}), 404
    
    if bcrypt.check_password_hash(user.password, password):
        access_token = create_access_token(identity=email)
        data = {
            "access_token": access_token,
            "user" : user.serialize(),
            "msg": "success"
        }
        return jsonify(data), 200
    
    elif user.password != password:
        data = {
            "msg": "password don't match (wrong password)"
        }
        return jsonify(data), 400


@app.route("/login", methods=["GET"])
def getLogin():
    logins = User.query.all()
    logins_json = list(map(lambda item: item.serialize(), logins))

    return jsonify(logins_json)



@app.route("/forgot-password", methods=["PUT"])
def forgotPasswordUser():

    if not request.is_json:
        return jsonify({"msge": "Missing Json in request"}), 400

    email = request.json.get("email", None)
    password = request.json.get("password", None)
    confirmPassword = request.json.get("confirmPassword", None)

    if not email:
        return jsonify({"msge": "Misssing email parameter"}), 400

    if not password:
        return({"msge": "Missing password parameter"}), 400

    if not confirmPassword:
        return({"msge": "Missing password parameter"}), 400

        user = User.query.filter_by(email=email).first()
    if user is None:
        return jsonify({"msge": "user dosent exist"}), 400

    if password != confirmPassword:
        return ({"msge": "Passwords dont match"}), 400

        user.password = password
        #db.session.add(user)
        db.session.commit()
        return jsonify(user.serialize()),200

@app.route("/admin", methods=["POST"])
def superAdmin():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400
    email = request.json.get('email', None)
    password = request.json.get('password', None)
    if not email:
        return jsonify({"msg": "Missing email parameter"}), 400
    if not password:
        return jsonify({"msg": "Missing password parameter"}), 400
    
    user = User.query.filter_by(email=email).first()

    if email is None:
        return jsonify({"msg": "Email not found"}), 404
    if email != "contacto@shipback.com" or password !="ShipBack211!":
        return jsonify({"msg": "Wrong Password or Email, not found"}), 404
    
    elif email == "contacto@shipback.com" and password =="ShipBack211!":
        access_token = create_access_token(identity=email)
        data = {
            "access_token": access_token,
            "user" : user.serialize(),
            "msg": "success"
        }
        return jsonify(data), 200


@app.route("/admi_usuario", methods=["GET"])
def getAdmi_Users():
    users = User.query.all()
    users_json = list(map(lambda item: item.serialize(),users))
    return jsonify(users_json)


@app.route("/newUser", methods=["POST"])
def postAdmi_Users():
    newUser = json.loads(request.data)
    user = User(
        firstname=newUser["firstname"],
        lastname=newUser["lastname"],
        email=newUser["email"], 
        password=newUser["password"])

    db.session.add(user)
    db.session.commit()

    return jsonify(list(map(lambda item: item.serialize(), User.query.all())))

@app.route("/update_user/<int:id>", methods=["PUT"])
def putAdmi_Usuarios(id):

    if not request.is_json:
        return jsonify({"msge": "Missing Json in request"}), 400
    if id is None:
        return jsonify({"msge":"bad request"}),400
    user = User.query.filter_by(id=id).first()
    if not user:
        return jsonify({"msge":"User not Found"}),400
        
    password = request.json.get("password", None)

    user.password = password
   # db.session.add(user)
    db.session.commit()
    return jsonify(user.serialize()),200
    



@app.route("/admi_usuario/<int:id>", methods=["DELETE"])
def deleteUser_Admin(id):

    if id is None:
      return jsonify({"msge":"bad request"}),400
    user = User.query.filter_by(id=id).first()
    if not user:
        return jsonify({"msge":"User not Found"}),400
  #delete palabra reserverda en accion siguiente??
    db.session.delete(user)
    db.session.commit()
    return jsonify({"msge": "User has been deleted"}),200



@app.route("/billingdetails/detailCards", methods=["GET"])
def billingDetailsGet():
    billingDetails = Billing_details.query.all()
    billingDetails_json = list(map(lambda item: item.serialize(), billingDetails))

    return (billingDetails_json)


@app.route("/billingdetails", methods=["POST"])
def billingDetailsPost():

    newInfo = json.loads(request.data)
    info = Billing_details(cvv=newInfo["cvv"], cardNumber=newInfo["cardNumber"], month=newInfo["month"],
                           year=newInfo["year"])

    # email = request.json.get("email",None)

    #user = User.query.filter_by(email=newInfo["user_email"]).first()
  #  if user is None:
   #     return jsonify({"msge": "user dosent exist"}), 400

    # Billing_details.user.append(user)
    db.session.add(info)
    db.session.commit()

    return jsonify(list(map(lambda item: item.serialize(), Billing_details.query.all())))


@app.route("/orders", methods=["GET"])
def getOrders():
    orders = Order.query.filter_by(confirmed = False)
    orders_json = list(map(lambda item: item.serialize(), orders))

    return jsonify(orders_json)


@app.route("/orders/<int:invoice_id>", methods=["PUT"]) #método PUT para las órdenes confirmadas. 
def confirmOrder(invoice_id):
    if invoice_id is None:
        return jsonify({"msge": "bad request"}), 400    
    
    order = Order.query.filter_by(invoice_id=invoice_id).first()

    if not order:
        return jsonify({"msge": "Order not found"}), 400
    
    order.confirmed = True

    db.session.commit()
    return jsonify({"msge": "Order has been confirmed"}), 200

@app.route("/tracking", methods=["GET"])
def getConfirmedOrders():
    orders = Order.query.filter_by(confirmed = True)
    orders_json = list(map(lambda item: item.serialize(), orders))

    return jsonify(orders_json)

@app.route("/orders/<int:invoice_id>", methods=["DELETE"])
def deleteOrder(invoice_id):
  if invoice_id is None:
      return jsonify({"msge":"bad request"}),400
  order = Order.query.filter_by(invoice_id=invoice_id).first()
  if not order:
    return jsonify({"msge":"Order not Found"}),400
  #delete palabra reserverda en accion siguiente??
  db.session.delete(order)
  db.session.commit()
  return jsonify({"msge": "Order has been deleted"}),200

@app.route("/orders", methods=["POST"])
def ordersPost():

    newOrder = json.loads(request.data) #revisar.

    order = Order(
        client_name=newOrder['client_name'],
        streetAddress=newOrder["streetAddress"],
        commune=newOrder["commune"],
        city=newOrder["city"],
        invoice_id=newOrder["invoice_id"],
        office_id=newOrder["office_id"],
        products=newOrder["products"],
        courrier=newOrder['courrier'],
        client_email=newOrder['client_email'],
        cellphone=newOrder['cellphone'],
        confirmed=newOrder['confirmed'])

    # user = User.query.filter_by(email=user.email).first() 
    # if user is None:
    #    return jsonify({"msge": "user doesn't exist"}), 400

    # order.user.append(user)
    db.session.add(order)
    db.session.commit()

    return jsonify(list(map(lambda item: item.serialize(), Order.query.all()))), 200


@app.route("/settings", methods=["POST"])
def sender_detailsPost():

    newDetails = json.loads(request.data)
    sender_details = Sender_details(storeName=newDetails["storeName"], contactName=newDetails["contactName"],
                                    companyName=newDetails["companyName"],contactPhone=newDetails["contactPhone"],industry=newDetails["industry"],address=newDetails["address"],city=newDetails["city"], emailContact=newDetails["emailContact"])

    # email = request.json.get("email",None)
     #pickup = PickUpAddress( Sender_details_id = sender_details.id, address=pickup["address"], city=pickup["city"])

    db.session.add(sender_details)
    db.session.commit()

  #  user = User.query.filter_by(email=email.).first()
  #  if user is None:
   #     return jsonify({"msge": "user doesn't exist"}), 400


    return jsonify(list(map(lambda item: item.serialize(), Sender_details.query.all())))


@app.route("/settings", methods=["GET"])
def senderdetailsGet():

    details = Sender_details.query.all()
    details_json = list(map(lambda item: item.serialize(), details))

    return jsonify(details_json)


@app.route("/settings/users", methods=["POST"])
def postEmployeeDetails():

    employee_details = json.loads(request.data)
    newEmployedDetails = Employee(employee_email=employee_details["employee_email"], employee_firstName=employee_details["employee_firstName"],
   employee_lastName=employee_details["employee_lastName"],employee_password=employee_details["employee_password"])

    db.session.add(newEmployedDetails)
    db.session.commit()

    return jsonify(list(map(lambda item: item.serialize(),Employee.query.all())))



@app.route("/settings/users/all", methods=["GET"])
def getEmployeeDetails():
    
    employed_details = Employee.query.all()
    employed_details_json = list(map(lambda item: item.serialize(),employed_details))

    return jsonify(employed_details_json)


@app.route("/petitions", methods=["GET"])
def getPetitions():
    petitions = Petition.query.all()
    petitions_json = list(map(lambda item: item.serialize(), petitions))

    return jsonify({petitions_json})


@app.route("/petitions", methods=["POST"])
def postPetitions():

    newPetition = json.loads(request.data)
    petition = Petition(id=newPetition["id"], email=newPetition["email"], phone_number=newPetition["phone_number"], description=newPetition["description"],
                        change_or_return=newPetition["change_or_return"])

    email = request.json.get("email", None)

    user = User.query.filter_by(email=email)
    if user is None:
        return jsonify({"msge": "user dosent exist"}), 400

    petition.Boughtproduct.append(Boughtproduct)
    db.session.add(petition)
    db.session.commit()

    return jsonify(list(map(lambda item: item.serialize(), Petition.query.all())))


@app.route("/boughtproducts", methods=["GET"])
def getBoughtProducts():
    boughtProducts = Boughtproduct.query.all()
    boughtProducts_json = list(
        map(lambda item: item.seralize(), boughtProducts))

    return jsonify(boughtProducts_json)


@app.route("/boughtproducts", methods=["POST"])
def postBoughtProducts():
    newBoughtProduct = json.loads(request.data)
    bought_Product = Boughtproduct(id=newBoughtProduct["id"], name=newBoughtProduct["name"], price=newBoughtProduct["price"],
                                   selected=newBoughtProduct["selected"], description=newBoughtProduct["description"])

    db.session.add(bought_Product)
    db.session.commit()

    return jsonify(list(map(lambda item: item.serialize(), Boughtproduct.query.all())))


@app.route("/changes", methods=["GET"])
def getChanges():
    changes = Change.query.all()
    changes_json = list(map(lambda item: item.serialize(), changes))

    return jsonify(changes_json)


@app.route("/changes", methods=["POST"])
def postChanges():
    newChange = json.loads(request.data)
    change = Change(id=newChange["id"], change_product=newChange["change_product"], state=newChange["state"], city=newChange["city"],
                    address=newChange["address"], commune=newChange["commune"])

    db.session.add(change)
    db.session.commit()
    return jsonify(list(map(lambda item: item.serialize(), Change.query.all())))


@app.route("/returns", methods=["GET"])
def getReturn():
    returns = Return.query.all()
    return_json = list(map(lambda item: item.serialize(), returns))

    return jsonify(return_json)


@app.route("/returns", methods=["POST"])
def postReturn():

    newReturn = json.loads(request.data)
    return_ = Return(id=newReturn["id"], bank=newReturn["bank"],
                     account_type=newReturn["account_type"], account_number=newReturn["account_number"])

    email = request.json.get("email", None)

    user = User.query.filter_by(email=email)
    if user is None:
        return jsonify({"msge": "user dosent exist"}), 400
    db.return_.append(user)
    db.session.add(return_)
    db.session.commit()

    return jsonify(list(map(lambda item: item.serialize(), Return.query.all())))


if __name__ == '__main__':
    Manager.run()
