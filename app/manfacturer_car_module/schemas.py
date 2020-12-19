from .models import Manufacturer

from app import ma

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

    manufacturer = ma.Nested("ManufacturerSchema")


# Init schema
manufacturer_schema = ManufacturerSchema()
manufacturers_schema = ManufacturerSchema(many=True)

car_schema = CarSchema()
cars_schema = CarSchema(many=True)
