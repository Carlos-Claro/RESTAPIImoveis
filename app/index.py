# -*- coding: utf-8 -*-#
from flask import render_template,request,jsonify,send_from_directory
from flask import Flask
from flask_api import status
import connexion
import sys, os
from flask_cors import CORS

sys.path.append('/library')
sys.path.append('/controller')
sys.path.append('/model')
from controller.Imoveis import Imoveis
from controller.Log import Log
from controller.Imoveis_relevancia import Imoveis_relevancia

app = connexion.App(__name__,specification_dir='./')
CORS(app.app)
#app.add_api('swagger.yml')

@app.route('/')
def index():
    return '<!DOCTYPE html!><html lang=pt-br><head><meta charset="UTF-8" ></head><body><h1>Pow internet API para imóveis</h1></body></html>'

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(str(app.root_path), 'images'),'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/imoveis',methods=['GET','POST'])
def imoveis():
    imoveis = Imoveis()
    if request.method == 'GET':
        retorno = imoveis.get()
    elif request.method == 'POST':
        retorno = imoveis.add()
    return jsonify(retorno)
    #return render_template('../templates/main.html')
    #return render_template('../templates/main.html')
    
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

@app.route('/imovel_images_copy/',methods=['GET'])
def imoveis_images_copy():
    retorno = {}
    imoveis = Imoveis()
    return jsonify(imoveis.imagesIDEmpresa())

@app.route('/imoveis_images_gerar/<limit>',methods=['GET'])
def imoveis_images_gerar(limit):
    retorno = {}
    imoveis = Imoveis()
    return jsonify(imoveis.imagesGerarMongo(limit))

@app.route('/imoveismongo',methods=['GET','POST'])
def imoveismongo():
    retorno = {}
    imoveis = Imoveis()
    if request.method == 'GET':
        retorno = imoveis.mongoGet()
    elif request.method == 'POST':
        data = request.args
        retorno = imoveis.add_mongo(data)
    status_r = status.HTTP_200_OK
    if retorno is False:
        status_r = status.HTTP_403_FORBIDDEN
    return jsonify(retorno), status_r

    #return render_template('../templates/main.html')
    #return render_template('../templates/main.html')
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


######################
    # Requests de estatisticas
    # Log_portal
    # Log_imoveis
    # Log_pesquisas
######################
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




    
@app.app.before_request
def before_request():
    if request.remote_addr in lista_ip():
        pass
    else:
        print("Kill by host")
        exit()

def lista_ip():
    return ["127.0.0.1","189.4.3.5","201.16.246.212","201.16.246.176"]

if __name__ == '__main__':
    if 'localhost' in sys.argv:
        app.run(host='127.0.0.1',port=5000,debug=True)
        #app.run(host='127.0.0.1',port=5000,debug=True,ssl_context='adhoc')
    else:
        app.run(host='127.0.0.1',port=80,debug=True,ssl_context='adhoc')


