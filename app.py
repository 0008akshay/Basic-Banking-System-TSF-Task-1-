from flask import Flask, render_template, url_for, request, redirect,flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///customers.db'
#app.config['SQLALCHEMY_TRACK_NOTIFICATIONS'] = False
app.config['SESSION_TYPE'] = 'memcached'
app.config['SECRET_KEY'] = 'super secret key'
db = SQLAlchemy(app)

class customer(db.Model):
    acc_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable = False)
    email = db.Column(db.String(50), nullable = False, unique = True)
    Balance = db.Column(db.Integer)

    def __repr__(self) -> str:
        return f"{self.acc_id} - {self.name}"




@app.route('/')
def index():
    return render_template("index.html")

@app.route('/allcustomers')
def allcustomers():
    allcustomers = customer.query.all()
    return render_template("customer.html",allcustomers = allcustomers)

@app.route('/view/<int:acc_id>')
def user(acc_id):
    user = customer.query.filter_by(acc_id= acc_id).first()
    return render_template("profile.html", user = user)


@app.route('/transfer', methods=['GET', 'POST'])
def transfer():
    if request.method == "POST":
        fromact = request.form['fromact']
        toact = request.form['toact']
        amt = request.form['amt']
        user = customer.query.filter_by(acc_id=fromact).first()
        if user.Balance < int(amt):
            flash("Insufficient Balance.")
        else:
            user.Balance = user.Balance - int(amt)
            db.session.commit()
            touser = customer.query.filter_by(acc_id=toact).first()
            touser.Balance = touser.Balance + int(amt)
            db.session.commit()
            flash("Payment is Successfully Transfer.")
            return redirect(url_for('transfer'))
    return render_template("transfer.html")

@app.route('/about')
def about():
    return render_template("about.html")
if __name__ == '__main__':
    app.debug = True
    app.run()