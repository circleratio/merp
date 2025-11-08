import sqlite3
import merp_db as db
from merp_logger import set_logger, getLogger

set_logger()
logger = getLogger(__name__)

class Merp:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)

    def __del__(self):
        self.conn.close()

    def import_persons(self, json_data):
        for item in json_data:
            db.create_person(self.conn, item)

    def import_departments(self, json_data):
        for item in json_data:
            db.create_department(self.conn, item)

    def import_assignment(self, persons):
        for p in persons:
            person = db.read_persons(self.conn, email=p['メールアドレス']) # 一意性担保のためメールアドレスを使用
            department = db.read_departments(self.conn, name=p['所属組織'])
            db.create_assignment(self.conn, person[0]['id'], department[0]['id'])
        
    def import_approvers(self, persons):
        for p in persons:
            pos = p['役職']
            if pos == '代表理事' or pos == '理事':
                name = '理事決裁'
            elif pos == '部長':
                name = '部長決裁'
            else:
                continue
        
            person = db.read_persons(self.conn, email=p['メールアドレス'])  # 一意性担保のためメールアドレスを使用
            department = db.read_departments(self.conn, name=p['所属組織'])
            db.create_approvers(self.conn, name, person[0]['id'], department[0]['id'])

    def get_department_list(self):
        result = []
        
        departments = db.read_departments(self.conn)
        for i in departments:
            result.append(i)

        return(result)

    def get_department_person_list(self, department_id):
        result = []
        persons = db.read_assignments(self.conn, department=department_id)
        for i in persons:
            person = db.read_persons(self.conn, id=i['person'])
            result.append(person[0])

        return(result)
        
    def get_department_approver_list(self, department_id):
        result = []
    
        persons = db.read_approvers(self.conn, department=department_id)
        for i in persons:
            person = db.read_persons(self.conn, id=i['person'])
            result.append(person[0])

        return(result)

    def get_department_upper_department(self, department_id):
        if department_id == None:
            return(None)
    
        department = db.read_departments(self.conn, id=department_id)

        return(department[0]['parent'])
    
    def get_person(self, person_id):
        person = db.read_persons(self.conn, id=person_id)
        return(person[0])
        
def main():
    merp = Merp('merp.db')

    #print(merp.get_department_list())
    #print(merp.get_department_person_list(2))
    #print(merp.get_department_approver_list(2))
    #print(merp.get_department_upper_department(2)) # 1
    #print(merp.get_department_upper_department(1)) # None
    print(merp.get_person(5))
    
if __name__ == '__main__':
    main()
