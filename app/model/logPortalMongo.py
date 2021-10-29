# -*- coding: utf-8 -*-
from library.myMongo import myMongo

class logPortalMongo(object):

    def __init__(self):
        self.db = myMongo('imoveis')
        self.collection = 'log_portal_test'

    def add(self, data):
        return self.db.add_one(self.collection, data)

    def update_id(self, id, data):
        return self.db.update_one(self.collection, {'_id': id}, data)

    def update_filtro(self, filtro, data):
        return self.db.update_many(self.collection, filtro, {"$set": data})

    def delete_id(self, id):
        return self.db.delete_one(self.collection, {'_id': id})

    def getItem(self, id):
        return self.db.getItem(self.collection, id)

    def getItens(self, data):
        return self.db.getItens(self.collection, data)


if __name__ == '__main__':
    pass
