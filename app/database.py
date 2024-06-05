import os
from .utils import *
import sqlite3

attendance_recorded = {}

# Функция инициализации базы данных
def db_init(app):
    db_path = os.path.join(app.root_path, 'app/db/database.db')
    app.config['DATABASE'] = db_path
    with app.app_context():
        db = get_db()
        create_tables(db)

# Функция для получения соединения с базой данных
def get_db():
    db = sqlite3.connect('app/db/database.db')
    db.row_factory = sqlite3.Row
    return db

# Функция для создания таблиц в базе данных
def create_tables(db):
    db.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INT NOT NULL, 
            name TEXT NOT NULL,
            lastname TEXT NOT NULL,
            class TEXT NOT NULL
    )''')

# Функция для добавления нового пользователя в базу данных
def add_new_user(newusername, newuserlastname, newuserclass):
    newid = totalreg()
    db = get_db()
    db.execute(
        'INSERT INTO users (id, name, lastname, class) VALUES (?, ?, ?, ?)',
        (newid, newusername, newuserlastname, newuserclass)
    )
    db.commit()


# Функция для получения всех пользователей
def getallusers():
    db = get_db()
    cursor = db.cursor()
    cursor.execute('''
        Select id, name, lastname, class
        From users
    ''')
    userlist = cursor.fetchall()
    id = []
    names = []
    lastnames = []
    classes = []

    for user in userlist:
        nid, name, lastname, classs = user['id'], user['name'], user['lastname'], user['class']

        id.append(nid)
        names.append(name)
        lastnames.append(lastname)
        classes.append(classs)
    l = len(names)
    
    return userlist, id, names, lastnames, classes, l



def delete_user(duser):
    db = get_db()
    db.execute(
        'DELETE FROM users WHERE id = ?',
        (duser,)
    )
    db.commit()

    user_dir = os.path.join('app/faces_data/faces', duser)

    # Удаление всех файлов в папке
    for filename in os.listdir(user_dir):
        file_path = os.path.join(user_dir, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)

    # Удаление пустой папки
    os.rmdir(user_dir)

    # Функция для добавления записи о посещаемости
def add_attendance(name):
    userid = name.split('_')[0]
    current_time = datetime.now().strftime("%H:%M:%S")
    datetoday = date.today().strftime("%d-%B-%Y")

    # Проверяем, была ли уже запись для этого пользователя сегодня
    if attendance_recorded.get(userid, '') == datetoday:
        return  # Если запись уже была, выходим из функции

    db = get_db()
    cursor = db.cursor()

    cursor.execute('''
        SELECT name, lastname, class
        FROM users
        WHERE id = cast(? as INTEGER)
    ''', (userid,))

    userlist = cursor.fetchall()
    for user in userlist:
        username, userlastname, userclass = user['name'], user['lastname'], user['class']

    attendance_file = f'app/Attendance/Attendance-{datetoday}.csv'
    try:
        df = pd.read_csv(attendance_file)
    except FileNotFoundError:
        df = pd.DataFrame(columns=['Id', 'Name', 'Lastname', 'Class', 'Time'])

    if int(userid) not in df['Id'].astype(int).tolist():
        with open(attendance_file, 'a', encoding='utf-8') as f:
            f.write(f'\n{userid},{username},{userlastname},{userclass},{current_time}')
        # Отмечаем, что запись для пользователя сделана
        attendance_recorded[userid] = datetoday