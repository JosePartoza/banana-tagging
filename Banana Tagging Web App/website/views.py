from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import Note, Tag
from . import db
import json
from datetime import datetime, timedelta

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')
            return redirect(url_for('views.home'))

    return render_template("home.html", user=current_user)


@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    note_id = note['noteId']
    note = Note.query.get(note_id)

    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})


@views.route('/banana', methods=['GET', 'POST'])
@login_required
def banana():
    if request.method == 'POST':
        date_str = request.form.get('date')
        color = request.form.get('color')
        tags = request.form.get('tags')
        price = request.form.get('price')

        if date_str and color and tags and price:
            date = datetime.strptime(date_str, '%Y-%m-%d').date()  # Convert string to date object
            new_tag = Tag(date=date, color=color, tags=int(tags), price=float(price))
            new_tag.average_weight = int(tags) * 13
            new_tag.harvest_date = date + timedelta(days=120)
            new_tag.total_sales = new_tag.price * new_tag.average_weight
            db.session.add(new_tag)
            db.session.commit()
            flash('Tag added!', category='success')
            return redirect(url_for('views.banana'))
        else:
            flash('Please fill in all fields!', category='error')

    tags = Tag.query.all()  # Retrieve all tags from the database
    
    return render_template("banana.html", user=current_user, tags=tags)

@views.route('/banana/delete/<int:tag_id>', methods=['POST'])
@login_required
def delete_tag(tag_id):
    tag = Tag.query.get(tag_id)
    if tag:
        db.session.delete(tag)
        db.session.commit()
        flash('Tag deleted successfully!', category='success')
    else:
        flash('Tag not found!', category='error')
    return redirect(url_for('views.banana'))
