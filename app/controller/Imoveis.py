#!/usr/bin/python3

import json
import sys
sys.path.append('../library')
sys.path.append('../controller')
sys.path.append('../model')
from model.imoveisModel import imoveisModel
from model.imoveisMongo import imoveisMongo
from library.myMongo import myMongo
from flask import request
import time
import datetime

class Imoveis(object):

    def __init__(self):
        self.imoveisModel = imoveisModel()
        self.imoveisMongo = imoveisMongo()
        self.myMongo = myMongo('imoveis')

    def add(self):
        return {'id': self.imoveisModel.add(request.args)}

    def add_test(self,data):
        return {'id': self.imoveisModel.add(data)}


    def update(self,id):
        return {'qtde': self.imoveisModel.update_id(request.args,id)}

    def update_test(self,id,data):
        return {'qtde': self.imoveisModel.update_id(data,id)}

    def delete(self,id):
        return {'qtde':self.imoveisModel.delete_id(id)}

    def get(self):
        return self.imoveisModel.getItens_integra({'limit':10})

    def get_in(self,id_empresa):
        get = request.args['id']
        a = json.loads(get);
        ids = []
        for i in a:
            ids.append(i)
        data = {}
        # print(ids)
        data['where'] = {'id_' : {'$in':ids}, 'id_empresa':str(id_empresa), 'cidades_id': {'$in': ['9730', '2', '10', '4', '5', '27','1']} }
        value = self.myMongo.get_itens('imoveis',data)
        # print(value)
        if len(ids) == value['qtde'] :
            res = {'deleta':False}
        else:
            if value['qtde'] == 0:
                res = {'deleta':True, 'todos':True}
            else:
                res = {'deleta':True, 'ids':[]}
                for item in value['itens']:
                    res['ids'].append(item['id'])
        return res

    def get_id_cidade(self,id_):
        data = {}
        data['where'] = {'id' : id_, 'cidades_id': {'$in': ['9730', '2', '10', '4', '5', '27','1']} }
        value = self.myMongo.get_itens('imoveis',data)
        if value['qtde'] == 0 :
            return False
        else:
            return value['itens']

    def get_ativos(self):
        data = {}
        data['limit'] = request.args['limit']
        value = self.imoveisModel.getItens_integra(data)
        if value['qtde'] == 0 :
            return False
        else:
            return value['itens']


    def get_id(self,id):
        return self.imoveisModel.getItem(id)

    def get_images_id_empresa(self,id):
        return self.imoveisModel.getImagesIDempresa(id)

    def add_images_imovel(self):
        return {'id':self.imoveisModel.getImagesIDimovel(request.args)}

    def add_images_imovel_test(self,data):
        return {'id':self.imoveisModel.add_images(data)}

    def update_images_id(self,id):
        return {'qtde':self.imoveisModel.update_images_id(request.args,id)}

    def update_images_id_imovel(self,id):
        return {'qtde':self.imoveisModel.update_images_id_imovel(request.args,id)}

    def update_images(self):
        retorno = 0
        data = request.args
        id = data['id']
        i = self.imoveisModel.update_images_id(data,id)
        return {'qtde':i}

    def update_images_id_test(self,id,data):
        return {'qtde':self.imoveisModel.update_images_id(data,id)}

    def delete_images_id(self,id):
        return {'qtde':self.imoveisModel.delete_images_id(id)}

    def delete_images_id_imovel(self,id):
        return {'qtde':self.imoveisModel.delete_images_id_imovel(id)}

    def set_args(self,array):
        retorno = {}
        for k,v in array.items():
            retorno[k] = v
        return retorno

    def alteraDatas(self,item):
        retorno = self.set_args(item)
        retorno['data_update'] = datetime.datetime.now()
        return retorno

    def mongoAdd(self):
        data = self.alteraDatas(json.loads(request.json))
        item = self.mongoGetId(data['_id'])
        if item:
            return {'qtde':self.myMongo.update_one('imoveis',{'_id': data['_id']}, data)}
        return {'qtde':self.myMongo.add_one('imoveis',data)}

    def mongoUpdate(self,id,data):
        alt = {}
        for k,v in data.items():
            if 'tem_foto' in k:
                # print('tem_ft')
                alt[k] = bool(v)
            else:
                alt[k] = v
        return {'qtde':self.myMongo.update_one('imoveis',{'_id':int(id)},alt)}

    def mongoDelete(self,id):
        return {'qtde':self.myMongo.delete_one('imoveis',{'_id':int(id)})}


    # array com ['limit', ''skip', coluna, ordem]
    #
    #
    def mongoGet(self, data):
        retorno = {}
        pesquisa = self.setDataPesquisa(data)
        retorno['itens'] = self.myMongo.get_itens('imoveis',pesquisa)
        retorno['qtde_total'] = self.myMongo.get_total_itens('imoveis',pesquisa)
        return retorno

    def setDataPesquisa(self,data):
        args = {}
        for k,v in data.items():
            args[k] = v
        retorno = {}
        url = {}
        if 'url' in args:
            url = self.trataUrl(args)
            del args['url']
        retorno['limit'] = 3
        if 'limit' in args:
            retorno['limit'] = int(args['limit'])
            del args['limit']
        if 'skip' in args:
            retorno['skip'] = int(args['skip'])
            del args['skip']
        retorno['sort'] = {'ordem':-1}
        if 'coluna' in args or 'ordem' in args:
            ordem = self.getOrdenacao(args);
            retorno['sort'] = {ordem[0]:ordem[1]}
            # print(retorno['sort'])
            if 'coluna' in args:
                del args['coluna']
            if 'ordem' in args:
                del args['ordem']
        # print(args)
        if len(args) > 0:
            retorno['where'] = self.getWhere(args, url)
        return retorno

    def getOrdenacao(self,data):
        coluna = 'ordem'
        if data['coluna'] in ['min','max']:
            a = data['coluna'].split('-')
            coluna = a[0]
            if a[1] == 'min':
                ordem = 1
            else:
                ordem = -1
        else:
            coluna = data['coluna']
            ordem = -1
        return [coluna,ordem];

    def getItemVirgula(self,valor,tipo):
        isin = False
        if ',' in valor:
            isin = True
            array = valor.split(',')
            v = []
            for a in array:
                v.append(self.getValorTipo(a,tipo))
        else:
            v = self.getValorTipo(valor,tipo)
        return v,isin

    def getValorTipo(self,valor,tipo):
        if tipo:
            if 'int' in tipo:
                return int(valor)
            return valor
        return valor

    isfloat = []
    isint = ['quartos', 'garagens', 'id_tipo', 'cidades_id']

    def getWhere(self,itens, url):
        retorno = {}
        for chave,valor in itens.items():
            # print(chave)
            if chave in url:
                retorno[chave] = url[chave]
                del url[chave]
            else:
                if chave in self.isint:
                    v,isin = self.getItemVirgula(valor,'int')
                else :
                    v,isin = self.getItemVirgula(valor,False)
                retorno[chave] = v
                if isin:
                    retorno[chave] = {'$in':v}
        for k,v in url.items():
            retorno[k] = v
        # print(retorno)
        return retorno

    def trataUrl(self, data):
        url = data['url'].split('-')
        retorno = {}
        if len(url):
            for item in url:
                print(item)
                if 'imoveis_tipos_link' not in retorno:
                    tipo = self.get_tipo(item)
                    if tipo:
                        retorno['imoveis_tipos_link'] = item
                if 'tipo_negocio' not in retorno:
                    tipo_negocio = self.get_tipo_negocio(item)
                    if tipo_negocio:
                        retorno['tipo_negocio'] = item
                if 'cidades_link' not in retorno:
                    cidade = self.get_cidade(item)
                    if cidade:
                        retorno['cidades_link'] = item
                if 'bairros_link' not in retorno:
                    if 'cidades_link' in retorno:
                        bairro = self.get_bairro(item, retorno['cidades_link'])
                        if bairro:
                            retorno['bairros_link'] = item
        return retorno

    def set_tipos(self, data):
        tipos = {
            "andar":{"id":"andar","descricao":"Andar","plural":"Andares","english":"Floor"},
            "apartamento":{"id":"apartamento","descricao":"Apartamento","plural":"Apartamentos","english":"Apartment"},
            "area":{"id":"area","descricao":"\u00c1rea","plural":"\u00c1reas","english":"Area"},
            "barracao_galpao":{"id":"barracao_galpao","descricao":"Barrac\u00e3o \/ Galp\u00e3o","plural":"Barrac\u00f5es e Galp\u00f5es","english":"Storage"},
            "casa":{"id":"casa","descricao":"Casa","plural":"Casas","english":"House"},
            "conjunto_comercial":{"id":"conjunto_comercial","descricao":"Conjunto Comercial","plural":"Conjuntos Comerciais","english":"Office"},
            "fazenda":{"id":"fazenda","descricao":"Fazenda","plural":"Fazendas","english":"Farm"},
            "flat":{"id":"flat","descricao":"Flat","plural":"Flats","english":"Flat"},
            "garagem":{"id":"garagem","descricao":"Garagem","plural":"Garagens","english":"Garage"},
            "haras":{"id":"haras","descricao":"Haras","plural":"Haras","english":"HorseFarm"},
            "hotel":{"id":"hotel","descricao":"Hotel","plural":"Hoteis","english":"Hotels"},
            "kitinete":{"id":"kitinete","descricao":"Kitinete","plural":"Kitinetes","english":"Studio"},
            "loft":{"id":"loft","descricao":"Loft","plural":"Lofts","english":"Lofts"},
            "loja":{"id":"loja","descricao":"Loja","plural":"Lojas","english":"Retail"},
            "lote_terreno":{"id":"lote_terreno","descricao":"Lote \/ Terreno","plural":"Lotes e Terrenos","english":"Land Lot"},
            "negocio_empresa":{"id":"negocio_empresa","descricao":"Neg\u00f3cio\/ Empresa","plural":"Neg\u00f3cios e Empresas","english":"Business"},
            "outro":{"id":"outro","descricao":"Outro","plural":"Outros","english":"Other"},
            "ponto_comercial":{"id":"ponto_comercial","descricao":"Ponto Comercial","plural":"Pontos Comerciais","english":"Office"},
            "pousada":{"id":"pousada","descricao":"Pousada","plural":"Pousadas","english":"Hostel"},
            "predio":{"id":"predio","descricao":"Pr\u00e9dio","plural":"Pr\u00e9dios","english":"Building"},
            "salao":{"id":"salao","descricao":"Sal\u00e3o","plural":"Sal\u00f5es","english":"Salon"},
            "sitio_chacara":{"id":"sitio_chacara","descricao":"S\u00edtio e Ch\u00e1cara","plural":"Sitios e Ch\u00e1caras","english":"Ranches"},
            "sobrado":{"id":"sobrado","descricao":"Sobrado","plural":"Sobrados","english":"Town home"}
        }
        if data in tipos:
            return tipos[data]
        return False

    def get_tipo(self,data):
        return self.set_tipos(data)


    def get_tipo_negocio(self,data):
        tipo_negocio = {
            'venda': {'id': 'venda', 'descricao': 'Venda'},
            'locacao': {'id': 'locacao', 'descricao': 'Aluguel'},
            'locacao_dia': {'id': 'locacao_dia', 'descricao': 'Aluguel dia'},
        }
        if data in tipo_negocio:
            return tipo_negocio[data]
        return False

    def get_cidade(self,item):
        data = {}
        data = {'link': item};
        retorno = self.myMongo.get_item_filtro('cidades', data)
        if retorno:
            return retorno
        return False

    def get_bairro(self,item,cidade):
        data = {}
        data = {'cidade_link': cidade,'link':item};
        retorno = self.myMongo.get_item_filtro('bairros', data)
        if retorno:
            return retorno
        return False

    def mongoGetId(self,id):
        imoveis = self.myMongo.get_item('imoveis',id)
        return imoveis

    def imagesIDEmpresa(self,idEmpresa):
        return self.imoveisModel.getImagesIDempresaHTTP(idEmpresa)

    def imagesGerar(self,limit):
        return self.imoveisModel.getImagesGerar(limit)

    def imagesGerarMongo(self,limit):
        data = {}
        if 'id_empresa' in request.args :
            data['where'] = {'tem_foto': False, 'cidades_id': {'$in': [9730, 2, 10, 4, 5, 27,1]}, 'id_empresa': request.args['id_empresa']}
        else:
            data['where'] = {'tem_foto': False, 'cidades_id': {'$in': [9730, 2, 10, 4, 5, 27,1]}}

        data['sort'] = {'data_update':0, 'cidades_id': 1, 'ordem':0}
        data['limit'] = int(limit)
        return self.myMongo.get_itens('imoveis',data)
    

if __name__ == '__main__':
    Imoveis.get()
    
