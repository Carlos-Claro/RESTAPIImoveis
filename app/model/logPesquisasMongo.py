# -*- coding: utf-8 -*-


from library.myMongo import myMongo

class logPesquisasMongo(object):

    def __init__(self):
        self.db = myMongo('imoveis')

    def add(self, data):
        return self.db.add_one('log_pesquisa', data)

    def update_id(self, id, data):
        return self.db.update_one('log_pesquisa', {'_id': id}, data)

    def delete_id(self, id):
        return self.db.delete_one('log_pesquisa', {'_id': id})

    def getItem(self, id):
        return self.db.getItem('log_pesquisa', id)

    def getItens(self, data):
        return self.db.getItens('log_pesquisa', data)


if __name__ == '__main__':
    print('')
