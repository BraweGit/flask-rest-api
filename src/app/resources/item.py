from flask import request
from flask_restful import Resource
from marshmallow.exceptions import ValidationError
from sqlalchemy.sql.sqltypes import JSON
from models.item import ItemModel
from schemas.item import ItemSchema

item_schema = ItemSchema()
items_schema = ItemSchema(many=True)

class ItemList(Resource):
    def get(self) -> JSON:
        items = ItemModel.query.all()
        return items_schema.dump(items)

    def post(self) -> JSON:
        try:
            request_item = item_schema.load(request.get_json())
            request_item.insert_to_db()
            return item_schema.dump(request_item), 201
        except ValidationError as err:
            return err.messages, 400

class Item(Resource):
    def get(self, id):
        item = ItemModel.get_by_id(id)
        if item:
            return item_schema.dump(item)
        return {'message': f'item with id: {id} not found'}, 404

    def delete(self, id):
        item = ItemModel.get_by_id(id)
        if item:
            item.delete_from_db()
            return 200
        return {'message': f'item with id: {id} not found'}, 404

    def put(self, id):
        try:
            request_item = item_schema.load(request.get_json())
            item = ItemModel.get_by_id(id)
        except ValidationError as err:
            return err.messages, 400

        # Update if exists.
        if item:
            try:
                item.name = request_item.name
                item.description = request_item.description
                item.commit_to_db()

                return item_schema.dump(item), 200

            except ValidationError as err:
                return err.messages, 400

        # Insert if doesn't exist.
        request_item.insert_to_db()

        return item_schema.dump(request_item), 201
