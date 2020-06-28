import os
from flask import Flask, session, render_template, request, redirect, url_for, flash, jsonify, Response
from flask_bcrypt import Bcrypt
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from database import Base,Users,Patients
from sqlalchemy import create_engine, exc
from sqlalchemy.orm import scoped_session, sessionmaker
from datetime import datetime

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.secret_key = os.urandom(24)

# Set up database
engine = create_engine('sqlite:///database.db',connect_args={'check_same_thread': False},echo=True)
Base.metadata.bind = engine
db = scoped_session(sessionmaker(bind=engine))

# Flask CLI Commands for database initialize, load and drop

# run flask db_create command into terminal for create .db file
@app.cli.command('db_create')
def db_create():
    SQLAlchemy(app).create_all()
    print('Database Created.')

# run flask db_drop command into terminal for drop all table from .db file
@app.cli.command('db_drop')
def db_drop():
    SQLAlchemy(app).drop_all()
    print('Database droped.')

# run flask db_seedData command into terminal for feed the initial user table data
# which make you able to login 
@app.cli.command('db_seedData')
def db_seedData():
    desk_executive = Users(
        id = 'C00000001',
        name = 'ramesh',
        user_type = 'RDE',
        password = bcrypt.generate_password_hash('Ramesh@001').decode('utf-8')
    )

    pharmacist = Users(
        id = 'C00000002',
        name = 'suresh',
        user_type = 'pharmacist',
        password = bcrypt.generate_password_hash('Suresh@002').decode('utf-8')
    )

    diagnostics_executive = Users(
        id = 'C00000003',
        name = 'mahesh',
        user_type = 'DSE',
        password = bcrypt.generate_password_hash('Mahesh@003').decode('utf-8')
    )

    db.add(desk_executive)
    db.add(pharmacist)
    db.add(diagnostics_executive)

    db.commit()
    print('Inital data added.')
    
# all route starts from here
@app.route('/')
@app.route("/dashboard")
def dashboard():
    return render_template("home.html", home=True)

@app.route("/addpatient", methods=["GET","POST"])
def addpatient():
    if 'user' not in session:
        return redirect(url_for('login'))
    if session['usert'] != "RDE":
        flash("You don't have access to this page","warning")
        return redirect(url_for('dashboard'))
    if session['usert']=="RDE":
        if request.method == "POST":
            id = int(request.form.get("ssn_id"))
            name = request.form.get("name")
            age= int(request.form.get("age"))
            date = (request.form.get("Date_of_Admission"))
            typeofbed = request.form.get("typeofbed")
            address = request.form.get("address")
            state = request.form.get("state")
            city = request.form.get("city")
            status = "Active"
            query = Patients(id=id,name=name,age=age,DateofAdm =date,TypeofBed=typeofbed,address=address,state=state,city=city,status=status)
            db.add(query)
            db.commit()
            flash(f'patient with id - {id} is added successfully','primary')
            return redirect(url_for('dashboard'))
    else:
        flash(f'id is already present in database.','warning')
    return render_template("addpatient.html",addpatient=True)

@app.route("/editpatient")
def editpatient():
    return render_template("editpatient.html",addpatient=True)

#     if 'user' not in session:
#         return redirect(url_for('login'))
#     if session['usert'] != "RDE":
#         flash("You don't have access to this page","warning")
#         return redirect(url_for('dashboard'))
#     if request.method == "POST":
#         id = int(request.form.get("ssn_id"))
#         name = request.form.get("name")
#         age= int(request.form.get("age"))
#         date = request.form.get("Date_of_Admission")
#         typeofbed = request.form.get("typeofbed")
#         address = request.form.get("address")
#         state = request.form.get("state")
#         city = request.form.get("city")
#         status = "Active"
#         query = Patients(id=id,name=name,age=age,DateofAdm =date,TypeofBed=typeofbed,address=address,state=state,city=city,status=status)
#         db.add(query)
#         db.commit()
#         return redirect(url_for('dashboard'))
#     else:
#         flash(f'is already present in database.','warning')
#         # flash(f'SSN id : {id} is already present in database.','warning')
#     return render_template("addpatient.html",addpatient=True)

@app.route("/viewpatient")
def viewpatient():
    if 'user' not in session:
        return redirect(url_for('login'))
    if session['usert'] != "RDE":
        flash("You don't have access to this page","warning")
        return redirect(url_for('dashboard'))
    if session['usert']=="RDE":
        result = db.execute("select * from patients").fetchall()
        return render_template('viewpatient.html', viewpatient=True,data=result)
    else:
        flash("You don't have access to this page","warning")
        return redirect(url_for('dashboard'))

# Logout 
@app.route("/logout")
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

# LOGIN
@app.route("/login", methods=["GET", "POST"])
def login():
    if 'user' in session:
        return redirect(url_for('dashboard'))
    
    if request.method == "POST":
        usern = request.form.get("username").upper()
        passw = request.form.get("password").encode('utf-8')
        result = db.execute("SELECT * FROM users WHERE id = :u", {"u": usern}).fetchone()
        if result is not None:
            if bcrypt.check_password_hash(result['password'], passw) is True:
                session['user'] = usern
                session['namet'] = result.name
                session['usert'] = result.user_type
                flash(f"{result.name.capitalize()}, you are successfully logged in!", "success")
                return redirect(url_for('dashboard'))
        flash("Sorry, Username or password not match.","danger")
    return render_template("login.html", login=True)

# route for 404 error
@app.errorhandler(404)
def not_found(e):
  return render_template("404.html")


# Main
if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
