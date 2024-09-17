from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
# ip integra
localhost =  '192.168.220.5'
# sqlite:///Blog.db

app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://alaiseide:Flashreverso2020..@{localhost}/blog'
app.config['SECRET_KEY'] = '9b4f2d8050ae28c1b0354f4bd7aa8e62'
app.config['UPLOAD_FOLDER'] = 'static/images'
login_manager = LoginManager(app)
database = SQLAlchemy(app)

# a pagina onde o usuario sera redirecionado caso tente acessar uma pagina sem fazer login
# passei login que é a minha pagina de cadastro
login_manager.login_view = "login"
login_manager.login_message = 'Faça login para acessar esta página, por favor.'
login_manager.login_message_category = 'alert-info'




from . import routes