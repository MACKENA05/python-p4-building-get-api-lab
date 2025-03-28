#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate
from sqlalchemy import desc

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries', methods = ['GET'])
def bakeries():
    try:
        bakeries = [bakery.to_dict() for bakery in Bakery.query.all()]
        return jsonify(bakeries)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/bakeries/<int:id>', methods = ['GET'])
def bakery_by_id(id):
    try:
        bakery = Bakery.query.filter(Bakery.id == id).first()
        bakery_dict = bakery.to_dict()
        response = make_response(bakery_dict, 200)
        return response
    except Exception as e:
        return jsonify({"error":str(e)})

@app.route('/baked_goods/by_price', methods = ['GET'])
def baked_goods_by_price():
    try:
        baked_goods = BakedGood.query.order_by(desc(BakedGood.price)).all()
        baked_goods_dict = [baked_good.to_dict() for baked_good in baked_goods]
        return jsonify(baked_goods_dict), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

@app.route('/baked_goods/most_expensive',methods = ['GET'])
def most_expensive_baked_good():
    try:
        baked_good = BakedGood.query.order_by(desc(BakedGood.price)).first()
        if not baked_good:
            return jsonify({"error": "No baked good found"}), 404
        return jsonify(baked_good.to_dict())
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(port=5555, debug=True)
