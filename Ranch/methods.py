import smtplib
import sys
import pymongo
from pymongo import errors as mongo_errors

import settings

conf = settings.Configure()

try:
    client = pymongo.MongoClient(host=conf.DB_URL, port=27017, socketTimeoutMS=10000, connectTimeoutMS=10000)
except mongo_errors.ConnectionFailure, e:
    # Create error page here
    sys.exit(1)

db = client.blog
posts_collection = db.posts


def reload_tags():
    return db.tags.find()[0]['tags']


def last_posts():
    return posts_collection.find({'tags': {'$nin': ['System Messages']}}).sort('date', pymongo.DESCENDING).limit(10)


def top_posts():
    return posts_collection.find({'tags': {'$nin': ['System Messages']}}).sort('views', pymongo.DESCENDING). \
        limit(10)


def email_post(title, primary_tag, date):
    with open('MAILING_LIST', 'r') as f:
        mailing_list = f.read().split('\n')
        if not mailing_list:
            return False
        email_user = 'goaz.maor'
        email_password = 'heuflxtukdyjckfb'
        origin = 'blog@BackendRanch.dom'
        to = mailing_list
        subject = 'New Post From BackendRanch'
        text = 'Hello, \nthe post \'{0}\' was published at {1} and is regarding {2}!\nYou should really check ' \
               'it out!\n{3}\n\nBackendRanch'.format(title, date, primary_tag, conf.POST_LINK + title)
        message = """From: %s\nTo: %s\nSubject: %s\n\n%s
        """ % (origin, ", ".join(to), subject, text)
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(email_user, email_password)
        server.sendmail(origin, to, message)
        server.close()

tags = reload_tags()