# -*- coding: utf-8 -*-#
from flask import render_template,request,jsonify,send_from_directory
from flask_api import status
import connexion
import sys, os
from flask_cors import CORS
from flask_basicauth import BasicAuth
import json
# from flask_bcrypt import Bcrypt
# from simplecrypt import encrypt, decrypt

sys.path.append('/library')
sys.path.append('/controller')
sys.path.append('/model')
from controller.Imoveis import Imoveis
from controller.Log import Log
from controller.Imoveis_relevancia import Imoveis_relevancia
from controller.Cadastros import Cadastros
from controller.Cidades import Cidades
from controller.Clientes_cadastros import Clientes_cadastros
from controller.Clientes_carrinhos import Clientes_carrinhos
from controller.Clientes_carrinhos_produtos import Clientes_carrinhos_produtos
from controller.Clientes_carrinhos_historico import Clientes_carrinhos_historico
from controller.Contato_site import Contato_site
from controller.Produtos import Produtos

from controller.Tempo import Tempo
from library.Exception import RequestInvalido, RequestIncompleto
from library.Exception import RequestRetornaZeroItens



app = connexion.App(__name__,specification_dir='./')
CORS(app.app, supports_credentials=True)
#app.add_api('swagger.yaml')

endereco = '/var/www/json/keys.json'
if 'programacao' in sys.argv:
    endereco = '/home/www/json/keys.json'
with open(endereco) as json_file:
    data = json.load(json_file)

app.app.config['BASIC_AUTH_USERNAME'] = data['basic']['user']
app.app.config['BASIC_AUTH_PASSWORD'] = data['basic']['passwd']
# app.app.config['BASIC_AUTH_FORCE'] = True
basic_auth = BasicAuth(app.app)

# bcrypt = Bcrypt(app.app)
# pw_hash = bcrypt.generate_password_hash(data['basic']['passwd'])
# print(bcrypt.check_password_hash(pw_hash, data['basic']['passwd'])) # returns True

@app.route('/')
@basic_auth.required
def index():
    status_r = status.HTTP_200_OK
    retorno = {'item':'POW Imoveis API, serve sites e portais imobiliários.'}
    return jsonify(retorno), status_r

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(str(app.root_path), 'images'),'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/imoveis',methods=['GET','POST'])
@basic_auth.required
def imoveis():
    imoveis = Imoveis()
    if request.method == 'GET':
        retorno = imoveis.get()
    elif request.method == 'POST':
        retorno = imoveis.add()
    return jsonify(retorno)

@app.route('/imoveis/<id>',methods=['GET'])
def imoveis_(id):
    retorno = {}
    imoveis = Imoveis()
    if request.method == 'GET':
        retorno = imoveis.get_id(id)
        status_r = status.HTTP_200_OK
        if retorno is False:
            status_r = status.HTTP_403_FORBIDDEN
    return jsonify(retorno), status_r

@app.route('/imoveis_cidade/<id>',methods=['GET'])
def imoveis_cidade(id):
    retorno = {}
    imoveis = Imoveis()
    if request.method == 'GET':
        retorno = imoveis.get_id_cidade(id)
        status_r = status.HTTP_200_OK
        if retorno is False:
            status_r = status.HTTP_403_FORBIDDEN
    return jsonify(retorno), status_r

@app.route('/imoveis_integra/',methods=['GET', 'POST'])
def imoveis_integra():
    retorno = {}
    imoveis = Imoveis()
    if request.method == 'GET':
        retorno = imoveis.get_ativos()
    else:
        retorno = imoveis.mongoAdd()
    status_r = status.HTTP_200_OK
    if retorno is False:
        status_r = status.HTTP_403_FORBIDDEN
    return jsonify(retorno), status_r


@app.route('/imoveis_in/<id>',methods=['GET'])
def imoveis_in(id):
    retorno = {}
    imoveis = Imoveis()
    if request.method == 'GET':
        retorno = imoveis.get_in(id)
    return jsonify(retorno)

@app.route('/imovel/<id>',methods=['PUT','DELETE'])
def imoveis_id(id):
    retorno = {}
    imoveis = Imoveis()
    if request.method == 'PUT':
        retorno = imoveis.update(id)
    elif request.method == 'DELETE':
        retorno = imoveis.delete(id)
    return jsonify(retorno)

@app.route('/imoveis_images/<id_empresa>',methods=['GET'])
def imoveis_images(id_empresa):
    retorno = {}
    imoveis = Imoveis()
    if request.method == 'GET':
        retorno = imoveis.get_images_id_empresa(id_empresa)
    return jsonify(retorno)

@app.route('/imovel_images/<id>',methods=['PUT'])
def imoveis_images_(id):
    retorno = {}
    imoveis = Imoveis()
    retorno = imoveis.update_images_id(id)
    return jsonify(retorno)

@app.route('/imovel_images_imovel/',methods=['PUT'])
def imoveis_images_imovel_():
    retorno = {}
    imoveis = Imoveis()
    retorno = imoveis.update_images()
    return jsonify(retorno)

@app.route('/imovel_images_imovel_/<id_imovel>',methods=['PUT'])
def imoveis_images_imovel(id):
    retorno = {}
    imoveis = Imoveis()
    retorno = imoveis.update_images()
    return jsonify(retorno)

@app.route('/update_imovel_verifica/<id_imovel>',methods=['PUT'])
def update_imoveis_images_imovel(id_imovel):
    retorno = {}
    imoveis = Imoveis()
    retorno = imoveis.update_images_id_imovel(id_imovel)
    return jsonify(retorno)

@app.route('/imovel_images_copy/<id>',methods=['GET'])
def imoveis_images_copy(id):
    retorno = {}
    imoveis = Imoveis()
    return jsonify(imoveis.imagesIDEmpresa(id))

@app.route('/imoveis_images_gerar/<limit>',methods=['GET'])
def imoveis_images_gerar(limit):
    retorno = {}
    imoveis = Imoveis()
    return jsonify(imoveis.imagesGerarMongo(limit))

# @basic_auth.required
@app.route('/imoveismongo',methods=['GET','POST'])
def imoveismongo():
    retorno = {}
    imoveis = Imoveis()
    if request.method == 'GET':
        data = request.args
        retorno = imoveis.mongoGet(data)
    elif request.method == 'POST':
        data = request.args
        retorno = imoveis.add_mongo(data)
    status_r = status.HTTP_200_OK
    if retorno is False:
        status_r = status.HTTP_403_FORBIDDEN
    return jsonify(retorno), status_r

# @basic_auth.required
@app.route('/imoveismongo/<id>',methods=['GET'])
def imoveismongo_(id):
    retorno = {}
    imoveis = Imoveis()
    if request.method == 'GET':
        retorno = imoveis.mongoGetId(id)
    return jsonify(retorno)

@app.route('/imoveismongo/<id>',methods=['PUT','DELETE'])
def imoveismongo_id(id):
    retorno = {}
    imoveis = Imoveis()
    if request.method == 'PUT':
        retorno = imoveis.mongoUpdate(id, request.args)
    elif request.method == 'DELETE':
        retorno = imoveis.mongoDelete(id)
    return jsonify(retorno)

@app.route('/imoveis_relevancia/',methods=['GET','POST'])
def imoveis_relevancia():
    retorno = {}
    imoveis_relevancia = Imoveis_relevancia()
    if request.method == 'GET':
        retorno = imoveis_relevancia.get_total()
    elif request.method == 'POST':
        retorno = imoveis_relevancia.add()
    return jsonify(retorno)

@app.route('/imoveis_relevancia_log/',methods=['GET','POST'])
def imoveis_relevancia_log():
    retorno = {}
    imoveis_relevancia = Imoveis_relevancia()
    if request.method == 'GET':
        retorno = imoveis_relevancia.get_total_log()
    elif request.method == 'POST':
        retorno = imoveis_relevancia.add_log()
    return jsonify(retorno)


########################################
    # Requests de Cidade            #
########################################


# @basic_auth.required
@app.route('/get_cidade/', methods={'GET'})
def get_cidade():
    print(basic_auth.authenticate())
    print(request.headers)
    retorno = {}
    cidades = Cidades()
    dominio = request.args['dominio']
    retorno = cidades.mongoGet(dominio)
    status_r = status.HTTP_200_OK
    if retorno is False:
        status_r = status.HTTP_403_FORBIDDEN
    return jsonify(retorno), status_r

@app.route('/get_cidade_in_ids/', methods={'GET','POST'})
def get_cidade_in_ids():
    retorno = {}
    cidades = Cidades()
    ids = tuple(map(int,request.args['ids'].split(',')))
    retorno = cidades.mongoGetinID(ids)
    status_r = status.HTTP_200_OK
    if retorno is False:
        status_r = status.HTTP_403_FORBIDDEN
    elif retorno['qtde'] == 0:
        status_r = status.HTTP_204_NO_CONTENT
    return jsonify(retorno['itens']), status_r


########################################
    # Requests de estatisticas      #
    # Log_portal                    #
    # Log_imoveis                   #
    # Log_pesquisas                 #
########################################
@app.route('/get_log_empresas/',methods=['GET'])
def get_log_empresas():
    retorno = {}
    imoveis = Log()
    retorno = imoveis.mongoGetLogEmpresaDia()
    return jsonify(retorno)

@app.route('/log_empresas/',methods=['GET'])
def log_empresas():
    retorno = {}
    imoveis = Log()
    retorno = imoveis.mongoGetLogEmpresaData()
    return jsonify(retorno) 

@app.route('/log_empresa/',methods=['POST'])
def log_empresa():
    retorno = {}
    imoveis = Log()
    retorno = imoveis.add_log_empresa_dia()
    return jsonify(retorno) 

@app.route('/log_empresa_max_data/',methods=['GET'])
def log_empresa_max():
    retorno = {}
    imoveis = Log()
    retorno = imoveis.mongoGetLogEmpresaMaxData()
    return jsonify(retorno)

@app.route('/log_empresa_min_data/',methods=['GET'])
def log_empresa_min():
    retorno = {}
    imoveis = Log()
    retorno = imoveis.mongoGetLogEmpresaMinData()
    return jsonify(retorno)

@app.route('/log_imoveis/',methods=['GET'])
def log_imoveis():
    retorno = {}
    imoveis = Log()
    retorno = imoveis.mongoGetLogImoveisData()
    return jsonify(retorno) 

@app.route('/log_imoveis_b/',methods=['GET'])
def log_imoveis_b():
    retorno = {}
    imoveis = Log()
    retorno = imoveis.mongoGetLogImoveisItem()
    return jsonify(retorno) 

@app.route('/log_imovel/',methods=['POST'])
def log_imovel():
    retorno = {}
    imoveis = Log()
    retorno = imoveis.add_log_imovel_dia()
    return jsonify(retorno) 

@app.route('/log_imovel_max_data/',methods=['GET'])
def log_imovel_max():
    retorno = {}
    imoveis = Log()
    retorno = imoveis.mongoGetLogImovelMaxData()
    return jsonify(retorno)

@app.route('/log_imovel_min_data/',methods=['GET'])
def log_imovel_min():
    retorno = {}
    imoveis = Log()
    retorno = imoveis.mongoGetLogImovelMinData()
    return jsonify(retorno)


########################################
    # Contato site    #
########################################

@app.route('/get_contatos/',methods=['GET'])
def get_contatos():
    retorno = {}
    contatos = Contato_site()
    retorno = contatos.getContatos()
    return jsonify(retorno)

@app.route('/contatos_site_sincronizado/',methods=['PUT'])
def contatos_site_sincronizado():
    contato = Contato_site()
    retorno = contato.update_sincronizado()

    return jsonify(retorno)

@app.route('/contatos_site_sincronizado_des/',methods=['PUT'])
def contatos_site_desincronizado():
    contato = Contato_site()
    retorno = contato.update_desincronizado()

    return jsonify(retorno)


########################################
    # Clientes Cadastros & cia    #
########################################

##
# clientes cadastros
# # GET
# id_empresa obrigatório
# limit, offset
# demais filtros
##
@app.route('/clientes_cadastros/',methods=['GET','POST','DELETE'])
def get_clientes_cadastros():
    retorno = {}
    clientes = Clientes_cadastros()
    status_r = status.HTTP_200_OK
    if request.method == 'GET':
        try:
            retorno = clientes.get()
        except RequestIncompleto:
            status_r = status.HTTP_304_NOT_MODIFIED
        if retorno is False:
            status_r = status.HTTP_204_NO_CONTENT
    elif request.method == 'DELETE':
        retorno = clientes.delete()
        print('delete')
        status_r = status.HTTP_200_OK
        if retorno is False:
            status_r = status.HTTP_304_NOT_MODIFIED
    else:
        try:
            retorno = clientes.add()
        except:
            pass
        status_r = status.HTTP_201_CREATED
        if retorno is False:
            status_r = status.HTTP_200_OK
    return jsonify(retorno), status_r


@app.route('/clientes_cadastros/<id>/<id_empresa>',methods=['GET','PUT'])
def clientes_cadastros_(id, id_empresa):
    retorno = {}
    clientes = Clientes_cadastros()
    if request.method == 'GET':
        retorno = clientes.getItem(id, id_empresa)
        status_r = status.HTTP_200_OK
        if retorno is False:
            status_r = status.HTTP_204_NO_CONTENT
    else:
        retorno = clientes.update(id, id_empresa)
        status_r = status.HTTP_202_ACCEPTED
        if retorno is False:
            status_r = status.HTTP_304_NOT_MODIFIED
    return jsonify(retorno), status_r

##
# clientes carrinhos
# # GET
# id_empresa obrigatório
# limit, offset
# demais filtros
# @return
#
##
@app.route('/clientes_carrinhos/',methods=['GET','POST','DELETE'])
def clientes_carrinhos():
    retorno = {}
    carrinhos = Clientes_carrinhos()
    status_r = status.HTTP_200_OK
    if request.method == 'GET':
        try:
            retorno = carrinhos.get()
        except RequestIncompleto:
            status_r = status.HTTP_304_NOT_MODIFIED
        if retorno is False:
            status_r = status.HTTP_204_NO_CONTENT
    elif request.method == 'DELETE':
        print('deleete')
        retorno = carrinhos.delete()
        status_r = status.HTTP_200_OK
        if retorno is False:
            status_r = status.HTTP_304_NOT_MODIFIED
    else:
        try:
            retorno = carrinhos.add()
        except:
            pass
        status_r = status.HTTP_201_CREATED
        if retorno is False:
            status_r = status.HTTP_200_OK
    return jsonify(retorno), status_r


@app.route('/clientes_carrinhos/<id>/<id_empresa>',methods=['GET','PUT'])
def clientes_carrinhos_(id, id_empresa):
    retorno = {}
    carrinhos = Clientes_carrinhos()
    if request.method == 'GET':
        retorno = carrinhos.getItem(id, id_empresa)
        status_r = status.HTTP_200_OK
        if retorno is False:
            status_r = status.HTTP_204_NO_CONTENT
    else:
        retorno = carrinhos.update(id, id_empresa)
        status_r = status.HTTP_202_ACCEPTED
        if retorno is False:
            status_r = status.HTTP_304_NOT_MODIFIED
    return jsonify(retorno), status_r

@app.route('/clientes_carrinhos_completo/',methods=['GET','POST'])
def clientes_carrinhos_completo():
    retorno = {}
    carrinhos = Clientes_carrinhos()
    status_r = status.HTTP_200_OK
    if request.method == 'GET':
        try:
            retorno = carrinhos.getCompleto()
        except:
            status_r = status.HTTP_404_NOT_FOUND
        if retorno is False:
            status_r = status.HTTP_204_NO_CONTENT
    elif request.method == 'POST':
        try:
            retorno = carrinhos.addCompleto()
            status_r = status.HTTP_201_CREATED
        except Exception as err :
            print(err)
            status_r = status.HTTP_204_NO_CONTENT
    else:
        retorno = False
    return jsonify(retorno), status_r

@app.route('/clientes_carrinhos_completo/<id>/<id_empresa>',methods=['GET'])
def clientes_carrinhos_completo_(id,id_empresa):
    retorno = {}
    carrinhos = Clientes_carrinhos()
    status_r = status.HTTP_200_OK
    if request.method == 'GET':
        try:
            retorno = carrinhos.getItemCompleto(id,id_empresa)
        except:
            status_r = status.HTTP_404_NOT_FOUND
        if retorno is False:
            status_r = status.HTTP_204_NO_CONTENT
    else:
        retorno = False
    return jsonify(retorno), status_r



##
# clientes carrinhos produtos
# # GET
# id_empresa obrigatório
# limit, offset
# demais filtros
# @return
#
##
@app.route('/clientes_carrinhos_produtos/',methods=['GET','POST','DELETE'])
def clientes_carrinhos_produtos():
    retorno = {}
    carrinhos_produtos = Clientes_carrinhos_produtos()
    status_r = status.HTTP_200_OK
    if request.method == 'GET':
        try:
            retorno = carrinhos_produtos.get()
        except RequestIncompleto:
            status_r = status.HTTP_304_NOT_MODIFIED
        if retorno is False:
            status_r = status.HTTP_204_NO_CONTENT
    elif request.method == 'DELETE':
        print('deleete')
        retorno = carrinhos_produtos.delete()
        status_r = status.HTTP_200_OK
        if retorno is False:
            status_r = status.HTTP_304_NOT_MODIFIED
    else:
        try:
            retorno = carrinhos_produtos.add()
        except:
            pass
        status_r = status.HTTP_201_CREATED
        if retorno is False:
            status_r = status.HTTP_200_OK
    return jsonify(retorno), status_r


@app.route('/clientes_carrinhos_produtos/<id>/<id_empresa>',methods=['GET','PUT'])
def clientes_carrinhos_produtos_(id, id_empresa):
    retorno = {}
    carrinhos_produtos = Clientes_carrinhos_produtos()
    if request.method == 'GET':
        retorno = carrinhos_produtos.getItem(id, id_empresa)
        status_r = status.HTTP_200_OK
        if retorno is False:
            status_r = status.HTTP_204_NO_CONTENT
    else:
        retorno = carrinhos_produtos.update(id, id_empresa)
        status_r = status.HTTP_202_ACCEPTED
        if retorno is False:
            status_r = status.HTTP_304_NOT_MODIFIED
    return jsonify(retorno), status_r



##
# clientes carrinhos historico
# # GET
# id_empresa obrigatório
# limit, offset
# demais filtros
# @return
#
##
@app.route('/clientes_carrinhos_historico/',methods=['GET','POST','DELETE'])
def clientes_carrinhos_historico():
    retorno = {}
    carrinhos_historico = Clientes_carrinhos_historico()
    status_r = status.HTTP_200_OK
    if request.method == 'GET':
        try:
            retorno = carrinhos_historico.get()
        except RequestIncompleto:
            status_r = status.HTTP_304_NOT_MODIFIED
        if retorno is False:
            status_r = status.HTTP_204_NO_CONTENT
    elif request.method == 'DELETE':
        print('deleete')
        retorno = carrinhos_historico.delete()
        status_r = status.HTTP_200_OK
        if retorno is False:
            status_r = status.HTTP_304_NOT_MODIFIED
    else:
        try:
            retorno = carrinhos_historico.add()
        except:
            pass
        status_r = status.HTTP_201_CREATED
        if retorno is False:
            status_r = status.HTTP_200_OK
    return jsonify(retorno), status_r


@app.route('/clientes_carrinhos_historico/<id>/<id_empresa>',methods=['GET','PUT'])
def clientes_carrinhos_historico_(id, id_empresa):
    retorno = {}
    carrinhos_historico = Clientes_carrinhos_historico()
    if request.method == 'GET':
        retorno = carrinhos_historico.getItem(id, id_empresa)
        status_r = status.HTTP_200_OK
        if retorno is False:
            status_r = status.HTTP_204_NO_CONTENT
    else:
        retorno = carrinhos_historico.update(id, id_empresa)
        status_r = status.HTTP_202_ACCEPTED
        if retorno is False:
            status_r = status.HTTP_304_NOT_MODIFIED
    return jsonify(retorno), status_r

##
# clientes carrinhos historico_ com update
# # POST
# data.clientes_carrinhos = {'data':{
#         'status_pagamento': $event.status,
#         'id_tipo_pagamento':$event.tipo_pagamento,
#         'complemento_tipo_pagamento':$event.complemento_pagamento
#       },'filtro':{
#         'id':this.id_clientes_carrinhos
#       }};
#       data.clientes_carrinhos_historico = {'data':{
#         'id_clientes_carrinhos': this.id_clientes_carrinhos,
#         'descricao':$event.descricao,
#         'id_status':$event.status,
#         'id_usuario':$('.id_usuario').val()
#       }};
#
##
@app.route('/clientes_carrinhos_historico_update/',methods=['POST'])
def clientes_carrinhos_historico_update():
    retorno = False
    carrinhos_historico = Clientes_carrinhos_historico()
    status_r = status.HTTP_200_OK
    try:
        retorno = carrinhos_historico.add_update()
    except:
        pass
    status_r = status.HTTP_201_CREATED
    if retorno is False:
        status_r = status.HTTP_406_NOT_ACCEPTABLE
    return jsonify(retorno), status_r



##
# clientes produtos
# # GET
# id_empresa obrigatório
# limit, offset
# demais filtros
# @return
#
##
@app.route('/produtos/',methods=['GET','POST','DELETE'])
def produtos():
    retorno = {}
    produtos = Produtos()
    status_r = status.HTTP_200_OK
    if request.method == 'GET':
        try:
            retorno = produtos.get()
        except RequestIncompleto:
            status_r = status.HTTP_304_NOT_MODIFIED
        if retorno is False:
            status_r = status.HTTP_204_NO_CONTENT
    elif request.method == 'DELETE':
        print('deleete')
        retorno = produtos.delete()
        status_r = status.HTTP_200_OK
        if retorno is False:
            status_r = status.HTTP_304_NOT_MODIFIED
    else:
        try:
            retorno = produtos.add()
        except:
            pass
        status_r = status.HTTP_201_CREATED
        if retorno is False:
            status_r = status.HTTP_200_OK
    return jsonify(retorno), status_r


@app.route('/produtos/<id>/<id_empresa>',methods=['GET','PUT'])
def produtos_(id, id_empresa):
    retorno = {}
    produtos = Produtos()
    if request.method == 'GET':
        retorno = produtos.getItem(id, id_empresa)
        status_r = status.HTTP_200_OK
        if retorno is False:
            status_r = status.HTTP_204_NO_CONTENT
    else:
        retorno = produtos.update(id, id_empresa)
        status_r = status.HTTP_202_ACCEPTED
        if retorno is False:
            status_r = status.HTTP_304_NOT_MODIFIED
    return jsonify(retorno), status_r




########################################
    # Requests app Tempo Malhada    #
########################################

@app.route('/tempo_malhada/',methods=['POST'])
def tempo_malhada():
    retorno = {}
    tempo = Tempo()
    retorno = tempo.add_tempo()
    return jsonify(retorno) 

########################################
    # teste    #
########################################

@app.route('/test_encrypt/',methods=['GET'])
def test_encrypt():
    # print(data['basic'])
    # ciphertext = encrypt(data['basic']['passwd'], 'my secret message')
    # print(ciphertext)
    # plaintext = decrypt(data['basic']['passwd'], ciphertext)
    # print(plaintext)
    # print(data['basic']['key'])
    return jsonify([])


########################################
    # Requests preparação    #
########################################

@app.app.errorhandler(401)
def page_not_found(error):
    print(basic_auth.check_credentials())
    response = {'status':False, 'msg':'bloqueio de usuário, por falta de credenciais'};
    return jsonify(response), status.HTTP_401_UNAUTHORIZED

#

@app.app.before_request
def before_request():
    if basic_auth.authenticate():
        print('basic')
        pass
    elif request.method == "OPTIONS" and 'authorization' in request.headers['Access-Control-Request-Headers']:
        print('options')
        retorno = {}
        retorno['message'] = 'Use Authorization to access the content'
        status_r = status.HTTP_200_OK
        return jsonify(retorno), status_r
    elif request.remote_addr in lista_ip():
        print('remote')
        pass
    else:
        print(basic_auth.check_credentials())
        print('nao autorizado')
        retorno = {}
        retorno['status'] = False
        retorno['message'] = 'bloqueio de usuário, por falta de credenciais'
        status_r = status.HTTP_401_UNAUTHORIZED
        return jsonify(retorno), status_r

#"127.0.0.1",
def lista_ip():
    return ["189.4.3.5",
            "201.16.246.212",
            "201.16.246.176",
            # "192.168.1",
            "192.168.1.20",
            "192.168.1.153",
            "189.39.42.133",
            "189.39.42.155",
            "189.39.42.153",
            "127.0.0.1"
            ]

if __name__ == '__main__':
    if 'localhost' in sys.argv:
        app.run(host='127.0.0.1',port=5000,debug=True)
        # app.run(host='192.168.10.109',port=5000,debug=True,ssl_context=('cert.pem', 'key.pem'))
    else:
        app.run(host='127.0.0.1',port=80,debug=False,ssl_context='adhoc')


