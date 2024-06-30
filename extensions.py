from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)

app.config["SECRET_KEY"] = "@JHSHDA$*!"
UPLOAD_FOLDER = "C:\\home\\user\\Desktop\\Final Project(hybrid)\\static\\Image\\Drums"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db = SQLAlchemy(app)

login_manager = LoginManager(app)

products = []
