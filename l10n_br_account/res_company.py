# -*- encoding: utf-8 -*-
###############################################################################
#                                                                             #
# Copyright (C) 2009  Renato Lima - Akretion                                  #
#                                                                             #
#This program is free software: you can redistribute it and/or modify         #
#it under the terms of the GNU Affero General Public License as published by  #
#the Free Software Foundation, either version 3 of the License, or            #
#(at your option) any later version.                                          #
#                                                                             #
#This program is distributed in the hope that it will be useful,              #
#but WITHOUT ANY WARRANTY; without even the implied warranty of               #
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the                #
#GNU Affero General Public License for more details.                          #
#                                                                             #
#You should have received a copy of the GNU Affero General Public License     #
#along with this program.  If not, see <http://www.gnu.org/licenses/>.        #
###############################################################################

from openerp.osv import orm, fields
from openerp.addons import decimal_precision as dp

COMPANY_WITHHOLDING_TYPE = [
    ('1', 'Regime de Caixa'),
    ('2', u'Regime de Competência'),
]

COMPANY_FISCAL_TYPE = [
    ('1', 'Simples Nacional'),
    ('2', 'Simples Nacional – excesso de sublimite de receita bruta'),
    ('3', 'Regime Normal')
]

COMPANY_FISCAL_TYPE_DEFAULT = '3'

SQL_CONSTRAINTS = [
    ('l10n_br_tax_definition_tax_id_uniq', 'unique (tax_id, company_id)',
    u'Imposto já existente nesta empresa!')
]


class ResCompany(orm.Model):
    _inherit = 'res.company'
    _columns = {
        'service_invoice_id': fields.many2one(
            'l10n_br_account.fiscal.document',
            'Documento Fiscal'),
        'document_serie_service_id': fields.many2one(
            'l10n_br_account.document.serie', u'Série Fiscais para Serviço',
            domain="[('company_id', '=', active_id),('active','=',True),"
            "('fiscal_type','=','service')]"),
        'annual_revenue': fields.float(
            'Faturamento Anual', required=True,
            digits_compute=dp.get_precision('Account'),
            help=u"Faturamento Bruto dos últimos 12 meses"),
        'fiscal_type': fields.selection(COMPANY_FISCAL_TYPE,
            u'Regime Tributário', required=True),
        'cnae_main_id': fields.many2one(
            'l10n_br_account.cnae', u'CNAE Primário'),
        'cnae_secondary_ids': fields.many2many(
            'l10n_br_account.cnae', 'res_company_l10n_br_account_cnae',
            'company_id', 'cnae_id', u'CNAE Segundários'),
        'ecnpj_a1_file': fields.binary('Arquivo e-CNPJ A1'),
        'ecnpj_a1_password': fields.char('Senha e-CNPJ A1', size=64),
        'fiscal_rule_parent_id': fields.many2one(
            'account.fiscal.position.rule', u'Conjunto de Regras Fiscais',
            domain="[('parent_id', '=', False)]"),
        'wh_type': fields.selection(COMPANY_WITHHOLDING_TYPE,
            u'Forma de Retenção',  help=u"Regime de Caixa: A retenção é aplicada caso soma dos vencimentos\
            mensais utrapasse os limites; Regime de Competência: A retenção é aplicada caso a soma do valor faturado \
              ultrapasse os limites"),
        'wh_on_nfe_limit': fields.boolean(
            u'Retenção sempre que ultrapassar o valor da NF?'),
        'irrf_wh_percent': fields.float(
            u'Alícota de IRRF (%)',
            digits_compute=dp.get_precision('Account')),
        'irrf_wh_value': fields.float(
            u'Valor mínimo IRRF',
            digits_compute=dp.get_precision('Account')),
        'cofins_wh_value': fields.float(
            u'Valor mínimo COFINS',
            digits_compute=dp.get_precision('Account')),
        'pis_wh_value': fields.float(
            u'Valor mínimo PIS',
            digits_compute=dp.get_precision('Account')),
        'csll_wh_value': fields.float(
            u'Valor mínimo CSLL',
            digits_compute=dp.get_precision('Account')),
        'issqn_wh': fields.boolean(
            u'Retém ISSQN'),
        'inss_wh': fields.boolean(
            u'Retém INSS'),
        'pis_wh': fields.boolean(
            u'Retém PIS'),
        'cofins_wh': fields.boolean(
            u'Retém COFINS'),
        'csll_wh': fields.boolean(
            u'Retém CSLL'),

    }
    _defaults = {
        'fiscal_type': COMPANY_FISCAL_TYPE_DEFAULT,
        'annual_revenue': 0.00,
    }
