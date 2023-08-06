# -*- coding: utf-8 -*-
# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.

from trytond.model import ModelSQL, ModelView, fields
from trytond.pool import Pool
from trytond.pyson import Eval
from trytond.report import Report
from trytond.cache import Cache
from trytond.transaction import Transaction
from trytond.modules.account.account import GeneralLedgerAccountContext
from sql import Literal
from sql.functions import Abs, Round
from sql.conditionals import Case


class PrimaNota(ModelSQL, ModelView):
    'Primanota'
    __name__ = 'account_primanota.primanota'

    movenumber = fields.Char(string='Number', readonly=True,
        help='Number of Move')
    post_number = fields.Char(string='Post Number', readonly=True,
        help='Also known as Folio Number.')
    period = fields.Many2One(string='Period', readonly=True,
        model_name='account.period')
    journal = fields.Many2One(string='Journal', readonly=True,
        model_name='account.journal')
    date = fields.Date(string='Effective Date', readonly=True)
    post_date = fields.Date(string='Post Date', readonly=True)
    description = fields.Char(string='Description', readonly=True)
    line_description = fields.Char(string='Line Description', readonly=True)
    origin2 = fields.Reference(string='Origin',
        selection='get_move_originsel', readonly=True)
    origin = fields.Function(fields.Reference(string='Origin',
        help='Origin of the Move',
        selection='get_move_originsel', readonly=True),
        'on_change_with_origin', searcher='search_origin')
    line_origin2 = fields.Reference(string='Line Origin',
        selection='get_line_originsel', readonly=True)
    line_origin = fields.Function(fields.Reference(string='Line Origin',
        help='Origin of the Moveline',
        selection='get_line_originsel', readonly=True),
        'on_change_with_line_origin', searcher='search_line_origin')
    state = fields.Selection(string='State', readonly=True,
        selection=[
            ('draft', 'Draft'),
            ('posted', 'Posted'),
        ])
    debit = fields.Numeric(string='Debit', readonly=True,
        digits=(16, Eval('currency_digits', 2)),
        depends=['currency_digits'])
    credit = fields.Numeric(string='Credit', readonly=True,
        digits=(16, Eval('currency_digits', 2)),
        depends=['currency_digits'])
    account = fields.Many2One(string='Account', readonly=True,
        model_name='account.account')
    account_code = fields.Char(string='Account Code', readonly=True)
    party = fields.Many2One(string='Party', readonly=True,
        model_name='party.party')
    reconciliation = fields.Many2One(string='Reconciliation',
        model_name='account.move.reconciliation',
        readonly=True)
    reconciliations_delegated = fields.One2Many(
        model_name='account.move.reconciliation', field='delegate_to',
        string="Reconciliations Delegated", readonly=True)
    tax_lines = fields.One2Many(string='Tax Lines',
        model_name='account.tax.line', field='move_line')
    amount_second_currency = fields.Numeric(string='Amount Second Currency',
        digits=(16, Eval('second_currency_digits', 2)),
        help='The amount expressed in a second currency.',
        readonly=True, depends=['second_currency_digits'])
    rate_second_currency = fields.Numeric(string='Rate',
        digits=(16, 4), readonly=True,
        help='The exchange rate of the second currency.')
    second_currency = fields.Many2One(string='Second Currency',
        model_name='currency.currency', readonly=True,
        help='The second currency.')

    currency = fields.Function(fields.Many2One(string="Currency",
        model_name='currency.currency'),
        'on_change_with_currency')
    currency_digits = fields.Function(fields.Integer(
        string='Currency Digits'),
        'on_change_with_currency_digits')
    second_currency_digits = fields.Function(fields.Integer(
        string='Second Currency Digits'),
        'on_change_with_second_currency_digits')

    _model_has_field_cache = Cache('account_primanota.primanota.model_has_field')

    @classmethod
    def __setup__(cls):
        super(PrimaNota, cls).__setup__()
        cls._order.insert(0, ('date', 'DESC'))
        cls._order.insert(1, ('movenumber', 'DESC'))
        cls._order.insert(2, ('id', 'DESC'))

    def get_rec_name(self, name):
        """ create rec_name
        """
        account_code = getattr(self.account, 'code', None)
        if account_code is None:
            account_code = '-'

        return '%(movenumber)s [%(post_number)s] %(date)s %(account)s %(debit)s/%(credit)s' % {
            'movenumber': self.movenumber or '-',
            'post_number': self.post_number or '-',
            'account': account_code,
            'debit': Report.format_currency(self.debit or 0, None, self.currency),
            'credit': Report.format_currency(self.credit or 0, None, self.currency),
            'date': Report.format_date(self.date),
            }

    @fields.depends('origin2')
    def on_change_with_origin(self, name=None):
        if self.origin2:
            return str(self.origin2)

    @classmethod
    def search_origin(cls, name, clause):
        """ search for 'rec_name' in move-origin
        """
        return cls.get_searcher_clause(
            name, clause, 'origin',
            [x[0] for x in cls.get_move_originsel()])

    @fields.depends('line_origin2')
    def on_change_with_line_origin(self, name=None):
        if self.line_origin2:
            return str(self.line_origin2)

    @classmethod
    def search_line_origin(cls, name, clause):
        """ search for 'rec_name' in line_origin
        """
        return cls.get_searcher_clause(
            name, clause, 'line_origin',
            [x[0] for x in cls.get_line_originsel()])

    @classmethod
    def get_searcher_clause(cls, name, clause, fieldname, type_lst):
        """ generate clause
        """
        pool = Pool()

        query = []
        fieldname2 = '%s2' % fieldname
        clause2 = (fieldname2 + clause[0][len(fieldname):],) + tuple(clause[1:])

        if len(clause2) > 3:
            query.append(clause2)
        else :
            for x in type_lst:
                if x is None:
                    continue
                if clause2[0] == fieldname2:
                    query.append((clause2[0] + '.rec_name',) + tuple(list(clause[1:]) + [x]))
                else :
                    # check if field is in model
                    field_chain = clause2[0].split('.')
                    if len(field_chain) > 1:
                        cache_key = '%s:%s' % (x, field_chain[1])

                        has_field = cls._model_has_field_cache.get(cache_key)
                        if has_field is None:
                            Model = pool.get(x)

                            has_field = field_chain[1] in Model._fields.keys()
                            cls._model_has_field_cache.set(cache_key, has_field)

                        if has_field:
                            query.append(tuple(list(clause2) + [x]))

        if len(query) > 1:
            query = ['OR'] + query
        return query

    @classmethod
    def search_rec_name(cls, name, clause):
        return ['OR',
            ('movenumber',) + tuple(clause[1:]),
            ('post_number',) + tuple(clause[1:]),
            ('description',) + tuple(clause[1:]),
            ('line_description',) + tuple(clause[1:]),
            ('party',) + tuple(clause[1:]),
            ]

    @fields.depends('account')
    def on_change_with_currency(self, name=None):
        if self.account:
            return self.account.currency.id

    @fields.depends('account')
    def on_change_with_currency_digits(self, name=None):
        if self.account:
            return self.account.currency_digits
        else:
            return 2

    @fields.depends('second_currency')
    def on_change_with_second_currency_digits(self, name=None):
        if self.second_currency:
            return self.second_currency.digits
        else:
            return 2

    @classmethod
    def get_move_originsel(cls):
        """ get list of selections
        """
        AccountMove = Pool().get('account.move')
        return AccountMove.get_origin()

    @classmethod
    def get_line_originsel(cls):
        """ get list of selections
        """
        AccountMoveLine = Pool().get('account.move.line')
        return AccountMoveLine.get_origin()

    @classmethod
    def table_query(cls):
        """ sql
        """
        pool = Pool()
        AccountMove = pool.get('account.move')
        AccountMoveLine = pool.get('account.move.line')
        Account = pool.get('account.account')
        GeneralLedger = pool.get('account.general_ledger.account')
        tab_move = AccountMove.__table__()
        tab_mvline = AccountMoveLine.__table__()
        tab_acc = Account.__table__()
        context = Transaction().context

        # query for period/fiscalyear
        start_period_ids = GeneralLedger.get_period_ids('start_period')
        end_period_ids = GeneralLedger.get_period_ids('end_period')
        period_ids = list(set(end_period_ids).difference(set(start_period_ids)))

        if len(period_ids) > 0:
            query = tab_move.period.in_(period_ids)
        else :
            query = Literal(True)

        if context.get('posted'):
            query &= tab_move.state == 'posted'

        if context.get('journal'):
            query &= tab_move.journal == context['journal']

        if context.get('from_date'):
            query &= tab_move.date >= context.get('from_date')

        if context.get('to_date'):
            query &= tab_move.date <= context.get('to_date')

        if context.get('journal'):
            query &= tab_move.journal == context.get('journal')

        if context.get('company'):
            query &= tab_move.company == context.get('company')

        qu1 = tab_move.join(tab_mvline,
                condition=tab_mvline.move==tab_move.id
            ).join(tab_acc,
                condition=tab_mvline.account==tab_acc.id
            ).select(tab_mvline.id,
                tab_mvline.create_uid,
                tab_mvline.create_date,
                tab_mvline.write_uid,
                tab_mvline.write_date,
                tab_move.number.as_('movenumber'),
                tab_move.post_number,
                tab_move.period,
                tab_move.journal,
                tab_move.date,
                tab_move.post_date,
                tab_move.description,
                tab_move.origin.as_('origin2'),
                tab_move.state,
                tab_mvline.debit,
                tab_mvline.credit,
                tab_mvline.origin.as_('line_origin2'),
                tab_mvline.description.as_('line_description'),
                tab_mvline.party,
                tab_mvline.reconciliation,
                tab_mvline.amount_second_currency,
                tab_mvline.second_currency,
                Case(
                    (Abs(tab_mvline.debit - tab_mvline.credit) > 0,
                        Round(Abs(tab_mvline.amount_second_currency / \
                            (tab_mvline.debit - tab_mvline.credit)), 4)
                        ),
                ).as_('rate_second_currency'),
                tab_acc.id.as_('account'),
                tab_acc.code.as_('account_code'),
                where=query,
            )
        return qu1

# end PrimaNota


class PrimaNotaContext(GeneralLedgerAccountContext):
    'Primanota Context'
    __name__ = 'account_primanota.primanota.context'

# end PrimaNotaContext
