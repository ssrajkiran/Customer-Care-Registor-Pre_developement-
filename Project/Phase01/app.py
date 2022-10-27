from sre_constants import SUCCESS
from turtle import st
from flask import Flask, render_template, request, redirect, url_for, session, flash
from markupsafe import escape
from flask import *
import ibm_db
import tkinter
from tkinter import messagebox

conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=824dfd4d-99de-440d-9991-629c01b3832d.bs2io90l08kqb1od8lcg.databases.appdomain.cloud;PORT=30119;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=lyw92716;PWD=DmHnDfNoz9ILvQAx", '', '')
print(conn)
print("connection successful...")

app = Flask(__name__)
app.secret_key = 'your secret key'


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/home', methods=['POST', 'GET'])
def index():
    return render_template('index.html')


@app.route('/signinpage', methods=['POST', 'GET'])
def signinpage():
    return render_template('signinpage.html')


@app.route('/signuppage', methods=['POST', 'GET'])
def signuppage():
    return render_template('signuppage.html')


@app.route('/welcome', methods=['POST', 'GET'])
def welcome():
    return render_template('welcome.html')


@app.route('/admin', methods=['POST', 'GET'])
def admin():
    return render_template('admin.html')


@app.route('/remove', methods=['POST', 'GET'])
def remove():
    insert_sql = f"delete from customer"
    prep_stmt = ibm_db.prepare(conn, insert_sql)
    ibm_db.execute(prep_stmt)
    flash("delected successfully", SUCCESS)
    return render_template('admin.html')

@app.route('/databases',methods = ['POST', 'GET'])
def databases():
    users = []
    sql = "SELECT * FROM customer"
    stmt = ibm_db.exec_immediate(conn, sql)
    dictionary = ibm_db.fetch_both(stmt)
    while dictionary != False:
        users.append(dictionary)
        dictionary = ibm_db.fetch_both(stmt)

    if users:
        return render_template('admin.html', users = users)

    

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        try:

            id = request.form['idn']
            password = request.form['password']
            print(id, password)
            if id == '1111' and password == '1111':
                return redirect(url_for('admin'))

            sql = f"select * from customer where id='{escape(id)}' and password='{escape(password)}'"
            stmt = ibm_db.exec_immediate(conn, sql)
            data = ibm_db.fetch_both(stmt)

            if data:
                session["name"] = escape(id)
                session["password"] = escape(password)
                return redirect(url_for('welcome'))

            else:
                flash("Mismatch in credetials", "danger")
        except:
            flash("Error in Insertion operation", "danger")

    return render_template('signinpage.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':

        try:

            name = request.form['name']
            email = request.form['email']
            password = request.form['password']
            phonenumber = request.form['phonenumber']
            sql = "SELECT * FROM customer WHERE email = ?"
            stmt = ibm_db.prepare(conn, sql)
            ibm_db.bind_param(stmt, 1, email)
            ibm_db.execute(stmt)
            account = ibm_db.fetch_assoc(stmt)

            if account:
                flash("Record Aldready found", "success")
            else:
                insert_sql = "insert into customer(name,email,password,phonenumber)values(?,?,?,?)"
                prep_stmt = ibm_db.prepare(conn, insert_sql)
                ibm_db.bind_param(prep_stmt, 1, name)
                ibm_db.bind_param(prep_stmt, 2, email)
                ibm_db.bind_param(prep_stmt, 3, password)
                ibm_db.bind_param(prep_stmt, 4, phonenumber)
                ibm_db.execute(prep_stmt)

                flash("Record Added Successfully", "success")

                sql = "SELECT id FROM Customer WHERE email=?"
                stmt = ibm_db.prepare(conn, sql)
                ibm_db.bind_param(stmt, 1, email)
                ibm_db.execute(stmt)
                hi = ibm_db.fetch_assoc(stmt)
                flash(hi)

        except:
            flash("Error in Insertion Operation", "danger")
        finally:
            return redirect(url_for("signuppage"))
            con.close()

    return render_template('signuppage.html')


if __name__ == '__main__':
    app.run(debug=True)
