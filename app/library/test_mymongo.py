# -*- coding: utf-8 -*-

import unittest
import random
import sys
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
    
    def test_get_one(self):
        res = self.db.get_item("imoveis",{"imovel_id_cidade":"2"})
        self.assertTrue(res['_id'])
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
        
        
        
    
if __name__ == '__main__':
    unittest.main()