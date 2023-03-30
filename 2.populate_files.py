# populate_init.py - Populate app/__init__.py

file_path = 'flask_blog/app/__init__.py'

content = '''
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

from app import views, models
'''

with open(file_path, 'w') as f:
    f.write(content.strip())

# populate_models.py - Populate app/models.py

file_path = 'flask_blog/app/models.py'

content = '''
from app import db

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f'<Post {self.title}>'
'''

with open(file_path, 'w') as f:
    f.write(content.strip())

# populate_forms.py - Populate app/forms.py

file_path = 'flask_blog/app/forms.py'

content = '''
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired

class CreatePostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Create')

class EditPostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Update')
'''

with open(file_path, 'w') as f:
    f.write(content.strip())

# populate_views.py - Populate app/views.py

file_path = 'flask_blog/app/views.py'

content = '''
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
'''

with open(file_path, 'w') as f:
    f.write(content.strip())

# populate_config.py - Populate config.py

file_path = 'flask_blog/config.py'

content = '''
import os

basedir = os.path.abspath(os.path.dirname(__file__))

# Database configuration
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Flask-WTF configuration
SECRET_KEY = 'your_secret_key'
'''

with open(file_path, 'w') as f:
    f.write(content.strip())

# populate_run.py - Populate run.py

file_path = 'flask_blog/run.py'

content = '''
from app import app, db

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
'''

with open(file_path, 'w') as f:
    f.write(content.strip())



# base_template.py

with open("flask_blog/app/templates/base.html", "w") as f:
    f.write("""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Flask Blog</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
</head>
<body>
    <header>
        <h1>Flask Blog</h1>
    </header>
    <nav>
        <a href="{{ url_for('home') }}">Home</a>
        <a href="{{ url_for('create_post') }}">Create Post</a>
    </nav>
    <main>
        {% block content %}
        {% endblock %}
    </main>
    <footer>
        &copy; Flask Blog 2023. All rights reserved.
    </footer>
</body>
</html>
""")

# home_template.py

with open("flask_blog/app/templates/home.html", "w") as f:
    f.write("""{% extends "base.html" %}

{% block content %}
    <h2>Recent Posts</h2>
    <ul>
        {% for post in posts %}
            <li>
                <a href="{{ url_for('view_post', post_id=post.id) }}">{{ post.title }}</a>
            </li>
        {% endfor %}
    </ul>
{% endblock %}
""")

# create_post_template.py

with open("flask_blog/app/templates/create_post.html", "w") as f:
    f.write("""{% extends "base.html" %}

{% block content %}
    <h2>Create Post</h2>
    <form method="post">
        {{ form.csrf_token }}
        <p>{{ form.title.label }}<br>{{ form.title(size=30) }}</p>
        <p>{{ form.content.label }}<br>{{ form.content(cols=50, rows=10) }}</p>
        <p>{{ form.submit() }}</p>
    </form>
{% endblock %}
""")

# edit_post_template.py

with open("flask_blog/app/templates/edit_post.html", "w") as f:
    f.write("""{% extends "base.html" %}

{% block content %}
    <h2>Edit Post</h2>
    <form method="post">
        {{ form.csrf_token }}
        <p>{{ form.title.label }}<br>{{ form.title(size=30) }}</p>
        <p>{{ form.content.label }}<br>{{ form.content(cols=50, rows=10) }}</p>
        <p>{{ form.submit() }}</p>
    </form>
{% endblock %}
""")

# populate_view_post_html - Populate view_post.html

file_path = 'flask_blog/app/templates/view_post.html'

content = '''
{% extends "base.html" %}

{% block content %}
    <h1>{{ post.title }}</h1>
    <p>{{ post.content }}</p>
    <p><small>{{ post.timestamp.strftime('%Y-%m-%d %H:%M') }}</small></p>
    <a href="{{ url_for('edit_post', post_id=post.id) }}" class="edit-button">Edit</a>
    <form action="{{ url_for('delete_post', post_id=post.id) }}" method="post" class="delete-form">
        <input type="submit" value="Delete" class="delete-button">
    </form>
{% endblock %}
'''

with open(file_path, 'w') as f:
    f.write(content.strip())



# style_css.py

with open("flask_blog/app/static/css/style.css", "w") as f:
    f.write("""/* Add your CSS rules here */
body {
    font-family: Arial, sans-serif;
    margin: 0;
    padding: 0;
}

header {
    background-color: #f8f9fa;
    padding: 20px;
}

nav {
    padding: 20px;
}

nav a {
    color: #007bff;
    text-decoration: none;
    margin-right: 10px;
}

nav a:hover {
    text-decoration: underline;
}

main {
    padding: 20px;
}

footer {
    background-color: #f8f9fa;
    padding: 20px;
    text-align: center;
}

.edit-button,
.delete-button {
    display: inline-block;
    background-color: #007bff;
    color: white;
    padding: 5px 10px;
    margin-top: 5px;
    text-decoration: none;
    border: none;
    cursor: pointer;
}

.delete-button {
    background-color: #dc3545;
    margin-left: 5px;
}

.edit-button:hover,
.delete-button:hover {
    opacity: 0.8;
}

.delete-form {
    display: inline;
}
""")
