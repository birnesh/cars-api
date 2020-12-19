from .schemas import manufacturer_schema, manufacturers_schema, car_schema, cars_schema
from .models import Manufacturer, Car
from flask import request, jsonify, abort, Blueprint
from marshmallow import ValidationError
from app import db

# from sqlalchemy.exc import IntegrityError
# from werkzeug.exceptions import NotFound

# API routes
# manufacturing
manufacturer_car_module = Blueprint("manufacturer_car", __name__, url_prefix="")


@manufacturer_car_module.route("/manufacturer", methods=["GET", "POST"])
def create_list_manufacturer():
    if request.method == "POST":
        json_data = request.get_json()
        if not json_data:
            return {"message": "No input data provided"}, 400
        # Validate and deserialize input
        try:
            data = manufacturer_schema.load(json_data)
        except ValidationError as err:
            return err.messages, 422
        name = data["name"]
        head_quarter = data["head_quarter"]
        founder = data["founder"]
        established_year = data["established_year"]

        try:
            new_manufacturer = Manufacturer(
                name, head_quarter, founder, established_year
            )
            db.session.add(new_manufacturer)
            db.session.commit()
            return manufacturer_schema.jsonify(new_manufacturer)
        except Exception as E:
            return jsonify({"msg": E})
    else:
        all_manufacturers = Manufacturer.query.all()
        response = manufacturers_schema.dump(all_manufacturers)

        return jsonify(response)


@manufacturer_car_module.route("/manufacturer/<int:id>", methods=["GET", "DELETE"])
def retrieve_delete_manufacturer(id):
    try:
        manufacturer = Manufacturer.query.get(id)
        if manufacturer is None:
            abort(404)
        if request.method == "GET":
            response = manufacturer_schema.dump(manufacturer)
            return response
        # request.method == "DELETE"
        response = manufacturer_schema.dump(manufacturer)
        db.session.delete(manufacturer)
        db.session.commit()
        return response
    except TypeError as type_error:
        return jsonify({"msg": type_error})


# car
@manufacturer_car_module.route("/car", methods=["GET", "POST"])
def create_list_car():
    if request.method == "POST":
        json_data = request.get_json()
        if not json_data:
            return {"message": "No input data provided"}, 400
        # Validate and deserialize input
        try:
            data = car_schema.load(json_data)
        except ValidationError as err:
            return err.messages, 422

        name = data["name"]
        manufacturer_id = data["manufacturer_id"]
        launched_year = data["launched_year"]
        top_speed = data["top_speed"]
        engine_type = data["engine_type"]
        max_horse_power = data["max_horse_power"]
        zero_to_hundred = data["zero_to_hundred"]

        try:
            new_car = Car(
                name,
                manufacturer_id,
                launched_year,
                top_speed,
                engine_type,
                max_horse_power,
                zero_to_hundred,
            )
            db.session.add(new_car)
            db.session.commit()
            return car_schema.jsonify(new_car)
        except Exception as E:
            return jsonify({"msg": E})
    else:
        all_cars = Car.query.all()
        response = cars_schema.dump(all_cars)

        return jsonify(response)


@manufacturer_car_module.route("/car/<int:id>", methods=["GET", "DELETE"])
def retrieve_delete_car(id):
    try:
        car = Car.query.get(id)
        if car is None:
            abort(404)
        if request.method == "GET":
            response = car_schema.dump(car)
            return response
        # request.method == "DELETE"
        response = car_schema.dump(car)
        db.session.delete(car)
        db.session.commit()
        return response
    except TypeError as type_error:
        return jsonify({"msg": type_error})
