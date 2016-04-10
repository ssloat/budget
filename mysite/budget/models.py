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

    items = db.relationship('Item', backref='budget')

    def __init__(self, name):
        self.name = name

    def html(self):
        results = {}
        for item in self.items:
            results[item.category] = results.get(item.category) or Table(item.category)
            results[item.category].items.append(item)

        results = sorted(results.values(), lambda x, y: cmp(x.sortkey, y.sortkey))
        lines = sum([x.html for x in results], [])
        lines.append("<tr><td colspan='6'>&nbsp</td></tr>")
        lines.append(
            "<tr><td colspan='4'>AGI</td><td class='num'>{:,.2f}</td></tr>".format(self.agi)
        )

        return lines
        

    @property
    def income(self):
        return sum([x.total for x in self.items if x.category == 'income'])

    @property
    def pretax(self):
        return sum([x.total for x in self.items if x.category == 'pretax'])

    @property
    def agi(self):
        return self.income - self.pretax

class Table(object):
    sortkeys = {'income': 1, 'pretax': 2}
    def __init__(self, name):
        self.name = name
        self.sortkey = Table.sortkeys.get(name, 3)
        self.items = []

    @property
    def total(self):
        return sum([x.total for x in self.items])

    def json(self):
        return {
            'name': self.name,
            'items': [x.json() for x in self.items],
            'total': '{:,.2f}'.format(sum([x.total for x in self.items])),
        }

    @property
    def html(self):
        lines = ["<tr><td colspan='6'>{}</td></tr>".format(self.name)]
        for x in self.items:
            lines.extend(x.html)
        lines.append("<tr><td colspan='4'><td class='num'>{:,.2f}</td></tr>".format(self.total))

        return lines


class Item(db.Model):
    __tablename__ = 'budget_items'

    id = db.Column(db.Integer, primary_key=True)
    budget_id = db.Column(db.Integer, db.ForeignKey('budgets.id'))
    category = db.Column(db.String(64), nullable=False)
    name = db.Column(db.String(64), nullable=False)
    monthly = db.Column(db.Float, nullable=False)
    yearly = db.Column(db.Float, nullable=False)
    deductible = db.Column(db.Float, nullable=False)

    def __init__(self, budget, category, name, monthly, yearly, deductible=None):
        self.budget = budget
        self.category = category
        self.name = name
        self.monthly = monthly
        self.yearly = yearly
        self.deductible = deductible or 0.0

    @property
    def total(self):
        return 12*self.monthly + self.yearly

    def json(self):
        return {
            'id': self.id,
            'name': self.name,
            'monthly': '{:,.2f}'.format(self.monthly),
            'monthly12': '{:,.2f}'.format(12*self.monthly),
            'yearly': '{:,.2f}'.format(self.yearly),
            'total': '{:,.2f}'.format(self.total),
        }

    @property
    def html(self):
        return (
            "<tr dbid='{}' category='{}'>".format(self.id, self.category)
            + "<td>{}</td>".format(self.name)
            + "<td class='num'>{:,.2f}</td>".format(self.monthly)
            + "<td class='num'>{:,.2f}</td>".format(12*self.monthly)
            + "<td class='num'>{:,.2f}</td>".format(self.yearly)
            + "<td class='num'>{:,.2f}</td>".format(self.total)
            + "<td><input type='button' value='X'><input type='button' value='Edit'</td>"
            + "</tr>",
        )

    def __html(self):
        style = "style='width:100px; text-align:right'"
        return "<tr dbid=%d>" % self.id \
            + " <td style='width:200px' class='name'>%s</td>" % self.name \
            + " <td {0} class='monthly'>{1:,.2f}</td>".format(style, self.monthly) \
            + " <td {0}>{1:,.2f}</td>".format(style, 12 * self.monthly) \
            + " <td {0} class='yearly'>{1:,.2f}</td>".format(style, self.yearly) \
            + " <td {0} class='amount'>{1:,.2f}</td>".format(style, 12*self.monthly + self.yearly) \
            + " <td > <input type='button' value='X'> </td>" \
            + " </tr>"
