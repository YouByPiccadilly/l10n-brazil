# -*- coding: utf-8 -*-
# Copyright (C) 2009 - TODAY Renato Lima - Akretion
# © 2016 KMEE(http://www.kmee.com.br)
#   @author Luis Felipe Mileo <mileo@kmee.com.br>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import models, fields, api
from openerp.addons import decimal_precision as dp
from openerp.exceptions import Warning as UserError

OPERATION_TYPE = {
    'out_invoice': 'output',
    'in_invoice': 'input',
    'out_refund': 'input',
    'in_refund': 'output'
}

JOURNAL_TYPE = {
    'out_invoice': 'sale',
    'in_invoice': 'purchase',
    'out_refund': 'sale_refund',
    'in_refund': 'purchase_refund'
}

FIELD_STATE = {'draft': [('readonly', False)]}


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'
    _order = 'date_invoice DESC, internal_number DESC'

    @api.one
    @api.depends(
        'move_id.line_id.reconcile_id.line_id',
        'move_id.line_id.reconcile_partial_id.line_partial_ids',
    )
    def _compute_receivables(self):
        lines = self.env['account.move.line']
        for line in self.move_id.line_id:
            if line.account_id.id == self.account_id.id and \
                line.account_id.type in ('receivable', 'payable') and \
                    self.journal_id.revenue_expense:
                lines |= line
        self.move_line_receivable_id = (lines).sorted()

    @api.multi
    @api.depends('invoice_line', 'tax_line.amount')
    def _amount_all_service(self):
        for inv in self:
            inv.amount_services = sum(
                line.price_subtotal for line in inv.invoice_line)
            inv.issqn_base = sum(line.issqn_base for line in inv.invoice_line)
            inv.issqn_value = sum(
                line.issqn_value for line in inv.invoice_line)
            inv.service_pis_value = sum(
                line.pis_value for line in inv.invoice_line)
            inv.service_cofins_value = sum(
                line.cofins_value for line in inv.invoice_line)
            inv.csll_base = sum(line.csll_base for line in inv.invoice_line)
            inv.csll_value = sum(line.csll_value for line in inv.invoice_line)
            inv.ir_base = sum(line.ir_base for line in inv.invoice_line)
            inv.ir_value = sum(line.ir_value for line in inv.invoice_line)
            inv.inss_base = sum(line.inss_base for line in inv.invoice_line)
            inv.inss_value = sum(line.inss_value for line in inv.invoice_line)

            inv.amount_total = inv.amount_tax + inv.amount_untaxed
            inv.amount_wh = (inv.issqn_value_wh + inv.pis_value_wh + inv.
                             cofins_value_wh + inv.csll_value_wh + inv.
                             irrf_value_wh + inv.inss_value_wh)

    @api.multi
    @api.depends('amount_total', 'amount_wh')
    def _amount_net(self):
        for inv in self:
            inv.amount_net = inv.amount_total - inv.amount_wh

    state = fields.Selection(
        selection_add=[
            ('sefaz_export', 'Enviar para Receita'),
            ('sefaz_exception', u'Erro de autorização da Receita'),
            ('sefaz_cancelled', 'Cancelado no Sefaz'),
            ('sefaz_denied', 'Denegada no Sefaz'),
        ])
    move_line_receivable_id = fields.Many2many(
        'account.move.line', string='Receivables',
        compute='_compute_receivables')
    document_serie_id = fields.Many2one(
        'l10n_br_account.document.serie', string=u'Série',
        domain="[('fiscal_document_id', '=', fiscal_document_id),\
        ('company_id','=',company_id)]", readonly=True,
        states={'draft': [('readonly', False)]})
    fiscal_document_id = fields.Many2one(
        'l10n_br_account.fiscal.document', string='Documento', readonly=True,
        states={'draft': [('readonly', False)]})
    fiscal_document_electronic = fields.Boolean(
        related='fiscal_document_id.electronic', type='boolean', readonly=True,
        store=True, string='Electronic')
    fiscal_document_code = fields.Char(
        related='fiscal_document_id.code',
        readonly=True,
        store=True,
        string='Document Code')
    fiscal_category_id = fields.Many2one(
        'l10n_br_account.fiscal.category', 'Categoria Fiscal',
        readonly=True, states={'draft': [('readonly', False)]})
    fiscal_position = fields.Many2one(
        'account.fiscal.position', 'Fiscal Position', readonly=True,
        states={'draft': [('readonly', False)]},
    )
    account_document_event_ids = fields.One2many(
        'l10n_br_account.document_event', 'document_event_ids',
        u'Eventos')
    fiscal_comment = fields.Text(u'Observação Fiscal')
    cnpj_cpf = fields.Char(
        string=u'CNPJ/CPF',
        related='partner_id.cnpj_cpf',
    )
    legal_name = fields.Char(
        string=u'Razão Social',
        related='partner_id.legal_name',
    )
    ie = fields.Char(
        string=u'Inscrição Estadual',
        related='partner_id.inscr_est',
    )
    revenue_expense = fields.Boolean(
        related='journal_id.revenue_expense',
        readonly=True,
        store=True,
        string='Gera Financeiro'
    )
    issqn_wh = fields.Boolean(
        u'Retém ISSQN', readonly=True, states=FIELD_STATE)

    issqn_value_wh = fields.Float(
        u'Valor da retenção do ISSQN', readonly=True,
        states=FIELD_STATE, digits_compute=dp.get_precision('Account'))
    pis_wh = fields.Boolean(
        u'Retém PIS', readonly=True, states=FIELD_STATE)
    pis_value_wh = fields.Float(
        u'Valor da retenção do PIS', readonly=True,
        states=FIELD_STATE, digits_compute=dp.get_precision('Account'))
    cofins_wh = fields.Boolean(
        u'Retém COFINS', readonly=True, states=FIELD_STATE)
    cofins_value_wh = fields.Float(
        u'Valor da retenção do Cofins', readonly=True,
        states=FIELD_STATE, digits_compute=dp.get_precision('Account'))
    csll_wh = fields.Boolean(
        u'Retém CSLL', readonly=True, states=FIELD_STATE)
    csll_value_wh = fields.Float(
        u'Valor da retenção de CSLL', readonly=True,
        states=FIELD_STATE, digits_compute=dp.get_precision('Account'))
    irrf_wh = fields.Boolean(
        u'Retém IRRF', readonly=True, states=FIELD_STATE)
    irrf_base_wh = fields.Float(
        u'Base de calculo retenção do IRRF', readonly=True,
        states=FIELD_STATE, digits_compute=dp.get_precision('Account'))
    irrf_value_wh = fields.Float(
        u'Valor da retenção de IRRF', readonly=True,
        states=FIELD_STATE, digits_compute=dp.get_precision('Account'))
    inss_wh = fields.Boolean(
        u'Retém INSS', readonly=True, states=FIELD_STATE)
    inss_base_wh = fields.Float(
        u'Base de Cálculo da Retenção da Previdência Social', readonly=True,
        states=FIELD_STATE, digits_compute=dp.get_precision('Account'))
    inss_value_wh = fields.Float(
        u'Valor da Retenção da Previdência Social ', readonly=True,
        states=FIELD_STATE, digits_compute=dp.get_precision('Account'))
    csll_base = fields.Float(
        string=u'Base CSLL', compute='_amount_all_service',
        digits_compute=dp.get_precision('Account'), store=True)
    csll_value = fields.Float(
        string=u'Valor CSLL', compute='_amount_all_service',
        digits_compute=dp.get_precision('Account'), store=True)
    ir_base = fields.Float(
        string=u'Base IR', compute='_amount_all_service',
        digits_compute=dp.get_precision('Account'), store=True)
    ir_value = fields.Float(
        string=u'Valor IR', compute='_amount_all_service',
        digits_compute=dp.get_precision('Account'), store=True)
    issqn_base = fields.Float(
        string=u'Base de Cálculo do ISSQN', compute='_amount_all_service',
        digits_compute=dp.get_precision('Account'), store=True)
    issqn_value = fields.Float(
        string=u'Valor do ISSQN', compute='_amount_all_service',
        digits_compute=dp.get_precision('Account'), store=True)
    inss_base = fields.Float(
        string=u'Valor do INSS', compute='_amount_all_service',
        digits_compute=dp.get_precision('Account'), store=True)
    inss_value = fields.Float(
        string=u'Valor do INSS', compute='_amount_all_service',
        digits_compute=dp.get_precision('Account'), store=True)
    service_pis_value = fields.Float(
        string=u'Valor do Pis sobre Serviços', compute='_amount_all_service',
        digits_compute=dp.get_precision('Account'), store=True)
    service_cofins_value = fields.Float(
        string=u'Valor do Cofins sobre Serviços',
        compute='_amount_all_service',
        store=True, digits_compute=dp.get_precision('Account'))
    amount_services = fields.Float(
        string=u'Total dos serviços',
        compute='_amount_all_service',
        store=True,
        digits_compute=dp.get_precision('Account'))
    amount_wh = fields.Float(
        string=u'Total de retenção',
        compute='_amount_all_service',
        store=True,
        digits_compute=dp.get_precision('Account'))
    amount_net = fields.Float(
        string=u'Total Líquido', compute='_amount_net',
        digits_compute=dp.get_precision('Account'))

    @api.multi
    def name_get(self):
        lista = []
        for obj in self:
            name = obj.internal_number if obj.internal_number else ''
            lista.append((obj.id, name))
        return lista

    @api.one
    @api.constrains('number')
    def _check_invoice_number(self):
        domain = []
        if self.number:
            fiscal_document = self.fiscal_document_id and\
                self.fiscal_document_id.id or False
            domain.extend([('internal_number', '=', self.number),
                           ('fiscal_type', '=', self.fiscal_type),
                           ('fiscal_document_id', '=', fiscal_document)
                           ])
            if self.issuer == '0':
                domain.extend([
                    ('company_id', '=', self.company_id.id),
                    ('internal_number', '=', self.number),
                    ('fiscal_document_id', '=', self.fiscal_document_id.id),
                    ('issuer', '=', '0')])
            else:
                domain.extend([
                    ('partner_id', '=', self.partner_id.id),
                    ('vendor_serie', '=', self.vendor_serie),
                    ('issuer', '=', '1')])

            invoices = self.env['account.invoice'].search(domain)
            if len(invoices) > 1:
                raise UserError(u'Não é possível registrar documentos\
                              fiscais com números repetidos.')

    _sql_constraints = [
        ('number_uniq', 'unique(number, company_id, journal_id,\
         type, partner_id)', 'Invoice Number must be unique per Company!'),
    ]

    def withholding_map(self, cr, uid, **kwargs):
        result = {}
        obj_partner = self.pool.get('res.partner').browse(
            cr, uid, kwargs.get('partner_id', False))
        obj_company = self.pool.get('res.company').browse(
            cr, uid, kwargs.get('company_id', False))

        result['issqn_wh'] = obj_company.issqn_wh or obj_partner.\
            partner_fiscal_type_id.issqn_wh
        result['inss_wh'] = obj_company.inss_wh or obj_partner.\
            partner_fiscal_type_id.inss_wh
        result['pis_wh'] = obj_company.pis_wh or obj_partner.\
            partner_fiscal_type_id.pis_wh
        result['cofins_wh'] = obj_company.cofins_wh or obj_partner.\
            partner_fiscal_type_id.cofins_wh
        result['csll_wh'] = obj_company.csll_wh or obj_partner.\
            partner_fiscal_type_id.csll_wh
        result['irrf_wh'] = obj_company.irrf_wh or obj_partner.\
            partner_fiscal_type_id.irrf_wh

        return result

    def onchange_partner_id(self, cr, uid, ids, type, partner_id,
                            date_invoice=False, payment_term=False,
                            partner_bank_id=False, company_id=False,
                            fiscal_category_id=False):

        result = super(AccountInvoice, self).onchange_partner_id(
            cr, uid, ids, type, partner_id, date_invoice, payment_term,
            partner_bank_id, company_id, fiscal_category_id)

        result['value'].update(self.withholding_map(
            cr, uid, partner_id=partner_id, company_id=company_id))

        return result

    @api.multi
    def _set_move_lines_withholding(self, move_lines):

        self.compute_withholding()

        # What we do here? IMPORTANT
        # We make a copy of the retention tax and calculate the new total
        # in the payment lines
        value_to_debit = 0.0
        move_lines_new = []
        move_lines_tax = [move for move in move_lines
                          if not move[2]['product_id'] and
                          not move[2]['date_maturity']]
        move_lines_payment = [move for move in move_lines
                              if not move[2]['product_id'] and
                              move[2]['date_maturity']]
        move_lines_products = [move for move in move_lines
                               if move[2]['product_id'] and
                               not move[2]['date_maturity']]

        move_lines_new.extend(move_lines_products)

        def copy_move(move):
            copy = (0, 0, move[2].copy())
            copy[2]['debit'] = move[2]['credit']
            copy[2]['credit'] = move[2]['debit']
            copy[2]['name'] += u'- Retenção'
            return copy

        for move in move_lines_tax:
            move_lines_new.append(move)

            tax_code = self.env['account.tax.code'].browse(
                move[2]['tax_code_id'])

            if tax_code.domain == 'issqn' and self.issqn_wh:
                value_to_debit += move[2]['credit'] or move[2]['debit']
                move_lines_new.append(copy_move(move))

            if tax_code.domain == 'pis' and self.pis_wh:
                value_to_debit += move[2]['credit'] or move[2]['debit']
                move_lines_new.append(copy_move(move))

            if tax_code.domain == 'cofins' and self.cofins_wh:
                value_to_debit += move[2]['credit'] or move[2]['debit']
                move_lines_new.append(copy_move(move))

            if tax_code.domain == 'inss' and self.inss_wh:
                value_to_debit += move[2]['credit'] or move[2]['debit']
                move_lines_new.append(copy_move(move))

            if tax_code.domain == 'csll' and self.csll_wh:
                value_to_debit += move[2]['credit'] or move[2]['debit']
                move_lines_new.append(copy_move(move))

            if tax_code.domain == 'irpj' and self.irrf_wh:
                value_to_debit += move[2]['credit'] or move[2]['debit']
                move_lines_new.append(copy_move(move))

        move_lines_new.extend(move_lines_payment)

        if value_to_debit > 0.0:
            value_item = value_to_debit / float(len(move_lines_payment))
            for move in move_lines_payment:
                if move[2]['debit']:
                    move[2]['debit'] = move[2]['debit'] - value_item
                elif move[2]['credit']:
                    move[2]['credit'] = move[2]['credit'] - value_item

        return move_lines_new

    @api.multi
    def compute_withholding(self):
        for inv in self:
            if inv.pis_value > inv.company_id.cofins_csll_pis_wh_base and \
                    inv.pis_wh:
                inv.pis_value_wh = inv.pis_value
            else:
                inv.pis_wh = False
                inv.pis_value_wh = 0.0

            if inv.cofins_value > inv.company_id.cofins_csll_pis_wh_base and \
                    inv.cofins_wh:
                inv.cofins_value_wh = inv.cofins_value
            else:
                inv.cofins_wh = False
                inv.cofins_value_wh = 0.0

            if inv.csll_value > inv.company_id.cofins_csll_pis_wh_base and \
                    inv.csll_wh:
                inv.csll_value_wh = inv.csll_value
            else:
                inv.csll_wh = False
                inv.csll_value_wh = 0.0

            if inv.issqn_wh:
                inv.issqn_value_wh = inv.issqn_value
            else:
                inv.issqn_value_wh = 0.0

            if inv.ir_value > inv.company_id.irrf_wh_base and inv.irrf_wh:
                inv.irrf_value_wh = inv.ir_value
                inv.irrf_base_wh = inv.ir_base
            else:
                inv.irrf_wh = False
                inv.irrf_value_wh = 0.0

            if inv.inss_value > inv.company_id.inss_wh_base and inv.inss_wh:
                inv.inss_base_wh = inv.inss_base
                inv.inss_value_wh = inv.inss_value
            else:
                inv.inss_wh = False
                inv.inss_value_wh = 0.0

            inv.amount_wh = inv.issqn_value_wh + inv.pis_value_wh + inv.\
                cofins_value_wh + inv.csll_value_wh + inv.irrf_value_wh + inv.\
                inss_value_wh

    @api.multi
    def finalize_invoice_move_lines(self, move_lines):
        """ finalize_invoice_move_lines(move_lines) -> move_lines

            Hook method to be overridden in additional modules to verify and
            possibly alter the move lines to be created by an invoice, for
            special cases.
            :param move_lines: list of dictionaries with the account.move.lines
            (as for create())
            :return: the (possibly updated) final move_lines to create for this
            invoice
        """
        move_lines = super(
            AccountInvoice, self).finalize_invoice_move_lines(move_lines)
        count = 1
        total = len([x for x in move_lines
                     if x[2]['account_id'] == self.account_id.id])
        number = self.name or self.number
        result = []
        for move_line in move_lines:
            if move_line[2]['debit'] or move_line[2]['credit']:
                if move_line[2]['account_id'] == self.account_id.id:
                    move_line[2]['name'] = '%s/%s-%s' % \
                        (number, count, total)
                    count += 1
                result.append(move_line)

        result = self._set_move_lines_withholding(result)

        return result


class AccountInvoiceLine(models.Model):
    _inherit = 'account.invoice.line'

    @api.one
    @api.depends('price_unit', 'discount', 'invoice_line_tax_id',
                 'quantity', 'product_id', 'invoice_id.partner_id',
                 'invoice_id.currency_id')
    def _compute_price(self):
        price = self.price_unit * (1 - (self.discount or 0.0) / 100.0)
        taxes = self.invoice_line_tax_id.compute_all(
            price, self.quantity, product=self.product_id,
            partner=self.invoice_id.partner_id,
            fiscal_position=self.fiscal_position)
        self.price_subtotal = taxes['total']
        self.price_tax_discount = taxes['total'] - taxes['total_tax_discount']
        if self.invoice_id:
            self.price_subtotal = self.invoice_id.currency_id.round(
                self.price_subtotal)
            self.price_tax_discount = self.invoice_id.currency_id.round(
                self.price_tax_discount)

    invoice_line_tax_id = fields.Many2many(
        'account.tax', 'account_invoice_line_tax', 'invoice_line_id',
        'tax_id', string='Taxes', domain=[('parent_id', '=', False)])
    fiscal_category_id = fields.Many2one(
        'l10n_br_account.fiscal.category', 'Categoria Fiscal')
    fiscal_position = fields.Many2one(
        'account.fiscal.position', u'Posição Fiscal',
    )
    price_tax_discount = fields.Float(
        string='Price Tax discount', store=True,
        digits=dp.get_precision('Account'),
        readonly=True, compute='_compute_price')
    csll_base = fields.Float('Base CSLL', required=True, default=0.0,
                             digits_compute=dp.get_precision('Account'))
    csll_value = fields.Float('Valor CSLL', required=True, default=0.0,
                              digits_compute=dp.get_precision('Account'))
    csll_percent = fields.Float('Perc CSLL', required=True, default=0.0,
                                digits_compute=dp.get_precision('Discount'))
    ir_base = fields.Float('Base IR', required=True, default=0.0,
                           digits_compute=dp.get_precision('Account'))
    ir_value = fields.Float('Valor IR', required=True, default=0.0,
                            digits_compute=dp.get_precision('Account'))
    ir_percent = fields.Float('Perc IR', required=True, default=0.0,
                              digits_compute=dp.get_precision('Discount'))
    inss_base = fields.Float('Base INSS', required=True, default=0.0,
                             digits_compute=dp.get_precision('Account'))
    inss_value = fields.Float('Valor INSS', required=True, default=0.0,
                              digits_compute=dp.get_precision('Account'))
    inss_percent = fields.Float('Perc. INSS', required=True, default=0.0,
                                digits_compute=dp.get_precision('Discount'))

    @api.model
    def move_line_get_item(self, line):
        """
            Overrrite core to fix invoice total account.move
        :param line:
        :return:
        """
        res = super(AccountInvoiceLine, self).move_line_get_item(line)
        res['price'] = line.price_tax_discount
        return res

    def _amount_tax_csll(self, cr, uid, tax=False):
        result = {
            'csll_base': tax.get('total_base', 0.0),
            'csll_value': tax.get('amount', 0.0),
            'csll_percent': tax.get('percent', 0.0) * 100,
        }
        return result

    def _amount_tax_irpj(self, cr, uid, tax=False):
        result = {
            'ir_base': tax.get('total_base', 0.0),
            'ir_value': tax.get('amount', 0.0),
            'ir_percent': tax.get('percent', 0.0) * 100,
        }
        return result

    def _amount_tax_inss(self, cr, uid, tax=False):
        result = {
            'inss_base': tax.get('total_base', 0.0),
            'inss_value': tax.get('amount', 0.0),
            'inss_percent': tax.get('percent', 0.0) * 100,
        }
        return result
