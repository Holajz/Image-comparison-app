import os
import re

import flask
from flask import (Blueprint, current_app, flash, g, redirect, render_template,
                   request, session, url_for)
from flask.cli import with_appcontext
from werkzeug.exceptions import abort

from app.auth import login_required
from app.db import get_db

bp = Blueprint('rating', __name__)


@bp.before_request
def csrf_protect():
    if request.method == "POST":
        token = str(session.get('_csrf_token', None))

        form_token = request.form.get('_csrf_token')

        if not token or token != form_token:
            abort(403)


# @bp.after_request
# def make_nav_active():
#     pass


def select_images():
    db = get_db()

    current_group = db.execute(
        'SELECT * FROM current_group'
    )

    curr_group = None
    for group in current_group:
        curr_group = group['current_group_name']


    images = db.execute(
        'SELECT DISTINCT *'
        ' FROM images'
        ' WHERE images.group_status = ?'
        ' ORDER BY RANDOM()'
        ' LIMIT 6',
        (curr_group, )
    )
    return images


@bp.route('/sortable1', methods=['GET'])
@login_required
def sortable1():
    return render_template('rating/sortable.html', images=select_images())


@bp.route('/sortable1', methods=['POST'])
@login_required
def sortable11():
    if not request.form['ratings']:
        flash("Error while selecting images.")
        return redirect(url_for('rating.sortable1'))

    ratings = request.form['ratings']
    int_ratings = [int(i) for i in ratings.split()]

    if not len(int_ratings) == 6:
        flash("Error while posting images.")
        return redirect(url_for('rating.sortable1'))

    db = get_db()
    message = None

    db.execute(
        'INSERT INTO rating (rated_first, rated_second, rated_third, rated_forth, rated_fifth, rated_sixth, author_id) VALUES (?, ?, ?, ?, ?, ?, ?)',
        (int_ratings[0], int_ratings[1], int_ratings[2], int_ratings[3], int_ratings[4], int_ratings[5], g.user['id'])
    )
    db.commit()

    return redirect(url_for('rating.sortable1'))




@bp.route("/sortable2", methods=['GET'])
@login_required
def sortable2():
    return render_template("rating/sortable2.html", images=select_images())


@bp.route("/sortable2", methods=['POST'])
@login_required
def sortable22():
    if not request.form['ratings']:
        flash("Error while selecting images.")
        return redirect(url_for('rating.sortable2'))

    ratings = request.form['ratings']
    int_ratings = [int(i) for i in ratings.split()]

    if not len(int_ratings) == 2:
        flash("Error while posting images.")
        return redirect(url_for('rating.sortable2'))

    db = get_db()
    message = None

    db.execute(
        'INSERT INTO selection (rated_first, rated_second, author_id) VALUES (?, ?, ?)',
        (int_ratings[0], int_ratings[1], g.user['id'])
    )
    db.commit()

    return redirect(url_for('rating.sortable2'))


@bp.route("/sortable3", methods=['GET'])
@login_required
def sortable3():
    return render_template("rating/sortable3.html", images=select_images())



@bp.route("/sortable3", methods=['POST'])
@login_required
def sortable33():
    if request.form['ratings'] and request.form['type']:
        if request.form['type'] == 'sortable':
            ratings = request.form['ratings']
            int_ratings = [int(i) for i in ratings.split()]

            db = get_db()
            message = None

            db.execute(
                'INSERT INTO rating (rated_first, rated_second, rated_third, rated_forth, rated_fifth, rated_sixth, author_id) VALUES (?, ?, ?, ?, ?, ?, ?)',
                (int_ratings[0], int_ratings[1], int_ratings[2], int_ratings[3], int_ratings[4], int_ratings[5], g.user['id'])
            )
            db.commit()
            # last_id = db.last_insert_rowid()

            return redirect(url_for('rating.sortable3'))
        elif request.form['type'] == 'select':
            ratings = request.form['ratings']
            int_ratings = [int(i) for i in ratings.split()]

            db = get_db()
            message = None

            db.execute(
                'INSERT INTO selection (rated_first, rated_second, author_id) VALUES (?, ?, ?)',
                (int_ratings[0], int_ratings[1], g.user['id'])
            )
            db.commit()

            return redirect(url_for('rating.sortable3'))
        else:
            ratings = request.form['ratings']
            int_ratings = [int(i) for i in ratings.split()]
            amount = request.form['amount']

            db = get_db()
            message = None

            db.execute(
                'INSERT INTO amount (image_rated, rating, author_id) VALUES (?, ?, ?)',
                (int_ratings[0], amount, g.user['id'])
            )
            db.commit()

            return redirect(url_for('rating.sortable3'))
    
    flash("Error while selecting images.")
    return redirect(url_for('rating.sortable3'))


@bp.route("/sortable4", methods=['GET'])
@login_required
def sortable4():
    return render_template("rating/sortable4.html", images=select_images())


@bp.route("/sortable4", methods=['POST'])
@login_required
def sortable44():
    if not request.form['ratings']:
        flash("Error while selecting images.")
        return redirect(url_for('rating.sortable4'))

    ratings = request.form['ratings']
    int_ratings = [int(i) for i in ratings.split()]
    amount = request.form['amount']

    db = get_db()
    message = None

    db.execute(
        'INSERT INTO amount (image_rated, rating, author_id) VALUES (?, ?, ?)',
        (int_ratings[0], amount, g.user['id'])
    )
    db.commit()

    return redirect(url_for('rating.sortable4'))
