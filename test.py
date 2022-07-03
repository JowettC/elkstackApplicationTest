from flask import Flask, request, jsonify
from random import randint
from os import environ
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

import time

# constructor 

app = Flask(__name__)

# for tas platform
servicekeyUri = "mysql+mysqlconnector://e4b69193154f41088c8e867fca9d1ce6:he4bdvj8q4dqa8zo@ef675a66-b071-4230-a80f-8e15fae65f04.mysql.service.internal:3306/service_instance_db"
app.config['SQLALCHEMY_DATABASE_URI'] = servicekeyUri

# for docker
# app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+mysqlconnector://root@host.docker.internal:3306/mydb_shop"

# for localhost
# app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL') or "mysql+mysqlconnector://testuser:testpass@localhost:3306/mydb_shop"


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

# create shop table 

# get all shop 
@app.route('/shop', methods=['GET'])
def getShops():
    ShopList = Shop.query.all()
    if len(ShopList):
       return jsonify(
           {
               "code": 200,
               "data": [shop.json() for shop in ShopList]
           }
       )
    return jsonify(
       {
           "code": 404,
           "message": "There are no shops."
       }
   ), 404

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

        


@app.route('/test', methods=['GET'])
def test():
    return "testing api endpoint"


# @app.route('/successful', methods=['GET'])
# def test1():
#     # app.logger.info('Successful logging')
#     return "Successful logging!"


# @app.route('/unsuccessful', methods=['GET'])
# def test2():
#     # app.logger.info('Unsuccessful logging')
#     return "Unsuccessful logging!",400
    
# @app.route('/long/successful', methods=['GET'])
# def test3():
#     # app.logger.info('Unsuccessful logging')
#     time.sleep(5)
#     return "5 second wait successful"

# @app.route('/random', methods=['GET'])
# def test4():
#     # app.logger.info('Unsuccessful logging')
#     value = randint(0,10)
#     if value > 5:
#         return "Successful logging!"
#     else:
#         return "Unsuccessful logging!",400

if __name__ == '__main__':
    # import logging
    # logging.basicConfig(filename='error.log',level=logging.DEBUG)
    app.run(host='0.0.0.0', port=8080, debug=True)