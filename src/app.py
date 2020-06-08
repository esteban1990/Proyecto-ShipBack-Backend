from flask import Flask
from models import db

app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:123.admin@localhost/ejemplo"

if __name__ == '__main__':
  app.run(host='127.0.0.1', port=3245, debug=True)