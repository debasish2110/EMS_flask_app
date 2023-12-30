from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import secrets

db = SQLAlchemy()

HOST = 'localhost'
USER = 'root'
PASSWORD = 'r00T#21!'
DATABASE = 'task_tracker'

class Task(db.Model):
    taskID = db.Column(db.String(50), nullable=False, primary_key=True)
    sprint = db.Column(db.String(100), nullable=True)
    employeeName = db.Column(db.String(100), nullable=False)
    startDate = db.Column(db.String(20), nullable=False)
    endDate = db.Column(db.String(20), nullable=False)
    duration = db.Column(db.String(255), nullable=False)
    remark = db.Column(db.String(255), nullable=False)

def init_app(app):
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+mysqlconnector://{USER}:{PASSWORD}@localhost/{DATABASE}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SESSION_TYPE'] = 'filesystem'
    app.secret_key = secrets.token_hex(16)
    db.init_app(app)
    migrate = Migrate(app, db)
