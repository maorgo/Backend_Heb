# -*- coding: utf-8 -*-

import smtplib
import sys
import pymongo
from pymongo import errors as mongo_errors
import psycopg2
from time import strftime, gmtime
import settings
from Ranch import DBSession
from models import Tag, Post
import logging
import sqlalchemy

conf = settings.Configure()
session = DBSession()

try:
    client = pymongo.MongoClient(host=conf.DB_URL, port=27017, socketTimeoutMS=10000, connectTimeoutMS=10000)
except mongo_errors.ConnectionFailure, e:
    # Create error page here
    sys.exit(1)

db = client.blog
posts_collection = db.posts


def view_add(post):
    post.Views += 1
    return post


def add_post(author, title, lead, text, img_loc, img_cap, prim_tag, second_tag):
    try:
        p = Post(author=author, image_location=img_loc, image_caption=img_cap, title=title, lead=lead, text=text,
                 primary_tag=prim_tag, secondary_tag=second_tag)
        session.add(p)
        session.commit()
        return True
    except psycopg2.IntegrityError, e:
        logging.exception('Error occurred while adding a post. Perhapd violating unique values?')
        return False


def reload_tags():
    return session.query(Tag).all()


def last_posts():
    return session.query(Post).filter(Post.Primary_Tag != 'System Messages').order_by(sqlalchemy.desc(Post.Date)).limit(5)


def top_posts():
    return session.query(Post).filter(Post.Primary_Tag != 'System Messages').order_by(sqlalchemy.desc(Post.Views)).limit(5)


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
last_posts = last_posts()
