from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

# Init app
app = Flask(__name__)
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
    BASE_DIR, "db.sqlite"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Init db
db = SQLAlchemy(app)

# Init ma
ma = Marshmallow(app)

# DB Models
class Manufacturer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    head_quarter = db.Column(db.String(20), nullable=True)
    founder = db.Column(db.String(50), nullable=True)
    established_year = db.Column(db.Integer)

    def __init__(self, name, head_quarter, founder, established_year):
        self.name = name
        self.head_quarter = head_quarter
        self.founder = founder
        self.established_year = established_year

    def __repr__(self):
        return f"<Manufacturer {self.name}"


# Schemas
class ManufacturerSchema(ma.Schema):
    class Meta:
        fields = ["name", "head_quarter", "founder", "established_year"]


# Init schema
manufacturer_schema = ManufacturerSchema()
manufacturers_schema = ManufacturerSchema(many=True)


@app.route("/manufacturer", methods=["GET", "POST"])
def add_manufacturer():
    if request.method == "POST":
        name = request.json["name"]
        head_quarter = request.json["head_quarter"]
        founder = request.json["founder"]
        established_year = request.json["established_year"]
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
        result = manufacturers_schema.dump(all_manufacturers)

        return jsonify(result)


# Run server
if __name__ == "__main__":
    app.run(debug=True)
