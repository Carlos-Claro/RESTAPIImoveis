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

class Log(object):
    
    def __init__(self):
        self.myMongo = myMongo('imoveis')

    def mongoGetLogEmpresaDia(self):
        data_i = request.args['data_inicio']
        d_i = data_i.split('-')
        data_f = request.args['data_fim']
        d_f = data_f.split('-')
        id_empresa = request.args['id_empresa']
        data = {}
        data['where'] = {'id_empresa': int(id_empresa),"data":
            {
                    "$gte":datetime.datetime(d_i[0],d_i[1],d_i[2],0,0),
                    "$lte":datetime.datetime(d_f[0],d_f[1],d_f[2],23,59)} 
            }
        data['sort'] = {'data':0}
        return self.myMongo.get_itens('log_empresas_dia',data)

    
    def mongoGetLogEmpresaData(self):
        dias = request.args['dias']
        da = datetime.datetime.now() - datetime.timedelta(days=int(dias))
        y = int(da.strftime('%Y'))
        m = int(da.strftime('%m'))
        d = int(da.strftime('%d'))
        pipeline = [
                {"$match":{"data":{"$gte":datetime.datetime(y,m,d,0,0),"$lte":datetime.datetime(y,m,d,23,59)}}},
                {"$group":{"_id":"$id_empresa","acesso":{"$sum":1}}}
                ]
        res = self.myMongo.aggregate(pipeline,'log_imoveis')
        res_p = self.myMongo.aggregate(pipeline,'log_portal')
        empresas = self.set_soma_dbs_int(res['itens'],res_p['itens'])
        retorno = {}
        for chave,valor in empresas.items():
            retorno[chave] = {}
            retorno[chave]['total_empresa'] = valor
            p2 = [
                {"$match":{"data":{"$gte":datetime.datetime(y,m,d,0,0),"$lte":datetime.datetime(y,m,d,23,59)},"id_empresa":chave}},
                {"$group":{"_id":"$tipo","acesso":{"$sum":1}}}
                    ]
            res2 = self.myMongo.aggregate(p2,'log_imoveis')
            res2_p = self.myMongo.aggregate(p2,'log_portal')
            tipos = self.set_soma_dbs_char(res2['itens'],res2_p['itens'])
            for chave_tipo,valor_tipo in tipos.items():
                p3 = [
                    {"$match":{"data":{"$gte":datetime.datetime(y,m,d,0,0),"$lte":datetime.datetime(y,m,d,23,59)},"id_empresa":chave,"tipo":chave_tipo}},
                    {"$group":{"_id":"$id_imovel","acesso":{"$sum":1}}}
                        ]
                res3 = self.myMongo.aggregate(p3,'log_imoveis')
                res3_p = self.myMongo.aggregate(p3,'log_portal')
                imoveis = self.set_soma_dbs_char(res3['itens'],res3_p['itens'])
                lista = []
                for id_imovel,valor_imovel in imoveis.items():
                    lista.append({id_imovel:valor_imovel})
                retorno[chave][chave_tipo] = {'total': valor_tipo,'imoveis':lista}
                del lista
        return retorno
    
    def mongoGetLogImoveisData(self):
        dias = request.args['dias']
        da = datetime.datetime.now() - datetime.timedelta(days=int(dias))
        y = int(da.strftime('%Y'))
        m = int(da.strftime('%m'))
        d = int(da.strftime('%d'))
        pipeline = [
                {"$match":{"data":{"$gte":datetime.datetime(y,m,d,0,0),"$lte":datetime.datetime(y,m,d,23,59)}}},
                {"$group":{"_id":"$id_imovel","acesso":{"$sum":1}}}
                ]
        res = self.myMongo.aggregate(pipeline,'log_imoveis')
        res_p = self.myMongo.aggregate(pipeline,'log_portal')
        imoveis = self.set_soma_dbs_int(res['itens'],res_p['itens'])
        return imoveis
        
    def mongoGetLogImoveisItem(self):
        dias = request.args['dias']
        da = datetime.datetime.now() - datetime.timedelta(days=int(dias))
        y = int(da.strftime('%Y'))
        m = int(da.strftime('%m'))
        d = int(da.strftime('%d'))
        id_imovel = request.args['id_imovel']
        retorno = {}
        p2 = [
            {"$match":{"data":{"$gte":datetime.datetime(y,m,d,0,0),"$lte":datetime.datetime(y,m,d,23,59)},"id_imovel":int(id_imovel)}},
            {"$group":{"_id":"$tipo","acesso":{"$sum":1}}}
            ]
        res2 = self.myMongo.aggregate(p2,'log_imoveis')
        res2_p = self.myMongo.aggregate(p2,'log_portal')
        tipos = self.set_soma_dbs_char(res2['itens'],res2_p['itens'])
        for chave_tipo,valor_tipo in tipos.items():
            retorno[chave_tipo] = valor_tipo
        return retorno
    
    def set_soma_dbs_int(self,imoveis,portal):
        retorno = {}
        for i in imoveis:
            if i['_id'] is not None and i['_id'] > 0:
                retorno[int(i['_id'])] = i['acesso']
        for p in portal:
            if p['_id'] is not None and p['_id'] > 0:
                c = int(p['_id'])
                if c in retorno:
                    retorno[c] = retorno[c] + p['acesso']
                else:
                    retorno[c] = p['acesso']
        return retorno
    
    def set_soma_dbs_char(self,imoveis,portal):
        retorno = {}
        for i in imoveis:
            if i['_id'] is not None:
                retorno[i['_id']] = i['acesso']
        for p in portal:
            if p['_id'] is not None:
                if p['_id'] in retorno:
                    retorno[p['_id']] = retorno[p['_id']] + p['acesso']
                else:
                    retorno[p['_id']] = p['acesso']
        return retorno
    
    def mongoGetLogImoveisTipo(self):
        dias = request.args['dias']
        imovel = request.args['imovel']
        da = datetime.datetime.now() - datetime.timedelta(days=int(dias))
        y = int(da.strftime('%Y'))
        m = int(da.strftime('%m'))
        d = int(da.strftime('%d'))
        pipeline = [
                {"$match":{"data":{"$gte":datetime.datetime(y,m,d,0,0),"$lte":datetime.datetime(y,m,d,23,59)},"id_imovel":imovel}},
                {"$group":{"_id":"$tipo","acesso":{"$sum":1}}}
                ]
        return self.myMongo.aggregate(pipeline,'log_imoveis')
    
    def mongoGetLogEmpresaMinData(self):
        pipeline = [
                {"$group":{"_id":{},"data":{"$min":'$data'}}}
                ]
        return self.myMongo.aggregate(pipeline,'log_empresas_dia')
    
    
    def mongoGetLogEmpresaMaxData(self):
        pipeline = [
                {"$group":{"_id":{},"data":{"$max":'$data'}}}
                ]
        return self.myMongo.aggregate(pipeline,'log_empresas_dia')
    
    def mongoGetLogImovelMinData(self):
        pipeline = [
                {"$group":{"_id":{},"data":{"$min":'$data'}}}
                ]
        return self.myMongo.aggregate(pipeline,'log_imoveis_dia')
    
    
    def mongoGetLogImovelMaxData(self):
        pipeline = [
                {"$group":{"_id":{},"data":{"$max":'$data'}}}
                ]
        return self.myMongo.aggregate(pipeline,'log_imoveis_dia')
    
    def add_log_empresa_dia(self):
        args = json.loads(request.get_json())
        data = args['data']
        del args['data']
        args['data'] = datetime.datetime(int(data[0]),int(data[1]),int(data[2]),0,0)
        return {'ok':self.myMongo.add_one('log_empresas_dia',args)}
    
    def add_log_imovel_dia(self):
        args = json.loads(request.get_json())
        data = args['data']
        del args['data']
        args['data'] = datetime.datetime(int(data[0]),int(data[1]),int(data[2]),0,0)
        return {'ok':self.myMongo.add_one('log_imoveis_dia',args)}
    
if __name__ == '__main__':
    Imoveis.get()
    