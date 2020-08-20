from flask_restful import Resource
from models.store import StoreModel

class Store(Resource):
    
    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        else:
            return {'message': "Store not found"}, 404
    
    def post(self, name):
        store = StoreModel.find_by_name(name)
        
        if store:
            return {'message': 'Store by the name {} already exists'.format(name)}, 400
        else:
            store = StoreModel(name)
            store.save_to_db()
            return store.json()
    
    def delete(self,name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()
            return {'message': 'Store deleted'}
        else:
            return {'message': "Store not found"}, 404
    
class StoreList(Resource):
    def get(self):
        return {'stores': [store.json() for store in StoreModel.query.all()]}
    