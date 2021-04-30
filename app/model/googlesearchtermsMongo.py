# -*- coding: utf-8 -*-


from library.myMongo import myMongo
import datetime


class GooglesearchtermsMongo(object):

    def __init__(self):
        self.db = myMongo('imoveis')

    def add(self, data):
        return self.db.add_one('google_search_terms', data)

    def update_id(self, id, data):
        return self.db.update_one('google_search_terms', {'_id': id}, data)

    def delete_id(self, id):
        return self.db.delete_one('google_search_terms', {'_id': id})

    def getItem(self, id):
        return self.db.getItem('google_search_terms', id)

    def getItens(self, data):
        return self.db.get_itens('google_search_terms', data)


if __name__ == '__main__':
    print('')
