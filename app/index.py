# -*- coding: utf-8 -*-
from flask import render_template,request,jsonify
from flask import Flask
from flask_api import status
import connexion
import sys, os


sys.path.append('/library')
sys.path.append('/controller')
sys.path.append('/model')
from controller.Imoveis import Imoveis

app = connexion.App(__name__,specification_dir='./')
#app.add_api('swagger.yml')

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
        retorno = imoveis.get_mongo()
    elif request.method == 'POST':
        data = request.args
        retorno = imoveis.add_mongo(data)
    return jsonify(retorno)
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
    else:
        app.run(host='127.0.0.1',port=80,debug=True)


