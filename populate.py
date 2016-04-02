from mysite.budget.models import Budget, Deduction

from mysite import db

if __name__ == '__main__':
    b = Budget('test')
    db.session.add(b)

    db.session.add( Deduction(b, 'giving', 'rez', 10000, 2000) )
    db.session.add( Deduction(b, 'giving', 'compassion', 2000, 0) )

    db.session.commit()
