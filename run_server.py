"""
    ***
    MOST IMPORTANT: DOCUMENT WHOLE PROJECT FROM THE START
    Comments - Activate upvote, downvote, reply
    Comments - Add (for admin) option to delete on hover over a comment
    Comments - show last comment first
    ***
    Edit comments from the Admin edit post Page
    Authentication for admin page
    Security for input from user
"""

import os

import sys

from Ranch import app
import Ranch.settings
from flask import Flask, request, abort
import logging


conf = Ranch.settings.Configure()

app._static_folder = os.path.abspath("Ranch/static/")
app.secret_key = conf.secret_key
app.config['UPLOAD_FOLDER'] = app.static_folder + '\pictures\\'
ALLOWED_EXTENSIONS = conf.ALLOWED_EXTENSIONS
ADMIN_USER = conf.ADMIN_USER
ADMIN_PASSWORD = conf.ADMIN_PASSWORD
BANNED_USERS = []
POST_LINK = conf.POST_LINK


if __name__ == "__main__":
    app.logger.addHandler(logging.StreamHandler(sys.stdout))
    app.logger.setLevel(logging.INFO)

    try:
        app.logger.info('myLogger: Attempting to start app')
        app.run()
        app.logger.info('myLogger: Finished starting the app')
    except Exception, e:
        app.logger.info('myLogger: Exception Caught: {0}'.format(e))
        print "Exception caught: {0}".format(e)
