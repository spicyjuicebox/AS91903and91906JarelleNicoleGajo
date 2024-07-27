from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from .models import Post, User, Like, Comment, Order
from . import db

views = Blueprint("views", __name__)


@views.route("/")
@views.route("/home")
def home():
    return render_template("home.html", user=current_user)


@views.route("/blog")
@login_required
def blog():
    posts = Post.query.all()
    return render_template("blog.html", user=current_user, posts=posts)

# Order
@views.route("/order", methods=['GET', 'POST'])
@login_required
def menu():
    if request.method == 'POST':
        order = request.form.get('order')
        if order:
            return redirect(url_for('views.payment_option', order=order))
    return render_template("order.html", user=current_user)

@views.route('/payment_option', methods=['GET', 'POST'])
@login_required
def payment_option():
    order = request.args.get('order')
    if not order:
        flash('No order found.', category='error')
        return redirect(url_for('views.menu'))
    return render_template('payment_option.html', user=current_user, order=order)

@views.route('/cash_payment', methods=['GET', 'POST'])
@login_required
def cash_payment():
    order = request.args.get('order')
    if not order:
        flash('No order found.', category='error')
        return redirect(url_for('views.menu'))
    new_order = Order(items=order, user_id=current_user.id, user_email=current_user.email, payment_method='Cash')
    db.session.add(new_order)
    db.session.commit()
    return render_template('cash_payment.html', user=current_user, order=order)

@views.route('/card_payment', methods=['GET', 'POST'])
@login_required
def card_payment():
    order = request.args.get('order')
    if not order:
        flash('No order found.', category='error')
        return redirect(url_for('views.menu'))
    return render_template('card_payment.html', user=current_user, order=order)

@views.route('/process_card_payment', methods=['POST'])
@login_required
def process_card_payment():
    order = request.form.get('order')
    new_order = Order(items=order, user_id=current_user.id, user_email=current_user.email, payment_method='Card')
    db.session.add(new_order)
    db.session.commit()
    return redirect(url_for('views.thank_you'))

@views.route('/thankyou', methods=['GET'])
@login_required
def thank_you():
    return render_template('thankyou.html', user=current_user)
# End Order


@views.route("/create-post", methods=['GET', 'POST'])
@login_required
def create_post():
    if request.method == "POST":
        text = request.form.get('text')
        if not text:
            flash('Post cannot be empty.', category='error')
        else:
            post = Post(text=text, author=current_user.id)
            db.session.add(post)
            db.session.commit()
            flash('Post created!', category='success')
            return redirect(url_for('views.blog'))
    return render_template('create_post.html', user=current_user)

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