import collections

from mysite import app, db
from mysite.budget.models import Budget, Deduction

from flask import jsonify, render_template, request


@app.route('/rest/budget/<budget_id>', methods=['GET'])
def rest_budget(budget_id):
    b = db.session.query(Budget).filter(Budget.id==budget_id).first()

    results = collections.defaultdict(list)
    for d in b.deductions:
        results[d.category].append([d.name, d.amount])

    return jsonify({ 'budget': results })

@app.route('/rest/add_item/<budget_id>', methods=['POST'])
def rest_add_item(budget_id):
    print request.headers
    b = db.session.query(Budget).filter(Budget.id==budget_id).first()

    json = request.form

    db.session.add( Deduction(b, 'giving', json['category'], json['amount']) )
    db.session.commit()

    return budget(budget_id)
    

@app.route('/budget/<budget_id>')
def budget(budget_id):
    return render_template('budget.html', budget_id=budget_id)
