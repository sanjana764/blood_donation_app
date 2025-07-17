from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+mysqlconnector://root:@localhost/blood_demo(updated)"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# Database Models
class bd_donate(db.Model):
    d_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    phno = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(25), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(20), nullable=False)
    bgroup = db.Column(db.String(5), nullable=False)

class bd_request(db.Model):
    r_id = db.Column(db.Integer, primary_key=True)
    r_name = db.Column(db.String(50), nullable=False)
    r_phno = db.Column(db.String(15), nullable=False)
    r_email = db.Column(db.String(25), nullable=False)
    r_hpname = db.Column(db.String(50), nullable=False)
    r_city = db.Column(db.String(20), nullable=False)
    r_bgroup = db.Column(db.String(5), nullable=False)
    r_quantity = db.Column(db.Integer, nullable=False)

# Home Route
@app.route("/")
def home():
    return render_template("index.html")

# Donation Route
@app.route("/donate", methods=['GET', 'POST'])
def add_donor():
    if request.method == 'POST':
        name = request.form['name']
        phno = request.form['no']
        email = request.form['email']
        address = request.form['address']
        city = request.form['city']
        bgroup = request.form['bg']

        donor = bd_donate(name=name, phno=phno, email=email, address=address, city=city, bgroup=bgroup)
        db.session.add(donor)
        db.session.commit()

        return redirect("/")
    return render_template("donate.html")

# Request Route
@app.route("/request", methods=['GET', 'POST'])
def req_donor():
    if request.method == 'POST':
        name = request.form['name']
        phno = request.form['no']
        email = request.form['email']
        hname = request.form['hname']
        city = request.form['city']
        bgroup = request.form['bg1']
        amount = request.form['quant']

        request_record = bd_request(
            r_name=name, r_phno=phno, r_email=email,
            r_hpname=hname, r_city=city,
            r_bgroup=bgroup, r_quantity=amount
        )
        db.session.add(request_record)
        db.session.commit()

        # Query for matching donors
        matching_donors = bd_donate.query.filter_by(bgroup=bgroup).all()

        if not matching_donors:
            return render_template("request.html", error="No matching donors found.")

        return render_template("request.html", det=matching_donors)

    return render_template("request.html")

if __name__ == "__main__":
    app.run(debug=True)
