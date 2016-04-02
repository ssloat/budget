from mysite import db

import datetime
import time
import os
import logging

logger = logging.getLogger(__name__)

class Budget(db.Model):
    __tablename__ = 'budgets'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)

    deductions = db.relationship('Deduction', backref='budget')

    def __init__(self, name):
        self.name = name

class Deduction(db.Model):
    __tablename__ = 'deductions'

    id = db.Column(db.Integer, primary_key=True)
    budget_id = db.Column(db.Integer, db.ForeignKey('budgets.id'))
    category = db.Column(db.String(64), nullable=False)
    name = db.Column(db.String(64), nullable=False)
    monthly = db.Column(db.Float, nullable=False)
    yearly = db.Column(db.Float, nullable=False)
    pre_tax = db.Column(db.Boolean, nullable=False)

    def __init__(self, budget, category, name, monthly, yearly, pre_tax=None):
        self.budget = budget
        self.category = category
        self.name = name
        self.monthly = monthly
        self.yearly = yearly
        self.pre_tax = pre_tax or False

    def html(self):
        return "<tr dbid=%d>" % self.id \
            + " <td style='width:200px' class='name'>%s</td>" % self.name \
            + " <td style='width:100px; text-align:right' class='monthly'>%s</td>" % self.monthly \
            + " <td style='width:100px; text-align:right'>%s</td>" % (12 * self.monthly) \
            + " <td style='width:100px; text-align:right' class='monthly'>%s</td>" % self.yearly \
            + " <td style='width:100px; text-align:right' class='amount'>%s</td>" % (12*self.monthly + self.yearly) \
            + " </tr>"
