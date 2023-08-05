# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.

try:
    from trytond.modules.account_stock_landed_cost_weight.tests.test_account_stock_landed_cost_weight import suite
except ImportError:
    from .test_account_stock_landed_cost_weight import suite

__all__ = ['suite']
