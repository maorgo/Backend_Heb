import os
import smtplib
import uuid
from datetime import datetime
import pymongo
from flask import render_template, redirect, request, url_for, send_from_directory, flash, make_response
from werkzeug.utils import secure_filename
from Ranch import app, DBSession
import methods
import settings
from methods import posts_collection, db
from models import Comments, Post, Test
import sqlalchemy

conf = settings.Configure()
session = DBSession()


@app.route('/')
def index():
    p = Post(author='Maor', image_location='Location', image_caption='Caption', title='Title', lead='Lead',
             date=sqlalchemy.DATE, text='Text', primary_tag='Primary_Tag', secondary_tag='second')
    #author, image_location, image_caption, title, lead, date, text, primary_tag, secondary_tag
    #session.add(p)
    #print session.query(Post).all().pop()
    #session.query(Post)
    last_post = posts_collection.find({'primary_tag': {'$ne': 'System Messages'}}).sort('date', -1).limit(1)
    if last_post.count() < 1:
        return render_template('oops.html', tags=methods.tags, last_posts=methods.last_posts(),
                               top_posts=methods.top_posts())
    last_post = last_post[0]
    return render_template('post.html', post=last_post, tags=methods.tags, newer_older=True,
                           top_posts=methods.top_posts(), last_posts=methods.last_posts())


@app.route('/archive')
def archive():
    # Placeholder. Should work on it.
    posts = posts_collection.find({'tags': {'$nin': ['System Messages']}}).sort('date', pymongo.DESCENDING)

    return render_template('archive.html', tags=methods.tags, last_posts=methods.last_posts(),
                           top_posts=methods.top_posts(), posts=posts)


@app.route('/about')
def about():
    about_post = posts_collection.find({'title': 'About this blog', 'primary_tag': 'System Messages'})
    if about_post.count() != 1:
        return render_template('oops.html', reason='No such post found')
    about_post = about_post[0]
    return render_template('post.html', post=about_post, tags=methods.tags, last_posts=methods.last_posts(),
                           top_posts=methods.top_posts())


@app.route('/contact')
def contact():
    # Placeholder. Should work on it.
    # contact_me = posts_collection.find({'title': 'Contact Me'}).limit(1)[0]
    # return render_template('post.html',post=contact_me, last_posts=methods.last_posts(),
    # top_posts=methods.top_posts(), tags=methods.tags)
    return render_template('contact.html', post='', last_posts=methods.last_posts(), top_posts=methods.top_posts(),
                           tags=methods.tags)


@app.route('/<title>')
def tag(title):
    tag_post = posts_collection.find({'primary_tag': title}).sort('date', pymongo.DESCENDING).limit(1)
    if tag_post.count() < 1:
        return render_template('oops.html', tags=methods.tags, last_posts=methods.last_posts(),
                               top_posts=methods.top_posts(), reason="No articles for this subject were found.")
    else:
        tag_post = tag_post[0]
    return redirect('/posts/{0}'.format(tag_post['title']))


@app.route('/posts/<title>')
def post(title):
    blog_post = posts_collection.find({'title': title})
    if blog_post.count() < 1:
        return render_template('oops.html', tags=methods.tags, last_posts=methods.last_posts(),
                               top_posts=methods.top_posts())
    blog_post = blog_post[0]

    posts_collection.update({'title': blog_post['title']}, {'$set': {'views': blog_post['views'] + 1}})
    return render_template('post.html', post=blog_post, top_posts=methods.top_posts(), last_posts=methods.last_posts(),
                           newer_older=True, tags=methods.tags)


@app.route('/older/<string:post_title>')
def older(post_title):
    older_post = posts_collection.find({'title': post_title}, {'date': 1, '_id': 0, 'primary_tag': 1})
    if older_post.count() != 1:
        return render_template('oops.html', tags=methods.tags, last_posts=methods.last_posts(),
                               top_posts=methods.top_posts(),
                               reason='While pressing older, found more or less than 1, maybe conflicting titles')
    older_post = older_post[0]
    older_post = posts_collection.find({'primary_tag': older_post['primary_tag'],
                                        'date': {'$lt': older_post['date']}}).sort('date', -1).limit(1)
    # Check that there was an older post
    if older_post.count() < 1:
        return redirect('/posts/{0}'.format(post_title))
    older_post = older_post[0]
    return redirect('/posts/{0}'.format(older_post['title']))


@app.route('/newer/<post_title>')
def newer(post_title):
    older_post = posts_collection.find({'title': post_title}, {'primary_tag': 1, 'date': 1, 'secondary_tags': 1,
                                                               'title': 1})
    if older_post.count() != 1:
        return render_template('oops.html', tags=methods.tags, last_posts=methods.last_posts(),
                               top_posts=methods.top_posts(),
                               reason='While pressing older, found more or less than 1, maybe conflicting titles')
    older_post = older_post[0]
    # new_post = posts_collection.find({'date': {'$gt': older_post['date'], 'primary_tag': older_post['primary_tag']}}
    #                                  ).sort('date', 1).limit(1)
    new_post = posts_collection.find({'primary_tag': older_post['primary_tag'], 'date': {'$gt': older_post['date']}}
                                     ).sort('date', 1)
    # return str(new_post[0]  )
    if new_post.count() == 0:
        new_post = posts_collection.find({'date': {'$gt': older_post['date'], 'secondary_tags':
                                                   {'$in': older_post['secondary_tags']}}}).sort('date', 1).limit(1)
        if new_post.count() == 0:
            # return str(old_post['title'])
            return post(older_post['title'])
    return post(new_post[0]['title'])


@app.route('/posts/<title>', methods=['POST'])
def add_comment(title):
    name = request.form['contactName']
    email = request.form['contactEmail']
    comment = request.form['contactComment']
    # db.posts.find({ "_id" : ObjectId("5797ce3372628cf1bac24b17")}, {'comments':1, '_id': 0})
    posts_collection.update(
            {'title': title},
            {'$push':
                {'comments':
                    {
                        'comment': comment,
                        'author': name,
                        'email': email,
                        'upvotes': 0,
                        'id': str(uuid.uuid4()),
                        'comment_date': datetime.utcnow(),
                        'reply': {}
                    }
                 }
             }
    )
    return redirect('/posts/{0}'.format(title))


@app.route('/done', methods=['POST'])
def contact_me():
    email_user = 'goaz.maor'
    email_password = 'heuflxtukdyjckfb'
    origin = 'blog@BackendRanch.dom'
    # TO = recipient if type(recipient) is list else [recipient]
    to = ['goaz.maor@gmail.com']
    subject = 'You have a message from BackendRanch blog.'

    # Prepare actual message
    # message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    # """ % (request.form['contactName'], ", ".join(to), subject, text)
    text = 'The following message sent from {0} that can be reached back at {1}:\n{2}'.format(
            request.form['contactName'], request.form['contactEmail'], request.form['contactComment'])

    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
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
    keyword = str(request.form['search-form'])
    # Search in titles, play with case sensitivity
    title_results = db.posts.find({'$or': [{"title": {'$regex': '.*' + keyword + '.*'}},
                                           {'title': {'$regex': '.*' + keyword.lower() + '.*'}},
                                           {'title': {'$regex': '.*' + keyword.upper() + '.*'}}]})
    # Search in body fields, play with case sensitivity
    body_results = db.posts.find({'$or': [{"text": {'$regex': '.*' + keyword + '.*'}},
                                 {"text": {'$regex': '.*' + keyword.lower() + '.*'}},
                                 {"text": {'$regex': '.*' + keyword.upper() + '.*'}}]})
    # Search in lead fields, play with case sensitivity
    lead_results = db.posts.find({'$or': [{"lead": {'$regex': '.*' + keyword + '.*'}},
                                          {"lead": {'$regex': '.*' + keyword.upper() + '.*'}},
                                          {"lead": {'$regex': '.*' + keyword.lower() + '.*'}}]})
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
    # Check if there are results. If so, return them
    if len(post_results) == 0:
        return render_template('search_results.html', keyword=keyword, no_results=True,
                               last_posts=methods.last_posts(), top_posts=methods.top_posts(), tags=methods.tags)
    return render_template('search_results.html', keyword=keyword, post_results=post_results,
                           last_posts=methods.last_posts(), top_posts=methods.top_posts(), tags=methods.tags)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('/login.html', last_posts=methods.last_posts(), top_posts=methods.top_posts(),
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
        return render_template('/admin/admin.html', last_posts=methods.last_posts(), top_posts=methods.top_posts(),
                               tags=methods.tags)
    return redirect(url_for('login'))


@app.route('/admin/posts')
def posts_admin():
    # Find all posts to show at the admin panel
    all_posts = posts_collection.find().sort('date', pymongo.DESCENDING)

    return render_template('admin/posts_list.html', tags=methods.tags, last_posts=methods.last_posts(),
                           top_posts=methods.top_posts(), all_posts=all_posts, posts_number=all_posts.count())


@app.route('/admin/tags')
def tags_admin(message=None):
    # Reload tags, get the newest list
    reloaded_tags = methods.reload_tags()
    return render_template('admin/tags.html', tags=reloaded_tags, top_posts=methods.top_posts(),
                           last_posts=methods.last_posts(), img='/static/pictures/x.jpg', message=message)


@app.route('/admin/edit/<title>')
def edit_post(title):
    # Find the post desired for edit
    post_to_edit = posts_collection.find({'title': title})[0]
    return render_template('admin/edit_post.html', post=post_to_edit, tags=methods.tags,
                           last_posts=methods.last_posts(), top_posts=methods.top_posts())


@app.route('/admin/edit/<title>', methods=['POST'])
def submit_edit_post(title):
    data = {}
    primary_tag = ''
    secondary_tag = []
    old_post = posts_collection.find({'title': title})[0]
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
            return redirect(url_for('edit_post', title=old_post['title']))
    else:
        image_location = old_post['img_location']
    # Check that the title, text, and primary_tag are not empty
    if request.form['title'] == '' or request.form['title'] == ' ':
        flash('Title should not be left blank')
    if request.form['text'] == '' or request.form['text'] == '\n':
        flash('Text field should not be left blank.')
    if primary_tag == '':
        flash('Primary tag should not be left blank.')
    redirect(url_for('edit_post', title=title))
    data.update({'author': 'Maor Goaz', 'date': old_post['date']})  # .strftime('%Y-%m-%d %H:%M:%S')
    # Data that came from the form itself
    data.update({'update_date': datetime.utcnow(),
                 'img_location': image_location,
                 'img_caption': request.form['image_caption'],
                 'lead': request.form['lead'],
                 'text': request.form['text'],
                 'title': request.form['title'],
                 'primary_tag': primary_tag,
                 'secondary_tags': secondary_tag,
                 'comments': [],
                 'views': old_post['views']
                 })
    # Update the new post
    insert_post = posts_collection.update({'title': title}, data)
    # Check update results
    if insert_post['updatedExisting'] and insert_post['nModified'] == 1:
        new_post = posts_collection.find({'title': request.form['title']})[0]
        return render_template('/admin/edit_post.html', post=new_post, tags=methods.tags,
                               last_posts=methods.last_posts(), top_posts=methods.top_posts(), successful=True)
    elif insert_post['updatedExisting'] and insert_post['nModified'] > 1:
        return render_template('oops.html', reason='Too many were updated: {0}'
                               .format(insert_post['nModified'], tags=methods.tags, top_posts=methods.top_posts(),
                                       last_posts=methods.last_posts()))
    else:
        return render_template('oops.html', reason=str(insert_post), tags=methods.tags, top_posts=methods.top_posts(),
                               last_posts=methods.last_posts())


@app.route('/admin/posts', methods=['POST'])
def delete_post():
    # For all posts that were selected, delete them
    for title in request.form:
        deleted = posts_collection.delete_one({'title': title})
        if deleted.deleted_count != 1:
            return render_template('oops.html', tags=methods.tags, last_posts=methods.last_posts(),
                                   top_posts=methods.top_posts(),
                                   reason='Deleted {0} posts'.format(deleted.deleted_count))
    all_posts = posts_collection.find().sort('date', pymongo.DESCENDING)
    return render_template('/admin/posts_list.html', tags=methods.tags, last_posts=methods.last_posts(),
                           top_posts=methods.top_posts(), all_posts=all_posts, posts_number=all_posts.count())


# Change to app.route('/admin/tags', methods=['DELETE'])
@app.route('/admin/delete_tag/<tag_to_delete>')
def delete_tag(tag_to_delete):
    tag_deletion = db.tags.update({}, {'$pull': {'tags': tag_to_delete}})
    # Check deletion results
    if tag_deletion['nModified'] == 1:
        return tags_admin('Successfully deleted tag {0}. '.format(tag_to_delete))
    return tags_admin('Error occurred while attempting deletion of tag {0}'.format(tag_to_delete))


@app.route('/admin/tags', methods=['POST'])
def add_tag():
    new_tag = request.form['new_tag']
    reloaded_tags = methods.reload_tags()
    # Check if it's ok to add the new tag
    if new_tag and (new_tag not in methods.tags):
        tag_addition = db.tags.update({}, {'$push': {'tags': new_tag}})
        if tag_addition['nModified'] == 1:
            methods.reload_tags()
            return tags_admin('Tag \'{0}\' added successfully.'.format(new_tag))
    else:
        return tags_admin('ERROR: Either the tag already exists of the form sent empty')
    if tag_addition['nModified'] == 1:
            return tags_admin()
    return render_template('oops.html', reason='Something went wrong while adding a tag.', tags=reloaded_tags,
                           top_posts=methods.top_posts(), last_posts=methods.last_posts())


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory('C:\users\goas\Desktop\personal\\blog\static\pictures\\',
                               filename)


@app.route('/admin/create_post', methods=['POST', 'GET'])
def create_post():
    if request.method == 'GET':
        return render_template('/admin/create_post.html', tags=methods.tags, top_posts=methods.top_posts(),
                               last_posts=methods.last_posts())
    image_location = ''
    if 'image_location' in request.files.keys():
        image = request.files['image_location']
        filename = secure_filename(image.filename)
        if filename.split('.')[-1] in conf.ALLOWED_EXTENSIONS:
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            image_location = '/static/pictures/' + filename
        print image_location

    data = {}
    primary_tag = ''
    secondary_tag = []
    # Go through all selected tags
    for i in request.form:
        if 'primary_tag_' in i:
            primary_tag = i.split('_')[-1]
        elif 'secondary_tag_' in i:
                secondary_tag.append(i.split('_')[-1])

    # Constant variables
    date = datetime.utcnow()
    data.update({'author': 'Maor Goaz', 'date': date})  # .strftime('%Y-%m-%d %H:%M:%S')
    # Data that came from the form itself
    data.update({'img_location': image_location,
                 'img_caption': request.form['image_caption'],
                 'lead': request.form['lead'],
                 'text': request.form['text'],
                 'title': request.form['title'],
                 'primary_tag': primary_tag,
                 'secondary_tags': secondary_tag,
                 'comments': [],
                 'views': 0
                 })
    # Create post
    insert_post = posts_collection.insert_one(data)
    # Check operation results
    if insert_post.acknowledged:
        methods.email_post(request.form['title'], primary_tag, date.strftime('%Y-%m-%d'))
        return render_template('/admin/create_post.html', successful=True, tags=methods.tags,
                               top_posts=methods.top_posts(), last_posts=methods.last_posts())
    else:
        return render_template('/admin/create_post.html', failure=True, error='An error occurred while saving post',
                               tags=methods.tags, top_posts=methods.top_posts(), last_posts=methods.last_posts())


@app.route('/posts/<title>/<comment_id>/upvote')
def upvote(comment_id, title):
    up = posts_collection.update({'title': title, 'comments.id': comment_id}, {'$inc': {'comments.$.upvotes': 1}})
    if up['updatedExisting']:
        return redirect('/posts/' + title)
    else:
        return render_template('oops.html', reason='Couldn\'t upvote the comment. Sorry.', tags=methods.tags,
                               top_posts=methods.top_posts(), last_posts=methods.last_posts())


@app.route('/posts/<title>/<comment_id>/downvote')
def downvote(comment_id, title):
    down = posts_collection.update({'title': title, 'comments.id': comment_id}, {'$inc': {'comments.$.upvotes': -1}})
    if down['updatedExisting']:
        return redirect('/posts/' + title)
    else:
        return render_template('oops.html', reason='Couldn\'t downvote the comment. Sorry.', tags=methods.tags,
                               top_posts=methods.top_posts(), last_posts=methods.last_posts())


@app.route('/subscribe', methods=['GET', 'POST'])
def subscribe():
    if request.method == 'GET':
        return render_template('subscribe.html', top_posts=methods.top_posts(), last_posts=methods.last_posts(),
                               tags=methods.tags)
    else:
        if request.form['email']:
            email = request.form['email']
        else:
            return render_template('subscribe.html', message='Received empty email address.',
                                   top_posts=methods.top_posts(), last_posts=methods.last_posts(), tags=methods.tags)
        if '@' in email and '.' in email:
            # process
            with open('MAILING_LIST', 'r') as f:
                if email in f.read().split('\n'):
                    return render_template('subscribe.html', message='Email already exists in the system.',
                                           top_posts=methods.top_posts(), last_posts=methods.last_posts(),
                                           tags=methods.tags)
            with open('MAILING_LIST', 'a') as f:
                f.write('{0}\n'.format(email))
            return render_template('subscribe.html', success_message='Email was successfully registered.',
                                   top_posts=methods.top_posts(), last_posts=methods.last_posts(), tags=methods.tags)
        else:
            return render_template('subscribe.html', message='Wrong email convention.', top_posts=methods.top_posts(),
                                   last_posts=methods.last_posts(), tags=methods.tags)
