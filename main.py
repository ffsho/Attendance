from flask import Flask, request, render_template
from app.routes import *  
from app.utils import *
from app.face_recognition import *
from app.database import *

app = Flask(__name__)

create_directories()
# Регистрация маршрутов
register_routes(app)

# Инициализация базы данных
db_init(app)

if __name__ == '__main__':
    app.run(debug=True)