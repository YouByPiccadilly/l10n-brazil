# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2015 KMEE (http://www.kmee.com.br)
#    @author Luis Felipe Miléo (mileo@kmee.com.br)
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
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp import models, fields


class ResConfig(models.Model):
    _inherit = 'account.config.settings'

    ipbt_token = fields.Char(
        string=u'IPBT Token',
        related='company_id.ipbt_token'
    )
    ibpt_update_days = fields.Integer(
        string=u'Quantidade de dias para Atualizar',
        related='company_id.ibpt_update_days'
    )
