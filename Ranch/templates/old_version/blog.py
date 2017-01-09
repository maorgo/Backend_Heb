# '''
# @app.route('/')
# def index():
#     curs = posts_collection.find().sort('date', pymongo.DESCENDING).limit(3)
#     return render_template('index.html', posts_cursor=curs, category_tags=category_tags_and_count)
# '''
#
# @app.route('/about')
# def about():
#     return render_template('about.py', category_tags=category_tags_and_count)
#
#
# @app.route('/contact')
# def contact():
#     return render_template('contact.html', category_tags=category_tags_and_count)
#
#
# @app.route('/posts')
# def posts():
#     return render_template('subjects.html', category_tags=category_tags_and_count)
#
#
# @app.route('/Python')
# def python():
#     subject_posts = posts_collection.find({'tags': 'Python'}).sort('date', pymongo.DESCENDING)
#     if subject_posts.count() == 0:
#         time_now = time.strftime('%Y-%m-%d %H:%M')
#         return render_template('subject_posts.html', posts=None, now=time_now, topic='Python')
#     return render_template('subject_posts.html', posts=subject_posts, category_tags=category_tags_and_count)
#
#
# @app.route('/MongoDB')
# def mongo():
#     subject_posts = posts_collection.find({'tags': 'MongoDB'}).sort('date', pymongo.DESCENDING)
#     if subject_posts.count() == 0:
#         time_now = time.strftime('%Y-%m-%d %H:%M')
#         return render_template('subject_posts.html', posts=None, now=time_now, topic='MongoDB',
#                                category_tags=category_tags_and_count)
#     return render_template('subject_posts.html', posts=subject_posts, category_tags=category_tags_and_count)
#
#
# @app.route('/Machine Learning')
# def mlearning():
#     subject_posts = posts_collection.find({'tags': 'Machine Learning'}).sort('date', pymongo.DESCENDING)
#     if subject_posts.count() == 0:
#         time_now = time.strftime('%Y-%m-%d %H:%M')
#         return render_template('subject_posts.html', posts=None, now=time_now, topic='Machine Learning',
#                                category_tags=category_tags_and_count)
#     return render_template('subject_posts.html', posts=subject_posts, category_tags=category_tags_and_count)
#
#
# @app.route('/Flask')
# def flask():
#     subject_posts = posts_collection.find({'tags': 'Flask'}).sort('date', pymongo.DESCENDING)
#     if subject_posts.count() == 0:
#         time_now = time.strftime('%Y-%m-%d %H:%M')
#         return render_template('subject_posts.html', posts=None, now=time_now, topic='Flask',
#                                category_tags=category_tags_and_count)
#     return render_template('subject_posts.html', posts=subject_posts, category_tags=category_tags_and_count)
#
#
# @app.route('/posts/<post_id>', methods=['GET', 'POST'])
# def show_full_post(post_id):
#     post = posts_collection.find_one({'title': post_id})
#     return render_template("full_post.html", post=post, category_tags=category_tags_and_count)
#
#
# # Check if user is permitted to get here
# @app.route('/admin')
# def admin():
#     return render_template('admin/admin.html', category_tags=category_tags_and_count)
#
#
# # Check if user is permitted to get here
# @app.route('/admin/manage_users')
# def manage_users():
#     return render_template('admin/manage_users.html', category_tags=category_tags_and_count)
#
#
# # Check if user is permitted to get here
# @app.route('/admin/manage_posts')
# def manage_posts():
#     return render_template('admin/manage_posts.html', category_tags=category_tags_and_count)
#
#
# @app.route('/admin/create_post')
# def create_post():
#     tags = dict(tags_collection.find_one({}, {'_id': 0}))
#     return render_template('admin/create_post.html', tags=tags, category_tags=category_tags_and_count)
#
#
# @app.route('/admin/create_post', methods=['POST'])
# def submit_post():
#     title = request.form['title']
#     post = request.form['post']
#     tags = ''
#     for field in request.form:
#         if request.form[field] == 'on' and field != 'title' and field != 'post':
#             tags += field + ','
#     tags = tags[:-1].split(',')
#     time_now = time.strftime('%Y-%m-%d %H:%M')
#     insert = posts_collection.insert_one({'author': 'Maor Goaz', 'date': time_now, 'title': title, 'text': post,
#                                           'tags': tags, 'update_date': time_now})
#
#     if not insert.acknowledged:
#         return "Error while inserting post"
#     reload_tag_index()
#     return render_template('admin/admin.html', admin_message='The post was uploaded successfully.',
#                            category_tags=category_tags_and_count)
#
#
# @app.route('/admin/change_post')
# def edit_post():
#     titles = posts_collection.find({}, {'title': 1, '_id': 0})
#     return render_template('admin/change_post.html', titles=titles, category_tags=category_tags_and_count)
#
#
# @app.route('/admin/change_post', methods=['POST'])
# def submit_change():
#     chosen_titles = []
#     if request.form['Submit']:
#         for item in request.form:
#             if request.form[item] == 'on' and item != 'delete':
#                 # title = json.dumps(item)[1:-1]
#                 # return str(title)
#                 chosen_titles.append(item.split(': u\'')[1][:-2])
#         if 'delete' in request.form:
#             for title in chosen_titles:
#                 posts_collection.remove({'title': title})
#             reload_tag_index()
#             return render_template('admin/admin.html', admin_message='The posts {0} were deleted successfully.'
#                                    .format(chosen_titles), category_tags=category_tags_and_count)
#         else:
#             if len(chosen_titles) > 1:
#                 return render_template('admin/admin.html', admin_message='ERROR: Only one post can be edited at a '
#                                                                          'time.', category_tags=category_tags_and_count)
#             else:
#                 # Edit the post
#                 post = posts_collection.find_one({'title': chosen_titles[0]}, {'_id': 0})
#                 tags = tags_collection.find_one({})
#                 reload_tag_index()
#                 return render_template('admin/edit_post.html', post=post, tags=tags)
#
#
# @app.route('/admin/edit_post', methods=['POST'])
# def commit_post_changes():
#     current_tags = []
#     old_title = request.form['old_title']
#     title = request.form['title']
#     text = request.form['post']
#     update_time = time.strftime('%Y-%m-%d %H:%M')
#     for item in request.form:
#         if item not in ['post', 'title', 'old_title']:
#             current_tags.append(item)
#     # Update the post
#     a = posts_collection.update_one({'title': old_title}, {'$set': {'title': title, 'text': text,
#                                                                     'tags': current_tags, 'update_date': update_time}})
#     reload_tag_index()
#     post = posts_collection.find_one({'title': title}, {'_id': 0})
#     tags = tags_collection.find_one({})
#     if a.modified_count == 0:
#         return render_template('admin/edit_post.html', post=post, tags=tags,
#                                message='<font color="red">The post \'' + title + '\' was not edited '
#                                                                                  'successfully</font>')
#     #     return render_template('admin/admin.html', admin_message='The post \'' + title +
#     #                                                              '\' was not updated successfully')
#     # return render_template('admin/admin.html', admin_message='The post \'' + title + '\' was updated successfully')
#     return render_template('admin/edit_post.html', post=post, tags=tags,
#                            message='<font color="green">The post \'' + title + '\' was edited successfully</font>')
#
#
# @app.route('/posts/<post_title>/comment', methods=['POST'])
# def add_comment(post_title):
#     result = posts_collection.update_one({'title': post_title},
#                                          {
#                                              '$push':
#                                                  {
#                                                      'comments':
#                                                          {
#                                                             'author': request.form['name'],
#                                                             'comment': request.form['comment'],
#                                                             'comment_date': time.ctime(),
#                                                             'upvotes': 0,
#                                                             'id': uuid.uuid4().hex
#                                                          }
#                                                  }
#                                          }
#                                          )
#     if result.modified_count == 1:
#         return redirect(request.referrer)
#     else:
#         return 'Comment Failed.'
#         # Add a redirect here to the original post. Maybe change the 'Comment Failed' message
#         # with js popup and then redirect.
#
#
# @app.route('/upvote/<title>', methods=['POST', 'GET'])
# def upvote(title):
#     comment_id = request.args.get('comment_id')
#     r = posts_collection.update_one({'comments.id': comment_id}, {'$inc': {'comments.$.upvotes': 1}})
#     if r.modified_count > 1:
#         return 'ERROR: More than one documents were upvoted. comment_id: {0}'.format(comment_id)
#     elif r.modified_count == 0:
#         return 'Could not perform upvote. comment_id: {0}'.format(comment_id)
#     else:
#         post = posts_collection.find_one({'title': title})
#         return render_template("full_post.html", post=post, category_tags=category_tags_and_count)
#
#
# @app.route('/downvote/<title>', methods=['POST', 'GET'])
# def downvote(title):
#     comment_id = request.args.get('comment_id')
#     r = posts_collection.update_one({'comments.id': comment_id}, {'$inc': {'comments.$.upvotes': -1}})
#     if r.modified_count > 1:
#         return 'ERROR: More than one documents were upvoted. comment_id: {0}'.format(comment_id)
#     elif r.modified_count == 0:
#         return 'Could not perform upvote. comment_id: {0}'.format(comment_id)
#     else:
#         post = posts_collection.find_one({'title': title})
#         # redirect(url_for('show_full_post', post_id=post))
#         return render_template("full_post.html", post=post, category_tags=category_tags_and_count)
#
#
# @app.route('/admin/change_user', methods=['GET', 'POST'])
# def change_user():
#     if request.form:
#         username_taken = False
#         email_taken = False
#         old_username = request.form['old_username']
#         username = request.form['username']
#         password = request.form['password']
#         confirm_password = request.form['confirm_password']
#         email = request.form['email']
#         interests = request.form['interests']
#         if not complexed_password(password):
#             return render_template('admin/change_user.html', message='<font color="red">Password is not complexed '
#                                                                      'enough. <br> Should be at least 8 characters, '
#                                                                      '1 letter and 1 digits.</font>',
#                                    category_tags=category_tags_and_count)
#         if not password == confirm_password:
#             return render_template('admin/change_user.html', message='<font color="red">Passwords do not match</font>',
#                                    category_tags=category_tags_and_count)
#         elif '@' not in email or '.' not in email:
#             return render_template('admin/change_user.html', message='<font color="red">Email is not valid</font>',
#                                    category_tags=category_tags_and_count)
#         users = users_collection.find({}, {'_id': 0, 'username': 1, 'email': 1})
#         for i in users:
#                 if i['username'] == username:
#                     username_taken = True
#                 elif i['email'] == email:
#                     email_taken = True
#                 if username_taken and not email_taken:
#                     return render_template('admin/change_user.html', message='<font color="red">This username is '
#                                                                              'already being used. Please choose '
#                                                                              'a different one.</font>',
#                                            category_tags=category_tags_and_count)
#                 elif not username_taken and email_taken:
#                     return render_template('admin/change_user.html', message='<font color="red">This email is already '
#                                                                              'being used. Please choose a different '
#                                                                              'one.</font>',
#                                            category_tags=category_tags_and_count)
#                 elif username_taken and email_taken:
#                     return render_template('admin/change_user.html', message='<font color="red">Both the username '
#                                                                              'and the email are being used. Please '
#                                                                              'choose others.</font>',
#                                            category_tags=category_tags_and_count)
#                 else:
#                     hash_object.update(password)
#                     password = hash_object.hexdigest()
#                     update = users_collection.update_one({'username': old_username},
#                                                          {'$set': {'username': username, 'password': password,
#                                                                    'email': email, 'interests': interests}})
#                     if update.modified_count < 1:
#                         return render_template('admin/change_user.html', message='<font color="red">Failed updating '
#                                                                                  'the user. <br>Check if the old '
#                                                                                  'username exists.</font>',
#                                                category_tags=category_tags_and_count)
#                     elif update.modified_count > 1:
#                         return render_template('admin/change_user.html', message='<font color="red">More than one '
#                                                                                  'users were modified.</font>',
#                                                category_tags=category_tags_and_count)
#                     else:
#                         return render_template('admin/change_user.html', message='<font color="green">The user was '
#                                                                                  'updated successfully.</font>',
#                                                category_tags=category_tags_and_count)
#     return render_template('admin/change_user.html', category_tags=category_tags_and_count)
#
#
# @app.route('/admin/create_user', methods=['POST', 'GET'])
# def create_user():
#     if request.form:
#         username_taken = False
#         email_taken = False
#         username = request.form['username']
#         password = request.form['password']
#         confirm_password = request.form['confirm_password']
#         email = request.form['email']
#         interests = request.form['interests']
#         if not complexed_password(password):
#             return render_template('admin/create_user.html', message='<font color="red">Password is not complexed '
#                                                                      'enough. <br> Should be at least 8 characters, '
#                                                                      '1 letter and 1 digits.</font>',
#                                    category_tags=category_tags_and_count)
#         if not password == confirm_password:
#             return render_template('admin/create_user.html', message='<font color="red">Passwords do not match</font>',
#                                    category_tags=category_tags_and_count)
#         elif '@' not in email or '.' not in email:
#             return render_template('admin/create_user.html', message='<font color="red">Email is not valid</font>',
#                                    category_tags=category_tags_and_count)
#         else:
#             users = users_collection.find({}, {'_id': 0, 'username': 1, 'email': 1})
#             if users.count() == 0:
#                 insert = users_collection.insert_one({'username': username, 'password': password, 'email': email,
#                                                       'interests': interests})
#                 if insert.acknowledged:
#                     return render_template('admin/create_user.html', message='<font color="green">The user was created '
#                                                                              'successfully.</font>',
#                                            category_tags=category_tags_and_count)
#                 else:
#                     return render_template('admin/create_user.html', message='<font color="red">Error occurred while'
#                                                                              ' creating the user.</font>',
#                                            category_tags=category_tags_and_count)
#             for i in users:
#                 if i['username'] == username:
#                     username_taken = True
#                 elif i['email'] == email:
#                     email_taken = True
#                 if username_taken and not email_taken:
#                     return render_template('admin/create_user.html', message='<font color="red">This username is '
#                                                                              'already being used. Please choose '
#                                                                              'a different one.</font>',
#                                            category_tags=category_tags_and_count)
#                 elif not username_taken and email_taken:
#                     return render_template('admin/create_user.html', message='<font color="red">This email is already '
#                                                                              'being used. Please choose a different '
#                                                                              'one.</font>',
#                                            category_tags=category_tags_and_count)
#                 elif username_taken and email_taken:
#                     return render_template('admin/create_user.html', message='<font color="red">Both the username '
#                                                                              'and the email are being used. Please '
#                                                                              'choose others.</font>',
#                                            category_tags=category_tags_and_count)
#                 else:
#                     hash_object.update(password)
#                     password = hash_object.hexdigest()
#                     insert = users_collection.insert_one({'username': username, 'password': password, 'email': email,
#                                                           'interests': interests})
#                     if insert.acknowledged:
#                         return render_template('admin/create_user.html', message='<font color="green">The user was '
#                                                                                  'created successfully.</font>',
#                                                category_tags=category_tags_and_count)
#                     else:
#                         return render_template('admin/create_user.html', message='<font color="red">Error occurred '
#                                                                                  'while creating the user.</font>',
#                                                category_tags=category_tags_and_count)
#     return render_template('admin/create_user.html', category_tags=category_tags_and_count)
#
#
# def complexed_password(password):
#     length = len(password) < 8
#     is_digit = any(char.isdigit() for char in password)
#     is_letter = any(char.isalpha() for char in password)
#     return str(length) + str(is_letter) + str(is_digit)