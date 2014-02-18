# utils.py
import MySQLdb


DATABASE='compSciConferenceDB'
DB_USER = 'conferenceUser'
DB_PASSWORD = 'conferencePassword'
HOST = 'localhost'

def db_connect():
  return MySQLdb.connect(HOST, DB_USER, DB_PASSWORD, DATABASE)
