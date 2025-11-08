from merp_logger import getLogger

logger = getLogger(__name__)

def create_person(conn, item):
    cur = conn.cursor()

    # 重複チェック
    cur.execute('SELECT id FROM persons WHERE name=? AND email=?;', (item['名前'], item['メールアドレス']))
    rows = cur.fetchall()
    if len(rows) >= 1:
        print('既に同じ名前、メールアドレスが存在します。登録をスキップします。({}, {})'.format(item['名前'], item['メールアドレス']))
        logger.warning('既に名前、同じメールアドレスが存在します。登録をスキップします。({}, {})'.format(item['名前'], item['メールアドレス']))
        return

    # 登録
    cur.execute('INSERT INTO persons(name, position, email) values(?, ?, ?);', (item['名前'], item['役職'], item['メールアドレス']))
    conn.commit()

def create_department(conn, item):
    cur = conn.cursor()

    # 重複チェック
    cur.execute('SELECT id FROM departments WHERE category=? AND name=?;', (item['分類'], item['名前']))
    rows = cur.fetchall()
    if len(rows) >= 1:
        print('既に同じ分類、名前の組織が存在します。登録をスキップします。({}, {})'.format(item['分類'], item['名前']))
        logger.warning('既に同じ分類、名前の組織が存在します。登録をスキップします。({}, {})'.format(item['分類'], item['名前']))
        return

    parent_id = None
    if '上位組織' in item:
        cur.execute('SELECT id FROM departments WHERE category=? AND name=?;', (item['分類'], item['上位組織']))
        rows = cur.fetchall()

        if len(rows) != 1:
            print('親組織がないか、複数あります。登録をスキップします。({}, {})'.format(item['分類'], item['上位組織']))
            logger.warning('親組織がないか、複数あります。登録をスキップします。({}, {})'.format(item['分類'], item['上位組織']))
            return

        parent_id = rows[0][0]

    # 登録
    cur.execute('INSERT INTO departments(name, category, parent) values(?, ?, ?);', (item['名前'], item['分類'], parent_id))
    conn.commit()
    
def read_persons(conn, **kwargs):
    result = []
    query_base = 'SELECT * FROM persons'
    query_add = ''
    query_kwargs = []
    args = ()

    cur = conn.cursor()

    if 'id' in kwargs:
        query_kwargs.append('id=?')
        args = args + (kwargs['id'],)
    if 'name' in kwargs:
        query_kwargs.append('name=?')
        args = args + (kwargs['name'],)
    if 'position' in kwargs:
        query_kwargs.append('position=?')
        args = args + (kwargs['position'],)
    if 'email' in kwargs:
        query_kwargs.append('email=?')
        args = args + (kwargs['email'],)

    if len(kwargs) > 0:
        query_add = ' WHERE ' + ' AND '.join(query_kwargs)

    query = '{}{};'.format(query_base, query_add)
    cur.execute(query, args)
    rows = cur.fetchall()
    for r in rows:
        person = {
            'id': r[0],
            'name': r[1],
            'position': r[2],
            'email': r[3],
        }
        result.append(person)
        
    return(result)

def read_departments(conn, **kwargs):
    result = []
    query_base = 'SELECT * FROM departments'
    query_add = ''
    query_kwargs = []
    args = ()

    cur = conn.cursor()

    if 'id' in kwargs:
        query_kwargs.append('id=?')
        args = args + (kwargs['id'],)
    if 'name' in kwargs:
        query_kwargs.append('name=?')
        args = args + (kwargs['name'],)
    if 'category' in kwargs:
        query_kwargs.append('category=?')
        args = args + (kwargs['category'],)

    if len(kwargs) > 0:
        query_add = ' WHERE ' + ' AND '.join(query_kwargs)

    query = '{}{};'.format(query_base, query_add)
    cur.execute(query, args)
    rows = cur.fetchall()
    for r in rows:
        department = {
            'id': r[0],
            'name': r[1],
            'category': r[2],
            'parent': r[3],
        }
        result.append(department)
        
    return(result)

# def read_person(conn, person_id):
#     cur = conn.cursor()
#     cur.execute('SELECT * FROM persons WHERE id=?;', (person_id,))
#     rows = cur.fetchall()
    
#     if len(rows) == 0:
#         return(None)
        
#     if len(rows) > 1:
#         print('idが重複しています。({})'.format(person_id))
#         logger.warning('idが重複しています。({})'.format(person_id))
#         return(None)
    
#     person = {
#         'id': rows[0][0],
#         'name': rows[0][1],
#         'position': rows[0][2],
#         'email': rows[0][3],
#     }
#     return(person)
            
def create_assignment(conn, person_id, department_id):
    cur = conn.cursor()

    # 重複チェック
    cur.execute('SELECT id FROM assignments WHERE person=? AND department=?;', (person_id, department_id))
    rows = cur.fetchall()
    if len(rows) >= 1:
        print('既に同じ配属が存在します。登録をスキップします。({}, {})'.format(person_id, department_id))
        logger.warning('既に同じ配属が存在します。登録をスキップします。({}, {})'.format(person_id, department_id))
        return

    # 登録
    cur.execute('INSERT INTO assignments(person, department) values(?, ?);', (person_id, department_id))
    conn.commit()

def read_assignments(conn, **kwargs):
    result = []
    query_base = 'SELECT * FROM assignments'
    query_add = ''
    query_kwargs = []
    args = ()

    cur = conn.cursor()

    if 'id' in kwargs:
        query_kwargs.append('id=?')
        args = args + (kwargs['id'],)
    if 'person' in kwargs:
        query_kwargs.append('person=?')
        args = args + (kwargs['person'],)
    if 'department' in kwargs:
        query_kwargs.append('department=?')
        args = args + (kwargs['department'],)

    if len(kwargs) > 0:
        query_add = ' WHERE ' + ' AND '.join(query_kwargs)

    query = '{}{};'.format(query_base, query_add)
    cur.execute(query, args)
    rows = cur.fetchall()
    for r in rows:
        department = {
            'id': r[0],
            'person': r[1],
            'department': r[2],
        }
        result.append(department)
        
    return(result)

def create_approvers(conn, name, person_id, department_id):
    cur = conn.cursor()

    # 重複チェック
    cur.execute('SELECT id FROM approvers WHERE person=? AND department=?;', (person_id, department_id))
    rows = cur.fetchall()
    if len(rows) >= 1:
        print('既に同じ承認権限が存在します。登録をスキップします。({}, {})'.format(person_id, department_id))
        logger.warning('既に同じ承認権限が存在します。登録をスキップします。({}, {})'.format(person_id, department_id))
        return

    # 登録
    cur.execute('INSERT INTO approvers(name, person, department) values(?, ?, ?);', (name, person_id, department_id))
    conn.commit()
        
def read_approvers(conn, **kwargs):
    result = []
    query_base = 'SELECT * FROM approvers'
    query_add = ''
    query_kwargs = []
    args = ()

    cur = conn.cursor()

    if 'id' in kwargs:
        query_kwargs.append('id=?')
        args = args + (kwargs['id'],)
    if 'person' in kwargs:
        query_kwargs.append('person=?')
        args = args + (kwargs['person'],)
    if 'department' in kwargs:
        query_kwargs.append('department=?')
        args = args + (kwargs['department'],)

    if len(kwargs) > 0:
        query_add = ' WHERE ' + ' AND '.join(query_kwargs)

    query = '{}{};'.format(query_base, query_add)
    cur.execute(query, args)
    rows = cur.fetchall()
    for r in rows:
        department = {
            'id': r[0],
            'name': r[1],
            'person': r[2],
            'department': r[3],
        }
        result.append(department)
        
    return(result)

def main():
    pass

if __name__ == '__main__':
    main()
