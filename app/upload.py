from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, send_from_directory
)
from werkzeug.exceptions import abort

from app.auth import login_required
from app.db import get_db
from werkzeug.utils import secure_filename
import os

bp = Blueprint('upload', __name__)
ALLOWED_EXTENSIONS = set(['jpg', 'jpeg'])
UPLOAD_FOLDER = 'C:/Users/Administrator/Documents/GitHub/pero/app/static/images/'

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route('/upload/image', methods=['GET', 'POST'])
@login_required
def upload():
    if request.method == 'POST':
        if 'file[]' not in request.files:
            flash('No file part')
            return redirect(request.url)
        files = request.files.getlist("file[]")

        if not request.form['group']:
            flash('You have to add group name')
            return redirect(request.url)

        group = request.form['group']
        # if user does not sele ct file, browser also
        # submit an empty part without filename
        if len(files) < 6:
            flash('You have to include atleast 6 images')
            return redirect(request.url)
        for file in files:
            if not file:
                flash('Did not select any file.')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                
                file.save(os.path.join(UPLOAD_FOLDER, filename))

                db = get_db()

                db.execute(
                    'INSERT INTO images (image_url, group_status) VALUES (?, ?)',
                    ("images/" + filename, group)
                )
                db.commit()
            else:
                flash('Wrong file type.')
        flash("Successfully added images.")
    
    
    return render_template('upload/upload.html')


@bp.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER,
                               filename)