from __init__ import create_app
from flask_restful import Api
from resources.item import ItemList, Item

app = create_app()
api = Api(app)

api.add_resource(ItemList, '/items')
api.add_resource(Item, '/items/<int:id>')

if __name__ == '__main__':
    app.run(debug=True)
