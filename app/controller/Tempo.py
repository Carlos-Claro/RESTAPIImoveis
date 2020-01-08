#!/usr/bin/python3

import json
import sys
sys.path.append('../library')
sys.path.append('../controller')
sys.path.append('../model')
from library.myMongo import myMongo
from flask import request
import time
import datetime

class Tempo(object):
    
    def __init__(self):
        self.myMongo = myMongo('carlos')

    def mongoGetTempo(self):
        dias = request.args['dias']
        da = datetime.datetime.now() - datetime.timedelta(days=int(dias))
        y = int(da.strftime('%Y'))
        m = int(da.strftime('%m'))
        d = int(da.strftime('%d'))
        empresa = request.args['id_empresa']
        data = {}
        data['where'] = {'id_empresa': int(empresa),"data":
                {
                        "$gte":datetime.datetime(y,m,d,0,0),
                }
            }
        data['sort'] = {'data':0}
        itens = self.myMongo.get_itens('log_empresas_dia',data)
        retorno = {}
        retorno['qtde'] = itens['qtde']
        retorno['itens'] = []
        retorno['totais'] = {}
        for valor in itens['itens']:
            valor_a = {}
            for c,v in valor.items():
                if 'data' in c:
                    valor_a[c] = v.strftime('%Y-%m-%d')
                elif '_id' in c:
                    pass
                else:
                    valor_a[c] = v
                    if c not in self.lista_negativa:
                        if c in retorno['totais']:
                            retorno['totais'][c] = retorno['totais'][c] + v['total']
                        else:
                            retorno['totais'][c] = v['total']
            retorno['itens'].append(valor_a)
            del valor_a
        return retorno

    lista_negativa = ['id_empresa','total_acessos']
    
    def add_tempo(self):
        args = request.get_json()
        print(args['dht11']['temperatura'])
        args['data'] = datetime.datetime.now() 
        return {'ok':self.myMongo.add_one('tempo_malhada',args)}
    
    
if __name__ == '__main__':
    Tempo.get()
    