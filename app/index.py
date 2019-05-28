# -*- coding: utf-8 -*-

from flask import render_template,request,jsonify
import connexion
import sys
sys.path.append('library')
sys.path.append('controller')
sys.path.append('model')
from Imoveis import Imoveis

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
    return jsonify(retorno)

@app.route('/imovel/<id>',methods=['PUT','DELETE'])
def imoveis_id(id):
    retorno = {}
    imoveis = Imoveis()
    if request.method == 'PUT':
        data = request.args
        retorno = data
    elif request.method == 'DELETE':
        data = request.args
        retorno = data
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

@app.route('/imovel_images_copy/',methods=['GET'])
def imoveis_images_copy():
    retorno = {}
    imoveis = Imoveis()
    return jsonify(imoveis.images())

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
def imoveismongo_():
    retorno = {}
    imoveis = Imoveis()
    if request.method == 'GET':
        retorno = imoveis.get_mongo()
    return jsonify(retorno)

@app.route('/imoveismongo/<id>',methods=['PUT','DELETE'])
def imoveismongo_id(id):
    retorno = {}
    imoveis = Imoveis()
    if request.method == 'PUT':
        data = request.args
        retorno = data
    elif request.method == 'DELETE':
        data = request.args
        retorno = data
    return jsonify(retorno)

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000,debug=True)


