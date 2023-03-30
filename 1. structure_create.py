import os

# Create directories
dirs = [
    'flask_blog/app/static/css',
    'flask_blog/app/templates'
]

for d in dirs:
    os.makedirs(d, exist_ok=True)

# Create files
files = {
    'flask_blog/app/__init__.py': '',
    'flask_blog/app/models.py': '',
    'flask_blog/app/forms.py': '',
    'flask_blog/app/views.py': '',
    'flask_blog/app/static/css/style.css': '',
    'flask_blog/app/templates/base.html': '',
    'flask_blog/app/templates/create_post.html': '',
    'flask_blog/app/templates/edit_post.html': '',
    'flask_blog/app/templates/home.html': '',
    'flask_blog/app/templates/view_post.html': '',
    'flask_blog/config.py': '',
    'flask_blog/run.py': '',
    'flask_blog/requirements.txt': 'flask\nflask-sqlalchemy\nflask-wtf\n'
}

for file, content in files.items():
    with open(file, 'w') as f:
        f.write(content)

print("Flask project structure created.")
