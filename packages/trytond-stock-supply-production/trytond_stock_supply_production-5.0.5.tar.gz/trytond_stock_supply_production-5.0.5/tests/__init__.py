# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.

try:
    from trytond.modules.stock_supply_production.tests.test_stock_supply_production import suite
except ImportError:
    from .test_stock_supply_production import suite

__all__ = ['suite']
