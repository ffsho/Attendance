# import sqlite3

# def get_db():
#     db = sqlite3.connect('app/db/database.db')
#     db.row_factory = sqlite3.Row
#     return db


# db = get_db()
# db.execute('''
#         Select name, lastname, class
#         From users
#         Where id = cast(? as INT)
#     ''', (str(0)))

# user = db.cursor().fetchall()
# print(user)

# import sqlite3

# def get_db():
#     db = sqlite3.connect('app/db/database.db')
#     db.row_factory = sqlite3.Row  # This sets rows to be returned as dictionaries
#     return db

# db = get_db()

# # Use a cursor to execute the query and fetch results
# cursor = db.cursor()
# cursor.execute('''
#     SELECT name, lastname, class
#     FROM users
#     WHERE id = ?
# ''', (0,))  # Note: Use a tuple for parameters, even if it's just one value

# users = cursor.fetchall()  # Fetch all results from the cursor

# # Print the results
# for user in users:
#     print(user['name'], user['lastname'], user['class'])

# db.close() 


# import sqlite3

# def get_db():
#     db = sqlite3.connect('app/db/database.db')
#     db.row_factory = sqlite3.Row
#     return db

# def get_all_users():
#     db = get_db()
#     cursor = db.cursor()
#     cursor.execute('''
#         SELECT name, lastname, class
#         FROM users
#     ''')
#     user_list = cursor.fetchall()
#     db.close()

#     names = []
#     lastnames = []
#     classes = []

#     for user in user_list:
#         name = user['name']
#         lastname = user['lastname']
#         classs = user['class']
#         names.append(name)
#         lastnames.append(lastname)
#         classes.append(classs)
#     l = len(names) + 1
#     return user_list, names, lastnames, classes, l

# # Example usage
# users, names, lastnames, classes, l = get_all_users()
# for i in range(l - 1):
#     print(names[i], lastnames[i], classes[i])


import pandas as pd
from datetime import date

def extract_attendance():
    datetoday = date.today().strftime("%d-%B-%Y")
    
    try:
        df = pd.read_csv(f'app/Attendance/Attendance-{datetoday}.csv', encoding='utf-8')
    except UnicodeDecodeError:
        df = pd.read_csv(f'app/Attendance/Attendance-{datetoday}.csv', encoding='latin1')  # Try a different encoding if utf-8 fails
    
    ids = df['Id']
    names = df['Name']
    lastnames = df['Lastname']
    classes = df['Class']
    times = df['Time']
    l = len(df)
    
    return ids, names, lastnames, classes, times, l
ids, names, lastnames, classes, times, l = extract_attendance()

for id in ids:
    print(id)