import re
from datetime import datetime

from flask import (Blueprint, Flask, flash, g, redirect, render_template,
                   request, session, url_for)
from werkzeug.security import check_password_hash, generate_password_hash
from flask import jsonify

from app.auth import admin_required, bp, login_required
from app.db import get_db

from . import app, auth

import json


@app.route("/", methods=['GET'])
def home():
    return render_template("home.html")

@app.route("/home", methods=['GET'])
def home_home():
    return render_template("home.html")

@app.route("/information", methods=['GET'])
def information():
    return render_template("information.html")


@app.route("/contact", methods=['GET'])
def contact():
    return render_template("contact.html")


@app.route("/api/rating/<num_of_ratings>", methods=['GET'])
@login_required
@admin_required
def get_data(num_of_ratings):
    db = get_db()
    num = str(num_of_ratings)


    ratings = db.execute(
        'SELECT *'
        ' FROM rating'
        ' WHERE id IN'
        '   (SELECT id'
        '    FROM rating'
        '    ORDER BY RANDOM()'
        '    LIMIT ?)', [num] 
    ).fetchall()

    listik = list()
    for rating in ratings:
        listik.append(list(rating))

    return jsonify(listik)
