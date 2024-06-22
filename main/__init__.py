from flask import Flask
from flask_mail import Mail
from itsdangerous import URLSafeSerializer
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_admin import Admin

app = Flask(__name__)
CORS(app)

app.config['SECRET_KEY'] = "0257hgr896743u0928652lkj0ps8252h604276og436"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'main/static/imgs/DiscountnEventImages'

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'ldzotsenidze4@gmail.com'
app.config['MAIL_PASSWORD'] = 'rcom lgpg furx fkbz'

mail = Mail(app)
serializer = URLSafeSerializer(app.config['SECRET_KEY'])

db = SQLAlchemy(app)
admin = Admin(app, name='SDO Administration', template_mode='bootstrap3')
bcrypt = Bcrypt(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from main import routes