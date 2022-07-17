from flask import Flask, request, jsonify
from random import randint
from os import environ
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os
import uuid
import requests;


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
# db= environ.get("db_name") or "mydb_shop"
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
@app.route('/', methods=['GET'])
def test2():
    # print("running api")
    # x = requests.get('http://google.com')
    # print(x)
    return "Running: " + instance_id

@app.route('/123', methods=['GET'])
def test3():
    print("running api")
    return "new end point"


# create shop table 

# get all shop 
@app.route('/shop/<int:shop_id>', methods=['GET'])
def getShops(shop_id):
    shop = Shop.query.filter_by(shop_id=shop_id).first()
    if shop != None:
       return jsonify(
           {
               "code": 200,
               "data": shop.json()
           }
       )
    return jsonify(
       {
           "code": 404,
           "message": "There are no shops."
       }
   ), 404

# get all shop 
@app.route('/shop', methods=['GET'])
def getShop():
    ShopList = Shop.query.all()
    # if len(ShopList):
    return jsonify(
        {
            "code": 200,
            "data": [shop.json() for shop in ShopList]
        }
    )
#     return jsonify(
#        {
#            "code": 404,
#            "message": "There are no shops."
#        }
#    ), 404


@app.route('/shop', methods=['post'])
def createShop():
    data = request.get_json()
    new_shop = Shop(data['shop_name'],data['location'])
    exist_shop = Shop.query.filter_by(shop_name=data['shop_name']).all()
    # print(exist_shop)
    if len(exist_shop)>0:
        return jsonify({
            
                "code": 400,
                "msg": "Shop name exist"
            
        })
    else:
        db.session.add(new_shop)
        db.session.commit()
        return jsonify({
            "code": 200,
            "msg" : "Successful"
        }
        )

# update shop
@app.route('/shop', methods=['put'])
def updateShop():
    data = request.get_json()
    shop_update = Shop.query.filter_by(shop_id=data["shop_id"]).first()
    # print(exist_shop)
    if shop_update == None:
        return jsonify({
            
                "code": 400,
                "msg": "Shop id doesn't exist"
            
        })
    else:
        shop_update.shop_name = data["shop_name"]
        shop_update.location = data["location"]
        # db.session.add(new_shop)
        db.session.commit()
        return jsonify({
            "code": 200,
            "msg" : "Successful"
        }
        )
    
# delete shop
@app.route('/shop/<int:shop_id>', methods=['delete'])
def deleteShop(shop_id):
    shop_delete = Shop.query.filter_by(shop_id=shop_id).first()
    if shop_delete == None:
        return jsonify({
                "code": 400,
                "msg": "Shop id doesn't exist"
            
        })
    else:
        db.session.delete(shop_delete)
        db.session.commit()
        return jsonify({
            "code": 200,
            "msg" : "Successful"
        }
        )


@app.route('/test', methods=['GET'])
def test():
    return "testing api endpoint"


if __name__ == '__main__':
    # import logging
    # logging.basicConfig(filename='error.log',level=logging.DEBUG)
    app.run(host='0.0.0.0', port=5000, debug=True,)