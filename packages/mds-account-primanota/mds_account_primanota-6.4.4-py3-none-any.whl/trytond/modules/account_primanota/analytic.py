# -*- coding: utf-8 -*-
# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.


from trytond.pool import PoolMeta, Pool
from trytond.model import fields
from trytond.transaction import Transaction
from sql.conditionals import Case


class PrimaNotaAnalytic(metaclass=PoolMeta):
    __name__ = 'account_primanota.primanota'

    analytic_lines = fields.One2Many(string='Analytic Lines',
        model_name='analytic_account.line', field='move_line',
        readonly=True)
    has_analytic_lines = fields.Function(fields.Boolean(
        string='Analytic Lines', readonly=True,
        help='Account move line has analytic lines.'),
        'get_has_analyticlines',
        searcher='search_has_analytic_lines')

    @classmethod
    def get_has_analyticlines_sql(cls):
        """ get sql-code for query
        """
        pool = Pool()
        AnalyticLine = pool.get('analytic_account.line')
        PrimaNota = pool.get('account_primanota.primanota')
        tab_anline = AnalyticLine.__table__()
        tab_pn = PrimaNota.__table__()

        query = tab_pn.join(
                tab_anline,
                condition=tab_anline.move_line == tab_pn.id,
                type_='LEFT OUTER',
            ).select(
                tab_pn.id,
                Case(
                    (tab_anline.id != None, True),
                    else_=False,
                ).as_('has_analytic'),
            )
        return (query, tab_pn)

    @classmethod
    def search_has_analytic_lines(cls, names, clause):
        """ search in has-analytic-lines
        """
        Operator = fields.SQL_OPERATORS[clause[1]]
        (tab_query, tab_pn) = cls.get_has_analyticlines_sql()

        query = tab_query.select(
                tab_query.id,
                where=Operator(tab_query.has_analytic, clause[2]),
            )
        return [('id', 'in', query)]

    @classmethod
    def get_has_analyticlines(cls, lines, names):
        """ return True if move-line is linked to analytic lines
        """
        pool = Pool()
        cursor = Transaction().connection.cursor()

        (query, tab_pn) = cls.get_has_analyticlines_sql()
        query.where = tab_pn.id.in_([x.id for x in lines])
        cursor.execute(*query)
        records = cursor.fetchall()

        result = {x: {y.id: None for y in lines} for x in names}
        for record in records:
            values = {
                'has_analytic_lines': record[1],
                }
            for name in names:
                result[name][record[0]] = values[name]
        return result

# end PrimaNotaAnalytic
