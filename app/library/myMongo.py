# -*- coding: utf-8 -*-
import pymongo 
import datetime
import pprint

class myMongo(object):
    def __init__(self,database):
        self.client = pymongo.MongoClient("localhost",27017)
        self.db = self.client[database]

    def add_one(self,collection,data):
        try:
            coll = self.db[collection]
            res = coll.insert_one(data)
            retorno = True
        except e:
            retorno = False
            pass
        return retorno
    
    def add_many(self,collection,data):
        coll = self.db[collection]
        res = coll.insert_many(data)
        return res
    
    def update_one(self,collection,filtro,data):
        coll = self.db[collection]
        res = coll.update_one(filtro,{'$set':data}).modified_count
        return res

    def update_many(self,collection,filtro,data):
        coll = self.db[collection]
        res = coll.update_many(filtro,data).modified_count
        return res
    
    def delete_one(self,collection,filtro):
        coll = self.db[collection]
        res = coll.delete_one(filtro).deleted_count
        return res

    def delete_many(self,collection,filtro):
        coll = self.db[collection]
        res = coll.delete_many(filtro).deleted_count
        return res

    def get_item(self,collection,id):
        coll = self.db[collection]
        p = coll.find_one({'_id':int(id)})
        return p
    
    def get_item_filtro(self,collection,where):
        coll = self.db[collection]
        p = coll.find_one(where)
        return p

    # data array: [where, limit, sort, ]
    def get_itens(self,collection,data):
        coll = self.db[collection]
        cursor = coll.find(data['where'])
        if 'limit' in data:
            cursor.limit(data['limit'])
        if 'sort' in data:
            s = self.set_sort(data['sort'])
            cursor.sort(s)
        contador = 0
        retorno = {}
        retorno['itens'] = []
        for c in cursor:
            contador += 1
            retorno['itens'].append(c)
        retorno['qtde'] = contador
        return retorno
        
    def set_sort(self, sort):
        retorno = []
        for k, v in sort.items():
            o = pymongo.DESCENDING
            if v == 1 :
                o = pymongo.ASCENDING
            retorno.append((k,o))
        
        return retorno

    def get_total_itens(self,collection,data):
        coll = self.db[collection]
        return coll.count_documents(data['where'])


    def aggregate(self,pipeline,collection):
        coll = self.db[collection]
        itens = {}
        req = list(coll.aggregate(pipeline))
        itens['qtde'] = 0
        itens['itens'] = []
        for i in req:
            itens['itens'].append(i)
            itens['qtde'] = itens['qtde'] + 1
        return itens
        


if __name__ == '__main__':
    try:
        m = myMongo("imoveis")
        data = {}
        data['where'] = {'id_cidade':'2'}
        t = m.get_total_itens("imoveis",data)
        print('total itens: ')
        print(t)
        p = m.get_itens("imoveis",data)
        #for a in p:
        #    print(a)
        #pprint.pprint(p)
    except KeyboardInterrupt:
        pass
    finally:
        print("Mongo finish")
