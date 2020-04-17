from library.myMysql import myMysql
from library.myQuery import myQuery


class cadastrosModel(object):

    def __init__(self):
        self.conn = myMysql()
        self.query = myQuery()

    def add(self, data):
        count = 0
        keys = '('
        values = '('
        for k, v in data.items():
            if count > 0:
                keys += ', '
                values += ', '
            keys += str(k)
            values += '"' + str(v) + '"'
            count += 1
        keys += ')'
        values += ')'
        query = 'INSERT INTO cadastros {} VALUES {}'.format(keys, values)
        return self.conn.add(query)

    def update_id(self, data, id):
        if isinstance(data, str):
            valor = data
        else:
            valor = ''
            count = 0
            for k, v in data.items():
                if count > 0:
                    valor += ', '
                valor += k + '= "' + str(v) + '"'
        qu = 'UPDATE cadastros set {} where id = {}'.format(valor, str(id))
        return self.conn.update(qu)

    def delete_id(self, id):
        q = 'SELECT id from cadastros where id = {} '.format(str(id))
        a = len(self.conn.get(q))
        if a > 0:
            que = 'DELETE from cadastros where id = {}'.format(str(id))
            self.conn.delete(que)
            if len(self.conn.get(q)) == 0:
                return True
        return False
