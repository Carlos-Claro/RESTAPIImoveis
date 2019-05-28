# -*- coding: utf-8 -*-

import unittest
import sys
from myMysql import myMysql

class TestMymysql(unittest.TestCase):
    def setUp(self):
        self.conn = myMysql()
        
    def test_keys(self):
        dados = self.conn.data
        self.assertEqual(dados['database'],'guiasjp')
    
    def test_get(self):
        query = 'select * from imoveis limit 0,2'
        self.assertTrue(isinstance(self.conn.get(query),list))
    
    def test_get_result_zero(self):
        query = 'select * from imoveis where id < 0 limit 0,1'
        self.assertTrue(len(self.conn.get(query)) == 0)
        
    def test_get_result_dois(self):
        query = 'select * from imoveis limit 0,2'
        self.assertTrue(len(self.conn.get(query)) == 2)
    
    def test_querys(self):
        query = 'INSERT INTO test_query (titulo, qtde) VALUES ("teste",1)'
        id = self.conn.add(query)
        self.assertTrue(isinstance(id,int))
        q = 'SELECT id from test_query where id = ' + str(id)
        self.assertTrue(len(self.conn.get(q)) == 1)
        qu = 'UPDATE test_query set titulo = "testeA" where id = ' + str(id)
        self.assertTrue(self.conn.update(qu))
        que = 'DELETE from test_query where id = ' + str(id)
        self.assertTrue(self.conn.delete(que))
        self.assertTrue(len(self.conn.get(q)) == 0)
        
        
if __name__ == '__main__':
    unittest.main()