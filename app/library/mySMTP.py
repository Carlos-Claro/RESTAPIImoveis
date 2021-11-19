import sys
sys.path.append('../model')
import smtplib, ssl
import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from .myKeys import myKeys
from model.empresasMongo import empresasMongo
from model.imoveisMongo import imoveisMongo

# https://realpython.com/python-send-email/

class mySMTP(object):

    def __init__(self, data):
        keys = myKeys()
        self.smtp = keys.getSMTP('pow')
        self.data = data
        empresas = empresasMongo()
        self.empresa = empresas.getItem(data['id_empresa'])
        imoveis = imoveisMongo()
        self.imovel = imoveis.getItem(int(data['id_item']))
        self.dataItem = self.dataEmail()



    def dataEmail(self):
        array = {
            'contato_nome': self.empresa['contato_nome'],
            'empresa_nome_fantasia': self.empresa['nome_fantasia'],
            'date': datetime.datetime.now(),
            'imovel_image': self.imovel['images'][0]['arquivo'],
            'imovel_nome': self.imovel['nome'],
            'imovel_link': self.data['link'],
            'assunto': self.data['assunto'],
            'usuario_nome': self.data['nome'],
            'usuario_email': self.data['email'],
            'usuario_telefone': '',
            'portal': self.data['portal'],
            'message': self.data['mensagem']
        }
        return array


    def envioEmpresa(self):
        with open('templates/email_empresa.html', 'r') as a:
            email = a.read()
        email_f = email.format(**self.dataItem)
        message = MIMEMultipart("alternative")
        message["Subject"] = self.dataItem['assunto']
        message["From"] = 'email@portaisimobiliarios.com.br'
        message["To"] = 'programacao@pow.com.br'
        part1 = MIMEText(email_f, "plain")
        part2 = MIMEText(email_f, "html")
        message.attach(part1)
        message.attach(part2)
        with smtplib.SMTP(self.smtp['smtp_host'], self.smtp['smtp_port']) as smtpServer:
            smtpServer.login(self.smtp['smtp_user'], self.smtp['smtp_pass'])
            smtpServer.sendmail('email@portaisimobiliarios.com.br','programacao@pow.com.br', message.as_string() )



    def envioUsuario(self):
        with open('templates/email_usuario.html', 'r') as a:
            email = a.read()
        email_f = email.format(**self.dataItem)
        message = MIMEMultipart("alternative")
        message["Subject"] = self.dataItem['assunto']
        message["From"] = 'email@portaisimobiliarios.com.br'
        message["To"] = self.dataItem['usuario_email']
        part1 = MIMEText(email_f, "plain")
        part2 = MIMEText(email_f, "html")
        message.attach(part1)
        message.attach(part2)
        with smtplib.SMTP(self.smtp['smtp_host'], self.smtp['smtp_port']) as smtpServer:
            smtpServer.login(self.smtp['smtp_user'], self.smtp['smtp_pass'])
            smtpServer.sendmail('email@portaisimobiliarios.com.br',self.dataItem['usuario_email'], message.as_string() )


