import os
from pathlib import Path
from PIL import Image
import secrets
from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify, abort
from flask_login import login_required, current_user
from .models import Post, User, Like, Comment
from .forms import UpdateAccountForm, PostForm
from . import db

views = Blueprint("views", __name__)

# Route for Home
# Directing the user to the Home page.
@views.route("/")
@views.route("/home")
def home(): # The 'home' function defined.
    return render_template("home.html", user=current_user) # Render the Home page for the current user.

# Q&A + Suggestions
# Route for Q&A + Suggestions
# Directing the user to the Q&A + Suggestions page.
# Includes the @login_required so this ensures that the user is logged into view the page. This decorator will be used for the rest of the routes below.
@views.route("/qasuggestions")
@login_required
def qasuggestions(): # The 'qasuggestions' function defined.
    posts = Post.query.all() # SQL is used to link all the posts posted in this page and into the database table, 'post'.
    return render_template("qasuggestions.html", user=current_user, posts=posts) # Render the Q&A + Suggestions page and the posts for the current user.

# Route for Creating a Post
# When the 'Create a Post' button is pressed, the user is directed to the 'create_post' page where this route will start.
@views.route("/create-post", methods=['GET', 'POST'])
@login_required
def create_post(): # The 'create_post' function defined.
    form = PostForm()
    if form.validate_on_submit():
        title = form.title.data
        text = form.text.data
        post = Post(title=title, text=text, author=current_user.id)
        db.session.add(post) # The post will be added to the 'post' table.
        db.session.commit() # After creating the post, the post, including the title and text, will be added to the database.
        flash('Post created! ✅', category='success') # Flash message will appear to inform the user that their post has been posted.
        return redirect(url_for('views.qasuggestions')) # After the post is created, the user will be directed back to the Q&A + Suggestions page.
    return render_template('create_post.html', form=form, user=current_user) # Render the Create a Post page and the form for creating a post for the current user.

# Route for Liking a Post
# When the like button is pressed, this route will start.
@views.route("/like-post/<post_id>", methods=['POST'])
@login_required
def like(post_id): # The 'like' function defined for liking a post.
    post = Post.query.filter_by(id=post_id).first() # The 'post' from the database is linked with the 'like' table.
    like = Like.query.filter_by(author=current_user.id, post_id=post_id).first() # SQL is used to link the likes with the database table, 'like'.
    # In the database, the 'like' table will link with the user that liked the post with the post_id of the post.
    if not post:
        return jsonify({'error': '🚨 Post does not exist.'}, 400)
    elif like:
        db.session.delete(like) # If the user already liked the post, clicking the like button again will remove it.
        db.session.commit() # When the like is removed, the database will be updated.
    else: # This will start if the post has not been liked.
        like = Like(author=current_user.id, post_id=post_id) # The like is linked with the user that liked the post and the post_id of the post.
        db.session.add(like) # The like for the post will be added in the database and update the like table.
        db.session.commit() # Database is updated after liking the post.
    return jsonify({"likes": len(post.likes), "liked": current_user.id in map(lambda x: x.author, post.likes)})


# Route for Posts of Users
# When the username of a user is clicked, the user will be directed to a separate page showing the posts of that user.
@views.route("/posts/<username>")
@login_required
def posts(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        flash('🚨 No user with that username exists.', category='error')
        return redirect(url_for('views.home'))
    posts = Post.query.filter_by(author=user.id).all() # This will show the posts that were created by the user with the username clicked.
    return render_template("posts.html", user=current_user, posts=posts, username=username) # The page that shows only the posts of the user clicked will run 'posts.html'.


# Route for Deleting a Post
@views.route("/delete-post/<id>")
@login_required
def delete_post(id):
    post = Post.query.filter_by(id=id).first()
    if not post:
        flash("🚨 Post does not exist.", category='error')
    elif post.author != current_user.id:
        flash('🚨 You do not have permission to delete this post.', category='error')
    else:
        db.session.delete(post)
        db.session.commit() # When the post is deleted, the database will be updated by removing the post from the post table.
        flash('Post deleted. ✅', category='success') # Flash message will appear to inform the user that their post has been deleted.
    return redirect(url_for('views.qasuggestions')) # After deleting the post, the user stays on the same page.


# Route for Creating a Comment on a Post
@views.route("/create-comment/<post_id>", methods=['POST'])
@login_required
def create_comment(post_id):
    text = request.form.get('text') # Text box form for where the user must type in their comment.
    if not text:
        flash('🚨 Comment cannot be empty.', category='error') # Flash message letting the user know that they cannot post an empty comment.
    else:
        post = Post.query.filter_by(id=post_id)
        if post:
            comment = Comment(
                text=text, author=current_user.id, post_id=post_id)
            db.session.add(comment)
            db.session.commit() # When a comment is posted, the database will be updated by adding the new comment into the comment table.
        else:
            flash('🚨 Post does not exist.', category='error')
    return redirect(url_for('views.qasuggestions')) # After creating the comment, the user stays on the same page.


# Route for Deleting a Comment on a Post
@views.route("/delete-comment/<comment_id>")
@login_required
def delete_comment(comment_id):
    comment = Comment.query.filter_by(id=comment_id).first() # The comment is linked with the comment_id for the post that the user posted the comment.
    if not comment:
        flash('🚨 Comment does not exist.', category='error')
    elif current_user.id != comment.author and current_user.id != comment.post.author:
        flash('🚨 You do not have permission to delete this comment.', category='error')
    else:
        db.session.delete(comment)
        db.session.commit() # When the comment is deleted, the database will be updated by removing the comment from the comment table.
    return redirect(url_for('views.qasuggestions')) # After deleting the comment, the user stays on the same page.
# Q&A + Suggestions End


# Route for Contact
# Directing the user to the Contact page.
@views.route("/contact")
@login_required
def contact(): # The 'contact' function defined.
    return render_template("contact.html", user=current_user) # Render the Contact page for the current user.


# Route for About
# Directing the user to the About page.
@views.route("/about")
@login_required
def about(): # The 'about' function defined.
    return render_template("about.html", user=current_user) # Render the About page for the current user.


# Account
# Route for Saving the Profile Picture
def save_picture(form_picture): # The 'form_picture' function defined.
    path = Path("website/static/profile_pics") # The path of where the profile pictures will be stored.
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(path, picture_fn)
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    
    return picture_fn

# Route for the Account
@views.route("/account", methods=['GET', 'POST'])
@login_required
def account(): # The 'account' function defined.
    form = UpdateAccountForm() # The form is what the user sees they can update on the page.
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit() # After updating the account of the username, profile picture or the email, the database will be updated.
        flash('Your account has been updated! ✅', 'success') # Flash message to let the user know that their account has been updated.
        return redirect(url_for('views.account')) # Directing the user back to the account page.
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename = 'profile_pics/' + current_user.image_file)
    return render_template('account.html', user = current_user, image_file = image_file, form = form)
# Account End


# Updating the Post.
@views.route("/update-post/<id>", methods=['GET', 'POST'])
@login_required
def update_post(id):
    post = Post.query.filter_by(id=id).first()
    if post.author != current_user.id:
        abort(403)
    form = PostForm() # The form is what the user sees they can update on the page.
    if form.validate_on_submit():
        post.title = form.title.data
        post.text = form.text.data
        db.session.commit() # When the user updates their post, the database will be updated.
        flash('Post Updated! ✅', category='success') # Flash message to let the user know that their post has been updated.
        page = request.args.get('page', 1, type=int)
        posts = Post.query.order_by(Post.date_created.desc()).paginate(page=page, per_page=4)
        return render_template("qasuggestions.html", user=current_user, posts=posts)
    
    elif request.method == 'GET': # When loading the page, it will get what is already in the database.
        form.title.data = post.title
        form.text.data = post.text
        image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('update_post.html', form=form, user=current_user, post=post, image_file=image_file)