import os
from pathlib import Path
from PIL import Image
import secrets
from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from .models import Post, User, Like, Comment, Order
from .forms import UpdateAccountForm, PostForm
from . import db


views = Blueprint("views", __name__)


@views.route("/")
@views.route("/home")
def home():
    return render_template("home.html", user=current_user)


@views.route("/blog")
@login_required
def blog():
    # New for paginating.
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_created.desc()).paginate(page=page, per_page=4)
    return render_template("blog.html", user=current_user, posts=posts)

# New
@views.route("/order", methods=['GET', 'POST'])
@login_required
def menu():
    if request.method == 'POST':
        order = request.form.get('order')
        total = request.form.get('total')
        if order and total:
            return redirect(url_for('views.payment_option', order=order, total=total))
    return render_template("order.html", user=current_user)

@views.route('/payment_option', methods=['GET', 'POST'])
@login_required
def payment_option():
    order = request.args.get('order')
    total = request.args.get('total')
    if not order or not total:
        flash('No order found.', category='error')
        return redirect(url_for('views.menu'))
    return render_template('payment_option.html', user=current_user, order=order, total=total)

@views.route('/cash_payment', methods=['GET', 'POST'])
@login_required
def cash_payment():
    order = request.args.get('order')
    total = request.args.get('total')
    if not order or not total:
        flash('No order found.', category='error')
        return redirect(url_for('views.menu'))
    new_order = Order(items=order, user_id=current_user.id, user_email=current_user.email, payment_method='Cash', total_price=total)
    db.session.add(new_order)
    db.session.commit()
    return render_template('cash_payment.html', user=current_user, order=order, total=total, total_price=total) # The total_price brings the total price from the cart.

@views.route('/card_payment', methods=['GET', 'POST'])
@login_required
def card_payment():
    order = request.args.get('order')
    total = request.args.get('total')
    if not order or not total:
        flash('No order found.', category='error')
        return redirect(url_for('views.menu'))
    new_order = Order(items=order, user_id=current_user.id, user_email=current_user.email, payment_method='Card', total_price=total)
    db.session.add(new_order)
    db.session.commit()
    return render_template('card_payment.html', user=current_user, order=order, total=total, total_price=total) # The total_price brings the total price from the cart.

@views.route('/process_card_payment', methods=['POST'])
@login_required
def process_card_payment():
    order = request.form.get('order')
    total = request.form.get('total')
    new_order = Order(items=order, user_id=current_user.id, user_email=current_user.email, payment_method='Card', total_price=total)
    db.session.add(new_order)
    db.session.commit()
    return redirect(url_for('views.thank_you'))

@views.route('/thankyou', methods=['GET'])
@login_required
def thank_you():
    return render_template('thankyou.html', user=current_user)
# End


@views.route("/create-post", methods=['GET', 'POST'])
@login_required
def create_post():
    form = PostForm()
    if form.validate_on_submit():
        title = form.title.data
        text = form.text.data
        post = Post(title=title, text=text, author=current_user.id)
        db.session.add(post)
        db.session.commit()
        flash('Post created!', category='success')
        return redirect(url_for('views.blog'))
    
    return render_template('create_post.html', form=form, user=current_user)


@views.route("/like-post/<post_id>", methods=['POST'])
@login_required
def like(post_id):
    post = Post.query.filter_by(id=post_id).first()
    like = Like.query.filter_by(author=current_user.id, post_id=post_id).first()
    if not post:
        return jsonify({'error': 'Post does not exist.'}, 400)
    elif like:
        db.session.delete(like)
        db.session.commit()
    else:
        like = Like(author=current_user.id, post_id=post_id)
        db.session.add(like)
        db.session.commit()
    return jsonify({"likes": len(post.likes), "liked": current_user.id in map(lambda x: x.author, post.likes)})



@views.route("/posts/<username>")
@login_required
def posts(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        flash('No user with that username exists.', category='error')
        return redirect(url_for('views.home'))
    
    posts = Post.query.filter_by(author=user.id).all()
    return render_template("posts.html", user=current_user, posts=posts, username=username)


@views.route("/delete-post/<id>")
@login_required
def delete_post(id):
    post = Post.query.filter_by(id=id).first()
    if not post:
        flash("Post does not exist.", category='error')
    elif post.author != current_user.id:
        flash('You do not have permission to delete this post.', category='error')
    else:
        db.session.delete(post)
        db.session.commit()
        flash('Post deleted.', category='success')
    return redirect(url_for('views.blog'))




@views.route("/create-comment/<post_id>", methods=['POST'])
@login_required
def create_comment(post_id):
    text = request.form.get('text')
    if not text:
        flash('Comment cannot be empty.', category='error')
    else:
        post = Post.query.filter_by(id=post_id)
        if post:
            comment = Comment(
                text=text, author=current_user.id, post_id=post_id)
            db.session.add(comment)
            db.session.commit()
        else:
            flash('Post does not exist.', category='error')
    return redirect(url_for('views.blog'))



@views.route("/delete-comment/<comment_id>")
@login_required
def delete_comment(comment_id):
    comment = Comment.query.filter_by(id=comment_id).first()
    if not comment:
        flash('Comment does not exist.', category='error')
    elif current_user.id != comment.author and current_user.id != comment.post.author:
        flash('You do not have permission to delete this comment.', category='error')
    else:
        db.session.delete(comment)
        db.session.commit()
    return redirect(url_for('views.blog'))


def save_picture(form_picture):
    path = Path("website/static/profile_pics")
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(path, picture_fn)
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    
    return picture_fn

@views.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated! ✅', 'success')
        return redirect(url_for('views.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', user=current_user, image_file=image_file, form=form)