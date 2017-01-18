import logging


class Configure:
    def __init__(self):
        self.secret_key = 'some_secret'
        self.ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg', 'gif']
        self.ADMIN_USER = 'Maor'
        self.ADMIN_PASSWORD = 'GOAZ'
        self.BANNED_USERS = []
        self.BLOG_URL = '127.0.0.1'
        self.DB_URL = 'localhost'
        self.POST_LINK = '{0}/posts'.format(self.BLOG_URL)
        self.database_connection_string = 'postgresql://postgres:postgres@localhost/blog'
        self.LOG_LEVEL = logging.DEBUG
        self.BLOG_NAME = 'BackendRanch'
        self.BLOG_PREFIX = 'com'
        self.LOG_NAME = 'BackendRanch.log'
        self.RECIEVE_ADDRESS = ''