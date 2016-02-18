# -*- encoding: utf-8 -*-
##############################################################################
#
#    Daniel Sadamo
#    Fernando Marcato
#    Copyright (C) 2016 - KMEE INFORMATICA LTDA <Http://kmee.com.br>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see http://www.gnu.org/licenses/.
#
##############################################################################

import openerp.addons.decimal_precision as dp
from openerp import models, fields, api, exceptions, _

_IND_MOV = [('0', u'Bloco com dados informados'),
            ('1', u'Bloco sem dados informados')]
_S_N = [('S', u'Sim'),
        ('N', u'Não')]
_COD_DISP = [
    ('00', u'Formulário de Segurança (FS) ­ impressor autônomo'),
    ('01', u'FS­DA ­ Formulário de Segurança para Impressão de Danfe'),
    ('02', u'Formulário de segurança ­ NF­e'),
    ('03', u'Formulário Contínuo'),
    ('04', u'Blocos'),
    ('05', u'Jogos Soltos'),
]


class L10nBrSpedFiscalBlocoZeroRegistroTemplate(models.Model):
    _name = 'l10n_br.sped.fiscal.bloco.zero.registro.template'
    _description = u"TEMPLATE DE REGISTRO"

    bloco_id = fields.Many2one('l10n_br.sped.fiscal.bloco.zero', string='Bloco')
    REG = fields.Char(string='REG', readonly=True)


_COD_FIN = [('0', 'Remessa do arquivo original'),
            ('1', 'Remessa do arquivo subistituto')]

_IND_PERFIL = [('A', 'Perfil A'),
               ('B', 'Perfil B'),
               ('C', 'Perfil C')]

_IND_ATIV = [('0', 'Industrial ou equiparado a industrial'),
             ('1', 'Outros')]


class L10nBrSpedFiscalBlocoZeroRegistro0000(models.Model):
    _name = 'l10n_br.sped.fiscal.bloco.zero.registro0000'
    _description = u"Abertura  do  Arquivo  Digital  e " \
                   u"Identificação da Entidade"

    bloco_id = fields.Many2one(
        'l10n_br.sped.fiscal.bloco.zero', string=u'Bloco')
    REG = fields.Char(string='REG', readonly=True, default='0000')
    COD_VER = fields.Char(string=u'Versão do Leiaute', readonly=True)
    COD_FIN = fields.Selection(
        selection=_COD_FIN, string=u'Código da Finalidade', readonly=True)
    DT_INI = fields.Date(string=u'Data Inicial', readonly=True)
    DT_FIN = fields.Date(string=u'Data Final', readonly=True)
    NOME = fields.Char(string='nome', readonly=True)
    CNPJ = fields.Char(string='CNPJ', readonly=True)
    CPF = fields.Char(string='CPF', readonly=True)
    UF = fields.Char(string='Sigla da UF', readonly=True)
    IE = fields.Char(string='Inscr. Estadual', readonly=True)
    COD_MUN = fields.Char(string=u'Cód. Município IBGE', readonly=True)
    IM = fields.Char(string='Inscr. Municipal', readonly=True)
    SUFRAMA = fields.Char(string='SUFRAMA', readonly=True)
    IND_PERFIL = fields.Selection(string=u'Perfil de Apresentação',
                                  selection=_IND_PERFIL, readonly=True)
    IND_ATIV = fields.Selection(string='Tipo de atividade',
                                selection=_IND_ATIV, readonly=True)

_IND_MOV = [('0', 'Bloco com dados informados'),
             ('1', 'Bloco sem dados informados')]


class L10nBrSpedFiscalBlocoZeroRegistro0001(models.Model):
    _name = 'l10n_br.sped.fiscal.bloco.zero.registro0001'
    _description = u"Abertura  do  Bloco  0"

    bloco_id = fields.Many2one(
        'l10n_br.sped.fiscal.bloco.zero', string='Bloco')
    REG = fields.Char(string='REG', readonly=True, default='0001')
    IND_ATIV = fields.Selection(string='Tipo de atividade',
                                selection=_IND_MOV, readonly=True)


class L10nBrSpedFiscalBlocoZeroRegistro0005(models.Model):
    _name = 'l10n_br.sped.fiscal.bloco.zero.registro0005'
    _description = u"Dados  Complementares  da Entidade"

    bloco_id = fields.Many2one('l10n_br.sped.fiscal.bloco.zero', string='Bloco')
    REG = fields.Char(string='REG', readonly=True, default='0005')
    FANTASIA = fields.Char(string='Nome Fantasia')
    CEP = fields.Char(string='CEP')
    END = fields.Char(string=u'Logradouro e endereço')
    NUM = fields.Char(string=u'Número')
    COMPL = fields.Char(string='Complemento')
    BAIRRO = fields.Char(string='Bairro')
    FONE = fields.Char(string='Telefone(DDD+FONE)',)
    FAX = fields.Char(string='Fax', readonly=True,)
    EMAIL = fields.Char(string='Email', )


class L10nBrSpedFiscalBlocoZeroRegistro0150(models.Model):
    _name = 'l10n_br.sped.fiscal.bloco.zero.registro0150'
    _description = u"Tabela  de  cadastro  do participante"

    bloco_id = fields.Many2one('l10n_br.sped.fiscal.bloco.zero', string='Bloco')
    REG = fields.Char(string='REG', readonly=True, default='0150')
    COD_PART = fields.Char(string=u'Código de identificação')
    NOME = fields.Char(string='Nome pessoal ou empresarial')
    COD_PAIS = fields.Char(string=u'Código do país')
    CNPJ = fields.Char(string=u'CNPJ')
    CPF = fields.Char(string=u'CPF')
    IE = fields.Char(string=u'Inscrição Estadual (IE)')
    COD_MUN = fields.Char(string=u'Código do município')
    SUFRAMA = fields.Char(string='SUFRAMA',)
    END = fields.Char(string=u'Logradouro e endereço', readonly=True,)
    NUM = fields.Char(string=u'Número', )
    COMPL = fields.Char(string='Complemento', )
    BAIRRO = fields.Char(string='Bairro', )


class L10nBrSpedFiscalBlocoZeroRegistro0175(models.Model):
    _name = 'l10n_br.sped.fiscal.bloco.zero.registro0175'
    _description = u"Alteração  da  Tabela  de Cadastro de Participante"

    bloco_id = fields.Many2one('l10n_br.sped.fiscal.bloco.zero', string='Bloco')
    REG = fields.Char(string='REG', readonly=True, default='0175')
    DT_ALT = fields.Date(string=u'Data de alteração')
    NR_CAMPO = fields.Char(string=u'Número do campo alterado'
                                  u'(Somente campos 03 a 13, exceto 07).')
    CONT_ANT = fields.Char(string=u'Conteúdo anterior do campo')


class L10nBrSpedFiscalBlocoZeroRegistro0190(models.Model):
    _name = 'l10n_br.sped.fiscal.bloco.zero.registro0190'
    _description = u"Identificação das Unidades de Medida"

    bloco_id = fields.Many2one('l10n_br.sped.fiscal.bloco.zero', string='Bloco')
    REG = fields.Char(string='REG', readonly=True, default='0190')
    UNID = fields.Char(string=u'Código da UM')
    DESCR = fields.Char(string=u'Descrição da UM')


class L10nBrSpedFiscalBlocoZeroRegistro0200(models.Model):
    _name = 'l10n_br.sped.fiscal.bloco.zero.registro0200'
    _description = u"Informar mercadorias serviços e produtos"

    bloco_id = fields.Many2one(
        'l10n_br.sped.fiscal.bloco.zero', string=u'Bloco')
    REG = fields.Char(string=u'REG', readonly=True, default='0200')
    COD_ITEM = fields.Char(string=u'Código do item')
    DESCR_ITEM = fields.Char(string=u'Descrição do item')
    COD_BARRA = fields.Char(
        string=u'Representação alfanumérico do código de barra do produto')
    COD_ANT_ITEM = fields.Char(
        string=u'Código anterior do item com relação à última informação '
               u'apresentada')
    UNID_INV = fields.Char(
        string=u'Unidade de medida utilizada na quantificação de estoques')


class L10nBrSpedFiscalBlocoZeroRegistro0205(models.Model):
    _name = 'l10n_br.sped.fiscal.bloco.zero.registro0205'
    _description = u"Alteração do item"

    bloco_id = fields.Many2one(
        'l10n_br.sped.fiscal.bloco.zero', string=u'Bloco')
    REG = fields.Char(string='REG', readonly=True, default='0205')
    DESCR_ANT_ITEM = fields.Char(string=u'Descrição anterior do item')
    DT_INI = fields.Char(
        string=u'Data inicial de utilização da descrição do item')
    DT_FIM = fields.Char(
        string=u'Data final de utilização da descrição do item')
    COD_ANT_ITEM = fields.Char(
        string=u'Código anterior do item com relação à última'
               u'informação apresentada')


class L10nBrSpedFiscalBlocoZeroRegistro0400(models.Model):
    _name = 'l10n_br.sped.fiscal.bloco.zero.registro0400'
    _description = u"Tabela de Natureza da Operação/Prestação"

    bloco_id = fields.Many2one(
        'l10n_br.sped.fiscal.bloco.zero', string='Bloco')
    REG = fields.Char(string=u'REG', readonly=True, default='0400')
    COD_NAT = fields.Char(string=u'Código da natureza da operação/prestação')
    DESCR_NAT = fields.Char(
        string=u'Descrição da natureza da operação/prestação')


class L10nBrSpedFiscalBlocoZeroRegistro0450(models.Model):
    _name = 'l10n_br.sped.fiscal.bloco.zero.registro0450'
    _description = u"Tabela de Informação Complementar do Documento Fiscal"

    bloco_id = fields.Many2one('l10n_br.sped.fiscal.bloco.zero', string='Bloco')
    REG = fields.Char(string=u'REG', readonly=True, default='0450')
    COD_INF = fields.Char(
        string=u'Código da informação complementar do documento fiscal')
    TXT = fields.Char(string=u'Informação complementar de documento fiscal')


class L10nBrSpedFiscalBlocoZeroRegistro0990(models.Model):
    _name = 'l10n_br.sped.fiscal.bloco.zero.registro0990'
    _description = u"Encerramento do Bloco 0"

    bloco_id = fields.Many2one(
        'l10n_br.sped.fiscal.bloco.zero', string=u'Bloco')
    REG = fields.Char(string=u'REG', readonly=True, default='0990')
    QTD_LIN_0 = fields.Char(string=u'Quantidade total de linhas do Bloco 0.')


class L10nBrSpedFiscalBlocoUmRegistro1001(models.Model):
    _name = 'l10n_br.sped.fiscal.bloco.um.registro1001'
    _description = u"Abertura do Bloco 1"

    bloco_id = fields.Many2one(
        'l10n_br.sped.fiscal.bloco.um', string=u'Bloco')
    REG = fields.Char(string='REG', readonly=True, default='1001')
    IND_MOV = fields.Selection(
        selection=_IND_MOV, string=u'Indicador de movimento')


class L10nBrSpedFiscalBlocoUmRegistro1010(models.Model):
    _name = 'l10n_br.sped.fiscal.bloco.um.registro1010'
    _description = u"Obrigatoriedade Registros Bloco 1"

    bloco_id = fields.Many2one(
        'l10n_br.sped.fiscal.bloco.um', string=u'Bloco')
    REG = fields.Char(string='REG', readonly=True, default='1010')
    IND_EXP = fields.Selection(selection=_S_N, string=u'Ocorreu  averbação de exportação no período')
    IND_CCRF = fields.Selection(selection=_S_N, string=u'Existe info a cerca de crédito de ICMS')
    IND_COMB = fields.Selection(selection=_S_N, string=u'É comércio varejista de combustíveis')
    IND_USINA = fields.Selection(selection=_S_N, string=u'Usina de açúcar/álcool')
    IND_VA = fields.Selection(selection=_S_N, string=u'Existe info a ser prestada nesse registro')
    IND_EE = fields.Selection(selection=_S_N, string=u'É distribuidora de energia')
    IND_CART = fields.Selection(selection=_S_N, string=u'Realizou vendas com cartão de crédito/débito')
    IND_FORM = fields.Selection(selection=_S_N, string=u'Emitiu documento fiscal em papel em UF que exige controle')
    IND_AER = fields.Selection(selection=_S_N, string=u'Prestou serviço de transporte aéreo')


class L10nBrSpedFiscalBlocoUmRegistro1700(models.Model):
    _name = 'l10n_br.sped.fiscal.bloco.um.registro1700'
    _description = u"Documentos fiscais utilizados no período a que se refere o arquivo Sped­Fiscal"

    bloco_id = fields.Many2one(
        'l10n_br.sped.fiscal.bloco.um', string=u'Bloco')
    REG = fields.Char(string='REG', readonly=True, default='1700')
    COD_DISP = fields.Selection(
        selection=_COD_DISP, string=u'Código dispositivo autorizado')
    COD_MOD = fields.Char(string=u'Código do modelo do dispositivo')
    SER = fields.Char(string=u'Série do dispositivo')
    SUB = fields.Char(string=u'Subsérie do dispositivo')
    NUM_DOC_INI = fields.Char(string=u'Número do dispositivo inicial')
    NUM_DOC_FIN = fields.Char(string=u'Número do dispositivo final')
    NUM_AUT = fields.Char(string=u'Número da autorização')


class L10nBrSpedFiscalBlocoUmRegistro1990(models.Model):
    _name = 'l10n_br.sped.fiscal.bloco.um.registro1990'
    _description = u"Encerramento  do  Bloco  1"

    bloco_id = fields.Many2one(
        'l10n_br.sped.fiscal.bloco.um', string=u'Bloco')
    REG = fields.Char(string='REG', readonly=True, default='1990')
    QTD_LIN_1 = fields.Char(string=u'Quantidade total de linhas do Bloco 1')


# Bloco 9
class L10nBrSpedFiscalBlocoNoveRegistro9001(models.Model):
    _name = 'l10n_br.sped.fiscal.bloco.nove.registro'
    _description = u"Abertura do Bloco 9"

    bloco_id = fields.Many2one(
        'l10n_br.sped.fiscal.bloco.nove', string=u'Bloco')
    REG = fields.Char(string='REG', readonly=True, default='9001')
    IND_MOV = fields.Selection(
        selection=_IND_MOV, string=u'Indicador de movimento')







# Classe base para copiar e colar
# class L10nBrSpedFiscalBlocoNoveRegistro(models.Model):
#     _name = 'l10n_br.sped.fiscal.bloco.nove.registro'
#     _description = u""
#
#     bloco_id = fields.Many2one(
#         'l10n_br.sped.fiscal.bloco.nove', string=u'Bloco')
#     REG = fields.Char(string='REG', readonly=True, default='')
#     campo = fields.Char(string=u'')
#     campo = fields.Char(string=u'')
#     campo = fields.Char(string=u'')
#     campo = fields.Char(string=u'')
#     campo = fields.Char(string=u'')
#     campo = fields.Char(string=u'')
#     campo = fields.Char(string=u'')
#     campo = fields.Char(string=u'')
#     campo = fields.Char(string=u'')
#     campo = fields.Char(string=u'')
