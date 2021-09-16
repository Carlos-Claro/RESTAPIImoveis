# -*- coding: utf-8 -*-


from library.myMongo import myMongo
import datetime


class usuarioPortalMongo(object):

    def __init__(self):
        self.db = myMongo('imoveis')

    def add(self, data):
        print(data)
        return self.db.add_one('usuario_portal', data)

    def update_id(self, id, data):
        return self.db.update_one('usuario_portal', {'_id': id}, data)

    def delete_id(self, id):
        return self.db.delete_one('usuario_portal', {'_id': id})

    def getItem(self, id):
        return self.db.get_item_id('usuario_portal', id)

    def getItens(self, data):
        return self.db.getItens('usuario_portal', data)


if __name__ == '__main__':
    pass
