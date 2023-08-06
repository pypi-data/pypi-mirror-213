# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.

from trytond.tests.test_tryton import (
    ModuleTestCase, with_transaction, activate_module, drop_db)
from trytond.pool import Pool
from trytond.transaction import Transaction
from trytond.modules.company.tests import create_company, set_company
from trytond.modules.account.tests import create_chart, get_fiscalyear
from datetime import date
from decimal import Decimal
from unittest.mock import MagicMock


class PMTestCase(ModuleTestCase):
    'Test pm module'
    module = 'account_primanota'

    @classmethod
    def setUpClass(cls):
        """ add modules
        """
        super(PMTestCase, cls).setUpClass()
        activate_module(['analytic_account'])

    def prep_fiscalyear(self, company1):
        """ prepare fiscal year, sequences...
        """
        pool = Pool()
        FiscalYear = pool.get('account.fiscalyear')

        fisc_year = get_fiscalyear(company1, today=date(2020, 1, 15))
        fisc_year.save()
        FiscalYear.create_period([fisc_year])

    def prep_analytic_accounts(self, company):
        """ add analytic accounts
        """
        AnalyticAccount = Pool().get('analytic_account.account')

        account_root, = AnalyticAccount.create([{
            'type': 'root',
            'name': 'mds',
            'code': 'ROOT',
            'company': company.id,
            'parent': None,
            'state': 'opened',
            }])

        account, = AnalyticAccount.create([{
            'root': account_root.id,
            'type': 'normal',
            'name': 'Office',
            'code': 'K001',
            'company': company.id,
            'parent': account_root.id,
            'state': 'opened',
            }])
        return account

    @with_transaction()
    def test_account_move(self):
        """ create account move, check values
        """
        pool = Pool()
        AccountMove = pool.get('account.move')
        Journal = pool.get('account.journal')
        Period = pool.get('account.period')
        Account = pool.get('account.account')
        Tax = pool.get('account.tax')
        PrimaNota = pool.get('account_primanota.primanota')
        IrDate = pool.get('ir.date')

        IrDate.today = MagicMock(return_value=date(2020, 5, 3))

        company1 = create_company('m-ds')
        with set_company(company1):
            with Transaction().set_context({'company': company1.id}):
                create_chart(company=company1, tax=True)
                self.prep_fiscalyear(company1)
                analytic = self.prep_analytic_accounts(company1)

                account_lst = Account.search([
                    ('name', 'in', [
                        'Main Expense', 'Main Revenue',
                        'Main Receivable'])
                    ], order=[('name', 'ASC')])
                self.assertEqual(len(account_lst), 3)
                self.assertEqual(account_lst[0].rec_name, 'Main Expense')
                self.assertEqual(account_lst[1].rec_name, 'Main Receivable')
                self.assertEqual(account_lst[2].rec_name, 'Main Revenue')
                account_lst[0].code = '001'
                account_lst[0].save()
                account_lst[1].code = '002'
                account_lst[1].save()
                account_lst[2].code = '003'
                account_lst[2].save()

                journ_lst = Journal.search([('name', '=', 'Revenue')])
                self.assertEqual(len(journ_lst), 1)

                tax_lst = Tax.search([])
                self.assertEqual(len(tax_lst), 1)

                am_rec = AccountMove.create([{
                    'date': date(2020, 5, 1),
                    'journal': journ_lst[0].id,
                    'period': Period.find(company1.id, date=date(2020, 5, 2)),
                    'description': 'Test 1',
                    'lines': [('create', [{
                        'debit': Decimal('10.0'),
                        'credit': Decimal('0.0'),
                        'account': account_lst[2].id,
                        'description': 'Line 1',
                        'analytic_lines': [('create', [{
                            'account': analytic.id,
                            'date': date(2020, 5, 1),
                            'debit': Decimal('10.0'),
                            'credit': Decimal('0.0'),
                            }])],
                        'tax_lines': [('create', [{
                            'amount': Decimal('10.0'),
                            'type': 'base',
                            'tax': tax_lst[0].id,
                            }])],
                        }, {
                        'debit': Decimal('0.0'),
                        'credit': Decimal('10.0'),
                        'account': account_lst[1].id,
                        'description': 'Line 2',
                        'party': company1.party.id,
                        }])],
                    }])
                self.assertEqual(len(am_rec), 1)
                am_rec[0].origin = am_rec[0]
                am_rec[0].save()
                am_rec[0].lines[0].origin = am_rec[0].lines[1]
                am_rec[0].lines[0].save()
                AccountMove.post(am_rec)

                pm_lst = PrimaNota.search([])
                self.assertEqual(len(pm_lst), 2)

                # 2
                self.assertEqual(pm_lst[0].movenumber, '1')
                self.assertEqual(pm_lst[0].post_number, '1')
                self.assertEqual(pm_lst[0].period.rec_name, '2020-05')
                self.assertEqual(pm_lst[0].journal.rec_name, 'Revenue')
                self.assertEqual(pm_lst[0].date, date(2020, 5, 1))
                self.assertEqual(pm_lst[0].description, 'Test 1')
                self.assertEqual(pm_lst[0].line_description, 'Line 2')
                self.assertEqual(pm_lst[0].origin.description, 'Test 1')
                self.assertEqual(pm_lst[0].line_origin.description, 'Line 1')
                self.assertEqual(pm_lst[0].state, 'posted')
                self.assertEqual(pm_lst[0].debit, Decimal('0.0'))
                self.assertEqual(pm_lst[0].credit, Decimal('10.0'))
                self.assertEqual(
                    pm_lst[0].account.rec_name,
                    '002 - Main Receivable')
                self.assertEqual(pm_lst[0].account_code, '002')
                self.assertEqual(pm_lst[0].party.rec_name, 'm-ds')
                self.assertEqual(pm_lst[0].reconciliation, None)
                self.assertEqual(len(pm_lst[0].reconciliations_delegated), 0)
                self.assertEqual(len(pm_lst[0].tax_lines), 0)
                self.assertEqual(pm_lst[0].amount_second_currency, None)
                self.assertEqual(pm_lst[0].rate_second_currency, None)
                self.assertEqual(pm_lst[0].second_currency, None)
                self.assertEqual(pm_lst[0].currency.rec_name, 'usd')
                self.assertEqual(pm_lst[0].currency_digits, 2)
                self.assertEqual(pm_lst[0].second_currency_digits, 2)
                self.assertEqual(
                    pm_lst[0].rec_name,
                    '1 [1] 05/01/2020 002 usd0.00/usd10.00')
                self.assertEqual(pm_lst[0].has_analytic_lines, False)
                self.assertEqual(len(pm_lst[0].analytic_lines), 0)

                # 1
                self.assertEqual(pm_lst[1].movenumber, '1')
                self.assertEqual(pm_lst[1].post_number, '1')
                self.assertEqual(pm_lst[1].period.rec_name, '2020-05')
                self.assertEqual(pm_lst[1].journal.rec_name, 'Revenue')
                self.assertEqual(pm_lst[1].date, date(2020, 5, 1))
                self.assertEqual(pm_lst[1].description, 'Test 1')
                self.assertEqual(pm_lst[1].line_description, 'Line 1')
                self.assertEqual(pm_lst[1].origin.description, 'Test 1')
                self.assertEqual(pm_lst[1].line_origin, None)
                self.assertEqual(pm_lst[1].state, 'posted')
                self.assertEqual(pm_lst[1].debit, Decimal('10.0'))
                self.assertEqual(pm_lst[1].credit, Decimal('0.0'))
                self.assertEqual(
                    pm_lst[1].account.rec_name,
                    '003 - Main Revenue')
                self.assertEqual(pm_lst[1].account_code, '003')
                self.assertEqual(pm_lst[1].party, None)
                self.assertEqual(pm_lst[1].reconciliation, None)
                self.assertEqual(len(pm_lst[1].reconciliations_delegated), 0)
                self.assertEqual(len(pm_lst[1].tax_lines), 1)
                self.assertEqual(
                    pm_lst[1].tax_lines[0].amount,
                    Decimal('10.0'))
                self.assertEqual(pm_lst[1].amount_second_currency, None)
                self.assertEqual(pm_lst[1].rate_second_currency, None)
                self.assertEqual(pm_lst[1].second_currency, None)
                self.assertEqual(pm_lst[1].currency.rec_name, 'usd')
                self.assertEqual(pm_lst[1].currency_digits, 2)
                self.assertEqual(pm_lst[1].second_currency_digits, 2)
                self.assertEqual(
                    pm_lst[1].rec_name,
                    '1 [1] 05/01/2020 003 usd10.00/usd0.00')
                self.assertEqual(pm_lst[1].has_analytic_lines, True)
                self.assertEqual(len(pm_lst[1].analytic_lines), 1)
                self.assertEqual(
                    pm_lst[1].analytic_lines[0].account.code,
                    'K001')

                # searcher
                # search in party
                self.assertEqual(PrimaNota.search_count([
                    ('rec_name', '=', 'm-ds')]), 1)
                # post-number/move-number
                self.assertEqual(PrimaNota.search_count([
                    ('rec_name', '=', '1')]), 2)

                # line-origin
                self.assertEqual(PrimaNota.search_count([
                    ('line_origin.description', '=',
                        'Line 1', 'account.move.line')
                    ]), 1)
                self.assertEqual(PrimaNota.search_count([
                    ('line_origin.description', '=', 'Line 1')
                    ]), 1)
                self.assertEqual(PrimaNota.search_count([
                    ('line_origin', 'ilike', '%003%')
                    ]), 1)

                # move-origin
                self.assertEqual(PrimaNota.search_count([
                    ('origin.description', '=', 'Test 1', 'account.move')
                    ]), 2)
                self.assertEqual(PrimaNota.search_count([
                    ('origin.description', '=', 'Test 1')
                    ]), 2)
                self.assertEqual(PrimaNota.search_count([
                    ('origin', 'ilike', '%1%')
                    ]), 2)

                # analytic lines
                self.assertEqual(PrimaNota.search_count([
                    ('has_analytic_lines', '=', True)
                    ]), 1)
                self.assertEqual(PrimaNota.search_count([
                    ('has_analytic_lines', '=', False)
                    ]), 1)
                a_line, = PrimaNota.search([
                    ('has_analytic_lines', '=', True)])
                self.assertEqual(len(a_line.analytic_lines), 1)
                self.assertEqual(
                    a_line.analytic_lines[0].account.code,
                    'K001')
                self.assertEqual(a_line.debit, Decimal('10.0'))
                self.assertEqual(a_line.credit, Decimal('0.0'))

# end PMTestCase


del ModuleTestCase
