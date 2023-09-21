from flask import Blueprint, render_template, request, flash, jsonify, redirect, session, url_for
from flask_login import login_required, current_user
from .models import Note, User, DarkMode
views = Blueprint('views' , __name__)
from . import db
import json


@views.route('/', methods=['GET'])
@login_required
def home():
    dark=False
    if current_user.is_authenticated:
        print(current_user.id)
        try:
            result = db.session.execute(db.select(DarkMode).filter_by(user_id=current_user.id)).scalar_one()
            print(result.darkModeEnabled)
        except Exception as e:
            new_darkmode = DarkMode(user_id=current_user.id)
            db.session.add(new_darkmode)
            db.session.commit()
            result = new_darkmode
        finally:
            dark=result.darkModeEnabled

    return render_template("home.html", user=current_user, user_name=current_user.username, dark=dark)

#add note logic
@views.route('/', methods=['POST'])
@login_required
def send_form():
    if request.method == 'POST':
        note = request.form.get('note')
        if len(note) < 1:
            flash('Note is too short', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note is added', category='success')
    return redirect(url_for('views.home'))


#delete note logic
@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
    return jsonify({})


@login_required
@views.route('/submitNote', methods=['GET'])
def load_submitNote():
    dark=False
    if current_user.is_authenticated:
        try:
            result = db.session.execute(db.select(DarkMode).filter_by(user_id=current_user.id)).scalar_one()
            print(result.darkModeEnabled)
        except Exception as e:
            new_darkmode = DarkMode(user_id=current_user.id)
            db.session.add(new_darkmode)
            db.session.commit()
            result = new_darkmode
        finally:
            dark=result.darkModeEnabled
    return render_template("submitNote.html", user=current_user, user_name=current_user.username, dark=dark)

@views.route('/darkmode', methods=['GET'])
def darkModeSwitch():
    if current_user.is_authenticated:
        try:
            result = db.session.execute(db.select(DarkMode).filter_by(user_id=current_user.id)).scalar_one()
            result.darkModeEnabled = not result.darkModeEnabled
            db.session.commit()
            return redirect(url_for('views.home'))
        except Exception as e:
            print("Error")
            