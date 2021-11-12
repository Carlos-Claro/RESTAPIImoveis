from library.myMysql import myMysql
from library.myQuery import myQuery
import datetime
import sys


class contatoSiteModel(object):

    def __init__(self):
        self.conn = myMysql()
        self.query = myQuery()

    def add(self, data):
        print(data)
        count = 0
        keys = '('
        values = '('
        for k, v in data.items():
            if count > 0:
                keys += ', '
                values += ', '
            keys += str(k)
            values += '"' + str(v) + '"'
            count += 1
        keys += ')'
        values += ')'
        query = 'INSERT INTO contatos_site {} VALUES {}'.format(keys, values)
        return self.conn.add(query)

    def update_id(self, data, id):
        if isinstance(data, str):
            valor = data
        else:
            valor = ''
            count = 0
            for k, v in data.items():
                if count > 0:
                    valor += ', '
                valor += k + '= "' + str(v) + '"'
        qu = 'UPDATE contatos_site set {} where id = {}'.format(valor, str(id))
        return self.conn.update(qu)

    def update_id_in(self, data, ids):
        if isinstance(data, str):
            valor = data
        else:
            valor = ''
            count = 0
            for k, v in data.items():
                if count > 0:
                    valor += ', '
                valor += k + '= "' + str(v) + '"'
        qu = 'UPDATE contatos_site set {} where id IN ({})'.format(valor, str(ids))
        print(qu)
        return self.conn.update(qu)

    def delete_id(self, id):
        q = 'SELECT id from contatos_site where id = {} '.format(str(id))
        a = len(self.conn.get(q))
        if a > 0:
            que = 'DELETE from contatos_site where id = {}'.format(str(id))
            self.conn.delete(que)
            if len(self.conn.get(q)) == 0:
                return True
        return False

    def getItem(self, id):
        query = {}
        query[
            'colunas'] = 'imoveis.id as _id, imoveis.id as id, imoveis.nome as nome, IF ( imoveis.preco_venda > 0, imoveis.preco_venda, IF ( imoveis.preco_locacao > 0, imoveis.preco_locacao, imoveis.preco_locacao_dia ) ) as preco, imoveis.data_atualizacao as data_atualizacao, imoveis.preco_venda as preco_venda, imoveis.preco_locacao as preco_locacao, imoveis.preco_locacao_dia as preco_locacao_dia, imoveis.logradouro as logradouro, IF( imoveis.video, 1, 0 ) as video, imoveis.condominio as terreno, imoveis.quartos as quartos, imoveis.garagens as garagens, imoveis.banheiros as banheiros, imoveis.area as area, imoveis.area_terreno as area_terreno, imoveis.area_util as area_util, empresas.mudou as mudou, IF ( imoveis.bairro <> bairros.nome, imoveis.bairro, "") as vila, bairros.nome as bairro, bairros.link as bairros_link, imoveis_tipos.nome as imoveis_tipos_titulo, imoveis_tipos.english as imoveis_tipos_english, imoveis_tipos.link as imoveis_tipos_link, imoveis_tipos.id as imoveis_tipos_id, imoveis.id_tipo as id_tipo, cidades.link as cidades_link, IF ( imoveis.venda = 1, "venda", IF ( imoveis.locacao = 1, "locacao", "locacao_dia" ) ) as tipo, imoveis.venda as tipo_venda, imoveis.locacao as tipo_locacao, imoveis.locacao_dia as tipo_locacao_dia, empresas.id as id_empresa, imoveis.views as views, imoveis.id_cidade as imovel_id_cidade, bairros.cidade as bairro_cidade, cidades.id as cidades_id, cidades.nome as cidade_nome, cidades.uf as uf, imoveis.bairro_combo as bairro_combo, empresas.empresa_nome_fantasia as nome_empresa, empresas.empresa_nome_fantasia as imobiliaria_nome, empresas.nome_seo as imobiliaria_nome_seo, empresas.empresa_telefone as imobiliaria_telefone, empresas.whatsapp as imobiliaria_whatsapp, empresas.pagina_logo_pequeno as logo, end_empresa.logradouro as imobiliaria_logradouro, end_empresa.bairro as imobiliaria_bairro, end_empresa.cidade as imobiliaria_cidade, empresas.empresa_numero as imobiliaria_numero, empresas.empresa_email as empresa_email, empresas.empresa_emaillocacao as locacao_email, empresas.pagina_creci as creci, imoveis.longitude as longitude, imoveis.latitude as latitude, logradouros.logradouro as logradouro_, imoveis.descricao as descricao, imoveis.referencia as referencia, imoveis.ordem_rad as ordem, IF ( imoveis.comercial = 1, "Comercial", IF ( imoveis.residencial = 1, "Residencial", "Lazer") ) as uso, IF( imoveis.latitude <> "", CONCAT( imoveis.latitude, ", ", imoveis.longitude ), "" ) as mapa, if ( imoveis.venda = 1, "venda", IF ( imoveis.locacao = 1, "locação", IF ( imoveis.locacao_dia = 1, "locação temporada", NULL ) ) ) as imovel_para, if ( imoveis.venda = 1, "venda", IF ( imoveis.locacao = 1, "locacao", IF ( imoveis.locacao_dia = 1, "locacao_dia", NULL ) ) ) as tipo_negocio, imoveis.venda as venda, imoveis.locacao as locacao, imoveis.locacao_dia as locacao_dia, imoveis.quartos as quartos, imoveis.suites as suites, imoveis.banheiros as banheiros, imoveis.garagens as garagens, imoveis.mobiliado as mobiliado, imoveis.cobertura as cobertura, imoveis.condominio as condominio, imoveis.condominio_valor as condominio_valor, imoveis.area_terreno as area_terreno, imoveis.area as area, imoveis.area_util as area_util, imoveis.preco_venda as preco_venda, imoveis.preco_locacao as preco_locacao, imoveis.preco_locacao_dia as preco_locacao_dia, imoveis.id_cidade as id_cidade, bairros.nome as bairro, bairros.link as bairros_link, imoveis.bairro as vila, imoveis.cep as cep, IF ( imoveis.id_logradouro > 0, logradouros.logradouro, imoveis.logradouro ) as logradouro, imoveis.numero as numero, imoveis.comercial as comercial, imoveis.residencial as residencial, imoveis.lazer as lazer, imoveis.video as video, imoveis.banheiros as banheiros, imoveis.mostramapa as mostramapa, imoveis.destaque_bairro as destaque_bairro, imoveis.destaque_tipo as destaque_tipo, imoveis.novo as novo, cidades.link as cidades_link, empresa_cidade.ddd as ddd, cidades.nome as cidade, cidades.uf as uf, estados.nome as estado, cidades.link as cidade_link, IF ( imoveis_corretor.recebe_email = 1, imoveis_corretor.email, "") as email_corretor, imoveis_corretor.nome as nome_corretor, imoveis_corretor.sms as sms_corretor, imoveis_corretor.celular as celular_corretor, hotsite_parametros.sms_quem as sms_quem, empresas.servicos_sms_limite as sms_limite, empresas.empresa_fone_sms as empresa_telefone_sms, empresas.pagina_limite_ofertas as pagina_limite_ofertas, CONCAT(imoveis.preco_venda, "-", imoveis.preco_locacao, "-", imoveis.preco_locacao_dia) as valores, CONCAT(imoveis.invisivel, "-", imoveis.reservaimovel, "-", imoveis.vendido, "-", imoveis.locado) as status, imoveis_situacao.titulo as situacao_titulo, imoveis_situacao.link as situacao_link'
        query['tabela'] = 'imoveis'
        query['join'] = [
            {'tabela': 'empresas', 'where': 'imoveis.id_empresa = empresas.id', 'tipo': 'INNER'}
            , {'tabela': 'imoveis_tipos', 'where': 'imoveis.id_tipo = imoveis_tipos.id', 'tipo': 'LEFT'}
            , {'tabela': 'imoveis_situacao', 'where': 'imoveis.novo = imoveis_situacao.id', 'tipo': 'LEFT'}
            , {'tabela': 'bairros', 'where': 'imoveis.bairro_combo = bairros.id', 'tipo': 'LEFT'}
            , {'tabela': 'logradouros', 'where': 'imoveis.id_logradouro = logradouros.id', 'tipo': 'LEFT'}
            , {'tabela': 'cidades', 'where': 'cidades.id = imoveis.id_cidade', 'tipo': 'LEFT'}
            , {'tabela': 'logradouros empresa_logradouro', 'where': 'empresas.id_logradouro = empresa_logradouro.id',
               'tipo': 'LEFT'}
            , {'tabela': 'cidades empresa_cidade', 'where': 'empresa_logradouro.id_cidade = empresa_cidade.id',
               'tipo': 'LEFT'}
            , {'tabela': 'estados', 'where': 'cidades.uf = estados.uf', 'tipo': 'LEFT'}
            , {'tabela': 'imoveis_corretor', 'where': 'imoveis.id_corretor = imoveis_corretor.id', 'tipo': 'LEFT'}
            , {'tabela': 'logradouros end_empresa', 'where': 'empresas.id_logradouro = end_empresa.id', 'tipo': 'LEFT'}
            , {'tabela': 'hotsite_parametros', 'where': 'imoveis.id_empresa = hotsite_parametros.id_empresa',
               'tipo': 'LEFT'}
        ]
        d = datetime.datetime.now().strftime('%Y-%m-%d')
        now = datetime.datetime.now()
        t = datetime.datetime.timestamp(now)
        query['where'] = [{'tipo': 'where', 'campo': 'imoveis.id', 'valor': id}]
        q = self.query.get(query)
        itens = self.conn.get(q)
        i = {}
        if len(itens):
            for item in itens:
                i[item['id']] = item
                i[item['id']]['images'] = self.getImagesIDimovel(item['id'])
            if i[item['id']]:
                retorno = i[item['id']]
            else:
                retorno = False
        else:
            retorno = False
        return retorno

    def getItensDisparo(self, data):
        query = {}
        query['colunas'] = 'GROUP_CONCAT(contatos_site.id SEPARATOR ",") as id,' \
                         'cadastros.id as id_cadastro,' \
                         'FROM_UNIXTIME(contatos_site.data,"%d/%m/%Y %H:%i") as data,' \
                         'contatos_site.nome as nome, ' \
                         'contatos_site.email as email,' \
                         'contatos_site.cidade as cidade,' \
                         'contatos_site_origem.tabela as tabela,' \
                         'COUNT(contatos_site.email) as qtde_contatos,' \
                         'GROUP_CONCAT(DISTINCT contatos_site.id_item SEPARATOR ",") as id_itens,' \
                         'GROUP_CONCAT(DISTINCT contatos_site.id_tipo_item SEPARATOR ",") as id_tipo_item,' \
                         'GROUP_CONCAT(DISTINCT contatos_site.id_cidade SEPARATOR ",") as cidades,' \
                         'GROUP_CONCAT(DISTINCT imoveis_tipos.link SEPARATOR ",") as tipos_item,' \
                         'GROUP_CONCAT(DISTINCT contatos_site.tipo_negocio_item SEPARATOR ",") as tipo_negocio_item'
        query['tabela'] = 'contatos_site'
        query['join'] = [
            {'tabela': 'empresas', 'where': 'contatos_site.id_empresa = empresas.id', 'tipo': 'LEFT'}
            , {'tabela': 'contatos_site_origem', 'where': 'contatos_site.origem = contatos_site_origem.origem', 'tipo': 'INNER'}
            , {'tabela': 'cadastros', 'where': 'contatos_site.email = cadastros.email', 'tipo': 'INNER'}
            , {'tabela': 'imoveis_tipos', 'where': 'contatos_site.id_tipo_item = imoveis_tipos.id', 'tipo': 'LEFT'}
        ]

        data_inicio = datetime.datetime.now() - datetime.timedelta(days=1)
        data_fim = datetime.datetime.now() - datetime.timedelta(days=int(data['dias']))

        query['where'] = [
        'contatos_site.data >= {} '.format(datetime.datetime.timestamp(data_fim))
        , 'contatos_site.data <= {} '.format(datetime.datetime.timestamp(data_inicio))
        , 'empresas.id_subcategoria = 138'
        , 'cadastros.news = 1'
        , 'contatos_site.sincronizado = 0'
        , '( contatos_site.tipo_negocio_item IS NOT NULL OR contatos_site.tipo_negocio_item <> 0)'
        , 'contatos_site.id_tipo_item > 0'
        , 'tabela = "imoveis"'
        ]
        if 'filtro' in data:
            query['where'].append(data['filtro'])
        query['group'] = 'contatos_site.email'
        query['ordem'] = 'contatos_site.id DESC'
        query['offset'] = 0
        query['limit'] = data['limit']
        q = self.query.get(query)
        itens = self.conn.get(q)
        return itens



if __name__ == '__main__':
    print('')

