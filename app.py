import os
from flask import Flask, session, render_template, request, redirect, url_for, flash, jsonify, Response
from flask_bcrypt import Bcrypt
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from database import Base,Users,Patients,Medicines,MedHist,Diagnostics,DiaHist
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
    print('Inital User data added.')

# run flask db_seed_med command into terminal for feed the initial medicine table data
@app.cli.command('db_seed_med')
def db_seed_med():
    med1 = Medicines(
        name="acebutolol",
        quantity = 150,
        rate = 50
    )
    med2 = Medicines(
        name="corgard",
        quantity = 150,
        rate = 2000
    )
    med3 = Medicines(
        name="tenormin",
        quantity = 150,
        rate = 100
    )
    med4 = Medicines(
        name="paracetamol",
        quantity = 150,
        rate = 10
    )
    med5 = Medicines(
        name="dio",
        quantity = 150,
        rate = 50
    )

    db.add(med1)
    db.add(med2)
    db.add(med3)
    db.add(med4)
    db.add(med5)

    db.commit()
    print('Inital Medicine data added.')

# run flask db_seed_diagno command into terminal for feed the initial medicine table data
@app.cli.command('db_seed_diagno')
def db_seed_diagno():
    d1 = Diagnostics(
        name="CBP",
        charge = 2000
    )
    d2 = Diagnostics(
        name="Lipid",
        charge = 1500
    )
    d3 = Diagnostics(
        name="ECG",
        charge = 3000
    )
    d4 = Diagnostics(
        name="Echo",
        charge = 4000
    )
    

    db.add(d1)
    db.add(d2)
    db.add(d3)
    db.add(d4)
    db.commit()
    print('Inital Diagnotic data added.')

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
            doa = datetime.strptime(request.form.get("doa"), '%Y-%m-%d').date()
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
        return render_template('searchpatient.html', searchpatient=True)
    else:
        flash("You don't have access to this page","warning")
        return redirect(url_for('dashboard'))

@app.route("/deletepatient",methods=['GET','POST'])
def deletepatient():
    if 'user' not in session:
        return redirect(url_for('login'))
    if session['usert'] != "RDE":
        flash("You don't have access to this page","warning")
        return redirect(url_for('dashboard'))
    if session['usert']=="RDE":
        if request.method == 'POST':
            id = request.form.get('ssn_id')
            patient_data = db.execute('select * from patients where id = :i and status = "Active"',{'i':id}).fetchone()
            if patient_data:
                med_hist_data = db.execute('select * from medhist where patient_id = :i',{'i':patient_data.id}).fetchall()
                med_data = []
                if med_hist_data:
                    for row in med_hist_data:
                        t = {
                            'name' : row.med_name,
                            'quantity' : row.med_quantity,
                            'rate' : row.med_rate,
                            'amount' : row.med_amount,
                        }
                        med_data.append(t)
                diagno_hist_data = db.execute("select * from diahist where patient_id = :i",{'i':patient_data.id}).fetchall()
                diagno_data = []
                if diagno_hist_data:
                    for row in diagno_hist_data:
                        t = {
                            'name' : row.dia_name,
                            'count' : row.dia_count,
                            'amount' : row.dia_amount,
                        }
                        diagno_data.append(t)

                return render_template('raisebill.html', p_data=patient_data, m_data=med_data, d_data=diagno_data)
            else:
                flash('Patient not found or discharged','warning')

        return render_template('deletepatient.html', deletepatient=True)
    else:
        flash("You don't have access to this page","warning")
        return redirect(url_for('dashboard'))

@app.route('/raisebill')
def raisebill():
    if 'user' not in session:
        return redirect(url_for('login'))
    if session['usert'] != "RDE":
        flash("You don't have access to this page","warning")
        return redirect(url_for('dashboard'))
    if session['usert']=="RDE":
        if request.method == 'POST':
            print()
        
        return render_template('raisebill.html', raisebill=True)


@app.route("/issuemedicines",methods=['GET','POST'])
def issuemedicines():
    if 'user' not in session:
        return redirect(url_for('login'))
    if session['usert'] != "pharmacist":
        flash("You don't have access to this page","warning")
        return redirect(url_for('dashboard'))
    if session['usert']=="pharmacist":
        if request.method == 'POST':
            id = request.form.get('ssn_id')
            patient_data = db.execute('select * from patients where id = :i and status = "Active"',{'i':id}).fetchone()
            if patient_data:
                for name,quantity,rate,amount in zip( request.form.getlist('name'), request.form.getlist('quantity'), request.form.getlist('rate'), request.form.getlist('amount') ):
                    med_data = db.execute('select * from medicines where lower(name) = :n',{'n':name.lower()}).fetchone()
                    if med_data and int(med_data.quantity) >= int(quantity):
                        try:
                            new_quantity = int(med_data.quantity) - int(quantity)
                            db.execute("UPDATE medicines SET quantity = :q WHERE lower(name) = :n", {'q':new_quantity,"n": med_data.name.lower()})
                            hist_data = db.execute('select * from medhist where patient_id = :i and lower(med_name) = :n',{'i':patient_data.id,'n':med_data.name.lower()}).fetchone()
                            if hist_data:
                                new_quantity = int(hist_data.med_quantity) + int(quantity)
                                new_amount = int(hist_data.med_amount) + ( int(med_data.rate) * int(quantity) )
                                db.execute("UPDATE medhist SET med_quantity = :q, med_amount = :a WHERE patient_id = :i and lower(med_name) = :n", {'q':new_quantity,'a':new_amount,'i':hist_data.patient_id,"n": hist_data.med_name.lower()})
                            else:
                                query = MedHist(
                                    patient_id = id,
                                    med_name = med_data.name.lower(),
                                    med_quantity = int(quantity),
                                    med_rate = int(med_data.rate),
                                    med_amount = int(med_data.rate) * int(quantity)
                                )
                                db.add(query)
                        except:
                            db.rollback()
                            flash(f'Opps!! Something went wrong with input {name}. Please check your input or try after some time','danger')
                            continue
                        else:
                            db.commit()
                    else:
                        flash(f'Medicine {name} Not found! or Insufficient Quantity','warning')
                else:
                    flash('Medicine Issued successfully','success')
            else:
                flash('Patient not found or discharged','warning')

        return render_template('issuemedicines.html', issuemedicines=True)

    else:
        flash("You don't have access to this page","warning")
        return redirect(url_for('dashboard'))

@app.route("/addDiagnostics",methods=['GET','POST'])
def addDiagnostics():
    if 'user' not in session:
        return redirect(url_for('login'))
    if session['usert'] != "DSE":
        flash("You don't have access to this page","warning")
        return redirect(url_for('dashboard'))
    if session['usert']=="DSE":
        if request.method == 'POST':
            id = request.form.get('ssn_id')
            patient_data = db.execute('select * from patients where id = :i and status = "Active"',{'i':id}).fetchone()
            if patient_data:
                for name,amount in zip( request.form.getlist('name'), request.form.getlist('amount') ):
                    med_data = db.execute('select * from diagnostics where lower(name) = :n',{'n':name.lower()}).fetchone()
                    if med_data:
                        try:
                            hist_data = db.execute('select * from diahist where patient_id = :i and lower(dia_name) = :n',{'i':patient_data.id,'n':med_data.name.lower()}).fetchone()
                            if hist_data:
                                new_amount = int(hist_data.dia_amount) + int(med_data.charge)
                                new_count = int(hist_data.dia_count) + 1
                                db.execute("UPDATE diahist SET dia_amount = :a, dia_count = :c WHERE patient_id = :i and lower(dia_name) = :n", {'a':new_amount,'c':new_count,'i':hist_data.patient_id,"n": hist_data.dia_name.lower()})
                            else:
                                query = DiaHist(
                                    patient_id = id,
                                    dia_name = med_data.name.lower(),
                                    dia_count = 1,
                                    dia_amount = int(med_data.charge)
                                )
                                db.add(query)
                        except:
                            db.rollback()
                            flash(f'Opps!! Something went wrong with input {name}. Please check your input or try after some time','danger')
                            continue
                        else:
                            db.commit()
                    else:
                        flash(f'Diagnostic {name} Not found! or Insufficient Quantity','warning')
                else:
                    flash('Diagnostics added successfully','success')
            else:
                flash('Patient not found or discharged','warning')

        return render_template('diagnostics.html', diagnostics=True)

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
            <a href="/api/v1/getmedicine">Get Medicines</a>
            <a href="/api/v1/getmedhist">Get Patient Medicines history</a>
        </li>
    </ol>
    """

# Api for fetch patient data
@app.route('/getPatientData', methods=["GET"])
@app.route('/api/v1/getPatientData', methods=["GET"])
def getPatientData():
    if 'user' not in session:
        return jsonify(message = 'You need to login for access this api.',query_status = 'fail')
    else:
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
                    return jsonify(message = 'Patient data not found or Patient discharged',query_status = 'fail')
            else:
                return jsonify(message = 'Must Required Patient id',query_status = 'fail')
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

# Api for get medicine data
@app.route('/getmedicine', methods=["GET"])
@app.route('/api/v1/getmedicine', methods=["GET"])
def getmedicine():
    if 'user' not in session:
        return jsonify(message = 'You need to login for access this api.',query_status = 'fail')
    if session['usert'] != "pharmacist":
        return jsonify(message = "You don't have access to this api",query_status = 'fail')
    if session['usert']=="pharmacist":
        if request.method == "GET":
            if 'name' in request.args:
                name = request.args['name']
                if name.strip():
                    data = db.execute("select * from medicines where lower(name) = :n and quantity >= 1",{'n':name.lower()}).fetchone()
                    if data:
                        result = {
                            'id' : data.id,
                            'name' : data.name.lower(),
                            'quantity' : data.quantity,
                            'rate' : data.rate
                        }
                        return jsonify(result)
                    else:
                        return jsonify(message = 'Medicine data not found',query_status = 'fail')
                else:
                    return jsonify(message = 'Must Required Medicine name',query_status = 'fail')
            else:
                data = db.execute("select * from medicines where quantity >= 1").fetchall()
                dict_data = []
                if data:
                    for row in data:
                        t = {
                            'id' : row.id,
                            'name' : row.name,
                            'quantity' : row.quantity,
                            'rate' : row.rate
                        }
                        dict_data.append(t)
                    return jsonify(dict_data)
                else:
                    return jsonify(message = 'data not found',query_status = 'fail')

# Api for get patient medicine history data
@app.route('/getmedhist', methods=["GET"])
@app.route('/api/v1/getmedhist', methods=["GET"])
def getmedhist():
    if 'user' not in session:
        return jsonify(message = 'You need to login for access this api.',query_status = 'fail')
    if session['usert']=="pharmacist" or session['usert']=="RDE":
        if request.method == "GET":
            if 'id' in request.args:
                id = request.args['id']
                if id.strip():
                    data = db.execute("select * from medhist where patient_id = :i",{'i':id}).fetchall()
                    dict_data = []
                    if data:
                        for row in data:
                            t = {
                                'name' : row.med_name,
                                'quantity' : row.med_quantity,
                                'rate' : row.med_rate,
                                'amount' : row.med_amount,
                            }
                            dict_data.append(t)
                        return jsonify(dict_data)
                    else:
                        return jsonify(message = 'Medicine history data not found',query_status = 'fail')
                else:
                    return jsonify(message = 'Must Required Patient id',query_status = 'fail')
            else:
                data = db.execute("select * from medhist limit 100").fetchall()
                dict_data = []
                if data:
                    for row in data:
                        t = {
                            'id' : row.id,
                            'patient_id' : row.patient_id,
                            'med_name' : row.med_name,
                            'med_quantity' : row.med_quantity,
                            'med_rate' : row.med_rate,
                            'med_amount' : row.med_amount,
                        }
                        dict_data.append(t)
                    return jsonify(dict_data)
                else:
                    return jsonify(message = 'Medicine history data not found',query_status = 'fail')

    else:
        return jsonify(message = "You don't have access to this api",query_status = 'fail')

# Api for get medicine data
@app.route('/getdiagnostic', methods=["GET"])
@app.route('/api/v1/getdiagnostic', methods=["GET"])
def getdiagnostic():
    if 'user' not in session:
        return jsonify(message = 'You need to login for access this api.',query_status = 'fail')
    if session['usert'] != "DSE":
        return jsonify(message = "You don't have access to this api",query_status = 'fail')
    if session['usert']=="DSE":
        if request.method == "GET":
            if 'name' in request.args:
                name = request.args['name']
                if name.strip():
                    data = db.execute("select * from diagnostics where lower(name) = :n;",{'n':name.lower()}).fetchone()
                    if data:
                        result = {
                            'id' : data.id,
                            'name' : data.name.lower(),
                            'charge' : data.charge
                        }
                        return jsonify(result)
                    else:
                        return jsonify(message = 'Diagnostic data not found',query_status = 'fail')
                else:
                    return jsonify(message = 'Must Required diagnostic name',query_status = 'fail')
            else:
                data = db.execute("select * from diagnostics").fetchall()
                dict_data = []
                if data:
                    for row in data:
                        t = {
                            'id' : row.id,
                            'name' : row.name,
                            'charge' : row.charge
                        }
                        dict_data.append(t)
                    return jsonify(dict_data)
                else:
                    return jsonify(message = 'data not found',query_status = 'fail')

# Api for get patient medicine history data
@app.route('/getdiahist', methods=["GET"])
@app.route('/api/v1/getdiahist', methods=["GET"])
def getdiahist():
    if 'user' not in session:
        return jsonify(message = 'You need to login for access this api.',query_status = 'fail')
    if session['usert']=="DSE" or session['usert'] == "RDE":
        if request.method == "GET":
            if 'id' in request.args:
                id = request.args['id']
                if id.strip():
                    data = db.execute("select * from diahist where patient_id = :i",{'i':id}).fetchall()
                    dict_data = []
                    if data:
                        for row in data:
                            t = {
                                'name' : row.dia_name,
                                'count' : row.dia_count,
                                'amount' : row.dia_amount,
                            }
                            dict_data.append(t)
                        return jsonify(dict_data)
                    else:
                        return jsonify(message = 'Diagnostics history data not found',query_status = 'fail')
                else:
                    return jsonify(message = 'Must Required Patient id',query_status = 'fail')
            else:
                data = db.execute("select * from diahist limit 100").fetchall()
                dict_data = []
                if data:
                    for row in data:
                        t = {
                            'id' : row.id,
                            'patient_id' : row.patient_id,
                            'dia_name' : row.dia_name,
                            'dia_count' : row.dia_count,
                            'dia_amount' : row.dia_amount,
                        }
                        dict_data.append(t)
                    return jsonify(dict_data)
                else:
                    return jsonify(message = 'Diagnostics history data not found',query_status = 'fail')
    
    else:
        return jsonify(message = "You don't have access to this api",query_status = 'fail')

# Main
if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
