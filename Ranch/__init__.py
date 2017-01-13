from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import settings
from database import engine, sessionmaker
import logging

conf = settings.Configure()
logging.basicConfig(filename=conf.LOG_NAME, level=conf.LOG_LEVEL, format='%(asctime)s %(message)s')


logging.debug('*** Starting {0}'.format(conf.BLOG_NAME))
app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = conf.database_connection_string
app.config["SECRET_KEY"] = conf.secret_key
db = SQLAlchemy(app)

DBSession = sessionmaker(bind=engine)

import views
