from nose.tools import assert_equals
import datetime
import unittest
import logging

from mysite import db, app
from mysite.budget.models import Budget, Item
from mysite.budget.tax_rates import TaxRate

class TestBudget(unittest.TestCase):
    def setup(self):
        logging.basicConfig(level=logging.ERROR)

        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

        self.app = app.test_client()
        db.create_all()

        db.session.add( TaxRate('Illinois', 2015, 0, 0, 0.02, 'Single') )

    def tearDown(self):
        db.session.remove()

    def test_budget(self):
        b = Budget('Test', 2015, 'Single')

        Item(b, 'income', 'bofa', 10000, 10000) 
        Item(b, 'pretax', '401k', 500, 1000) 
        

        assert_equals(b.income, 130000)
        assert_equals(b.agi, 123000)
        assert_equals(b.state_tax, 2460)


class TestItem(unittest.TestCase):

    def test_item(self):
        b = Budget('Test', 2015, 'Single')
        item = Item(b, 'income', 'bofa', 10000, 10000)

        assert_equals(item.total, 130000)

 
