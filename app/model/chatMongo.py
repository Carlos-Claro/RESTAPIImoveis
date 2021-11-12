# -*- coding: utf-8 -*-


from library.myMongo import myMongo
import datetime


class chatMongo(object):

    def __init__(self):
        self.db = myMongo('chat')
        self.collection = 'conversas'

    def add(self, data):
        return self.db.add_one(self.collection, data)

    def update_id(self, id, data):
        return self.db.update_one(self.collection, {'_id': id}, data)

    def delete_id(self, id):
        return self.db.delete_one(self.collection, {'_id': id})

    def getItem(self, id):
        return self.db.get_item_id(self.collection, id)

    def getItemFiltro(self, data):
        return self.db.get_item_filtro(self.collection, data)

    def getItens(self, data):
        return self.db.getItens(self.collection, data)




if __name__ == '__main__':
    print('')
