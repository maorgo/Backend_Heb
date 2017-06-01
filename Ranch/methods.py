# -*- coding: utf-8 -*-

import smtplib
import psycopg2
import settings
from Ranch import DBSession
from models import Tag, Post, Subscription
import logging
import sqlalchemy

conf = settings.Configure()
session = DBSession()


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
    subscribers = [i[0] for i in session.query(Subscription.email).all()]

    email_user = 'goaz.maor'
    email_password = 'ioqgnvyovfnppstb'
    origin = 'blog@BackendRanch.dom'
    bcc = subscribers
    subject = 'New Post From BackendRanch'
    text = u'Hello, \nthe post \'{0}\' was published at {1} and is regarding {2}!\nYou should really check ' \
           u'it out!\n{3}\n\nBackendRanch'.format(title, date, primary_tag, conf.POST_LINK + title)
    message = """From: %s\nBcc: %s\nSubject: %s\n\n%s
    """ % (origin, ", ".join(bcc), subject, text)

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()
    server.login(email_user, email_password)
    server.sendmail(origin, bcc, message)
    server.close()

# tags = reload_tags()
tags = [1,2]
last_posts = [1,2]
# last_posts = last_posts()
