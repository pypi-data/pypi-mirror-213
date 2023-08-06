# -*- coding: utf-8 -*-

from trytond.pool import Pool
from .primanota import PrimaNota, PrimaNotaContext
from .analytic import PrimaNotaAnalytic

def register():
    Pool.register(
        PrimaNota,
        PrimaNotaContext,
        module='account_primanota', type_='model')
    Pool.register(
        PrimaNotaAnalytic,
        module='account_primanota', type_='model', depends=['analytic_account'])
