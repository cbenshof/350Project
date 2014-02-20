from flask import Flask, render_template, request
import MySQLdb

app = Flask(__name__)

# Configuration

@app.route('/')
def mainIndex():
  return render_template('index.html')

@app.route('/conferences', methods=['GET'])
def confTable():
  db = connectDB()
  cur = db.cursor()

  cur.execute('select * from conferences;')
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
