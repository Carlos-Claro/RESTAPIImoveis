# -*- coding: utf-8 -*-


from library.myMongo import myMongo
import datetime


class GooglesearchMongo(object):

    def __init__(self):
        self.db = myMongo('imoveis')

    def add(self, data):
        return self.db.add_one('google_search', data)

    def update_id(self, id, data):
        return self.db.update_one('google_search', {'_id': id}, data)

    def delete_id(self, id):
        return self.db.delete_one('google_search', {'_id': id})

    def getItem(self, id):
        return self.db.getItem('google_search', id)

    def getItens(self, data):
        return self.db.getItens('google_search', data)


if __name__ == '__main__':
    print('')
