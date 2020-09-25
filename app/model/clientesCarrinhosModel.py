from library.myMysql import myMysql
from library.myQuery import myQuery
import datetime
import sys

from library.Exception import RequestIncompleto
from library.Logs import Logs


class clientesCarrinhosModel(object):

    def __init__(self):
        self.conn = myMysql()
        self.query = myQuery()
        self.table = 'clientes_carrinhos'

    def add(self, data):
        query = self.query.add(self.table,data)
        return self.conn.add(query)

    def update_id(self, data, id):
        query = self.query.update(self.table, data, id)
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
        query['colunas'] = 'clientes_carrinhos.*, clientes_carrinhos_status.titulo as status'
        query['tabela'] = self.table
        query['join'] = [
            {'tabela': 'clientes_cadastros', 'where': 'clientes_carrinhos.id_clientes_cadastros = clientes_cadastros.id', 'tipo': 'INNER'},
            {'tabela': 'clientes_carrinhos_status',
             'where': 'clientes_carrinhos_status.id = clientes_carrinhos.id_status', 'tipo': 'INNER'},
            {'tabela': 'empresas', 'where': 'clientes_cadastros.id_empresa = empresas.id', 'tipo': 'INNER'},
        ]
        d = datetime.datetime.now().strftime('%Y-%m-%d')
        now = datetime.datetime.now()
        t = datetime.datetime.timestamp(now)
        query['where'] = [
            {'tipo': 'where', 'campo': 'clientes_carrinhos.id', 'valor': id},
            {'tipo': 'where', 'campo': 'clientes_cadastros.id_empresa', 'valor': id_empresa},
        ]
        q = self.query.get(query)
        itens = self.conn.get(q)
        # todo
        # Retornar todos os itens, quando estiver com o model correspondente criado
        return itens



    def getItens(self, data):
        query = {}
        query['colunas'] = 'clientes_carrinhos.*' \
                           ', status_geral.titulo as status' \
                           ', status_geral.complemento as status_complemento' \
                           ', status_pagamento.titulo as status_pagamento' \
                           ', status_pagamento.complemento as status_pagamento_complemento' \
                           ', status_envio.titulo as status_envio' \
                           ', status_envio.complemento as status_envio_complemento'
        query['tabela'] = self.table
        query['join'] = [
            {'tabela': 'clientes_cadastros', 'where': 'clientes_carrinhos.id_clientes_cadastros = clientes_cadastros.id',
             'tipo': 'INNER'},
            {'tabela': 'clientes_carrinhos_status status_geral',
             'where': 'status_geral.id = clientes_carrinhos.id_status', 'tipo': 'INNER'},
            {'tabela': 'clientes_carrinhos_status status_pagamento',
             'where': 'status_pagamento.id = clientes_carrinhos.id_status_pagamento', 'tipo': 'INNER'},
            {'tabela': 'clientes_carrinhos_status status_envio',
             'where': 'status_envio.id = clientes_carrinhos.id_status_envio', 'tipo': 'INNER'},
            {'tabela': 'empresas', 'where': 'clientes_cadastros.id_empresa = empresas.id', 'tipo': 'INNER'},
        ]
        query['offset'] = 0
        query['limit'] = 10
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
        query['group'] = 'clientes_carrinhos.id'
        query['ordem'] = 'clientes_carrinhos.id DESC'
        q = self.query.get(query)
        itens = {}
        itens['itens'] = self.conn.get(q)
        itens['total'] = 0
        if len(itens['itens']):
            itens['total'] = self.getTotalItens(query['where'])
        return itens

    def getTotalItens(self, where):
        query = {}
        query['colunas'] = 'count(clientes_carrinhos.id) as qtde'
        query['tabela'] = self.table
        query['join'] = [
            {'tabela': 'clientes_cadastros',
             'where': 'clientes_carrinhos.id_clientes_cadastros = clientes_cadastros.id',
             'tipo': 'INNER'},
            {'tabela': 'clientes_carrinhos_status',
             'where': 'clientes_carrinhos_status.id = clientes_carrinhos.id_status', 'tipo': 'INNER'},
            {'tabela': 'empresas', 'where': 'clientes_cadastros.id_empresa = empresas.id', 'tipo': 'INNER'},
        ]
        query['where'] = where
        query['group'] = 'clientes_cadastros.id_empresa'
        q = self.query.get(query)
        itens = self.conn.get(q)
        return itens[0]['qtde']

    filtros = {
        'id_empresa': {'tipo': 'where', 'campo': 'empresas.id'},
        'id': {'tipo': 'where', 'campo': 'clientes_carrinhos.id'},
    }




if __name__ == '__main__':
    print('')

