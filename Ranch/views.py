# -*- coding: utf-8 -*-
# todo: Add admin button to those who are authenticated as admins
# todo: Subsribers' email: fix bcc issue

import os
import smtplib
import uuid
from datetime import datetime
from flask import render_template, redirect, request, url_for, send_from_directory, flash, make_response
from werkzeug.utils import secure_filename
from Ranch import app, DBSession
import methods
import settings
from methods import tags
from models import Post, Tag, Comment, Subscription
import sqlalchemy

conf = settings.Configure()
session = DBSession()


@app.route('/')
def index():
    print 'This had started!'
    app.logger.info('This had started! 1')
    last_post = session.query(Post).filter(Post.Primary_Tag != 'System Messages').\
                order_by(sqlalchemy.desc(Post.Date)).limit(1).first()
    app.logger.info('This had started! 2')
    if not last_post:
        app.logger.info('This had started! 3')
        return render_template('oops.html', tags=tags, last_posts=methods.last_posts, top_posts=methods.top_posts())
    app.logger.info('This had started! 4')
    comments = session.query(Comment).filter(Comment.PostTitle == last_post.Title).all()
    app.logger.info('This had started! 5')
    return render_template('post.html', post=last_post, last_posts=methods.last_posts, tags=methods.tags,
                           top_posts=methods.top_posts(), newer_older=True, comments=comments)


@app.route('/archive')
def archive():
    posts = session.query(Post).filter(Post.Primary_Tag != 'System Messages').order_by(sqlalchemy.desc(Post.Date)).all()
    return render_template('archive.html', posts=posts, last_posts=methods.last_posts, tags=methods.tags,
                           top_posts=methods.top_posts())


@app.route('/about')
def about():
    return render_template('about.html', last_posts=methods.last_posts, tags=methods.tags,
                           top_posts=methods.top_posts())


@app.route('/contact')
def contact():
    # Placeholder. Should work on it.
     return render_template('contact.html', post='', last_posts=methods.last_posts, top_posts=methods.top_posts(),
                            tags=methods.tags)


@app.route('/<title>')
def tag(title):
    tag_post = session.query(Post).filter(Post.Primary_Tag == title).first()
    if tag_post:
        return render_template('post.html', last_posts=methods.last_posts, post=tag_post, tags=methods.tags,
                               top_posts=methods.top_posts(), newer_older=True)

    return render_template('oops.html', last_posts=methods.last_posts, top_posts=methods.top_posts(),
                           tags=methods.tags)


@app.route('/posts/<title>')
def post(title):
    blog_post = session.query(Post).filter(Post.Title == title).first()
    if blog_post:
        blog_post.Views += 1
        session.commit()
        comments = session.query(Comment).filter(Comment.PostTitle == title).all()

        return render_template('post.html', last_posts=methods.last_posts, post=blog_post, tags=methods.tags,
                               top_posts=methods.top_posts(), newer_older=True, comments=comments)
    else:
        return render_template('oops.html', last_posts=methods.last_posts, top_posts=methods.top_posts(),
                               tags=methods.tags)


@app.route('/older/<string:post_title>')
def older(post_title):
    current_post = session.query(Post).filter(Post.Title == post_title).first()
    if current_post:
        older_post = session.query(Post).filter(Post.Date < current_post.Date).order_by(sqlalchemy.desc(Post.Date)).first()
        if older_post:
            older_post.Views += 1
            return redirect(u'/posts/{0}'.format(older_post.Title))
        return redirect(u'/posts/{0}'.format(current_post.Title))
        # return render_template('oops.html', last_posts=methods.last_posts, tags=methods.tags,
        #                        top_posts=methods.top_posts(),
        #                        newer_older=True, reason=u'שגיאה בעת מציאת פוסט ישן יותר.')
    return render_template('oops.html', last_posts=methods.last_posts, tags=methods.tags, top_posts=methods.top_posts(),
                           newer_older=True, reason=u'שגיאה בעת מציאת פוסט נוכחי.')


@app.route('/newer/<post_title>')
def newer(post_title):
    current_post = session.query(Post).filter(Post.Title == post_title).first()
    if current_post:
        newer_post = session.query(Post).filter(Post.Date > current_post.Date).order_by(sqlalchemy.desc(Post.Date)).first()
        if newer_post:
            newer_post.Views += 1
            return redirect(u'/posts/{0}'.format(newer_post.Title))
        else:
            return redirect(u'/posts/{0}'.format(post_title))
        # return render_template('oops.html', last_posts=methods.last_posts, tags=methods.tags,
        #                        top_posts=methods.top_posts(),
        #                        newer_older=True, reason=u'שגיאה בעת מציאת פוסט חדש יותר.')
    return render_template('oops.html', last_posts=methods.last_posts, tags=methods.tags, top_posts=methods.top_posts(),
                           newer_older=True, reason=u'שגיאה בעת מציאת פוסט נוכחי.')


@app.route('/posts/<title>', methods=['POST'])
def add_comment(title):
    name = unicode(request.form['contactName'])
    email = unicode(request.form['contactEmail'])
    comment = unicode(request.form['contactComment'])
    title = unicode(title)
    if name != '' and comment != '' and title != '' and name and comment and title:
        new_comment = Comment(post_title=title, name=name, comment=comment, comment_id=uuid.uuid4().hex,
                              comment_to=None, email=email, date=datetime.utcnow())
        session.add(new_comment)
        session.commit()
        return redirect(u'/posts/{0}'.format(title))
    else:
        return render_template('oops.html', top_posts=methods.top_posts(), last_posts=methods.last_posts(),
                               tags=methods.tags, reason=u'התרחשה בעיה עם התגובה. מצטערים.')


@app.route('/done', methods=['POST'])
def contact_me():
    email_user = 'goaz.maor'
    email_password = 'heuflxtukdyjckfb'
    origin = 'blog@{0}.{1}'.format(conf.BLOG_NAME, conf.BLOG_PREFIX)
    # TO = recipient if type(recipient) is list else [recipient]
    to = ['{0}'.format(conf.RECIEVE_ADDRESS)]
    subject = 'You have a message from {0} blog.'.format(conf.BLOG_NAME)
    # Prepare actual message
    # message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    # """ % (request.form['contactName'], ", ".join(to), subject, text)
    text = u'The following message sent from {0} that can be reached back at {1}:\n{2}'.format(
            request.form['contactName'], request.form['contactEmail'], request.form['contactComment'])
    message = u"""From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (request.form['contactEmail'], ", ".join(to), subject, text)
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(email_user, email_password)
        server.sendmail(origin, to, message)
        server.close()
        return render_template('contact.html', success=True, last_posts=methods.last_posts(),
                               top_posts=methods.top_posts(), tags=methods.tags, post='')
    except Exception, exception:
        return render_template('contact.html', failure=True, last_posts=methods.last_posts(),
                               top_posts=methods.top_posts(), tags=methods.tags, post='', failure_reason=exception)


@app.route('/search', methods=['POST', 'GET'])
def search():
    post_results = []
    # Get the searched word
    keyword = unicode(request.form['search-form'])
    # Search in titles, play with case sensitivity
    title_results = session.query(Post).filter(
        sqlalchemy.or_(Post.Title.like(u'%{0}%'.format(keyword)),
                       Post.Title.like(u'%{0}%'.format(keyword.lower())),
                       Post.Title.like(u'%{0}%'.format(keyword.upper()))))\
        .order_by(sqlalchemy.desc(Post.Date)).all()

    # Search in body fields, play with case sensitivity
    body_results = session.query(Post).filter(
        sqlalchemy.or_(Post.Text.like(u'%{0}%'.format(keyword)),
                       Post.Text.like(u'%{0}%'.format(keyword.lower())),
                       Post.Text.like(u'%{0}%'.format(keyword.upper()))))\
        .order_by(sqlalchemy.desc(Post.Date)).all()

    # Search in lead fields, play with case sensitivity
    lead_results = session.query(Post).filter(
        sqlalchemy.or_(Post.Lead.like(u'%{0}%'.format(keyword)),
                       Post.Lead.like(u'%{0}%'.format(keyword.lower())),
                       Post.Lead.like(u'%{0}%'.format(keyword.upper()))))\
        .order_by(sqlalchemy.desc(Post.Date)).all()

    # Search tags
    tag_results = session.query(Post).filter(
        sqlalchemy.or_(Post.Primary_Tag.like(u'%{0}%'.format(keyword)),
                       Post.Primary_Tag.like(u'%{0}%'.format(keyword.lower())),
                       Post.Primary_Tag.like(u'%{0}%'.format(keyword.upper()))))\
        .order_by(sqlalchemy.desc(Post.Date)).all()

    # Collect all results into one list
    for title in title_results:
        if title not in post_results:
            post_results.append(title)
    for lead in lead_results:
        if lead not in post_results:
            post_results.append(lead)
    for sentence in body_results:
        if sentence not in post_results:
            post_results.append(sentence)
    for each_tag in tag_results:
        if each_tag not in post_results:
            post_results.append(each_tag)

    # Check if there are results. If so, return them
    if len(post_results) == 0:
        return render_template('search_results.html', keyword=keyword, no_results=True,
                               last_posts=methods.last_posts, top_posts=methods.top_posts(), tags=methods.tags)
    return render_template('search_results.html', keyword=keyword, post_results=post_results,
                           last_posts=methods.last_posts, top_posts=methods.top_posts(), tags=methods.tags)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('/login.html', last_posts=methods.last_posts, top_posts=methods.top_posts(),
                               tags=methods.tags)
    else:
        if request.form['username'] == conf.ADMIN_USER and request.form['password'] == conf.ADMIN_PASSWORD:
            # Create a cookie or something

            return successful_login_cookie(request.form['username'])
        else:
            return failed_login()


def successful_login_cookie(username):
    resp = make_response(redirect(url_for('admin')))
    resp.set_cookie('username', username)
    return resp


def failed_login():
    resp = make_response(redirect(url_for('login')))
    if 'failed_login' not in request.cookies:
        resp.set_cookie('failed_login', '1')
    else:
        try:
            login_failure = int(request.cookies['failed_login']) + 1
        except ValueError as err:
            print 'Something went wrong: {0}'.format(err)
            return render_template('oops.html', top_posts=methods.top_posts(), last_posts=methods.last_posts(),
                                   tags=methods.tags)
        if login_failure >= 2:
            ban_user(request.remote_addr, 'Too many login failures')
            resp = make_response(redirect(url_for('index')))
            resp.set_cookie('failed_login', '0')
            return resp
        else:
            resp.set_cookie('failed_login', str(login_failure))
    return resp


def ban_user(user_ip, reason):
    conf.BANNED_USERS.append([user_ip, reason, datetime.now()])
    # BANNED_USERS.update({user_ip: reason})
    with open('BANNED_USERS.txt', 'a') as f:
        f.write(str([user_ip, reason, datetime.now().strftime('%Y-%m-%d %H:%M')]) + '\n')
    return 1


@app.route('/admin')
def admin():
    if request.cookies.get('username') == conf.ADMIN_USER:
        return render_template('/admin/admin.html', last_posts=methods.last_posts, top_posts=methods.top_posts(),
                               tags=methods.tags)
    return redirect(url_for('login'))


@app.route('/admin/posts')
def posts_admin():
    # Find all posts to show at the admin panel
    all_posts = session.query(Post).order_by(sqlalchemy.desc(Post.Date)).all()
    return render_template('admin/posts_list.html', tags=methods.tags, last_posts=methods.last_posts,
                           top_posts=methods.top_posts(), all_posts=all_posts)


@app.route('/admin/tags')
def tags_admin(message=None):
    # Reload tags, get the newest list
    reloaded_tags = methods.reload_tags()
    return render_template('admin/tags.html', tags=reloaded_tags, top_posts=methods.top_posts(),
                           last_posts=methods.last_posts, img='/static/pictures/x.jpg', message=message)


@app.route('/admin/edit/<title>')
def edit_post(title):
    # Find the post desired for edit
    post_to_edit = session.query(Post).filter(Post.Title == title).first()
    return render_template('admin/edit_post.html', post=post_to_edit, tags=methods.tags,
                           last_posts=methods.last_posts, top_posts=methods.top_posts())


@app.route('/admin/edit/<title>', methods=['POST'])
def submit_edit_post(title):
    data = {}
    primary_tag = ''
    secondary_tag = []
    old_post = session.query(Post).filter(Post.Title == title).first()
    # Collect all tags that were chosen into two lists (primary, secondary)
    for i in request.form:
        if 'primary_tag_' in i:
            primary_tag = i.split('_')[-1]
        elif 'secondary_tag_' in i:
                secondary_tag.append(i.split('_')[-1])

    # Check if an image was uploaded.
    image = request.files['image_location']
    filename = secure_filename(image.filename)
    if filename != '':
        if filename.split('.')[-1] in conf.ALLOWED_EXTENSIONS:
            # Save the image
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            image_location = '/static/pictures/' + filename
        else:
            # Return the error about the file type
            flash('This image file type is not supported.')
            return redirect(url_for('edit_post', title=old_post.Title))
    else:
        image_location = old_post.Image_Location
    # Check that the title, text, and primary_tag are not empty
    if request.form['title'] == '' or request.form['title'] == ' ':
        flash('Title should not be left blank')
    if request.form['text'] == '' or request.form['text'] == '\n':
        flash('Text field should not be left blank.')
    if primary_tag == '':
        flash('Primary tag should not be left blank.')
    redirect(url_for('edit_post', title=title))

    count = session.query(Post).filter(Post.Title == title).\
        update({Post.Date: old_post.Date, Post.Image_Location: image_location,
                Post.Image_Caption: request.form['image_caption'], Post.Lead: request.form['lead'],
                Post.Text: request.form['text'], Post.Title: request.form['title'], Post.Primary_Tag: primary_tag,
                Post.Secondary_Tag: secondary_tag, Post.Views: old_post.Views})
    session.commit()
    if count == 1:
        new_post = session.query(Post).filter(Post.Title == request.form['title']).first()
        return render_template('/admin/edit_post.html', post=new_post, tags=methods.tags,
                               last_posts=methods.last_posts, top_posts=methods.top_posts(), successful=True)
    elif count == 0:
        return render_template('oops.html', reason='No posts were matched to the old title', tags=methods.tags,
                               top_posts=methods.top_posts(), last_posts=methods.last_posts)
    else:
        return render_template('oops.html', reason='Too many were updated: {0}'.format(count, tags=methods.tags,
                                                                                       top_posts=methods.top_posts(),
                                                                                       last_posts=methods.last_posts))


@app.route('/admin/posts', methods=['POST'])
def delete_post():
    # For all posts that were selected, delete them
    for title in request.form:
        deleted = session.query(Post).filter(Post.Title == title).delete()
        if deleted != 1:
            return render_template('oops.html', last_posts=methods.last_posts, top_posts=methods.top_posts(),
                                   reason='Deleted {0} posts'.format(deleted), tags=methods.tags)
    all_posts = session.query(Post).order_by(sqlalchemy.desc(Post.Date)).all()
    return render_template('/admin/posts_list.html', tags=methods.tags, last_posts=methods.last_posts,
                           top_posts=methods.top_posts(), all_posts=all_posts,
                           posts_number=sqlalchemy.func.count(all_posts))


# Change to app.route('/admin/tags', methods=['DELETE'])
@app.route('/admin/delete_tag/<tag_to_delete>')
def delete_tag(tag_to_delete):
    # tag_deletion = db.tags.update({}, {'$pull': {'tags': tag_to_delete}})
    tag_deletion = session.query(Tag).filter(Tag.tag == tag_to_delete).delete()
    session.commit()
    # Check deletion results
    # if tag_deletion['nModified'] == 1:
    if tag_deletion == 1:
        return tags_admin('Successfully deleted tag {0}. '.format(tag_to_delete))
    return tags_admin('Error occurred while attempting deletion of tag {0}'.format(tag_to_delete))


@app.route('/admin/tags', methods=['POST'])
def add_tag():
    new_tag = request.form['new_tag']
    reloaded_tags = methods.reload_tags()
    # Check if it's ok to add the new tag
    if new_tag and (new_tag not in methods.tags):
        # tag_addition = db.tags.update({}, {'$push': {'tags': new_tag}})
        tag_obj = Tag(tag=new_tag)
        try:
            session.add(tag_obj)
            session.commit()
        except sqlalchemy.exc.InvalidRequestError, e:
            return render_template('oops.html', reason='Something went wrong while adding a tag.', tags=reloaded_tags,
                                   top_posts=methods.top_posts(), last_posts=methods.last_posts)
        methods.reload_tags()
        return tags_admin('Tag \'{0}\' added successfully.'.format(new_tag))


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory('C:\users\goas\Desktop\personal\\blog\static\pictures\\',
                               filename)


@app.route('/admin/create_post', methods=['POST', 'GET'])
def create_post():
    if request.method == 'GET':
        return render_template('/admin/create_post.html', tags=methods.tags, top_posts=methods.top_posts(),
                               last_posts=methods.last_posts)
    image_location = ''
    # todo: add path verification for the image uploaded (don't allow ../ and such)
    # todo: if '../' in path: return?
    if 'image_location' in request.files.keys():
        image = request.files['image_location']
        filename = secure_filename(image.filename)
        image_location = '/static/pictures/' + filename

        if session.query(Post).filter(Post.Image_Location == image_location).first():
            return render_template('/admin/create_post.html', failure=True, error=u'שם הקובץ קיים במערכת',
                                   detail=u'שם הקובץ: {0}'.format(image_location),
                                   tags=methods.tags, top_posts=methods.top_posts(), last_posts=methods.last_posts)
        image = request.files['image_location']

        if filename.split('.')[-1] in conf.ALLOWED_EXTENSIONS:
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        else:
            return render_template('/admin/create_post.html', failure=True, error=u'סוג הקובץ לא מאושר',
                                   tags=methods.tags, top_posts=methods.top_posts(), last_posts=methods.last_posts)

    primary_tag = ''
    secondary_tag = []
    # Go through all selected tags
    for i in request.form:
        if 'primary_tag_' in i:
            primary_tag = i.split('_')[-1]
        elif 'secondary_tag_' in i:
                secondary_tag.append(i.split('_')[-1])

    new_post = Post(author='מאור גואז', date=datetime.utcnow(), image_location=image_location,
                    image_caption=request.form['image_caption'], lead=request.form['lead'], text=request.form['text'],
                    title=request.form['title'], primary_tag=primary_tag, secondary_tag=secondary_tag)
    try:
        session.add(new_post)
        session.commit()
    except sqlalchemy.exc.SQLAlchemyError, e:
        session.rollback()
        return render_template('/admin/create_post.html', failure=True, error=e.message, detail=e.statement,
                               tags=methods.tags, top_posts=methods.top_posts(), last_posts=methods.last_posts)

    # TODO: FIX: methods.email_post(request.form['title'], primary_tag, datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'))
    methods.email_post(request.form['title'], primary_tag, datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'))
    return render_template('/admin/create_post.html', successful=True, tags=methods.tags, top_posts=methods.top_posts(),
                           last_posts=methods.last_posts)


@app.route('/posts/<title>/<comment_id>/upvote')
def upvote(comment_id, title):
    comment = session.query(Comment).filter(Comment.CommentID == comment_id).first()
    comment.CommentVotes += 1
    return redirect('/posts/' + title)
    # up = posts_collection.update({'title': title, 'comments.id': comment_id}, {'$inc': {'comments.$.upvotes': 1}})
    # if up['updatedExisting']:
    #     return redirect('/posts/' + title)
    # else:
    #     return render_template('oops.html', reason='Couldn\'t upvote the comment. Sorry.', tags=methods.tags,
    #                            top_posts=methods.top_posts(), last_posts=methods.last_posts)


@app.route('/posts/<title>/<comment_id>/downvote')
def downvote(comment_id, title):
    comment = session.query(Comment).filter(Comment.CommentID == comment_id).first()
    comment.CommentVotes -= 1
    return redirect('/posts/' + title)
#     down = posts_collection.update({'title': title, 'comments.id': comment_id}, {'$inc': {'comments.$.upvotes': -1}})
#     if down['updatedExisting']:
#         return redirect('/posts/' + title)
#     else:
#         return render_template('oops.html', reason='Couldn\'t downvote the comment. Sorry.', tags=methods.tags,
#                                top_posts=methods.top_posts(), last_posts=methods.last_posts)


@app.route('/subscribe', methods=['GET', 'POST'])
def subscribe():
    if request.method == 'GET':
        return render_template('subscribe.html', last_posts=methods.last_posts, tags=methods.tags,
                               top_posts=methods.top_posts())
    else:
        if request.form['email']:
            email = request.form['email']
        else:
            return render_template('subscribe.html', message=u'הוכנסה כתובת ריקה.',
                                   top_posts=methods.top_posts(), last_posts=methods.last_posts, tags=methods.tags)
        # if '@' in email and '.' in email and ['<', '>'] not in email:
        if all(x in email for x in ['@', '.']) and not any(x in email for x in ['<', '>', '!', '?']):
            # process
            # with open('MAILING_LIST', 'r') as f:
            #     if email in f.read().split('\n'):
            email_is_exists = session.query(Subscription).filter(Subscription.email == email).first()
            if email_is_exists:
                return render_template('subscribe.html', message=u'הכתובת כבר קיימת במערכת.',
                                       top_posts=methods.top_posts(), last_posts=methods.last_posts, tags=methods.tags)
            session.add(Subscription(email))
            session.commit()
            return render_template('subscribe.html', success_message=u'תודה, ההרשמה בוצעה בהצלחה.',
                                   top_posts=methods.top_posts(), last_posts=methods.last_posts, tags=methods.tags)
        else:
            return render_template('subscribe.html', message=u'פורמט דוא"ל שגוי.', top_posts=methods.top_posts(),
                                   last_posts=methods.last_posts, tags=methods.tags)
