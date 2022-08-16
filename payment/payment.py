from flask import Flask, request, jsonify
from os import environ
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os
import uuid
# import requests;


instance_id = uuid.uuid4().hex
# import time

# constructor 

app = Flask(__name__)

# for tas platform
# servicekeyUri = "mysql+mysqlconnector://e4b69193154f41088c8e867fca9d1ce6:he4bdvj8q4dqa8zo@ef675a66-b071-4230-a80f-8e15fae65f04.mysql.service.internal:3306/service_instance_db"
# app.config['SQLALCHEMY_DATABASE_URI'] = servicekeyUri

# for docker
# app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+mysqlconnector://root@host.docker.internal:3306/mydb_shop"

# for localhost
# user = "root"
# app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL') or "mysql+mysqlconnector://testuser:testpass@localhost:3306/mydb_shop"

# # for k8s


pw = os.getenv("db_root_password") or ""
db= environ.get("db_name") or "mydb_shop"
host = environ.get("MYSQL_SERVICE_HOST") or "host.docker.internal"
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL') or "mysql+mysqlconnector://root:"+pw+"@mysql:3306/mydb_shop"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

db = SQLAlchemy(app)
CORS(app) 

class Shop(db.Model):
   __tablename__ = 'shop'
   shop_id = db.Column(db.Integer, primary_key=True)
   shop_name = db.Column(db.String(256))
   location =db.Column(db.String(256))

   def __init__(self, shop_name, location):
       self.shop_name = shop_name
       self.location = location
 
   def json(self):
       return {
            "shop_id": self.shop_id,
            "shop_name": self.shop_name,
            "location": self.location,
        }
db.create_all()

# kubectl rollout restart -n default deployment flaskapi-deployment-jowett
# test route
@app.route('/successful', methods=['GET'])
def test2():
    return "Payment Successfully", 200

@app.route('/unsuccessful', methods=['GET'])
def test3():
    return "payment Unsuccessfully", 400


@app.route('/test', methods=['GET'])
def test():
    return "testing api endpoint"


if __name__ == '__main__':
    # import logging
    # logging.basicConfig(filename='error.log',level=logging.DEBUG)
    app.run(host='0.0.0.0', port=5000, debug=True,)