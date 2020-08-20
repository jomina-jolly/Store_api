from db import db


class ItemModel(db.Model):
    __tablename__ = "items"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    price = db.Column(db.Float(precision=2))
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))
    store = db.relationship('StoreModel')
    
    def __init__(self, name, price, store_id):
        self.name = name
        self.price = price
        self.store_id = store_id
        
    def json(self):
        return {'name': self.name, 'price': self.price, 'store_id': self.store_id}
    
    @classmethod
    def find_by_name(cls, name):
        
            ### CODE BEFORE USING SQLACHEMY!!
            # connection = sqlite3.connect('data.db')
            # cursor = connection.cursor()
            # query = "SELECT * FROM items WHERE name = ?"
            # result = cursor.execute(query,(name,))
            # row = result.fetchone()
            # connection.close()
            # if row:
            #     item = {
            #         'name': row[0],
            #         'price': row[1]
            #     }
            #     return cls(row[0], row[1])
                #return cls(*row) ##same meaning
                
            return cls.query.filter_by(name=name).first() ###SELECT * FROM __tablename where name = name LIMIT 1 >> to object
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
            
    def delete_from_db(self):
          db.session.delete(self)
          db.session.commit()