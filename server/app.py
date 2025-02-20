#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)


@app.route("/")
def index():
    return "<h1>Bakery GET API</h1>"


@app.route("/bakeries")
def bakeries():
    
    bakeries = Bakery.query.all()
    bakeries_serialized = [
        bakery.to_dict() for bakery in bakeries
    ]

    response = make_response(bakeries_serialized, 200)
    return response


@app.route("/bakeries/<int:id>")
def bakery_by_id(id):
    bakery = Bakery.query.filter(Bakery.id == id).first()
    bakeries_serialized = bakery.to_dict()

    # if bakery is None:
    #     return jsonify({"error": "Bakery not found"}), 404

    # bakery_dict = {
    #     "id": bakery.id,
    #     "name": bakery.name,
    #     "created_at": bakery.created_at,
    # }

    response = make_response(jsonify(bakeries_serialized), 200)
    return response


@app.route("/baked_goods/by_price")
def baked_goods_by_price():
    baked_good_by_price = BakedGood.query.order_by(BakedGood.price).all()
    baked_good_by_price_serialized = [
        baked_good.to_dict() for baked_good in baked_good_by_price
    ]
    response = make_response(baked_good_by_price_serialized, 200)
    return response


@app.route("/baked_goods/most_expensive")
def most_expensive_baked_good():
    highest_price = db.session.query(db.func.max(BakedGood.price)).scalar()

    # highest_price_bakeries = BakedGood.query.filter(
    #     BakedGood.price == highest_price
    # ).all()

    # results = [
    #     {
    #         "id": item.id,
    #         "name": item.name,
    #         "price": item.price,
    #         "created_at": item.created_at,
    #     }
    #     for item in highest_price_bakeries
    # ]

    highest_price_bakery = BakedGood.query.filter(
        BakedGood.price == highest_price
    ).first()

    # results = {
    #         "id": highest_price_bakery.id,
    #         "name": highest_price_bakery.name,
    #         "price": highest_price_bakery.price,
    #         "created_at": highest_price_bakery.created_at
    # }

    most_expensive_serialized = highest_price_bakery.to_dict()


    response = make_response(jsonify(most_expensive_serialized), 200)
    return response


if __name__ == "__main__":
    app.run(port=5555, debug=True)