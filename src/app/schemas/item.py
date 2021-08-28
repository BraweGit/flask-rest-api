from marshmallow import Schema, fields, validate, validates, ValidationError, post_load, post_dump
from models.item import ItemModel

class ItemSchema(Schema):
    name = fields.Str(required=True)
    description = fields.Str(required=True, validate=validate.Length(min=1))

    @validates('name')
    def validate_name(self, name):
        if bool(ItemModel.query.filter_by(name=name).first()):
            raise ValidationError(f'{name} already exists, please use a different name')

    @post_load
    def make_item(self, data, **kwargs):
        return ItemModel(**data)