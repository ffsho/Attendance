from flask import Blueprint, render_template, request
from .face_recognition import *
from .database import *

# Создание blueprints для маршрутов
home_bp = Blueprint('home', __name__)
listusers_bp = Blueprint('listusers', __name__)
deleteuser_bp = Blueprint('deleteuser', __name__)
add_bp = Blueprint('add', __name__)
start_bp = Blueprint('start', __name__)

# Маршруты для домашней страницы
@home_bp.route('/')
def home():
    names, lastnames, classes, times, l = extract_attendance()
    return render_template('home.html', names=names, lastnames=lastnames, classes = classes, times=times, l=l, totalreg=totalreg(), datetoday=datetoday)

# Маршруты для страницы списка пользователей
@listusers_bp.route('/listusers')
def listusers():
    userlist, id, names, lastnames, classes, l = getallusers()
    return render_template('listusers.html', userlist=userlist, id=id, names=names, lastnames=lastnames, classes=classes, l=l, totalreg=totalreg(), datetoday=datetoday)

# Маршруты для удаления пользователя
@deleteuser_bp.route('/deleteuser', methods=['GET'])
def deleteuser():
    duser = request.args.get('user')
    delete_user(duser)  # Вызываем функцию удаления из базы данных
    train_model()
    userlist, id, names, lastnames, classes, l = getallusers()
    return render_template('listusers.html', userlist=userlist, id=id, names=names, lastnames=lastnames, classes=classes, l=l, totalreg=totalreg(), datetoday=datetoday)

# Маршруты для добавления нового пользователя
@add_bp.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        newusername = request.form['newusername']
        newuserlastname = request.form['newuserlastname']
        newuserclass = request.form['newuserclass']
        add_new_user(newusername, newuserlastname, newuserclass)
        tot = totalreg()
        add_new_user_with_camera(str(tot)) 
        names, lastnames, classes, times, l = extract_attendance()
        return render_template('home.html', names=names, lastnames=lastnames, classes=classes, times=times, l=l, totalreg=totalreg(), datetoday=datetoday)
    else:
        return render_template('add_user.html')

# Маршруты для запуска распознавания лиц
@start_bp.route('/start', methods=['GET'])
def start():
    names, lastnames, classes, times, l = extract_attendance()
    if 'face_recognition_model.pkl' not in os.listdir('app/faces_data'):
        return render_template('home.html', names=names, lastnames=lastnames, classes=classes, times=times, l=l, totalreg=totalreg(), datetoday=datetoday, mess='There is no trained model in the faces_data folder. Please add a new face to continue.')
    start_recognition()
    names, lastnames, classes, times, l = extract_attendance()
    return render_template('home.html', names=names, lastnames=lastnames, classes=classes, times=times, l=l, totalreg=totalreg(), datetoday=datetoday)

# Регистрация blueprints
def register_routes(app):
    app.register_blueprint(home_bp)
    app.register_blueprint(listusers_bp)
    app.register_blueprint(deleteuser_bp)
    app.register_blueprint(add_bp)
    app.register_blueprint(start_bp)