#!/usr/bin/python3

import json
import sys
sys.path.append('../library')
sys.path.append('../controller')
sys.path.append('../model')
from model.imoveisModel import imoveisModel
from model.imoveisMongo import imoveisMongo

from controller.Log_pesquisas import Log_pesquisas

from library.myMongo import myMongo
from flask import request
import time
import datetime
from jwcrypto import jwt,jwk


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
        retorno['qtde_total'] = self.myMongo.get_total_itens('imoveis', pesquisa)
        retorno['titulo'] = self.getTitulo(pesquisa)
        retorno['itens'] = self.myMongo.get_itens('imoveis',pesquisa)
        return retorno

    # array com ['limit', ''skip', coluna, ordem]
    #
    #
    def mongoGetIds(self):
        get_id = request.args['ids']
        retorno = []
        if get_id:
            ids = get_id.split(',')
            data = {}
            data['where'] = {'id': {'$in': ids}}
            retorno = self.getCamposLista(self.myMongo.get_itens('imoveis', data))
        return retorno

    # array com ['limit', ''skip', coluna, ordem]
    #
    #
    def mongoGetQtde(self, data):
        retorno = {}
        pesquisa = self.setDataPesquisa(data)
        print(pesquisa)
        retorno['qtde_total'] = self.myMongo.get_total_itens('imoveis', pesquisa)
        return retorno

    # array com ['limit', ''skip', coluna, ordem]
    #
    #
    def mongoGetTituloQtde(self, data, key):
        retorno = {}
        pesquisa = self.setDataPesquisa(data)
        retorno['qtde_total'] = self.myMongo.get_total_itens('imoveis', pesquisa)
        retorno['titulo'] = self.getTitulo(pesquisa)
        retorno['parametros'] = self.retornaParametros(pesquisa['where'])
        retorno['uri'] = self.retornaURI(pesquisa['where'])
        retorno['itens'] = self.getCamposLista(self.myMongo.get_itens('imoveis', pesquisa))
        self.setLogPesquisa(retorno['parametros'],  key)
        return retorno

    # array com ['limit', ''skip', coluna, ordem]
    #
    #
    def mongoGetURL(self, data, key):
        retorno = {}
        pesquisa = self.setDataPesquisa(data)
        retorno['parametros'] = self.retornaParametros(pesquisa['where'])
        retorno['uri'] = self.retornaURI(pesquisa['where'])
        self.setLogPesquisa(retorno['parametros'], key)
        return retorno

    def setLogPesquisa(self, pesquisa, key):
        token = request.headers['authorization'].replace('Bearer ', '').strip()
        ET = jwt.JWT(key=key, jwt=token)
        info = json.loads(ET.claims)
        data_p = {'usuario_portal': info['id'],
                  'ip': request.remote_addr,
                  'host': request.headers['origin'],
                  'date': datetime.datetime.now()
                  }
        log = Log_pesquisas()
        log.add(data_p,pesquisa)
        return True




    def retornaURI(self,data):
        retorno = 'imoveis'
        if 'imoveis_tipos_link' in data:
            if '$in' in data['imoveis_tipos_link']:
                retorno = '+'.join(data['imoveis_tipos_link']['$in'])
            else:
                retorno = data['imoveis_tipos_link']
        retorno += '-'
        if 'tipo_negocio' in data:
            retorno += data['tipo_negocio']
        else:
            retorno += 'venda'
        retorno += '-'
        if 'cidade_link' in data:
            retorno += data['cidade_link']
        else:
            retorno += 'sao_jose_dos_pinhais_pr'
        if 'bairros_link' in data:
            retorno += '-'
            if '$in' in data['bairros_link']:
                retorno += '+'.join(data['bairros_link']['$in'])
            else:
                retorno += data['bairros_link']
        return retorno

    def retornaParametros(self, where):
        retorno = {}
        for chave,valor in where.items():
            if chave == 'tem_foto':
                pass
            else:
                if isinstance(valor, int):
                    retorno[chave] = valor
                elif '$in' in valor:
                    retorno[chave] = valor['$in']
                elif '$gte' in valor and '$lte' in valor:
                    retorno[chave] = [valor['$gte'], valor['$lte']]
                elif '$gte' in valor:
                    retorno[chave] = valor['$gte']
                elif '$lte' in valor:
                    retorno[chave] = valor['$lte']
                else:
                    retorno[chave] = valor
        return retorno

    camposLista = [
        "_id",
        "area",
        "area_terreno",
        "area_util",
        "bairro",
        "bairros_link",
        "banheiros",
        "cidade",
        "cidade_link",
        "descricao",
        "estado",
        "garagens",
        "id_empresa",
        "imobiliaria_nome",
        "imobiliaria_whatsapp",
        "imobiliaria_telefone",
        "imobiliaria_nome_seo",
        "imoveis_tipos_link",
        "imoveis_tipos_titulo",
        "imovel_para",
        "latitude",
        "longitude",
        "location",
        "logo",
        "logradouro",
        "nome",
        "preco",
        "preco_locacao",
        "preco_locacao_dia",
        "preco_venda",
        "quartos",
        "referencia",
        "tipo_negocio",
        "uf"
    ]

    def getCamposLista(self,imoveis):
        retorno = []
        qtdeimoveis = 0
        for imovel in imoveis['itens']:
            i = {}
            for campo in self.camposLista:
                i[campo] = imovel[campo]
            qtdeimages = 0
            i['images'] = []
            for images in imovel['images']:
                # if qtdeimages < 3:
                im = {'arquivo': images['arquivo'],'titulo':images['titulo']}
                i['images'].append(im)
                # qtdeimages = qtdeimages + 1
            retorno.append(i)
            qtdeimoveis = qtdeimoveis + 1
        return retorno



    def getTitulo(self,pesquisa):
        titulo = 'Imóveis '
        if 'imoveis_tipos_link' in self.pesquisados:
            titulo = self.pesquisados['imoveis_tipos_link']['plural']
        elif 'imoveis_tipos_link' in pesquisa['where']:
            if '$in' in pesquisa['where']['imoveis_tipos_link']:
                tipos = []
                for tipo_link in pesquisa['where']['imoveis_tipos_link']['$in']:
                    tipo = self.getTipo(tipo_link)
                    tipos.append(tipo['plural'])
                titulo = ', '.join(tipos)
            else:
                tipo = self.getTipo(pesquisa['where']['imoveis_tipos_link'])
                titulo = tipo['plural']
        if 'tipo_negocio' in pesquisa['where']:
            tipo_negocio = self.getTipoNegocio(pesquisa['where']['tipo_negocio'])
            titulo += tipo_negocio['titulo']
        if 'bairros_link' in pesquisa['where'] and 'cidade_link' in pesquisa['where']:
            if '$in' in pesquisa['where']['bairros_link']:
                titulo += ' no '
                chave = 0
                for bairro in pesquisa['where']['bairros_link']['$in']:
                    bairroItem = self.getBairro(bairro, pesquisa['where']['cidade_link'])
                    if bairroItem:
                        if chave:
                            titulo += ', ' + bairroItem['nome']
                        else:
                            titulo += bairroItem['nome']

                    chave = chave + 1
            else:
                bairroItem = self.getBairro(pesquisa['where']['bairros_link'], pesquisa['where']['cidade_link'])
                titulo += ' no ' + bairroItem['nome']
        if 'cidade_link' in self.pesquisados:
            titulo += ' em ' + self.pesquisados['cidade_link']['nome'] + ', ' + self.pesquisados['cidade_link']['estado']
        elif 'cidade_link' in pesquisa['where']:
            cidade = self.getCidade(pesquisa['where']['cidade_link'])
            titulo += ' em ' + cidade['nome'] + ', ' + cidade['estado']
        if 'quartos' in pesquisa['where'] or 'banheiros' in pesquisa['where'] or 'garagens' in pesquisa['where']:
            titulo += ', com'
            if 'quartos' in pesquisa['where']:
                titulo += ' + de ' + str(pesquisa['where']['quartos']['$gte']) + ' quarto' + ( '' if pesquisa['where']['quartos']['$gte'] == 1 else 's')
            if 'banheiros' in pesquisa['where']:
                titulo += ' + de ' + str(pesquisa['where']['banheiros']['$gte']) + ' banheiro' + ( '' if pesquisa['where']['banheiros']['$gte'] == 1 else 's')
            if 'garagem' in pesquisa['where']:
                titulo += ' + de ' + str(pesquisa['where']['garagem']['$gte']) + ' vaga' + ( '' if pesquisa['where']['garagem']['$gte'] == 1 else 's') + ' de garagem'
        return titulo

    pesquisados = {}

    def setDataPesquisa(self,data):
        args = {}
        for k,v in data.items():
            args[k] = v
        retorno = {}
        url = {}
        if 'url' in args:
            url = self.trataUrl(args)
            del args['url']
        retorno['limit'] = 6
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
        if len(args) > 0 or url:
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

    isfloat = ['preco_venda','preco_locacao', 'area_util']
    isint = ['quartos', 'garagem', 'garagens', 'banheiros', 'id_tipo', 'cidades_id']
    ismaior = ['quartos', 'vagas', 'banheiros', 'garagem']
    isvalor = ['preco_venda','preco_locacao', 'area_util']
    valoresMaximos = {
        "preco_venda": 50000000,
        "preco_locacao": 50000,
        "area_util": 50000
    }

    def getWhere(self,itens, url):
        retorno = {}
        for chave,valor in itens.items():
            if chave in url:
                v, isin = self.getItemVirgula(url[chave], False)
                retorno[chave] = v
                if isin:
                    retorno[chave] = {'$in': v}
                del url[chave]
            else:
                if chave in self.isint:
                    v,isin = self.getItemVirgula(valor,'int')
                else:
                    v,isin = self.getItemVirgula(valor,False)
                retorno[chave] = v
                if isin:
                    if chave in self.isvalor:
                        retorno[chave] = {}
                        retorno[chave]['$gte'] =  int(v[0])
                        if self.valoresMaximos[chave] != int(v[1]):
                            retorno[chave]['$lte'] = int(v[1])
                    else:
                        retorno[chave] = {'$in':v}
                elif chave in self.ismaior:
                    retorno[chave] = {'$gte': v}

        for k,va in url.items():
            v, isin = self.getItemVirgula(va, False)
            retorno[k] = v
            if isin:
                retorno[k] = {'$in': v}
            else:
                retorno[k] = v
        if 'localhost' in sys.argv:
            retorno['tem_foto'] = True
        print(retorno)
        return retorno

    def trataUrl(self, data):
        url = data['url'].split('-')
        retorno = {}
        if len(url):
            for item in url:
                if 'imoveis_tipos_link' not in retorno:
                    if ' ' in item:
                        array = item.split(' ')
                        t = []
                        tipo = False
                        for a in array:
                            e = self.getTipo(a)
                            if e:
                                tipo = True
                        if tipo:
                            retorno['imoveis_tipos_link'] = item.replace(' ',',')
                    else:
                        tipo = self.getTipo(item)
                        if tipo:
                            self.pesquisados['imoveis_tipos_link'] = tipo
                            retorno['imoveis_tipos_link'] = item
                if 'tipo_negocio' not in retorno:
                    tipo_negocio = self.getTipoNegocio(item)
                    if tipo_negocio:
                        self.pesquisados['tipo_negocio'] = tipo_negocio
                        retorno['tipo_negocio'] = item
                if 'cidade_link' not in retorno:
                    cidade = self.getCidade(item)
                    if cidade:
                        self.pesquisados['cidade_link'] = cidade
                        retorno['cidade_link'] = item
                if 'bairros_link' not in retorno:
                    if 'cidade_link' in retorno:
                        if ' ' in item:
                            array = item.split(' ')
                            t = []
                            bairro = False
                            for a in array:
                                e = self.getBairro(a, retorno['cidade_link'])
                                if e:
                                    bairro = True
                            if bairro:
                                retorno['bairros_link'] = item.replace(' ',',')
                        else:
                            bairro = self.getBairro(item, retorno['cidade_link'])
                            if bairro:
                                self.pesquisados['bairros_link'] = bairro
                                retorno['bairros_link'] = item
        print('trataurl')
        print(retorno)
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

    def getTipo(self,data):
        return self.set_tipos(data)


    def getTipoNegocio(self,data):
        tipo_negocio = {
            'venda': {'id': 'venda', 'descricao': 'Venda','titulo': ' a venda'},
            'locacao': {'id': 'locacao', 'descricao': 'Aluguel','titulo': ' para alugar'},
            'locacao_dia': {'id': 'locacao_dia', 'descricao': 'Aluguel dia','titulo': ' para temporada'},
        }
        if data in tipo_negocio:
            return tipo_negocio[data]
        return False

    def getCidade(self,item):
        data = {}
        data = {'link': item};
        retorno = self.myMongo.get_item_filtro('cidades', data)
        if retorno:
            return retorno
        return False

    def getBairro(self,item,cidade):
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
    
