from flask_restful import Resource, reqparse
from models.store import StoreModel
from flask_jwt import jwt_required

class Store(Resource):       
    @jwt_required()
    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json(), 200
        return {'message': 'Store not found'}, 404
        
    
    def post(self, name):
        if StoreModel.find_by_name(name):
            return {'message':
                    f'Store {name} already exists'}, 400

        try:
            store = StoreModel(name)
            store.save_to_db()
            return store.json(), 201
        except:
            return {
                "message": "An error occurred during insert"
            }, 500

    @jwt_required()
    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            try:
                store.delete_from_db()
                return {'message': f'Store {name} deleted'}
            except:
                return {
                "message": "An error occurred during delete"
                }, 500
        return {'message':'store not found'}


class StoreList(Resource):
    def get(self):
        return {"stores": [ s.json() for s in StoreModel.query.all()]}

