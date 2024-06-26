import sqlite3
import course



con = sqlite3.connect('classmate')
cur = con.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS classes (
            name text, 
            code text PRIMARY KEY, 
            hours integer
            )''')

cur.execute('''CREATE TABLE IF NOT EXISTS grades (
            code text,
            name text,
            weight real,
            assignments integer,
            entered integer,
            grade0 real default null, grade1 real default null, grade2 real default null, grade3 real default null, grade4 real default null, grade5 real default null,
            grade6 real default null, grade7 real default null, grade8 real default null, grade9 real default null, grade10 real default null,
            grade11 real default null, grade12 real default null, grade13 real default null, grade14 real default null, grade15 real default null,
            grade16 real default null, grade17 real default null, grade18 real default null, grade19 real default null, grade20 real default null,
            grade21 real default null, grade22 real default null, grade23 real default null, grade24 real default null, grade25 real default null,
            grade26 real default null, grade27 real default null, grade28 real default null, grade29 real default null, grade30 real default null,
            grade31 real default null, grade32 real default null, grade33 real default null, grade34 real default null, grade35 real default null,
            grade36 real default null, grade37 real default null, grade38 real default null, grade39 real default null
            )''')

cur.execute('''CREATE TABLE IF NOT EXISTS scale (
            code text PRIMARY KEY,
            Ap real default 97, An real default 93, Am real default 90,
            Bp real default 87, Bn real default 83, Bm real default 80,
            Cp real default 77, Cn real default 73, Cm real default 70,
            Dp real default 67, Dn real default 63, Dm real default 60
            )''')


def insert_class(course):
    with con:
        cur.execute("INSERT OR IGNORE INTO classes VALUES(:name, :code, :hours)", 
                    {'name': course.name, 'code': course.code, 'hours': course.hours})
        
def add_letters(code):
    with con:       
        cur.execute('INSERT OR IGNORE INTO scale (code) VALUES (?)',
                    (code,))
    
def get_letters(code):
    output=[]
    with con:
        cur.execute('SELECT * FROM scale WHERE code = :code', {'code': code})
        data=cur.fetchone()
        for i in range(1, len(data)):
            output.append(data[i])
    return output
 
def get_class_by_code(code):
    with con:
        cur.execute("SELECT * FROM classes WHERE code = :code", {'code': code})
        output = cur.fetchone()
        return output

def remove_class(code):
    with con:
        cur.execute("DELETE from classes WHERE code = :code", {'code': code})
        cur.execute('DELETE FROM grades WHERE code = :code', {'code': code})

def insert_category(category):
    with con:
        cur.execute("INSERT OR IGNORE INTO grades (code, name, weight, assignments, entered)VALUES(?, ?, ?, ?, ?)",
                    (category.code, category.name, category.weight, category.assignments, category.entered))
        for i in range (0, category.assignments):
            update_statement = f"UPDATE grades SET grade{i}=0 WHERE code = :code and name = :name "
            cur.execute(update_statement, {'code': category.code, 'name': category.name})

def remove_category(code, name):
    with con:
        cur.execute('DELETE FROM grades WHERE code = :code and name = :name', {'code': code, 'name': name})

def get_course_codes():
    output=[]
    with con:
        cur.execute("SELECT code FROM classes")
        data = cur.fetchall()
        for row in data:
            output.append(row[0])  
        return output   
    
def get_course_categories(code):
    output=[]
    with con:
        cur.execute('SELECT name FROM grades where code = :code', {'code': code})
        data = cur.fetchall()
        for row in data:
            output.append(row[0])
    return output

def get_category_info(code, name):
    output=[]
    with con:
        cur.execute('SELECT * FROM grades where code = :code and name = :name', 
                    {'code': code, 'name': name})
        data=cur.fetchone()
        for i in data:
            output.append(i)
    return output

def add_grade(code, categoryName, score):
    entered=get_category_info(code, categoryName)[4]
    if entered >= get_category_info(code, categoryName)[3]:
        return 0
    new = entered+1
    with con:
        grade_update_statement=f'UPDATE grades SET grade{entered}={score} where code=:code and name=:name'
        cur.execute(grade_update_statement, {'code': code, 'name': categoryName})
        entered_update_statement=f'UPDATE grades SET entered = {new} where code=:code and name=:name'
        cur.execute(entered_update_statement, {'code': code, 'name': categoryName})
    return 1

def update_grade(code, category, oldScore, newScore):
    grades=get_category_grades(code, category)
    index=-1
    for i in range(len(grades)):
        if grades[i] == oldScore:
            index=i
            pass
    if index==-1:
        return 0
    with con:
        update_statement = f'UPDATE grades SET grade{index}={newScore} where code = :code and name = :name'
        cur.execute(update_statement, {'code': code, 'name': category})

def grade_average(code, categoryName):
    average=0
    info=get_category_info(code, categoryName)
    if info[4] == 0: return -1
    for i in range(info[4]):
        j=i+5
        average+=info[j]
    average/=info[4]
    return round(average, 2)

def grade_progress(code, categoryName):
    average=0
    info=get_category_info(code, categoryName)
    for i in range(info[4]):
        j=i+5
        average+=info[j]
    average/=info[3]
    return round(average, 2)

def check_category_weights(code):
    ret=0
    with con:
        cur.execute('SELECT weight fROM grades where code =:code', {'code': code})
        weights=cur.fetchall()
        for i in weights:
            ret+=i[0]
    return ret

def grade_potential(code, categoryName):
    info = get_category_info(code, categoryName)
    entered = info[4]
    unentered = info[3]-entered
    potential=0
    for i in range (entered):
        j = i+5
        potential+=info[j]
    for i in range (unentered):
        j = i+5
        j += entered
        potential+=100
    potential/=info[3]
    return round(potential, 2)

def course_average(code):
    categories=get_course_categories(code)
    total=0
    weighted=0
    for i in categories:
        info=get_category_info(code, i)
        weight=info[2]
        category_average=grade_average(code, i)
        if category_average >= 0:
            total+= category_average*weight/100
            weighted+=weight
    if weighted == 0:
        return 0
    total*=100
    total/=weighted
    return round(total, 2)

def course_progress(code):
    categories=get_course_categories(code)
    total=0
    for i in categories:
        info=get_category_info(code, i)
        weight=info[2]
        category_progress=grade_progress(code, i)
        total+= category_progress*weight/100
    return round(total, 2)

def course_potential(code):
    categories=get_course_categories(code)
    total=0
    for i in categories:
        info=get_category_info(code, i)
        weight=info[2]
        category_progress=grade_potential(code, i)
        total+= category_progress*weight/100
    return round(total, 2)

def get_category_grades(code, category):
    info=get_category_info(code, category)
    entered=info[4]
    grades=[]
    for i in range(entered):
        j=i+5
        grades.append(info[j])
    return grades

def update_letter_cutoff(code, letter, new):
    newInt = float(new)
    current = get_letters(code)
    letters = ['A+', 'A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'C-', 'D+', 'D', 'D-']
    letters_db = ['Ap', 'An', 'Am', 'Bp', 'Bn', 'Bm', 'Cp', 'Cn', 'Cm', 'D+p', 'Dn', 'Dm']
    index = -1
    for i in range(len(current)):
        if letter == letters[i]: index = i
    if newInt >= current[index-1]:
        return 0
    if newInt <= current[index+1]:
        return 0
    with con:
        update_statement = f'UPDATE scale SET {letters_db[index]} = {newInt} where code = :code'
        cur.execute(update_statement, {'code': code})




con.commit()


#i love drake <3