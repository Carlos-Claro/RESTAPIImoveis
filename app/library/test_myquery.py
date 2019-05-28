#!/usr/bin/python3.6

import unittest
import sys
from myQuery import myQuery

class TestQuery(unittest.TestCase):
    def setUp(self):
        self.query = myQuery()
    
    def test_string(self):
        string = 'select * from imoveis'
        valor = self.query.get(string)
        self.assertEqual(valor,string)

    def test_array(self):
        query = {}
        query['colunas'] = 'imoveis.*'
        query['tabela'] = 'imoveis'
        query['join'] = [{'tabela':'empresas','where':'imoveis.id_empresa = empresas.id','tipo':'INNER'},{'tabela':'imoveis_tipos','where':'imoveis.id_tipo = imoveis_tipos.id','tipo':'LEFT'}]
        query['where'] = [{'tipo':'where','campo':'imoveis.id_tipo','valor':'1'}]
        query['ordem'] = 'imoveis.id desc'
        query['offset'] = 0
        query['limit'] = 10
        string = 'SELECT imoveis.* FROM imoveis INNER JOIN empresas ON imoveis.id_empresa = empresas.id LEFT JOIN imoveis_tipos ON imoveis.id_tipo = imoveis_tipos.id WHERE imoveis.id_tipo = 1 ORDER BY imoveis.id desc LIMIT 0, 10'
        valor = self.query.get(query)
        self.assertEqual(valor,string)
    
    def test_where_string(self):
        query = {}
        query['colunas'] = 'imoveis.*'
        query['tabela'] = 'imoveis'
        query['join'] = [{'tabela':'empresas','where':'imoveis.id_empresa = empresas.id','tipo':'INNER'},{'tabela':'imoveis_tipos','where':'imoveis.id_tipo = imoveis_tipos.id','tipo':'LEFT'}]
        query['where'] = 'imoveis.id_tipo = 1'
        query['ordem'] = 'imoveis.id desc'
        query['offset'] = 0
        query['limit'] = 10
        string = 'SELECT imoveis.* FROM imoveis INNER JOIN empresas ON imoveis.id_empresa = empresas.id LEFT JOIN imoveis_tipos ON imoveis.id_tipo = imoveis_tipos.id WHERE imoveis.id_tipo = 1 ORDER BY imoveis.id desc LIMIT 0, 10'
        valor = self.query.get(query)
        self.assertEqual(valor,string)
    
    def test_like_string(self):
        query = {}
        query['colunas'] = 'imoveis.*'
        query['tabela'] = 'imoveis'
        query['join'] = [{'tabela':'empresas','where':'imoveis.id_empresa = empresas.id','tipo':'INNER'},{'tabela':'imoveis_tipos','where':'imoveis.id_tipo = imoveis_tipos.id','tipo':'LEFT'}]
        query['where'] = [{'tipo':'like','campo':'imoveis.id_tipo','valor':'1'}]
        query['ordem'] = 'imoveis.id desc'
        query['offset'] = 0
        query['limit'] = 10
        string = 'SELECT imoveis.* FROM imoveis INNER JOIN empresas ON imoveis.id_empresa = empresas.id LEFT JOIN imoveis_tipos ON imoveis.id_tipo = imoveis_tipos.id WHERE imoveis.id_tipo LIKE "1" ORDER BY imoveis.id desc LIMIT 0, 10'
        valor = self.query.get(query)
        self.assertEqual(valor,string)
    
    def test_where_string_array(self):
        query = {}
        query['colunas'] = 'imoveis.*'
        query['tabela'] = 'imoveis'
        query['join'] = [{'tabela':'empresas','where':'imoveis.id_empresa = empresas.id','tipo':'INNER'},{'tabela':'imoveis_tipos','where':'imoveis.id_tipo = imoveis_tipos.id','tipo':'LEFT'}]
        query['where'] = ['imoveis.id_tipo = 1']
        query['ordem'] = 'imoveis.id desc'
        query['offset'] = 0
        query['limit'] = 10
        string = 'SELECT imoveis.* FROM imoveis INNER JOIN empresas ON imoveis.id_empresa = empresas.id LEFT JOIN imoveis_tipos ON imoveis.id_tipo = imoveis_tipos.id WHERE imoveis.id_tipo = 1 ORDER BY imoveis.id desc LIMIT 0, 10'
        valor = self.query.get(query)
        self.assertEqual(valor,string)
    
    def test_where_or(self):
        query = {}
        query['colunas'] = 'imoveis.*'
        query['tabela'] = 'imoveis'
        query['join'] = [{'tabela':'empresas','where':'imoveis.id_empresa = empresas.id','tipo':'INNER'},{'tabela':'imoveis_tipos','where':'imoveis.id_tipo = imoveis_tipos.id','tipo':'LEFT'}]
        query['where'] = ['imoveis.id_tipo = 1',{'tipo':'where_or','campo':'imoveis.id_tipo','valor':'2'}]
        query['ordem'] = 'imoveis.id desc'
        query['offset'] = 0
        query['limit'] = 10
        string = 'SELECT imoveis.* FROM imoveis INNER JOIN empresas ON imoveis.id_empresa = empresas.id LEFT JOIN imoveis_tipos ON imoveis.id_tipo = imoveis_tipos.id WHERE imoveis.id_tipo = 1 OR imoveis.id_tipo = 2 ORDER BY imoveis.id desc LIMIT 0, 10'
        valor = self.query.get(query)
        self.assertEqual(valor,string)
    
    def test_where_in(self):
        query = {}
        query['colunas'] = 'imoveis.*'
        query['tabela'] = 'imoveis'
        query['join'] = [{'tabela':'empresas','where':'imoveis.id_empresa = empresas.id','tipo':'INNER'},{'tabela':'imoveis_tipos','where':'imoveis.id_tipo = imoveis_tipos.id','tipo':'LEFT'}]
        query['where'] = [{'tipo':'where_in','campo':'imoveis.id_tipo','valor':[1,2,3]}]
        query['ordem'] = 'imoveis.id desc'
        query['offset'] = 0
        query['limit'] = 10
        string = 'SELECT imoveis.* FROM imoveis INNER JOIN empresas ON imoveis.id_empresa = empresas.id LEFT JOIN imoveis_tipos ON imoveis.id_tipo = imoveis_tipos.id WHERE imoveis.id_tipo IN (1,2,3) ORDER BY imoveis.id desc LIMIT 0, 10'
        valor = self.query.get(query)
        self.assertEqual(valor,string)

    def test_where_not_in(self):
        query = {}
        query['colunas'] = 'imoveis.*'
        query['tabela'] = 'imoveis'
        query['join'] = [{'tabela':'empresas','where':'imoveis.id_empresa = empresas.id','tipo':'INNER'},{'tabela':'imoveis_tipos','where':'imoveis.id_tipo = imoveis_tipos.id','tipo':'LEFT'}]
        query['where'] = [{'tipo':'where_not_in','campo':'imoveis.id_tipo','valor':[1,2,3]}]
        query['ordem'] = 'imoveis.id desc'
        query['offset'] = 0
        query['limit'] = 10
        string = 'SELECT imoveis.* FROM imoveis INNER JOIN empresas ON imoveis.id_empresa = empresas.id LEFT JOIN imoveis_tipos ON imoveis.id_tipo = imoveis_tipos.id WHERE imoveis.id_tipo NOT IN (1,2,3) ORDER BY imoveis.id desc LIMIT 0, 10'
        valor = self.query.get(query)
        self.assertEqual(valor,string)

    def test_where_not_in_string(self):
        query = {}
        query['colunas'] = 'imoveis.*'
        query['tabela'] = 'imoveis'
        query['join'] = [{'tabela':'empresas','where':'imoveis.id_empresa = empresas.id','tipo':'INNER'},{'tabela':'imoveis_tipos','where':'imoveis.id_tipo = imoveis_tipos.id','tipo':'LEFT'}]
        query['where'] = [{'tipo':'where_not_in','campo':'imoveis.id_tipo','valor':'1'}]
        query['ordem'] = 'imoveis.id desc'
        query['offset'] = 0
        query['limit'] = 10
        string = 'SELECT imoveis.* FROM imoveis INNER JOIN empresas ON imoveis.id_empresa = empresas.id LEFT JOIN imoveis_tipos ON imoveis.id_tipo = imoveis_tipos.id WHERE imoveis.id_tipo NOT IN (1) ORDER BY imoveis.id desc LIMIT 0, 10'
        valor = self.query.get(query)
        self.assertEqual(valor,string)

    def test_where_gt(self):
        query = {}
        query['colunas'] = 'imoveis.*'
        query['tabela'] = 'imoveis'
        query['join'] = [{'tabela':'empresas','where':'imoveis.id_empresa = empresas.id','tipo':'INNER'},{'tabela':'imoveis_tipos','where':'imoveis.id_tipo = imoveis_tipos.id','tipo':'LEFT'}]
        query['where'] = [{'tipo':'where_gt','campo':'imoveis.id_tipo','valor':'1'}]
        query['ordem'] = 'imoveis.id desc'
        query['offset'] = 0
        query['limit'] = 10
        string = 'SELECT imoveis.* FROM imoveis INNER JOIN empresas ON imoveis.id_empresa = empresas.id LEFT JOIN imoveis_tipos ON imoveis.id_tipo = imoveis_tipos.id WHERE imoveis.id_tipo > 1 ORDER BY imoveis.id desc LIMIT 0, 10'
        valor = self.query.get(query)
        self.assertEqual(valor,string)

    def test_where_gte(self):
        query = {}
        query['colunas'] = 'imoveis.*'
        query['tabela'] = 'imoveis'
        query['join'] = [{'tabela':'empresas','where':'imoveis.id_empresa = empresas.id','tipo':'INNER'},{'tabela':'imoveis_tipos','where':'imoveis.id_tipo = imoveis_tipos.id','tipo':'LEFT'}]
        query['where'] = [{'tipo':'where_gte','campo':'imoveis.id_tipo','valor':'1'}]
        query['ordem'] = 'imoveis.id desc'
        query['offset'] = 0
        query['limit'] = 10
        string = 'SELECT imoveis.* FROM imoveis INNER JOIN empresas ON imoveis.id_empresa = empresas.id LEFT JOIN imoveis_tipos ON imoveis.id_tipo = imoveis_tipos.id WHERE imoveis.id_tipo >= 1 ORDER BY imoveis.id desc LIMIT 0, 10'
        valor = self.query.get(query)
        self.assertEqual(valor,string)

    def test_where_lt(self):
        query = {}
        query['colunas'] = 'imoveis.*'
        query['tabela'] = 'imoveis'
        query['join'] = [{'tabela':'empresas','where':'imoveis.id_empresa = empresas.id','tipo':'INNER'},{'tabela':'imoveis_tipos','where':'imoveis.id_tipo = imoveis_tipos.id','tipo':'LEFT'}]
        query['where'] = [{'tipo':'where_lt','campo':'imoveis.id_tipo','valor':'1'}]
        query['ordem'] = 'imoveis.id desc'
        query['offset'] = 0
        query['limit'] = 10
        string = 'SELECT imoveis.* FROM imoveis INNER JOIN empresas ON imoveis.id_empresa = empresas.id LEFT JOIN imoveis_tipos ON imoveis.id_tipo = imoveis_tipos.id WHERE imoveis.id_tipo < 1 ORDER BY imoveis.id desc LIMIT 0, 10'
        valor = self.query.get(query)
        self.assertEqual(valor,string)

    def test_where_lte(self):
        query = {}
        query['colunas'] = 'imoveis.*'
        query['tabela'] = 'imoveis'
        query['join'] = [{'tabela':'empresas','where':'imoveis.id_empresa = empresas.id','tipo':'INNER'},{'tabela':'imoveis_tipos','where':'imoveis.id_tipo = imoveis_tipos.id','tipo':'LEFT'}]
        query['where'] = [{'tipo':'where_lte','campo':'imoveis.id_tipo','valor':'1'}]
        query['ordem'] = 'imoveis.id desc'
        query['offset'] = 0
        query['limit'] = 10
        string = 'SELECT imoveis.* FROM imoveis INNER JOIN empresas ON imoveis.id_empresa = empresas.id LEFT JOIN imoveis_tipos ON imoveis.id_tipo = imoveis_tipos.id WHERE imoveis.id_tipo <= 1 ORDER BY imoveis.id desc LIMIT 0, 10'
        valor = self.query.get(query)
        self.assertEqual(valor,string)

    def test_no_coluna(self):
        query = {}
        query['tabela'] = 'imoveis'
        query['join'] = [{'tabela':'empresas','where':'imoveis.id_empresa = empresas.id','tipo':'INNER'},{'tabela':'imoveis_tipos','where':'imoveis.id_tipo = imoveis_tipos.id','tipo':'LEFT'}]
        query['where'] = [{'tipo':'where_lte','campo':'imoveis.id_tipo','valor':'1'}]
        query['ordem'] = 'imoveis.id desc'
        query['offset'] = 0
        query['limit'] = 10
        string = 'SELECT * FROM imoveis INNER JOIN empresas ON imoveis.id_empresa = empresas.id LEFT JOIN imoveis_tipos ON imoveis.id_tipo = imoveis_tipos.id WHERE imoveis.id_tipo <= 1 ORDER BY imoveis.id desc LIMIT 0, 10'
        valor = self.query.get(query)
        self.assertEqual(valor,string)

if __name__ == '__main__':
    unittest.main()
