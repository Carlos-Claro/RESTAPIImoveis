from library.myMysql import myMysql
from library.myQuery import myQuery
import datetime
import sys

from library.Exception import RequestIncompleto
from library.Logs import Logs


class clientesCadastrosModel(object):

    def __init__(self):
        self.conn = myMysql()
        self.query = myQuery()
        self.table = 'clientes_cadastros'

    def add(self, data):
        query = self.query.add(self.table,data)
        return self.conn.add(query)

    def update_id(self, data, id):
        query = self.query.update(self.table, data, id)
        print(query)
        return self.conn.update(query)

    def update_id_in(self, data, ids):
        query = self.query.update_in(self.table,data,ids)
        return self.conn.update(query)

    def delete_id(self, id):
        q = 'SELECT id from {} where id = {} '.format(self.table, str(id))
        a = len(self.conn.get(q))
        if a > 0:
            que = 'DELETE from {} where id = {}'.format(self.table, str(id))
            self.conn.delete(que)
            if len(self.conn.get(q)) == 0:
                return True
        return False

    def getItem(self, id, id_empresa):
        query = {}
        query['colunas'] = 'clientes_cadastros.*'
        query['tabela'] = self.table
        query['join'] = [
            {'tabela': 'empresas', 'where': 'clientes_cadastros.id_empresa = empresas.id', 'tipo': 'INNER'},
        ]
        d = datetime.datetime.now().strftime('%Y-%m-%d')
        now = datetime.datetime.now()
        t = datetime.datetime.timestamp(now)
        query['where'] = [
            {'tipo': 'where', 'campo': 'clientes_cadastros.id', 'valor': id},
            {'tipo': 'where', 'campo': 'clientes_cadastros.id_empresa', 'valor': id_empresa},
        ]
        q = self.query.get(query)
        itens = self.conn.get(q)
        # todo
        # Retornar todos os itens, quando estiver com o model correspondente criado
        return itens

    def getItens(self, data):
        query = {}
        query['colunas'] = 'clientes_cadastros.*'
        query['tabela'] = self.table
        query['join'] = [
            {'tabela': 'empresas', 'where': 'clientes_cadastros.id_empresa = empresas.id', 'tipo': 'INNER'},
        ]
        query['offset'] = 0
        query['limit'] = 10
        print(data)
        if 'offset' in data:
            query['offset'] = data['offset']
            del data['offset']
        if 'limit' in data:
            query['limit'] = data['limit']
            del data['limit']
        query['where'] = self.query.getFiltro(data, self.filtros)
        if 'id_empresa' not in data:
            message = 'O campo id_empresa é obrigatório.'
            erro = {
                'formato': 'geral',
                'arquivo': 'log',
                'data': {
                    'data': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'message': message
                }
            }
            Logs(erro)
            raise RequestIncompleto(message)
        query['group'] = 'clientes_cadastros.id'
        query['ordem'] = 'clientes_cadastros.id DESC'
        q = self.query.get(query)
        itens = {}
        itens['itens'] = self.conn.get(q)
        itens['total'] = 0
        if len(itens['itens']):
            itens['total'] = self.getTotalItens(query['where'])
        return itens

    def getTotalItens(self, where):
        query = {}
        query['colunas'] = 'count(clientes_cadastros.id) as qtde'
        query['tabela'] = self.table
        query['join'] = [
            {'tabela': 'empresas', 'where': 'clientes_cadastros.id_empresa = empresas.id', 'tipo': 'INNER'},
        ]
        query['where'] = where
        query['group'] = 'clientes_cadastros.id_empresa'
        q = self.query.get(query)
        itens = self.conn.get(q)
        return itens[0]['qtde']

    filtros = {
        'id_empresa': {'tipo': 'where', 'campo': 'empresas.id'},
        'id': {'tipo': 'where', 'campo': 'clientes_cadastros.id'},
    }


if __name__ == '__main__':
    print('')

