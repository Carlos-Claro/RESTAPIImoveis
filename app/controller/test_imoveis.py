# -*- coding: utf-8 -*-

import unittest
import random
import sys
import datetime
from Imoveis import Imoveis
import time

class TestImoveis(unittest.TestCase):
    def setUp(self):
        self.imoveis = Imoveis()
        
    INS = {
            'imovel':{
                    'nome':'Teste Adionar imóvel',
                    'id_tipo': '2',
                    'id_cidade': '1',
                    'data':int(time.time()),
                    'id_empresa':'99999'
                    },
            'images':[
                    {
                            'id_empresa':'{{id_empresa}}',
                            'id_imovel':'{{id_imovel}}',
                            'arquivo':'F_{{id_imovel}}_{{id_image}}',
                            'data':datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                            'titulo':'Arquivo image 1',
                            'ordem':'0',
                     },
                    {
                            'id_empresa':'{{id_empresa}}',
                            'id_imovel':'{{id_imovel}}',
                            'arquivo':'F_{{id_imovel}}_{{id_image}}',
                            'data':datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                            'titulo':'Arquivo image 2',
                            'ordem':'1',
                     },
                    {
                            'id_empresa':'{{id_empresa}}',
                            'id_imovel':'{{id_imovel}}',
                            'arquivo':'F_{{id_imovel}}_{{id_image}}',
                            'data':datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                            'titulo':'Arquivo image 3',
                            'ordem':'2',
                     },
                    ]
            }
            
            
    def test_add_update_delete(self):
        id = self.imoveis.add_test(self.INS['imovel'])
        self.assertTrue(id['id'])
        data = {'id_cidade':1000}
        up = self.imoveis.update_test(id['id'],data)
        self.assertTrue(up['qtde'] == 1)
        d = self.imoveis.delete(id['id'])
        self.assertTrue(d['qtde'] == 1)
    
    def test_add_com_images(self):
        id = self.imoveis.add_test(self.INS['imovel'])
        self.assertTrue(id['id'])
        for image in self.INS['images']:
            image['id_empresa'] = image['id_empresa'].replace('{{id_empresa}}',self.INS['imovel']['id_empresa'])
            image['id_imovel'] = image['id_imovel'].replace('{{id_imovel}}',str(id['id']))
            image['arquivo'] = image['arquivo'].replace('{{id_imovel}}',str(id['id']))
            print(image)
            im = self.imoveis.add_images_imovel_test(image)
            data_up = {'arquivo':image['arquivo'].replace('{{id_image}}',str(im['id']))}
            up = self.imoveis.update_images_id_test(im['id'],data_up)
            self.assertTrue(up['qtde'] == 1)
        d = self.imoveis.delete_images_id(im['id'])
        self.assertTrue(d['qtde'])
        de = self.imoveis.delete_images_id_imovel(id['id'])
        self.assertTrue(de['qtde'])
        di = self.imoveis.delete(id['id'])
        self.assertTrue(di['qtde'])
        
        
        
    
if __name__ == '__main__':
    unittest.main()# -*- coding: utf-8 -*-

