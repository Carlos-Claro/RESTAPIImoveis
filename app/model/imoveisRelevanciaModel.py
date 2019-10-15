# -*- coding: utf-8 -*-


from library.myMysql import myMysql
from library.myQuery import myQuery
import datetime

class imoveisRelevanciaModel(object):
    
    def __init__(self):
        self.conn = myMysql()
        self.query = myQuery()
        
    def add(self,data):
        count = 0
        keys = '('
        values = '('
        for k,v in data.items():
            if count > 0:
                keys += ', '
                values += ', '
            keys += str(k)
            values += '"' + str(v) + '"'
            count += 1
        keys += ')'
        values += ')'
        query = 'INSERT INTO imoveis_relevancia {} VALUES {}'.format(keys,values)
        return self.conn.add(query)
    
    def update_id(self,data,id):
        if isinstance(data,str):
            valor = data
        else:
            valor = ''
            count = 0
            for k,v in data.items():
                if count > 0:
                    valor += ', '
                valor += k + '=' + str(v)
        qu = 'UPDATE imoveis_relevancia set {} where id = {}'.format(valor,str(id))
        return self.conn.update(qu)
    
    def delete_id(self, id):
        q = 'SELECT id from imoveis_relevancia where id = {} '.format(str(id))
        a = len(self.conn.get(q))
        if a > 0:
            que = 'DELETE from imoveis_relevancia where id = {}'.format(str(id))
            self.conn.delete(que)
            if len(self.conn.get(q)) == 0:
                return True
        return False
    
    def getItem(self,id):
        query = {}
        query['colunas'] = '*'
        query['tabela'] = 'imoveis_relevancia'
        d = datetime.datetime.now().strftime('%Y-%m-%d')
        now = datetime.datetime.now()
        t = datetime.datetime.timestamp(now)
        query['where'] = [{'tipo':'where','campo':'imoveis_relevancia.id','valor':id}]
        q = self.query.get(query)
        itens = self.conn.get(q)
        return itens['itens'][0]
    
    
    def getItens(self, data):
        query = {}
        query['colunas'] = '*'
        query['tabela'] = 'imoveis_relevancia'
        d = datetime.datetime.now().strftime('%Y-%m-%d')
        now = datetime.datetime.now()
        t = datetime.datetime.timestamp(now)
        if 'filtro' in data:
            query['where'].append(data['filtro'])
        query['ordem'] = 'imoveis_relevancia.id DESC'
        query['offset'] = 0
        query['limit'] = 2000
        q = self.query.get(query)
        itens = self.conn.get(q)
        return itens
    
    def getTotalItens(self, data):
        query = {}
        query['colunas'] = '*'
        query['tabela'] = 'imoveis_relevancia'
        d = datetime.datetime.now().strftime('%Y-%m-%d')
        now = datetime.datetime.now()
        t = datetime.datetime.timestamp(now)
        query['where'] = data['filtro']
        query['ordem'] = 'imoveis_relevancia.id DESC'
        query['offset'] = 0
        query['limit'] = 2000
        q = self.query.get(query)
        itens = self.conn.get(q)
        return itens['qtde']
    
    def add_log(self,data):
        count = 0
        keys = '('
        values = '('
        for k,v in data.items():
            if count > 0:
                keys += ', '
                values += ', '
            keys += str(k)
            values += '"' + str(v) + '"'
            count += 1
        keys += ')'
        values += ')'
        query = 'INSERT INTO imoveis_relevancia_log {} VALUES {}'.format(keys,values)
        return self.conn.add(query)
    
    def update_id_log(self,data,id):
        if isinstance(data,str):
            valor = data
        else:
            valor = ''
            count = 0
            for k,v in data.items():
                if count > 0:
                    valor += ', '
                valor += k + '=' + str(v)
        qu = 'UPDATE imoveis_relevancia_log set {} where id = {}'.format(valor,str(id))
        return self.conn.update(qu)
    
    def delete_id_log(self, id):
        q = 'SELECT id from imoveis_relevancia_log where id = {} '.format(str(id))
        a = len(self.conn.get(q))
        if a > 0:
            que = 'DELETE from imoveis_relevancia_log where id = {}'.format(str(id))
            self.conn.delete(que)
            if len(self.conn.get(q)) == 0:
                return True
        return False
    
    def getItem_log(self,id):
        query = {}
        query['colunas'] = '*'
        query['tabela'] = 'imoveis_relevancia_log'
        d = datetime.datetime.now().strftime('%Y-%m-%d')
        now = datetime.datetime.now()
        t = datetime.datetime.timestamp(now)
        query['where'] = [{'tipo':'where','campo':'imoveis_relevancia_log.id','valor':id}]
        q = self.query.get(query)
        itens = self.conn.get(q)
        return itens['itens'][0]
    
    
    def getItens_log(self, data):
        query = {}
        query['colunas'] = '*'
        query['tabela'] = 'imoveis_relevancia_log'
        d = datetime.datetime.now().strftime('%Y-%m-%d')
        now = datetime.datetime.now()
        t = datetime.datetime.timestamp(now)
        if 'filtro' in data:
            query['where'].append(data['filtro'])
        query['ordem'] = 'imoveis_relevancia_log.id DESC'
        query['offset'] = 0
        query['limit'] = 2000
        q = self.query.get(query)
        itens = self.conn.get(q)
        return itens
    
    def getTotalItens_log(self, data):
        query = {}
        query['colunas'] = '*'
        query['tabela'] = 'imoveis_relevancia_log'
        d = datetime.datetime.now().strftime('%Y-%m-%d')
        now = datetime.datetime.now()
        t = datetime.datetime.timestamp(now)
        query['where'] = data['filtro']
        query['ordem'] = 'imoveis_relevancia_log.id DESC'
        query['offset'] = 0
        query['limit'] = 2000
        q = self.query.get(query)
        itens = self.conn.get(q)
        return itens['qtde']

if __name__ == '__main__':
    print('')
    
