# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.

from trytond.pool import Pool
from .account import *


def register():
    Pool.register(
        LandedCost,
        module='account_stock_landed_cost_weight', type_='model')
