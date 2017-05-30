from Ranch import db
from sqlalchemy import func


class Post(db.Model):
    __tablename__ = 'posts'
    Author = db.Column(db.String(64))
    Image_Location = db.Column(db.String(64), unique=True)
    Image_Caption = db.Column(db.String(64))
    Title = db.Column(db.String(120), unique=True, primary_key=True)
    Lead = db.Column(db.String(512))
    Date = db.Column(db.DateTime, default=func.now())
    Text = db.Column(db.String(512))
    Primary_Tag = db.Column(db.String(256))
    Secondary_Tag = db.Column(db.String(256))
    Views = db.Column(db.Integer)

    def __init__(self, author, image_location, image_caption, title, lead, text, primary_tag, secondary_tag, date):
        self.Author = author
        self.Image_Location = image_location
        self.Image_Caption = image_caption
        self.Title = title
        self.Lead = lead
        self.Text = text
        self.Primary_Tag = primary_tag
        self.Secondary_Tag = secondary_tag
        self.Views = 0
        self.Date = date

    def __repr__(self):
        return u'<Post Title {0}>'.format(self.Title)


class Comment(db.Model):
    __tablename__ = 'comments'
    CommentID = db.Column(db.String(64), primary_key=True)
    PostTitle = db.Column(db.String(64))
    Name = db.Column(db.String(128))
    Comment = db.Column(db.Text())
    CommentTo = db.Column(db.String(64))
    ContactEmail = db.Column(db.Text())
    CommentDate = db.Column(db.DateTime, default=func.now())
    CommentVotes = db.Column(db.Numeric())

    def __init__(self, comment_id, post_title, name, comment, date, comment_to=None, email=None):
        self.CommentID = comment_id
        self.PostTitle = post_title
        self.Name = name
        self.Comment = comment
        self.CommentTo = comment_to
        self.ContactEmail = email
        self.CommentDate = date
        self.CommentVotes = 0


class Tag(db.Model):
    __tablename__ = 'tag'
    tag = db.Column(db.String(128), primary_key=True)

    def __init__(self, tag):
        self.tag = tag


class Subscription(db.Model):
    __tablename__ = 'subscription'
    email = db.Column(db.String(120), primary_key=True)

    def __init__(self, email):
        self.email = email
