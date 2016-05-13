from nose.tools import assert_equals
import datetime
import logging

from flask import Flask
from flask.ext.testing import TestCase

from mysite import db, create_app
from budget.models import Budget, Item
from budget.tax_rates import TaxRate

class TestBudget(TestCase):

    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

    def create_app(self):
        return create_app(self)

    def setup(self):
        db.create_all()

        db.session.add( TaxRate('Illinois', 2015, 0, 0, 0.02, 'Single') )

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_budget(self):
        b = Budget('Test', 2015, 'Single')

        Item(b, 'income', 'bofa', 10000, 10000) 
        Item(b, 'pretax', '401k', 500, 1000) 
        

        assert_equals(b.income, 130000)
        assert_equals(b.agi, 123000)
        assert_equals(b.state_tax, 2460)


'''
class TestItem(unittest.TestCase):

    def test_item(self):
        b = Budget('Test', 2015, 'Single')
        item = Item(b, 'income', 'bofa', 10000, 10000)

        assert_equals(item.total, 130000)

'''
 
