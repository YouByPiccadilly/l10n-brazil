# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2015 KMEE INFORMATICA LTDA - Luis Felipe Miléo
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
import logging

from itertools import groupby
from operator import itemgetter
from openerp.openupgrade import openupgrade
from openerp import pooler, SUPERUSER_ID

logger = logging.getLogger('OpenUpgrade.l10n_br_account_product')


def load_data(cr):
    openupgrade.load_data(cr, 'l10n_br_account_product',
                          'migrations/8.0.2.0.0/modified_data.xml',
                          mode='init')

@openupgrade.migrate()
def migrate(cr, version):
    load_data(cr)
    cr.execute("UPDATE product_template SET fiscal_classification_id=ncm_id")
