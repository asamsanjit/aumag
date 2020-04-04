from flask import Flask, render_template, request,url_for,redirect
import sqlite3 as sql

con = sql.connect('database.db')
cur = con.cursor()
app = Flask(__name__)

@app.route('/')
def home():
	return render_template('home.html')

@app.route('/enternew')
def new_student():
	return render_template('student.html')

@app.route('/addrec',methods = ['POST', 'GET'])
def addrec():
	if request.method == 'POST':
		nm = request.form['nm']
		addr = request.form['add']
		city = request.form['city']
		pin = request.form['pin']
		con = sql.connect('database.db')
		cur = con.cursor()
		con.execute('''CREATE TABLE stud(name CHAR PRIMARY KEY     NOT NULL,addr   CHAR(50)    NOT NULL,city  CHAR   NOT NULL,pin INT);''')
		cur.execute("INSERT INTO stud(name,addr,city,pin)VALUES(?,?,?,?)",(nm,addr,city,pin) )
		con.commit()
		msg = "Record successfully added"
		return redirect(url_for("list"))
		con.close()

@app.route('/list')
def list():
	con = sql.connect("database.db")
	con.row_factory = sql.Row
	cur = con.cursor()
	cur.execute("select * from stud")
	rows = cur.fetchall();
	return render_template("list.html",rows = rows)

if __name__ == '__main__':
	app.run(debug = True)
