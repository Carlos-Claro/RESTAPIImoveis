import sys, os
import json

class myKeys(object):

    def __init__(self):
        self.default = 'server'
        endereco = '/var/www/json/keys.json'
        if 'localhost' in sys.argv:
            self.default = 'localhost'
        elif 'programacao' in sys.argv:
            self.default = 'localhost'
            endereco = '/home/www/json/keys.json'
        with open(endereco) as json_file:
            self.data = json.load(json_file)

    # pega campo necessário
    def get(self, campo, useDefault):
        if useDefault:
            return self.data[self.default][campo]
        return self.data[campo]

    def getDB(self, db):
        return self.data['database'][self.default][db]

    def getSMTP(self,agente):
        return self.data['email'][agente]

    def getFTP(self,tipo):
        return self.data['ftp'][self.default][tipo]