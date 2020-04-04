from flask import Flask, session, url_for, redirect, request,render_template,flash
from flask import jsonify
from flask import send_from_directory
from flask_sqlalchemy import SQLAlchemy 
import sqlite3 as sql 
import os
import random

con = sql.connect("database.db, check_same_thread=False")
cur = con.cursor()

upload_path = os.path.join('static', 'upload')
question_path= os.path.join('static', 'question_upload')
result_path= os.path.join('static', 'result_upload')
PEOPLE_FOLDER = os.path.join('static', 'img')


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PEOPLE_FOLDER'] = upload_path
app.config['UPLOAD_FOLDER'] = PEOPLE_FOLDER
app.config['QUESTION_FOLDER'] = question_path
app.config['RESULT_FOLDER'] = result_path
app.secret_key="sanjit rai"

db = SQLAlchemy(app) 

class User(db.Model):
	user_id=db.Column(db.Integer, autoincrement=True,primary_key=True)
	email_address=db.Column(db.String(300), unique=True, nullable=False)
	address=db.Column(db.String(300), nullable=False)
	contact_no=db.Column(db.String(300),nullable=False)

	category=db.relationship('Category', secondary='user_category', backref='user',lazy='dynamic')


	def __init__(self, email_address,address,contact_no):
		self.email_address=email_address
		self.address=address
		self.contact_no=contact_no

	def __repr__(self):
		return '< User: id= %r >'% self.user_id

class Category(db.Model):
	test_id=db.Column(db.Integer , autoincrement=True, primary_key=True)
	test_category=db.Column(db.String(200), nullable=False)
	category_image=db.Column(db.String(200))
	question=db.relationship('Question', backref='category', lazy='dynamic')

	def __init__(self, test_category,category_image):
		self.test_category=test_category
		self.category_image=category_image

	def __repr__(self):
		return '<aumag_category id= %r>' % self.test_id


db.Table('user_category',
	db.Column('user_id', db.Integer, db.ForeignKey('user.user_id')),
	db.Column('test_id', db.Integer, db.ForeignKey('category.test_id')))		

class Question(db.Model):
	question_id=db.Column(db.Integer ,autoincrement=True, primary_key=True)
	test_id=db.Column(db.Integer, db.ForeignKey('category.test_id'))
	test_question=db.Column(db.String(200), nullable=False)
	question_imgpath=db.Column(db.String(300))
	result=db.relationship('Result', backref='question', lazy='dynamic')

	def __init__(self, test_id,test_question,question_imgpath):
		self.test_id=test_id
		self.test_question=test_question
		self.question_imgpath=question_imgpath
    
	def __repr__(self):
		return '<Question:  question_id={}'.format(self.question_id)


class Result(db.Model):
	result_id=db.Column(db.Integer ,autoincrement=True, primary_key=True)
	question_id=db.Column(db.Integer, db.ForeignKey('question.question_id'))
	test_result=db.Column(db.String(300))
	result_image=db.Column(db.String(300))
	
	def __init__(self,question_id,test_result,result_image):
		self.question_id=question_id
		self.test_result=test_result
		self.result_image=result_image

	def __repr__(self):
		return '<Result: result_id %r >'% self.result_id


class aumag_test(db.Model):
	test_id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(250))
	test_name = db.Column(db.String(300))
	test_result1 = db.Column(db.String(300))
	test_result2 = db.Column(db.String(300))
	test_result3 = db.Column(db.String(300))
	test_result4 = db.Column(db.String(300))
	test_result5 = db.Column(db.String(300))
	test_result6 = db.Column(db.String(300))


class tables(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(200))
	test_name = db.Column(db.String(200))
	test_result = db.Column(db.String(200))

	def __repr__(self):
		return "<tables ( username={},test_name={}, test_result={}) >".format(self.username, self.test_name,self.test_result)


@app.route('/')
def index():
	title="auto match generate"
	rows=Category.query.all()
	return render_template('index.html', title=title, rows=rows)

@app.route('/admin')
def admin():
	return render_template('admin.html')

@app.route('/admin/create_user')
def creator():
	return render_template('user.html')

@app.route('/admin/user_submit', methods=['POST'])
def user_submit():
    if request.method=='POST':
    	user=request.form['user']
    	address=request.form['address']
    	phone=request.form['phone']
    	formCreate= User(user,address,phone)
    	db.session.add(formCreate)
    	db.session.commit()
    	message="1 user has create successfully !"
    	return render_template('message.html', mg=message)							


@app.route('/admin/category')
def category():
	return render_template('category.html')	

@app.route('/admin/category_submit', methods=['POST'])
def category_submit():
	if request.method == 'POST':
		test_category=request.form['test_category']
		file=request.files['category_file']
		file.save(os.path.join(app.config['PEOPLE_FOLDER'], file.filename))
		file_path=os.path.join(app.config['PEOPLE_FOLDER'], file.filename)
		data= Category(test_category,file_path)
		db.session.add(data)
		db.session.commit()
		message="1 Category created successfully !"
		return render_template('message.html', mg=message)
   	

@app.route('/admin/question')
def question():
	data=Category.query.all()
	#category_data=Category.query.join(Question).add_columns(Category.test_id,Category.test_category, Question.test_question, Question.question_imgpath).filter(Category.test_id==Question.test_id).distinct()
	return render_template('question.html', category=data)	

@app.route('/admin/question_form_submit', methods=['POST'])
def Question_submit():
    if request.method=='POST':
    	test_id=request.form['test_id']
    	test_question=request.form['test_question']
    	file=request.files['question_img']
    	#print("Values: {}, {} ,{} ".format(test_id,test_question,file))
    	file.save(os.path.join(app.config['QUESTION_FOLDER'], file.filename))
    	file_path=os.path.join(app.config['QUESTION_FOLDER'], file.filename)
    	record1= Question(test_id,test_question,file_path)
    	db.session.add(record1)
    	db.session.commit()
    	message="1 Question has created !"
    	return render_template('message.html', mg=message)

@app.route('/admin/test_result')
def test_result():
	data=Question.query.all()
	return render_template('test_result.html',data=data)	

@app.route('/admin/result_form_submit', methods=['POST'])
def Result_submit():
    if request.method=='POST':
    	question_id=request.form['question_id']
    	test_result=request.form['test_result']
    	file=request.files['result_img']
    	#print("Values: {}, {} ,{} ".format(test_id,test_question,file))
    	file.save(os.path.join(app.config['RESULT_FOLDER'], file.filename))
    	file_path=os.path.join(app.config['RESULT_FOLDER'], file.filename)
    	results= Result(question_id,test_result,file_path)
    	db.session.add(results)
    	db.session.commit()
    	message="1 Question has created !"
    	return render_template('message.html', mg=message)

@app.route('/wtf')
def wtf():
	return render_template('wtf.html')


@app.route('/create', methods = ['POST', 'GET'])
def create():
	username = request.form['username']
	test_name = request.form['test_name']
	test_result1 = request.form['test_result1']
	test_result2 = request.form['test_result2']
	test_result3 = request.form['test_result3']
	session['username']=username;
	session['test_name']=test_name;
	con = sql.connect("database.db")
	con.row_factory = sql.Row
	cur = con.cursor()
	cur.execute("INSERT INTO aumag_test(username,test_name,test_result1,test_result2,test_result3) VALUES (?,?,?,?,?)",(username,test_name,test_result1,test_result2,test_result3) )
	con.commit()
	return redirect(url_for("create1"))
	con.close()

@app.route('/create1',methods = ['POST', 'GET'])
def create1():
	full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'paper4.png')
	con = sql.connect("database.db")
	con.row_factory = sql.Row
	cur = con.cursor()
	val = session['username']
	query_str="select * from aumag_test where username='"+val+"'"
	cur.execute(query_str);
	rows = cur.fetchall();
	return render_template('create1.html',rows=rows,user_image=full_filename)	

@app.route('/step1')
def step1():
	rows = aumag_test.query.filter_by(username='sanjit@gmail.com').all()
	return render_template('step1.html',rows=rows)	
	
@app.route('/<test_id>')
def test(test_id):
	Tid=test_id
	title="testing"
	data=Question.query.filter_by(test_id=Tid)
	return render_template('future.html', title=title,data=data)

@app.route('/<question_id>')
def test2(question_id):
	qid=question_id
	title="testing"
	data=Result.query.filter_by(question_id=qid)
	return render_template('future.html', title=title,data=data)



@app.route('/trial/<question_id>')
def test1(question_id):
	Qid=question_id
	d1=Result.query.filter_by(question_id=Qid).all()
	user=random.choice(d1)					
	title='Result page'
	return render_template('result_page.html',title=title, d1=d1,user=user)


@app.route('/<test_id>')
def relation(test_id):
	Tid=test_id
	data=Category.query.filter_by(test_id=Tid)
	title="testing"
	return render_template('relation.html', title=title,data=data)	

@app.route('/science1',methods = ['GET', 'POST'])
def science1():
	foo = ['a', 'b', 'c', 'd', 'e']
	username = random.choice(foo)	
	error=None
	
	if request.method == 'POST':
		if username =='a':
			flash("Your origin of planet is jupiter")
			full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'jupiter.png')
			return render_template("result.html", user_image = full_filename)
		elif username =='b':		
			flash('Your origin of planet is mars')
			full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'mars.png')
			return render_template("result.html", user_image = full_filename)
		elif username=='c':		
			flash('Your origin of planet is venus')
			full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'venus.gif')
			return render_template("result.html", user_image = full_filename)
		elif username =='d':		
			flash('Your origin of planet is moon')
			full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'moon.png')
			return render_template("result.html", user_image = full_filename)					
		else:
			flash('Your origin of planet is sun')
			full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'sun.png')
			return render_template("result.html", user_image = full_filename)
	return render_template('science.html', error = error)

@app.route('/science2')
def science2():
	foo = ['a', 'b', 'c', 'd', 'e']
	username = random.choice(foo)
	if username =='a':
		flash("You are jupiter planet")
		full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'jupiter.png')
		return render_template("result.html", user_image = full_filename,rdom=username)
	elif username =='b':
		flash('You are mars planet')
		full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'mars.png')
		return render_template("result.html", user_image = full_filename,rdom=username)
	elif username=='c':
		flash('You are venus planet')
		full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'venus.gif')
		return render_template("result.html", user_image = full_filename,rdom=username)
	elif username =='d':
		flash('You are moon planet')
		full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'moon.png')
		return render_template("result.html", user_image = full_filename,rdom=username)					
	else:
		flash('You are sun planet')
		full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'sun.png')
		return render_template("result.html", user_image = full_filename,rdom=username)

@app.route('/relationR2')
def relationR2():
	foo = ['a', 'b', 'c', 'd', 'e']
	username = random.choice(foo)
	if username =='a':
		flash("Handsome")
		full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'lier.jpg')
		return render_template("relationR2.html",user_image = full_filename)
	elif username =='b':
		full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'cute.png')
		return render_template("relationR2.html",user_image = full_filename)
	elif username=='c':
		full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'angry.png')
		return render_template("relationR2.html",user_image = full_filename)
	elif username =='d':
		full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'lazy.png')
		return render_template("relationR2.html",user_image = full_filename)					
	else:
		flash("Stupid")
		full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'lier.jpg')
		return render_template("relationR2.html",user_image = full_filename)

@app.route('/relationR')
def relationR():
	foo = ['a', 'b', 'c', 'd', 'e']
	username = random.choice(foo)
	if username =='a':
		flash("Selena Gomez")
		full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'selena.jpg')
		return render_template("relationR.html", user_image = full_filename,rdom=username)
	elif username =='b':
		flash('Deepika')
		full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'deepika.jpg')
		return render_template("relationR.html", user_image = full_filename,rdom=username)
	elif username=='c':
		flash('katrina')
		full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'katrina.jpg')
		return render_template("relationR.html", user_image = full_filename,rdom=username)
	elif username =='d':
		flash('Aishwarya')
		full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'Aishwarya.jpg')
		return render_template("relationR.html", user_image = full_filename,rdom=username)					
	else:
		flash('Taylor swift')
		full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'taylor.jpg')
		return render_template("relationR.html", user_image = full_filename,rdom=username)	

@app.route('/fut1')
def fut1():
	foo = ['a', 'b', 'c', 'd', 'e']
	username = random.choice(foo)
	if username =='a':
		full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'japan.png')
		return render_template("relationR.html", user_image = full_filename)
	elif username =='b':
		full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'nepal.png')
		return render_template("relationR.html", user_image = full_filename)
	elif username=='c':
		full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'korea.png')
		return render_template("relationR.html", user_image = full_filename)
	elif username =='d':
		full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'usa.png')
		return render_template("relationR.html", user_image = full_filename)					
	else:
		full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'aus.png')
		return render_template("relationR.html", user_image = full_filename)		



@app.route('/science', methods = ['GET', 'POST'])
def science():
	error=None
	if request.method == 'POST':
		if request.form['username'] =='a':
			flash("Ur origin of planet is jupiter")
			full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'jupiter.png')
			return render_template("result.html", user_image = full_filename)
		elif request.form['username'] =='b':		
			flash('Your Origin of planet is mars')
			full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'mars.png')
			return render_template("result.html", user_image = full_filename)
		elif request.form['username'] =='c':		
			flash('Your Origin of planet is venus')
			full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'venus.gif')
			return render_template("result.html", user_image = full_filename)
		elif request.form['username'] =='d':		
			flash('Your Origin of planet is moon')
			full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'moon.png')
			return render_template("result.html", user_image = full_filename)
		elif request.form['username'] =='e':		
			flash('Your Origin of planet is earth')
			full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'earth.png')
			return render_template("result.html", user_image = full_filename)
		elif request.form['username'] =='f':		
			flash('Your Origin of planet is pluto')
			full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'pluto.png')
			return render_template("result.html", user_image = full_filename)	
		elif request.form['username'] =='g':		
			flash('Your Origin of planet is uranus')
			full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'uranus.png')
			return render_template("result.html", user_image = full_filename)
		elif request.form['username'] =='h':		
			flash('Your Origin of planet is saturn')
			full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'saturn.gif')
			return render_template("result.html", user_image = full_filename)
		elif request.form['username'] =='i':		
			flash('Your Origin of planet is sun')
			full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'sun.png')
			return render_template("result.html", user_image = full_filename)
		elif request.form['username'] =='j':		
			flash('Your Origin of planet is Mercury')
			full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'mercury.png')
			return render_template("result.html", user_image = full_filename)	
		elif request.form['username'] =='k':		
			flash('Your Origin of planet is moon')
			full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'moon.png')
			return render_template("result.html", user_image = full_filename)
		elif request.form['username'] =='l':		
			flash('Your Origin of planet is Neptune')
			full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'neptune.png')
			return render_template("result.html", user_image = full_filename)
		elif request.form['username'] =='m':		
			flash('Your Origin of planet is Neptune')
			full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'neptune.png')
			return render_template("result.html", user_image = full_filename)		
		elif request.form['username'] =='n':		
			flash('Your Origin of planet is earth')
			full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'earth.png')
			return render_template("result.html", user_image = full_filename)	
		elif request.form['username'] =='o':		
			flash('Your Origin of planet is uranus')
			full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'uranus.png')
			return render_template("result.html", user_image = full_filename)
		elif request.form['username'] =='p':		
			flash('Your Origin of planet is uranus')
			full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'uranus.png')
			return render_template("result.html", user_image = full_filename)
		elif request.form['username'] =='q':		
			flash('Your Origin of planet is venus')
			full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'venus.gif')
			return render_template("result.html", user_image = full_filename)
		elif request.form['username'] =='r':		
			flash('Your Origin of planet is venus')
			full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'venus.gif')
			return render_template("result.html", user_image = full_filename)	
		elif request.form['username'] =='s':		
			flash('Your Origin of planet is earth')
			full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'earth.png')
			return render_template("result.html", user_image = full_filename)
		elif request.form['username'] =='t':		
			flash('Your Origin of planet is mars')
			full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'mars.png')
			return render_template("result.html", user_image = full_filename)
		elif request.form['username'] =='u':		
			flash('Your Origin of planet is sun')
			full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'sun.png')
			return render_template("result.html", user_image = full_filename)	
		elif request.form['username'] =='v':		
			flash('Your Origin of planet is pluto')
			full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'pluto.png')
			return render_template("result.html", user_image = full_filename)
		elif request.form['username'] =='w':		
			flash('Your Origin of planet is pluto')
			full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'pluto.png')
			return render_template("result.html", user_image = full_filename)
		elif request.form['username'] =='x':		
			flash('Your Origin of planet is sun')
			full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'sun.png')
			return render_template("result.html", user_image = full_filename)	
		elif request.form['username'] =='y':		
			flash('Your Origin of planet is venus')
			full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'venus.gif')
			return render_template("result.html", user_image = full_filename)
		elif request.form['username'] =='z':		
			flash('Your Origin of planet is jupiter')
			full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'jupiter.png')
			return render_template("result.html", user_image = full_filename)							
		elif len('username') >=2:
			error='Invalid input!'
		else:			
			error='Invalid input!'	 							
	return render_template('science.html', error = error)


@app.route('/result')
def result():
	return render_template('result.html')
	

@app.route('/about.html/')
def about():
	return render_template('about.html')

@app.route("/create-test.html")
def create_test():
	title="Create Test"
	return render_template('create-test.html',title=title)

#Run the python app file 
if __name__ == '__main__':
	app.run(debug=True)