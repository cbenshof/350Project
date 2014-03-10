from flask import Flask, render_template, request
from datetime import datetime
import MySQLdb

app = Flask(__name__)

# Configuration

@app.route('/')
def mainIndex():
  return render_template('index.html')

# Post an event Form page - Logan & Candice

@app.route('/postEvent')
def eventPost():
	return render_template('postEvent.html')

# Display added event and add to the database - Logan & Candice

@app.route('/postEvent2', methods=['POST'])
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
	query = "INSERT INTO conferences VALUES (NULL, '" + MySQLdb.escape_string(request.form['conference_name']) + "', '" + MySQLdb.escape_string(request.form['acronym']) + "', '" + MySQLdb.escape_string(request.form['district']) + "', '" + MySQLdb.escape_string(request.form['country']) + "', '" + MySQLdb.escape_string(request.form['venue']) + "', '" + theDate + "', '" + theDate2 + "');"
	print query
	cur.execute(query)
	db.commit()

	return render_template('postEvent2.html', events=events)

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

  return render_template('conferences.html', conferences=rows)

# Connects to the database. If the database doesn't exist, it is created. If the conferences table
# does not exist, it is also created. Returns the db object.
def connectDB():
  db = MySQLdb.connect(host = 'localhost', user = 'root', passwd = 'password')
  cur = db.cursor()
  sql = 'CREATE DATABASE IF NOT EXISTS compSciConferenceDB;'
  print sql
  cur.execute(sql)
  sql = 'USE compSciConferenceDB;'
  print sql
  cur.execute(sql)
  sql = 'CREATE TABLE IF NOT EXISTS conferences (conference_id INT NOT NULL AUTO_INCREMENT, conference_name VARCHAR(175) NOT NULL, acronym VARCHAR(20) default NULL, district VARCHAR(25) default NULL, country VARCHAR(25) default NULL, venue VARCHAR(200) default NULL, start_date DATE NOT NULL, end_date DATE NOT NULL, PRIMARY KEY(conference_id));'
  print sql
  cur.execute(sql)
  db.commit()
  return db

if __name__ == '__main__':
  app.debug = True
  app.run(host='0.0.0.0', port=3000)
