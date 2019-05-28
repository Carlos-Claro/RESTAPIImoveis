import os
from PIL import Image
from resizeimage import resizeimage

# https://github.com/charlesthk/python-resize-image
class myImages(object):

    def __init__(self, id_empresa):
        self.ID = id_empresa

    def executa(self,image):
        for tamanho in self.tamanhos():
            self.geraImages(image,nome,tamanho)

    def geraImages(self,image,nome,tamanho):
        with Image.open(image) as imagem:
            cover = resizeimage.resize_width(imagem,tamanho)
            cover.save('images_modificadas/' + nome + '-' + str(tamanho) + 'x' + str(tamanho)+'.jpeg', 'jpeg')

    def tamanhos(self):
        tamanho = [
                    {'width':80,      'height':60,    'salva':FALSE, 'pasta':'powsites/'+self.ID+'/imo/', 'prefixo':'T_F_'},
                    {'width':'240',   'height':'180', 'salva':FALSE, 'pasta':'powsites/'+self.ID+'/imo/', 'prefixo':'TM_F_'},
                    {'width':'120',   'height':'90',  'salva':FALSE, 'pasta':'powsites/'+self.ID+'/imo/', 'prefixo':'T3_F_'},
                    {'width':'650',   'height':'auto','salva':FALSE, 'pasta':'powsites/'+self.ID+'/imo/', 'prefixo':'T5_F_'},
                    {'width':'900',   'height':'auto','salva':FALSE, 'pasta':'powsites/'+self.ID+'/imo/', 'prefixo':'650F_F_'},
                    {'width':'1150',  'height':'auto','salva':FALSE, 'pasta':'powsites/'+self.ID+'/imo/', 'prefixo':'1150F_F_'},
                ]
        return tamanho


if __name__ == '__main__':
    try:
        myPNG()
        #c.getItens()
    except KeyboardInterrupt:
        pass
    finally:
        print("Finaliza myPNG")
