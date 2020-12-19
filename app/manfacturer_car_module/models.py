from app import db


class Manufacturer(db.Model):
    __tablename__ = "manufacturer"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    head_quarter = db.Column(db.String(20), nullable=True)
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
    engine_type = db.Column(db.String(30), nullable=False)
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