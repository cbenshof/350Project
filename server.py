from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime
import MySQLdb

app = Flask(__name__)
app.secret_key = 'oN3P0C1dBe96Bdjqjxu3'
# Configuration

def esc(string):
  return MySQLdb.escape_string(request.form[string])

@app.route('/')
def mainIndex():
  if 'username' in session:
    return render_template('index.html', user = session['username'])
  else:
    return render_template('index.html', user = "")

# Post an event Form page - Logan & Candice

@app.route('/postEvent')
def eventPost():
  if 'username' in session:
    return render_template('postEvent.html', user = session['username'])
  else:
    return render_template('postEvent.html', user = "")

# Display added event and add to the database - Logan & Candice

@app.route('/postEvent2', methods=['GET', 'POST'])
def postEvent2():
  db = connectDB()
  cur = db.cursor()
	
  events = {
    'conference_name': request.form['conference_name'],
    'acronym': request.form['acronym'],
    'district': request.form['district'],
    'country': request.form['country'],
    'venue': request.form['venue'],
    'month': request.form['month'],
    'month2': request.form['month2'],
    'day': request.form['day'],
    'day2': request.form['day2'],
    'year': request.form['year'],
    'year2': request.form['year2']
  }
  theDate = request.form['year'] + "-" + request.form['month'] + "-" + request.form['day']
  startDate = datetime.strptime(theDate, '%Y-%m-%d')

  theDate2 = request.form['year2'] + "-" + request.form['month2'] + "-" + request.form['day2']
  endDate = datetime.strptime(theDate2, '%Y-%m-%d')
  
  # enter the query
  query = "INSERT INTO conferences VALUES (NULL, '%s', '%s', '%s', '%s', '%s', '%s', '%s');" % (esc('conference_name'), esc('acronym'), esc('district'), esc('country'), esc('venue'), theDate, theDate2)
  print query
  cur.execute(query)
  db.commit()
  if 'username' in session:
    return render_template('postEvent2.html', events = events, user = session['username'])
  else:
    return render_template('postEvent2.html', events = events, user = "")

# edit a conference 
@app.route('/edit', methods=['GET', 'POST'])
def editEntry():
	db = connectDB()
	cur = db.cursor()
	events = {
		

	}
	
	return render_template('postEvent2.html', events = events, user ="")


@app.route('/conferences', methods=['GET', 'POST'])
def confTable():
  db = connectDB()
  cur = db.cursor()

  if request.method == 'GET':
    cur.execute('select * from conferences;')
    rows = cur.fetchall()
  if request.method == 'POST':
    query = "select * from conferences WHERE conference_name LIKE '%" + MySQLdb.escape_string(request.form['search_field']) + "%' OR acronym LIKE '%" + MySQLdb.escape_string(request.form['search_field']) + "%' OR district LIKE '%" + MySQLdb.escape_string(request.form['search_field']) + "%' OR country LIKE '%" + MySQLdb.escape_string(request.form['search_field']) + "%' OR venue LIKE '%" + MySQLdb.escape_string(request.form['search_field']) + "%';"
    print query
    cur.execute(query)
    rows = cur.fetchall()
    
  if 'username' in session:
    return render_template('conferences.html', conferences = rows, user = session['username'])
  else:
    return render_template('conferences.html', conferences = rows, user = "")

# Displays the login form. If the form is submitted (request.method == 'POST'),
# attempt to log the user in. If successful, redirect to the index page.
# If unsuccessful, display an error message and allow the user to try again.
# Cody Reibsome (creibsom@mail.umw.edu) - 3/11/2014
@app.route('/login', methods=['GET', 'POST'])
def login():
  db = connectDB()
  cur = db.cursor()
  errorMsg = ""

  if request.method == 'POST':
    query = "SELECT * FROM users WHERE username = '%s' AND password = SHA2('%s', 0);" % (esc('username'), esc('password'))
    cur.execute(query)
    row = cur.fetchone()
    if row:
      session['username'] = row[1]
      session['email'] = row[3]
      # Any more session imports would go here
      return redirect(url_for('mainIndex'))
    else:
      errorMsg = "Incorrect username or password."
  if 'username' in session:
    return render_template('login.html', user = session['username'], errorMessage = errorMsg)
  else:
    return render_template('login.html', user = "", errorMessage = errorMsg)

# Pops the user's information out of the session variable and redirects to index page.
# Cody Reibsome (creibsom@mail.umw.edu) - 3/11/2014
@app.route('/logout')
def logout():
  session.pop('username', None)
  session.pop('email', None)
  # Be sure to pop off any additional session variables
  return redirect(url_for('mainIndex'))

# Displays the registration form. If the form is submitted (request.method == 'POST'),
# redisplay with any error messages, or, if valid, add the user to the database and
# redirect to the index page.
# Cody Reibsome (creibsom@mail.umw.edu) - 3/11/2014
@app.route('/register', methods=['GET', 'POST'])
def register():
  db = connectDB()
  cur = db.cursor()
  errorMsg = ""

  if request.method == 'POST':
    query = "SELECT * FROM users WHERE username = '%s';" % (esc('username'))
    print query
    cur.execute(query)
    rows = cur.fetchall()

    # [NON-URGENT] Add a way to check for valid e-mail address format [NON-URGENT]
    if rows:
      errorMsg = "Username %s already in use, please try another username." % (esc('username'))
    elif (esc('password') != esc('confirmPassword')):
      errorMsg = "Passwords do not match, please try again."
    else:
      query = "INSERT INTO users VALUES (NULL, '%s', SHA2('%s', 0), '%s');" % (esc('username'), esc('password'), esc('email'))
      print query
      cur.execute(query)
      db.commit()
      session['username'] = request.form['username']
      session['email'] = request.form['email']
      return redirect(url_for('mainIndex'))

  if 'username' in session:
    return render_template('register.html', user = session['username'], errorMessage = errorMsg)
  else:
    return render_template('register.html', user = "", errorMessage = errorMsg)

# Connects to the database. If the database doesn't exist, it is created. If the conferences table
# does not exist, it is also created. Returns the db object.
# Cody Reibsome (creibsom@mail.umw.edu)
def connectDB():
  db = MySQLdb.connect(host = 'localhost', user = 'root', passwd = 'password')
  cur = db.cursor()
  sql = 'CREATE DATABASE IF NOT EXISTS compSciConferenceDB;'
  print sql
  cur.execute(sql)
  sql = 'USE compSciConferenceDB;'
  print sql
  cur.execute(sql)
  sql = "CREATE TABLE IF NOT EXISTS conferences (conference_id INT NOT NULL AUTO_INCREMENT, conference_name VARCHAR(175) NOT NULL, acronym VARCHAR(20) default NULL, district VARCHAR(25) default NULL, country VARCHAR(25) default NULL, venue VARCHAR(200) default NULL, start_date DATE NOT NULL, end_date DATE NOT NULL, PRIMARY KEY(conference_id));"
  print sql
  cur.execute(sql)
  sql = "CREATE TABLE IF NOT EXISTS users (user_id INT NOT NULL AUTO_INCREMENT, username VARCHAR(20) NOT NULL, password VARCHAR(64) NOT NULL, email VARCHAR(80) default NULL, PRIMARY KEY(user_id));"
  print sql
  cur.execute(sql)
  db.commit()
  return db

if __name__ == '__main__':
  app.debug = True
  app.run(host='0.0.0.0', port=3000)
