# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.

try:
    from trytond.modules.carrier_weight.tests.test_carrier_weight import suite
except ImportError:
    from .test_carrier_weight import suite

__all__ = ['suite']
