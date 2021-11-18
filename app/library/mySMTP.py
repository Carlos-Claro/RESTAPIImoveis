import sys
sys.path.append('../model')
import smtplib, ssl
import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from .myKeys import myKeys
from model.empresasMongo import empresasMongo

# https://realpython.com/python-send-email/

class mySMTP(object):

    def __init__(self, data):
        keys = myKeys()
        self.smtp = keys.getSMTP('pow')
        self.data = data
        empresas = empresasMongo()
        self.empresa = empresas.getItem(data['id_empresa'])



    def dataEmail(self):
        print(self.empresa['contato_nome'])
        array = {
            'contato_nome': self.empresa['contato_nome'],
            'empresa_nome_fantasia': self.empresa['nome_fantasia'],
            'date': datetime.datetime.now(),
            'assunto': self.data['assunto'],
            'usuario_nome': self.data['nome'],
            'usuario_email': self.data['email'],
            'usuario_telefone': '',
            'link_imovel': self.data['link'],
            'portal': self.data['portal'],
            'message': self.data['mensagem']
        }
        return array


    def envioEmpresa(self):
        dados = self.dataEmail()
        with open('templates/email_empresa.html', 'r') as a:
            email = a.read()
        email_f = email.format(**dados)

        message = MIMEMultipart("alternative")
        message["Subject"] = dados['assunto']
        message["From"] = 'email@portaisimobiliarios.com.br'
        message["To"] = 'programacao@pow.com.br'
        part1 = MIMEText(email_f, "plain")
        part2 = MIMEText(email_f, "html")
        message.attach(part1)
        message.attach(part2)
        with smtplib.SMTP(self.smtp['smtp_host'], self.smtp['smtp_port']) as smtpServer:
            smtpServer.login(self.smtp['smtp_user'], self.smtp['smtp_pass'])
            smtpServer.sendmail('email@portaisimobiliarios.com.br','programacao@pow.com.br', message.as_string() )
        return 0


    def envioUsuario(self):
        return 0


    def messageUsuario(self):

        return 0


    def messageEmpresa(self):
        return 0

# import smtplib, ssl
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart
#
# sender_email = "my@gmail.com"
# receiver_email = "your@gmail.com"
# password = input("Type your password and press enter:")
#
# message = MIMEMultipart("alternative")
# message["Subject"] = "multipart test"
# message["From"] = sender_email
# message["To"] = receiver_email
#
# # Create the plain-text and HTML version of your message
# text = """\
# Hi,
# How are you?
# Real Python has many great tutorials:
# www.realpython.com"""
# html = """\
# <html>
#   <body>
#     <p>Hi,<br>
#        How are you?<br>
#        <a href="http://www.realpython.com">Real Python</a>
#        has many great tutorials.
#     </p>
#   </body>
# </html>
# """
#
# # Turn these into plain/html MIMEText objects
# part1 = MIMEText(text, "plain")
# part2 = MIMEText(html, "html")
#
# # Add HTML/plain-text parts to MIMEMultipart message
# # The email client will try to render the last part first
# message.attach(part1)
# message.attach(part2)
#
# # Create secure connection with server and send email
# context = ssl.create_default_context()
# with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
#     server.login(sender_email, password)
#     server.sendmail(
#         sender_email, receiver_email, message.as_string()
#     )

###