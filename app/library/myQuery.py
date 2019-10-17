#!/usr/bin/python3

class myQuery(object):
    
    def __init__(self):
        self.tipo = 'string'            
    
    def get(self,query):
        retorno = ''
        if isinstance(query,str):
            return query
        else:
            retorno += 'SELECT '
            if 'colunas' in query:
                retorno += query['colunas']
            else:
                retorno += '*'
            if 'tabela' in query:
                retorno += ' FROM ' + query['tabela']
            else:
                return False
            if 'join' in query:
                for join in query['join']:
                    retorno += ' ' + join['tipo'] + ' JOIN ' + join['tabela'] + ' ON ' + join['where']
            retorno += self.getWhere(query)
            if 'group' in query:
                retorno += ' GROUP BY ' + query['group']
            if 'ordem' in query:
                retorno += ' ORDER BY ' + query['ordem']
            if 'limit' in query:
                retorno += ' LIMIT' 
                if 'offset' in query:
                    retorno += ' ' + str(query['offset']) + ','
                retorno += ' ' + str(query['limit'])
            return retorno
    
    # Tipo de where
    # where, where_or, where_in, where_not_in, where_gt, where_gte, where_lt, where_lte,like, like_or
    def getWhere(self,query):
        retorno = ''
        if 'where'in query:
            retorno += ' WHERE '
            if isinstance(query['where'],str):
                retorno += query['where']
            else:
                count_where = 0
                for where in query['where']:
                    if isinstance(where,str):
                        if count_where > 0:
                            retorno += ' AND '
                        retorno += where
                    else:
                        if count_where > 0:
                            if where['tipo'].find('or') >= 0:
                                retorno += ' OR '
                            else:
                                retorno += ' AND '
                        if where['tipo'].find('like') >= 0:
                            retorno += where['campo'] + ' LIKE "' + where['valor'] + '"'
                        elif 'where' in where['tipo']:
                            if 'not_in' in where['tipo']:
                                retorno += where['campo'] + ' NOT IN (' + ','.join(map(str, where['valor'])) + ')'
                            elif 'in' in where['tipo']:
                                retorno += where['campo'] + ' IN (' + ','.join(map(str, where['valor'])) + ')'
                            elif 'gte' in where['tipo']:
                                retorno += where['campo'] + ' >= ' + where['valor']
                            elif 'gt' in where['tipo']:
                                retorno += where['campo'] + ' > ' + where['valor']
                            elif 'lte' in where['tipo']:
                                retorno += where['campo'] + ' <= ' + where['valor']
                            elif 'lt' in where['tipo']:
                                retorno += where['campo'] + ' < ' + where['valor']
                            elif 'not' in where['tipo']:
                                retorno += where['campo'] + ' NOT ' + where['valor']
                            else:
                                if isinstance(where['valor'],str):
                                    retorno += where['campo'] + ' = "' + where['valor'] + '"'
                                else:
                                    retorno += where['campo'] + ' = ' + where['valor']
                    count_where += 1
        return retorno

if __name__ == '__main__':
    try:
        a = myQuery()
        query = {}
        query['colunas'] = 'imoveis.*'
        query['tabela'] = 'imoveis'
        query['join'] = [{'tabela':'empresas','where':'imoveis.id_empresa = empresas.id','tipo':'INNER'},{'tabela':'imoveis_tipos','where':'imoveis.id_tipo = imoveis_tipos.id','tipo':'LEFT'}]
        query['where'] = [{'tipo':'like','campo':'imoveis.id_tipo','valor':'1'},{'tipo':'where_or','campo':'imoveis.id_tipo','valor':'2'}]
        query['ordem'] = 'imoveis.id desc'
        query['offset'] = 0
        query['limit'] = 10
        
        b = a.get(query)
        print(b)
    except KeyboardInterrupt:
        pass
    finally:
        pass        

    
     
    