from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help='This field cannot be left blank')
    parser.add_argument('store_id',
                        type=int,
                        required=True,
                        help='This field cannot be left blank')
        
    @jwt_required()
    def get(self, name):
        item = ItemModel.get_item_by_name(name)
        if item:
            return item.json(), 200
        return {'message': 'Item not found'}, 404
        
    
    def post(self, name):
        if ItemModel.get_item_by_name(name):
            return {'message':
                    f'item with name {name} already exists'}, 400

        try:
            data = Item.parser.parse_args()
            item = ItemModel(name, data["price"], data["store_id"])
            item.save_to_db()
            return item.json(), 201
        except:
            return {
                "message": "An error occurred during insert"
            }, 500

    @jwt_required()
    def delete(self, name):
        item = ItemModel.get_item_by_name(name)
        if item:
            try:
                item.delete_from_db()
                return {'message': 'item deleted'}
            except:
                return {
                "message": "An error occurred during delete"
                }, 500
        return {'message':'item not found'}

    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.get_item_by_name(name)
        if not item:
            item = ItemModel(name, data['price'], data["store_id"])
        else:
            item.price = data["price"]
            item.store_id = data["store_id"]
        item.save_to_db()
        return item.json(), 201

class ItemList(Resource):
    def get(self):
        return {"items": [ i.json() for i in ItemModel.query.all()]}

