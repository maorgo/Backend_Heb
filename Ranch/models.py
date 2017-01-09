from Ranch import db
from Ranch.database import Base


class Post(db.Model):
    __tablename__ = 'posts'
    Author = db.Column(db.String(64))
    Image_Location = db.Column(db.String(64), unique=True)
    Image_Caption = db.Column(db.String(64))
    Title = db.Column(db.String(120), unique=True, primary_key=True)
    Lead = db.Column(db.String(512))
    Date = db.Column(db.Date)
    Text = db.Column(db.Text())
    Primary_Tag = db.Column(db.String(256))
    Secondary_Tag = db.Column(db.String(256))
    Views = db.Column(db.Integer)


def __init__(self, author, image_location, image_caption, title, lead, date, text, primary_tag, secondary_tag):
    self.Author = author
    self.image_location = image_location
    self.image_caption = image_caption
    self.title = title
    self.lead = lead
    self.date = date
    self.text = text
    self.primary_tag = primary_tag
    self.secondary_tag = secondary_tag
    self.views = 0


def __repr__(self):
    return '<Post Title {0}>'.format(self.title)


class Comments(db.Model):
    __tablename__ = 'comments'
    CommentID = db.Column(db.String(64), primary_key=True)
    PostID = db.Column(db.String(64))
    Name = db.Column(db.String(128))
    Comment = db.Column(db.Text())
    CommentTo = db.Column(db.String(64))


class Test(db.Model):
    __tablename__ = 'test'
    col = db.Column(db.Integer, primary_key=True)

    def __init__(self, col):
        self.col = col


