from flask import render_template, url_for, flash, redirect, request
from app import app, db
from app.forms import CreatePostForm, EditPostForm
from app.models import Post
import datetime

@app.route('/')
@app.route('/home')
def home():
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    return render_template('home.html', posts=posts)

@app.route('/create', methods=['GET', 'POST'])
def create_post():
    form = CreatePostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data,
                    content=form.content.data,
                    timestamp=datetime.datetime.utcnow())
        db.session.add(post)
        db.session.commit()
        flash('Post created successfully.', 'success')
        return redirect(url_for('home'))

    return render_template('create_post.html', form=form)

@app.route('/post/<int:post_id>')
def view_post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('view_post.html', post=post)

@app.route('/post/<int:post_id>/edit', methods=['GET', 'POST'])
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    form = EditPostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Post updated successfully.', 'success')
        return redirect(url_for('view_post', post_id=post.id))

    form.title.data = post.title
    form.content.data = post.content
    return render_template('edit_post.html', form=form, post=post)

@app.route('/post/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash('Post deleted successfully.', 'success')
    return redirect(url_for('home'))