import sqlite3
import json
import util
from merp_logger import set_logger, getLogger

logger = getLogger(__name__)

dbname = 'merp.db'
conn = sqlite3.connect(dbname)

cur = conn.cursor()

cur.execute('CREATE TABLE persons(id INTEGER PRIMARY KEY AUTOINCREMENT, name STRING, position STRING, email STRING)')
cur.execute('CREATE TABLE departments(id INTEGER PRIMARY KEY AUTOINCREMENT, name STRING, category INTEGER, parent INTEGER)')
cur.execute('CREATE TABLE approvers(id INTEGER PRIMARY KEY AUTOINCREMENT, name STRING, person INTEGER, department INTEGER)')
cur.execute('CREATE TABLE assignments(id INTEGER PRIMARY KEY AUTOINCREMENT, person INTEGER, department INTEGER)')

with open('data/persons.json', 'r', encoding='utf-8') as f:
    js = json.load(f)
    util.import_persons(conn, js)
        
with open('data/departments.json', 'r', encoding='utf-8') as f:
    js = json.load(f)
    util.import_departments(conn, js)

with open('data/persons.json', 'r', encoding='utf-8') as f:
    js = json.load(f)
    util.import_assignment(conn, js)
    
with open('data/persons.json', 'r', encoding='utf-8') as f:
    js = json.load(f)
    util.import_approvers(conn, js)
    
conn.commit()
conn.close()
