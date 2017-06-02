import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import settings
from database import engine, sessionmaker
import logging

conf = settings.Configure()
logging.basicConfig(filename=conf.LOG_NAME, level=conf.LOG_LEVEL, format='%(asctime)s %(message)s')


logging.debug('*** Starting {0}'.format(conf.BLOG_NAME))
app = Flask(__name__)


# app.config["SQLALCHEMY_DATABASE_URI"] = conf.database_connection_string
app.logger.info('myLogger: setting 1')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.logger.info('myLogger: setting 2')
app.config["SECRET_KEY"] = conf.secret_key
app.logger.info('myLogger: setting 3')
db = SQLAlchemy(app)
app.logger.info('myLogger: setting 4')

DBSession = sessionmaker(bind=engine)

import views
