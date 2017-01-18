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
        self.image_Caption = image_caption
        self.Title = title
        self.Lead = lead
        self.Text = text
        self.Primary_Tag = primary_tag
        self.Secondary_Tag = secondary_tag
        self.Views = 0
        self.Date = date

    def __repr__(self):
        return '<Post Title {0}>'.format(self.Title)


class Comments(db.Model):
    __tablename__ = 'comments'
    CommentID = db.Column(db.String(64), primary_key=True)
    PostID = db.Column(db.String(64))
    Name = db.Column(db.String(128))
    Comment = db.Column(db.Text())
    CommentTo = db.Column(db.String(64))

    def __init__(self, comment_id, post_id, name, comment, comment_to):
        self.CommentID = comment_id
        self.PostID = post_id
        self.Name = name
        self.Comment = comment
        self.CommentTo = comment_to


class Tag(db.Model):
    __tablename__ = 'tag'
    tag = db.Column(db.String(128), primary_key=True)

    def __init__(self, tag):
        self.tag = tag


