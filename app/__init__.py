from flask import Flask, flash, request, g, redirect, url_for, session
import os
group_for_annotation = "default"

app = Flask(__name__, instance_relative_config=True)
app.config.from_mapping(
    ENV='development',
    SECRET_KEY=os.urandom(16),
    DATABASE=os.path.join(app.instance_path, 'app.sqlite'),
)

# if test_config is None:
#     # load the instance config, if it exists, when not testing
#     app.config.from_pyfile('config.py', silent=True)
# else:
#     # load the test config if passed in
#     app.config.from_mapping(test_config)

try:
    os.makedirs(app.instance_path)
except OSError:
    pass

from . import db
db.init_app(app)

from app.commands import push_images
push_images.init_images(app)

from app.commands import set_group
set_group.set_group(app)

from . import auth
app.register_blueprint(auth.bp)

from . import rating
app.register_blueprint(rating.bp)
app.add_url_rule('/', endpoint='home')

from . import upload
app.register_blueprint(upload.bp)

def generate_csrf_token():
    if '_csrf_token' not in session:
        session['_csrf_token'] = os.urandom(16)
    return session['_csrf_token']

app.jinja_env.globals['csrf_token'] = generate_csrf_token


