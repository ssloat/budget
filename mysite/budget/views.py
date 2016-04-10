import collections

from mysite import app, db
from mysite.budget.models import Budget, Item

from flask import jsonify, render_template, request

@app.template_filter('money')
def money_filter(s):
    return "{:,.2f}".format(s)

@app.route('/rest/budget/<int:budget_id>', methods=['GET'])
def rest_budget(budget_id):
    b = db.session.query(Budget).filter(Budget.id==budget_id).first()

    data = {'name': b.name, 'rows': b.html() }
    return jsonify(data)

@app.route('/rest/add_item/<int:budget_id>', methods=['POST'])
def rest_add_item(budget_id):
    b = db.session.query(Budget).filter(Budget.id==budget_id).first()

    json = request.form

    monthly = float(json['monthly']) / 12.0 if json['monthly'] else 0.0
    yearly = float(json['yearly']) if json['yearly'] else 0.0

    db.session.add( 
        Item(b, json['category'], json['name'], monthly, yearly) 
    )
    db.session.commit()

    return rest_budget(budget_id)
    
@app.route('/rest/remove_item/<int:budget_id>', methods=['POST'])
def rest_remove_item(budget_id):
    b = db.session.query(Budget).filter(Budget.id==budget_id).first()

    json = request.form

    db.session.query(Item).filter(Item.id==json['dbid']).delete()
    db.session.commit()

    return rest_budget(budget_id)
 
@app.route('/budget/<int:budget_id>')
def budget(budget_id):
    return render_template('budget.html', budget_id=budget_id)
