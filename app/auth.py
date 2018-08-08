import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from app.db import get_db

from passlib.hash import sha256_crypt


# A Blueprint is a way to organize a group of related views 
# and other code. Rather than registering views and other 
# code directly with an application, they are registered 
# with a blueprint. Then the blueprint is registered with 
# the application when it is available in the factory function.
bp = Blueprint('auth', __name__, url_prefix='/auth')


# bp.before_app_request() registers a function that runs 
# before the view function, no matter what URL is requested. 
# load_logged_in_user checks if a user id is stored in the session 
# and gets that user’s data from the database
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            flash("Insufficient permissions.")
            return redirect(url_for('auth.login'))

        return view(**kwargs)
    return wrapped_view

def admin_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            flash("Insufficient permissions.")
            return redirect(url_for('auth.login'))
        else:
            if g.user['role'] != 'admin':
                flash("Insufficient permissions.")
                return redirect(url_for('home'))

        return view(**kwargs)
    return wrapped_view


# @bp.route associates the URL /register with the register view
# function. When Flask receives a request to /auth/register, 
# it will call the register view and use the return value 
# as the response.
@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        username = request.form['username']
        password = request.form['password']
        city = request.form['city']
        state = request.form['state']
        zip_code = request.form['zip']

        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif not firstname:
            error = 'Firstname is required.'
        elif not lastname:
            error = 'Lastname is required.'
        elif not city:
            error = 'City is required.'
        elif not state:
            error = 'State is required.'
        elif not zip_code:
            error = 'Zip code is required.'
        

        # ? placeholders for any user input, and a tuple of values to 
        # replace the placeholders with.
        elif db.execute(
            'SELECT id FROM user WHERE username = ?', (username,)
        ).fetchone() is not None:
            error = 'User {} is already registered.'.format(username)
        # fetchone() returns one row from the query. If the query returned 
        # no results, it returns None. Later, fetchall() is used, which 
        # returns a list of all results.


        if error is None:
            db.execute(
                'INSERT INTO user (username, password, first_name, second_name, city, state, zip, role) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                (username, sha256_crypt.encrypt(password), firstname, lastname, city, state, zip_code, 'user')
            )
            db.commit()
            return redirect(url_for('auth.login'))

        flash(error)

    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        try:
            if not sha256_crypt.verify(password, user['password']):
                error = 'Incorrect password3.'
        except:
            error = 'Incorrect password2.'
        

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('home'))
            # session is a dict that stores data across requests. 
            # When validation succeeds, the user’s id is stored in a 
            # new session. The data is stored in a cookie that is sent 
            # to the browser, and the browser then sends it back with 
            # subsequent requests. Flask securely signs the data so that 
            # it can’t be tampered with.

        flash(error)

    return render_template('auth/login.html')


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))
