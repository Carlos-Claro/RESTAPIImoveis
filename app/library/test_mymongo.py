# -*- coding: utf-8 -*-

import unittest
import random
import sys
import datetime
from myMongo import myMongo

class TestmyMongo(unittest.TestCase):
    def setUp(self):
        self.db = myMongo('imoveis')
        
    def test_qtde(self):
        data = {}
        data['where'] = {'id_cidade':'2'}
        self.assertTrue(self.db.get_total_itens("imoveis",data))
        
        
    def test_get(self):
        data = {}
        data['where'] = {"imovel_id_cidade":"2"}
        data['limit'] = 10
        data['sort'] = {'_id':-1}
        res = self.db.get_itens("imoveis",data)
        self.assertTrue(isinstance(res['itens'],object))
        self.assertTrue(res['qtde'] > 0)
    
    def test_get_in(self):
        data = {}
        data['where'] = {'id_cidade' : {'$in':['1', '2']}}
        res = self.db.get_itens("imoveis",data)
        self.assertTrue(isinstance(res['itens'],object))
        self.assertTrue(res['qtde'] > 0)
    
    def test_get_one(self):
        res = self.db.get_item_filtro("imoveis",{"imovel_id_cidade":"2"})
        self.assertTrue('_id' in res)
#    
 #   def test_delete_true(self):
  #      filtro = {"_id":self.INS['_id']}
   #     d = self.db.delete_one("imoveis",filtro)
    #    self.assertTrue(d == 1)
        
        
#    def test_delete_false(self):
 #       filtro = {"_id":self.INS['_id']}
  #      d = self.db.delete_one("imoveis",filtro)
   #     self.assertTrue(d == 1)
    
    INS = {
            'nome':'Teste Adionar imóvel',
            'id_tipo': '2',
            'imoveis_tipo_link': 'apartamento',
            'imoveis_cidade_link': 'curitiba_pr',
            'id_cidade': 1  
            }
    def test_add_update_delete(self):
        self.INS['_id'] = random.randrange(100000,200000)
        _id = self.db.add_one('imoveis', self.INS)
        print('ID: ')
        print(_id)
        self.assertTrue(_id)
        filtro = {"_id":self.INS['_id']}
        data = {'id_cidade':1000}
        up = self.db.update_one("imoveis",filtro,data)
        self.assertTrue(up == 1)
        d = self.db.delete_one("imoveis",filtro)
        self.assertTrue(d == 1)
        
    def test_get_aggregate(self):
        pipeline = [
                {"$match":{"data":{"$gte":(datetime.datetime.now() - datetime.timedelta(days=10))}}},
                {"$group":{"_id":"$tipo","acesso":{"$sum":1}}}
                ]
        res = self.db.aggregate(pipeline,'log_imoveis')
        self.assertTrue(res['qtde'] > 0)
        
    def test_get_aggregate_id_imovel(self):
        da = datetime.datetime.now() - datetime.timedelta(days=10)
        y = int(da.strftime('%Y'))
        m = int(da.strftime('%m'))
        d = int(da.strftime('%d'))
        pipeline = [
                {"$match":{"data":{"$gte":datetime.datetime(y,m,d,0,0),"$lte":datetime.datetime(y,m,d,23,59)}}},
                {"$group":{"_id":"$id_imovel","acesso":{"$sum":1}}}
                ]
        res = self.db.aggregate(pipeline,'log_imoveis')
        self.assertTrue(res['qtde'] > 0)
        
    def test_get_aggregate_id_empresa(self):
        da = datetime.datetime.now() - datetime.timedelta(days=10)
        y = int(da.strftime('%Y'))
        m = int(da.strftime('%m'))
        d = int(da.strftime('%d'))
        pipeline = [
                {"$match":{"data":{"$gte":datetime.datetime(y,m,d,0,0),"$lte":datetime.datetime(y,m,d,23,59)}}},
                {"$group":{"_id":"$id_empresa","acesso":{"$sum":1}}}
                ]
        res = self.db.aggregate(pipeline,'log_imoveis')
        self.assertTrue(res['qtde'] > 0)
        retorno = {}
        for item in res['itens']:
            retorno[item['_id']] = []
            retorno[item['_id']].append({'qtde':item['acesso']})
            print(item)
            print(item['_id'])
            p2 = [
                {"$match":{"data":{"$gte":datetime.datetime(y,m,d,0,0),"$lte":datetime.datetime(y,m,d,23,59)},"id_empresa":item['_id']}},
                {"$group":{"_id":"$tipo","acesso":{"$sum":1}}}
                    ]
            res2 = self.db.aggregate(p2,'log_imoveis')
            self.assertTrue(res2['qtde'] > 0)
            for tipo in res2['itens']:
                p3 = [
                    {"$match":{"data":{"$gte":datetime.datetime(y,m,d,0,0),"$lte":datetime.datetime(y,m,d,23,59)},"id_empresa":item['_id'],"tipo":tipo['_id']}},
                    {"$group":{"_id":"$id_imovel","acesso":{"$sum":1}}}
                        ]
                res3 = self.db.aggregate(p3,'log_imoveis')
                self.assertTrue(res3['qtde'] > 0)
                lista = []
                for id_imovel in res3['itens']:
                    lista.append({id_imovel['_id']:id_imovel['acesso']})
                retorno[item['_id']].append({tipo['_id']:{'qtde':tipo['acesso'],'lista':lista}})
                del lista
        print(retorno)

if __name__ == '__main__':
    unittest.main()