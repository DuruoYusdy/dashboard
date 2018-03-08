from flask import Flask
# from apscheduler.schedulers.background import BackgroundScheduler
from flask_apscheduler import APScheduler
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)
scheduler = APScheduler()
scheduler.init_app(app)

import server.model
import server.view
import server.schedule

db.create_all()
scheduler.start()

