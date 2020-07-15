import datetime
import logging

from library.Exception import LogInvalido


class Logs:

    def __init__(self, data):
        logging.warning('whatch out!')
        formato = self.formatos({'tipo':'formato', 'chave':data['formato']})
        arquivo = self.formatos({'tipo':'arquivo', 'chave':data['arquivo']})
        linha = self.formata(formato, data['data'])
        print(linha)
        self.set_log(arquivo, linha)

    def formatos(self, data):
        arquivos = {
            'log': '/var/log/sistema/RESTAPI.log'
        }
        formatos = {
            'request_erro': '{data} - status_code {status_code} - message {message} - erro_request ',
            'geral': '{data} - message {message} - geral ',
        }
        if data['tipo'] == 'arquivo':
            try:
                return arquivos[data['chave']]
            except KeyError:
                message = 'Não existe este arquivo - {}'.format(data['chave'])
                self.log_error(message)
                raise LogInvalido(message)
        try:
            return formatos[data['chave']]
        except KeyError:
            message = 'Não existe este formato - {}'.format(data['chave'])
            self.log_error(message)
            raise LogInvalido(message)

    def set_log(self,arquivo,linha):
        try:
            print(arquivo)
            logging.basicConfig(filename=arquivo, filemode='w', level=logging.INFO, format='%(asctime)s %(message)s')
            logging.info(linha)
            # with open(arquivo, 'a') as arq:
            #     arq.write(linha)
            #     arq.write('\r\n')
            return True
        except:
            print('error write')
            message = 'não foi possivel adicionar a linha, verifique as permissões do arquivo.'
            self.log_error(message)
            raise LogInvalido(message)

    def formata(self, chave, valor):
        return chave.format(**valor)

    def log_error(self, message):
        data = {
            'formato': 'geral',
            'arquivo': 'log',
            'data': {
                'data': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'message': message
            }
        }
        Logs(data)


