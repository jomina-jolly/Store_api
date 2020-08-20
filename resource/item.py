from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help="This field cannot be left blank")
    
    parser.add_argument('store_id',
        type=int,
        required=True,
        help="Items need to have store id")
    
    @jwt_required()
    def get(self, name):
        
        item = ItemModel.find_by_name(name)
        
        if item:
            return item.json(), 200
        else:
            return {'message': "Item does not exist"}, 404
    
    
 
    def post(self, name):
        check_item = ItemModel.find_by_name(name)
        print ("check done")
        if check_item:
            return {'message': "An item with name {} already exists".format(name)}
        
        data = Item.parser.parse_args()
        new_item = ItemModel(name, data['price'], data['store_id'])
        print (new_item.json())
        try:
            new_item.save_to_db()      
        except Exception as e:
            print(e)
            return {'message': 'Item could not be inserted'}, 500
        return new_item.json(), 202
    
    def delete(self, name):
        
        check_item = ItemModel.find_by_name(name)
        if not check_item:
            return {'message': "An item with name {} doesn't exists".format(name)}
        
        check_item.delete_from_db()
        return {'message': "Item deleted!"},200

    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)
        
        if item:
            item.price = data['price']
        else:
            item = ItemModel(name, data['price'], data['store_id']) #NO item present ,hence 'item' will be None
            
        item.save_to_db()
        return item.json(), 200
    
      
            
        
class ItemList(Resource):
    def get(self):
        return {'items': [item.json() for item in ItemModel.query.all()]}  ### {'item': list(map(lambda x:x.json(), ItemModel.query))}
        
