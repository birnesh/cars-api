import os

from flask import Flask, abort, jsonify, request
from flask_marshmallow import Marshmallow
# from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
# swagger_ui
from flask_swagger_ui import get_swaggerui_blueprint
from marshmallow import ValidationError, pre_load
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import NotFound

# Init app
app = Flask(__name__)
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# configuration
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = os.environ.get("DATABASE_URL", "postgresql://postgres:postgres@127.0.0.1:5432/super_cars")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JSON_SORT_KEYS"] = False

# Init db
db = SQLAlchemy(app)

# Init ma
ma = Marshmallow(app)

# migrate = Migrate(app, db)
### swagger specific ###
SWAGGER_URL = "/swagger"
API_URL = "/static/swagger.yaml"
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL, API_URL, config={"app_name": "Super Cars API Using FLask"}
)

app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)
### end swagger specific ###

# DB Models
class Manufacturer(db.Model):
    __tablename__ = "manufacturer"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    head_quarter = db.Column(db.String(40), nullable=True)
    founder = db.Column(db.String(50), nullable=True)
    established_year = db.Column(db.Integer)
    cars = db.relationship(
        "Car", cascade="all,delete", backref="manufacturer", lazy=True
    )

    def __init__(self, name, head_quarter, founder, established_year):
        self.name = name
        self.head_quarter = head_quarter
        self.founder = founder
        self.established_year = established_year

    def __repr__(self):
        return f"<Manufacturer {self.name}>"


class Car(db.Model):
    __tablename__ = "car"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    manufacturer_id = db.Column(
        db.Integer, db.ForeignKey("manufacturer.id"), nullable=False
    )
    launched_year = db.Column(db.Integer)
    top_speed = db.Column(db.Integer)
    engine_type = db.Column(db.String(100), nullable=False)
    max_horse_power = db.Column(db.Integer)
    zero_to_hundred = db.Column(db.Float, nullable=True)

    def __init__(
        self,
        name,
        manufacturer_id,
        launched_year,
        top_speed,
        engine_type,
        max_horse_power,
        zero_to_hundred,
    ):
        self.name = name
        self.manufacturer_id = manufacturer_id
        self.launched_year = launched_year
        self.top_speed = top_speed
        self.engine_type = engine_type
        self.max_horse_power = max_horse_power
        self.zero_to_hundred = zero_to_hundred

    def __repr__(self):
        return f"<Car {self.name}>"


# Schemas


class ManufacturerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        ordered = True
        model = Manufacturer


class CarSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        ordered = True
        fields = (
            "id",
            "name",
            "launched_year",
            "top_speed",
            "engine_type",
            "max_horse_power",
            "zero_to_hundred",
            "manufacturer_id",
            "manufacturer",
        )

    manufacturer = ma.Hyperlinks(
        ma.URLFor("retrieve_delete_manufacturer", values=dict(id="<manufacturer_id>"))
    )


# Init schema
manufacturer_schema = ManufacturerSchema()
manufacturers_schema = ManufacturerSchema(many=True)

car_schema = CarSchema()
cars_schema = CarSchema(many=True)


# API routes
# manufacturing
@app.route("/manufacturers", methods=["GET", "POST"])
def create_list_manufacturer():
    if request.method == "POST":
        try:
            json_data = request.get_json()
            if not json_data:
                raise Exception("Request Body is empty")
            # Validate and deserialize input
            # Validation Error may occur here
            data = manufacturer_schema.load(json_data)
            name = data["name"]
            head_quarter = data["head_quarter"]
            founder = data["founder"]
            established_year = data["established_year"]
            # db integrity Error may occur here
            new_manufacturer = Manufacturer(
                name, head_quarter, founder, established_year
            )
            db.session.add(new_manufacturer)
            db.session.commit()
            response = jsonify({"message":"Success Ok"})
            response.status_code = 201
            response.headers["location"] = "/manufacturer/" + str(new_manufacturer.id)
            return response
        except IntegrityError:
            return (
                jsonify(
                    {
                        "error": {
                            "code": 400,
                            "message": "The request failed because it contained an invalid value.",
                        }
                    }
                ),
                400,
            )
        except ValidationError as validation_error:
            return jsonify({"error": {"message": validation_error.messages}}), 422 
        except Exception as empty_request_body:
            return (
                        jsonify({"error": {"message": empty_request_body.messages}}),
                        400,
                    )       
    else: # GET
        try:
            all_manufacturers = Manufacturer.query.all()
            response = manufacturers_schema.dump(all_manufacturers)
            return jsonify(response)
        except Exception:
            return jsonify({"error": {"message": "Internal server error"}}), 500


@app.route("/manufacturer/<int:id>", methods=["GET", "DELETE"])
def retrieve_delete_manufacturer(id):
    try:
        manufacturer = Manufacturer.query.get(id)
        if manufacturer is None:
            return (
                jsonify(
                    {
                        "error": {
                            "code": 404,
                            "message": "The data that you are looking for does not exist",
                        }
                    }
                ),
                404,
            )
        if request.method == "GET":
            response = manufacturer_schema.dump(manufacturer)
            return response
        # request.method == "DELETE"
        db.session.delete(manufacturer)
        db.session.commit()
        return jsonify({"message":"Success OK"}),200
    except Exception:
        return jsonify({"error": {"message": "Internal server error"}}), 500


# car
@app.route("/cars", methods=["GET", "POST"])
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


@app.route("/car/<int:id>", methods=["GET", "DELETE"])
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


