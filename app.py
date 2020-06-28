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
    if os.path.exists("database.db"):
        os.remove("database.db")
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
@app.route("/home")
@app.route("/index")
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
            doa = datetime.strptime(request.form.get("Date_of_Admission"), '%Y-%m-%d').date()
            typeofbed = request.form.get("typeofbed")
            address = request.form.get("address")
            state = request.form.get("state")
            city = request.form.get("city")
            status = "Active"
            query = Patients(id=id,name=name,age=age,DateofAdm = doa,TypeofBed=typeofbed,address=address,state=state,city=city,status=status)
            db.add(query)
            db.commit()
            flash(f'patient with id - {id} is added successfully','primary')
            return redirect(url_for('dashboard'))
    else:
        flash(f'id is already present in database.','warning')
    return render_template("addpatient.html",addpatient=True)

@app.route("/editpatient",methods=['GET','POST'])
def editpatient():
    if 'user' not in session:
        return redirect(url_for('login'))
    if session['usert'] != "RDE":
        flash("You don't have access to this page","warning")
        return redirect(url_for('dashboard'))
    if session['usert'] == "RDE":
        if request.method == "POST":
            id = int(request.form.get("ssn_id"))
            name = request.form.get("name")
            age= int(request.form.get("age"))
            doa = datetime.strptime(request.form.get("doa"), '%Y-%m-%d').date()
            typeofbed = request.form.get("typeofbed")
            address = request.form.get("address")
            state = request.form.get("state")
            city = request.form.get("city")
            data = db.execute("select * from patients where id = :i and status='Active'",{'i':id}).fetchone()
            if data:
                db.execute("UPDATE patients SET name = :n, age = :ag, DateofAdm = :d, TypeofBed = :t, address = :ad, state = :s, city = :c WHERE id = :i", {"n": name,'ag':age,'d':doa,'t':typeofbed,"ad": address,'s':state,'c':city,"i": id})
                db.commit()
                flash(f"Patient data updated successfully.","success")
                return redirect(url_for('dashboard'))
        else:
            flash('Invalid Patient Id. Please, check Patient Id.','warning')

    return render_template("editpatient.html",editpatient=True)

@app.route("/viewpatient")
def viewpatient():
    if 'user' not in session:
        return redirect(url_for('login'))
    if session['usert'] != "RDE":
        flash("You don't have access to this page","warning")
        return redirect(url_for('dashboard'))
    if session['usert']=="RDE":
        result = db.execute("select * from patients where status = 'Active'").fetchall()
        return render_template('viewpatient.html', viewpatient=True,data=result)
    else:
        flash("You don't have access to this page","warning")
        return redirect(url_for('dashboard'))

@app.route("/searchpatient")
def searchpatient():
    if 'user' not in session:
        return redirect(url_for('login'))
    if session['usert'] != "RDE":
        flash("You don't have access to this page","warning")
        return redirect(url_for('dashboard'))
    if session['usert']=="RDE":
        return render_template('searchpatient.html', viewpatient=True)
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

# Api
@app.route('/api')
@app.route('/api/v1')
def api():
    return """
    <h2>List of Api</h2>
    <ol>
        <li>
            <a href="/api/v1/getPatientData">Patient Data</a>
        </li>
    </ol>
    """

# Api for update perticular customer log change in html table onClick of refresh
@app.route('/getPatientData', methods=["GET"])
@app.route('/api/v1/getPatientData', methods=["GET"])
def getPatientData():
    if 'user' not in session:
        flash("Please login","warning")
        return redirect(url_for('login'))
    if request.method == "GET":
        if 'id' in request.args:
            id = request.args['id']
            if id.strip():
                data = db.execute("select * from patients where id = :i and status = 'Active'",{'i':id}).fetchone()
                if data:
                    result = {
                        'id' : data.id,
                        'name' : data.name,
                        'age' : data.age,
                        'DateofAdm' : data.DateofAdm,
                        'TypeofBed' : data.TypeofBed,
                        'address' : data.address,
                        'state' : data.state,
                        'city' : data.city,
                        'status' : data.status
                    }
                    return jsonify(result)
                else:
                    return jsonify(message = 'data not found',query_status = 'fail')
        else:
            data = db.execute("select * from patients where status='Active'").fetchall()
            dict_data = []
            if data:
                for row in data:
                    t = {
                        'id' : row.id,
                        'name' : row.name,
                        'age' : row.age,
                        'DateofAdm' : row.DateofAdm,
                        'TypeofBed' : row.TypeofBed,
                        'address' : row.address,
                        'state' : row.state,
                        'city' : row.city,
                        'status' : row.status
                    }
                    dict_data.append(t)
                return jsonify(dict_data)
            else:
                return jsonify(message = 'data not found',query_status = 'fail')

# Main
if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
