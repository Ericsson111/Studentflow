import os
import secrets
from flask import render_template, url_for, flash, redirect, request, abort, session, jsonify
from studentflow import app, db
from studentflow.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm, FeedbackForm, ChatForm, CommentForm # import forms from forms.py
from studentflow.models import User, Post, Feedback, Chat, Comment # import models from models.py
from flask_login import login_user, current_user, logout_user, login_required

@app.route("/", methods=['GET', 'POST']) # Bring users to login page, method = ['GET','POST"]
def main():
    if current_user.is_authenticated: # if user has login already
        return redirect(url_for('home')) # redirect to home page
    form = RegistrationForm() # form = Register_form
    if form.validate_on_submit(): # validate = input form and submit
        user = User(username=form.username.data, email=form.email.data, password=form.password.data) # user_data = username + email + password
        db.session.add(user) # add this user to db file
        db.session.commit() # save
        flash('Your account has been created! You are now able to log in', 'success') # show this messages to user
        return redirect(url_for('home')) # redirect page to login, double checl
    return render_template('main.html', title='Register', form=form) # return to register.html, title=Register, form=form

@app.route("/home")
def home():
    posts = Post.query.order_by(Post.date_posted.desc())
    return render_template('home.html', posts=posts)

@app.route("/login", methods=['GET', 'POST']) # Bring users to login page, method = ['GET','POST"]
def login():
    if current_user.is_authenticated: # if users had login already
        return redirect(url_for('home')) # redirect to home page
    form = LoginForm() # form =  Login_form
    if form.validate_on_submit(): # validate = input form and submit
        user = User.query.filter_by(email=form.email.data).first() # user filter by email
        if user and bcrypt.check_password_hash(user.password, form.password.data): # check user's password
            login_user(user, remember=form.remember.data) # login user, remember current user
            next_page = request.args.get('next') # turn to next page
            return redirect(next_page) if next_page else redirect(url_for('home')) # redirect to home page
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger') # show this messages to user
    return render_template('login.html', title='Login', form=form) # return to login.html, title = Login, form = form

@app.route("/logout") # logout user
def logout():
    logout_user()
    return redirect(url_for('login')) # redirect to main page

@app.route("/updateaccount", methods=['GET', 'POST']) # Bring user to account page, method = ['Get','POST']
@login_required # login before access to this page
def updateaccount():
    form = UpdateAccountForm() # form = Updateaccount_form
    if form.validate_on_submit(): # validate = input form and submit
        current_user.username = form.username.data # current username = current username data form
        current_user.email = form.email.data # current user_email = current user email data form
        db.session.commit() # save
        flash('Your account has been updated!', 'success') # show this message to user
        return redirect(url_for('updateaccount')) # redirect to account page
    elif request.method == 'GET':
        form.username.data = current_user.username # username form data = current username
        form.email.data = current_user.email # user_email form data = current user email
        form.about.data = current_user.about 
        form.location.data = current_user.location 
        form.phone.data = current_user.phone
        form.birth.data = current_user.birth
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form) # return to account.html, title=Account, account form = account form

@app.route("/post/new", methods=['GET', 'POST']) # Bring user to /post/new, methods=['GET','POST']
@login_required # login before user access to this page
def new_post():
    form = PostForm() # form = Post_form
    if form.validate_on_submit(): # validate = input form and submit
        post = Post(title=form.title.data, content=form.content.data, tag=form.tag.data, author=current_user) # post = post_title + post_content + post_author
        db.session.add(post) # add post
        db.session.commit() # save
        flash('Your post has been created!', 'success') # show this message to user
        return redirect(url_for('home')) # redirect to home page
    return render_template('create_post.html', title='New Post', form=form, legend='New Post') # return to create_post.html, title = New Post, post_form = post_form

@app.route("/commentpost/<int:post_id>", methods=['GET', 'POST'])
@login_required
def commentpost(post_id):
    post = Post.query.get_or_404(post_id)
    form = CommentForm() # form = Post_form
    if form.validate_on_submit():
        comment = Comment(name=form.name.data, content=form.content.data)
        db.session.add(comment)
        db.session.commit() 
        flash('Your comment has been posted!', 'success')
        return redirect(url_for('home'))
    return render_template("comment.html", title='New Comment', form=form, legend='New Comment')

@app.route("/allcomment/<int:post_id>")
@login_required
def allcomment(post_id): 
    post = Post.query.get_or_404(post_id)
    comments = Comment.query.order_by(Comment.date_posted.desc())
    return render_template('allcomment.html', comments=comments)

@app.route("/get_my_ip", methods=["GET"])
def get_my_ip():
    return jsonify({'ip': request.remote_addr}), 200

@app.route("/feedback/new", methods=['GET', 'POST'])
@login_required
def new_feedback():
    form = FeedbackForm() # form = Post_form
    if form.validate_on_submit():
        feedback = Feedback(content=form.content.data, author=current_user)
        db.session.add(feedback)
        db.session.commit() 
        flash('Your feedback has been posted! We will check as soon as we see it', 'success')
        return redirect(url_for('home'))
    return render_template("feedback.html", title='New Feedback', form=form, legend='New Feedback')

@app.route("/all-feedback/templates/allfeedback.html")
@login_required
def allfeedback():
    feedbacks = Feedback.query.order_by(Feedback.date_posted.desc())
    return render_template('allfeedback.html', feedbacks=feedbacks)

@app.route("/message/new", methods=['GET', 'POST'])
@login_required
def new_message():
    form = ChatForm() # form = Post_form
    if form.validate_on_submit():
        chat = Chat(content=form.content.data, author=current_user)
        db.session.add(chat)
        db.session.commit() 
        flash('Your chat has been sended!', 'success')
        return redirect(url_for('allmessage'))
    return render_template("message.html", title='New Chat', form=form, legend='New Chat')  

@app.route("/allmessage")
@login_required
def allmessage():
    chats = Chat.query.order_by(Chat.date_posted.desc())
    return render_template('allmessage.html', chats=chats) 

@app.route("/post/<int:post_id>/update", methods=['GET', 'POST']) # Bring user to post/post_id/update, methods=['GET','POST']
@login_required # login before access to this page
def update_post(post_id): # post_id form
    post = Post.query.get_or_404(post_id) # post = get post_id
    if post.author != current_user: # if current user != author
        abort(403) # don't have this feature
    form = PostForm() # form = Postform
    if form.validate_on_submit(): # validate = input form and submit
        post.title = form.title.data # post_title = post_title form data
        post.content = form.content.data # post_content = post_content form data
        post.tag = form.tag.data
        db.session.commit() # save
        flash('Your post has been updated!', 'success') # show this message to user
        return redirect(url_for('post', post_id=post.id)) # redirect to post page, post_id = post_id
    elif request.method == 'GET':
        form.title.data = post.title # post_title data form = post_title
        form.content.data = post.content # post_content data form = post_content
        form.tag.data = post.tag
    return render_template('create_post.html', title='Update Post',
                           form=form, legend='Update Post') # return to create_post.html, title=Update Post, post_form = post_form

@app.route("/post/<int:post_id>/deletepost", methods=['POST']) # Bring user to /post/post_id/deletepost, methods=['POST']
@login_required # login before user access this page 
def delete_post(post_id): # post_id
    post = Post.query.get_or_404(post_id) # post.query by post_id
    if post.author != current_user: # if current_user != author
        abort(403) # don't have this feature
    db.session.delete(post) # delete post
    db.session.commit() # save
    flash('Your post has been deleted!', 'success') # show this message to user
    return redirect(url_for('home')) # redirect to home page

@app.route("/base") # Bring user to /base
def base():
    return render_template("base.html") # return to base.html

@app.route("/NucleusCellMembraneCytoplasmRibosomesEndoplasmicReticulumMitochondriaGolgiBodiesLysosomesVacuolesCellWallChloroplasts") # Admin page
@login_required # login first
def view():
    return render_template("view.html", values=User.query.all()) # return to view.html, values=User.query.all(), take all the user data from db

@app.route("/post/<int:post_id>", methods=['GET', 'POST']) # Bring user to /post/post_id, methods=['GET','POST']
def post(post_id):
    post = Post.query.get_or_404(post_id) # post = Get post by post_id
    return render_template('post.html', title=post.title, post=post) # return to post.html, title=post_title, post_form=post_form

@app.route("/users/<string:username>") # route = users/username
@login_required # login before user access to this page
def user_posts(username): # from username data
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=10)
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('user_posts.html', posts=posts, image_file=image_file, user=user)

# ----------------------------------------------

# help section

@app.route("/question")
def question():
    return render_template('question.html')

@app.route("/help") # Bring user to /help 
def help():
    return render_template("help.html") # return to help.html

@app.route("/help/privacy")
def privacy():
    return render_template("privacy.html")

@app.route("/help/terms")
def terms():
    return render_template("terms.html")

@app.route("/help/question-for-post")
@login_required
def help_question_for_post():
    return render_template("question-for-post.html")

@app.route("/help/contact")
@login_required 
def contact():
    return render_template("contact.html")

@app.route("/inbox/<string:username>")
@login_required
def user_inbox(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=10)
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('inbox.html', posts=posts, image_file=image_file, user=user)
# ----------------------------------------------

# find section 
@app.route("/post/findpost")
@login_required 
def findpost():
    return render_template("findpost.html", values=Post.query.all())

@app.route("/post/how-to-find-post")
@login_required 
def how_to_find_post():
    return render_template("howtofindpost.html")

@app.route("/user/finduser") # Bring users to home page
@login_required 
def user_finduser():                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        
    return render_template('finduser.html', values=User.query.all()) # return to home.html, posts = posts

@app.route('/post/findtags')
@login_required 
def post_findtag():
    return render_template('tags.html', values=Post.query.all())

# ----------------------------------------------

@app.route("/welcome/<string:username>/")
@login_required 
def user_welcome(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=10)
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('welcome.html', posts=posts, image_file=image_file, user=user)

@app.route('/about')
def about():
    return render_template('about.html')

# help page ask 
@app.route('/help/what-post')
@login_required
def help_what_post():
    return render_template('what-post.html')
    
@app.route('/help/on-topic')
@login_required
def help_on_topic():
    return render_template('on-topic.html')

@app.route('/help/write-good-post')
@login_required
def help_write_good_post():
    return render_template('write-good-post.html')

@app.route('/help/all-badges-can-earn')
@login_required
def help_allbadges():
    return render_template('allbadges.html')