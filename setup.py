import sqlite3
import json
import merp
from merp_logger import getLogger

logger = getLogger(__name__)

dbname = 'merp.db'
conn = sqlite3.connect(dbname)

cur = conn.cursor()

cur.execute('CREATE TABLE persons(id INTEGER PRIMARY KEY AUTOINCREMENT, name STRING, position STRING, email STRING)')
cur.execute('CREATE TABLE departments(id INTEGER PRIMARY KEY AUTOINCREMENT, name STRING, category INTEGER, parent INTEGER)')
cur.execute('CREATE TABLE approvers(id INTEGER PRIMARY KEY AUTOINCREMENT, name STRING, person INTEGER, department INTEGER)')
cur.execute('CREATE TABLE assignments(id INTEGER PRIMARY KEY AUTOINCREMENT, person INTEGER, department INTEGER)')

merp = merp.Merp('merp.db')

with open('data/persons.json', 'r', encoding='utf-8') as f:
    js = json.load(f)
    merp.import_persons(js)
        
with open('data/departments.json', 'r', encoding='utf-8') as f:
    js = json.load(f)
    merp.import_departments(js)

with open('data/persons.json', 'r', encoding='utf-8') as f:
    js = json.load(f)
    merp.import_assignment(js)
    
with open('data/persons.json', 'r', encoding='utf-8') as f:
    js = json.load(f)
    merp.import_approvers(js)
    
conn.commit()
conn.close()
