import os
from flask import Blueprint, render_template, redirect, url_for, flash, current_app, request
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from app import db
from app.models import Complaint
from app.forms import ComplaintForm

complaints = Blueprint('complaints', __name__, url_prefix='/complaints')
@complaints.before_request
@login_required
def block_driver():
    if current_user.role == 'driver':
        flash('Drivers may only use their dashboard.', 'warning')
        return redirect(url_for('driver.list_pickups'))


@complaints.route('/', methods=['GET', 'POST'])
@login_required
def list_complaints():
    form = ComplaintForm()
    if form.validate_on_submit():
        
        # Prevent duplicate complaints for the same location
        existing = Complaint.query.filter_by(
            user_id=current_user.id,
            location=form.location.data
        ).first()
        if existing:
            flash(
                'You have already submitted a complaint for this location. '
                'Please wait for resolution before filing a new one.',
                'warning'
            )
            return redirect(url_for('complaints.list_complaints'))

        # Save the uploaded photo
        photo = form.photo.data
        filename = secure_filename(photo.filename)
        upload_path = os.path.join(current_app.root_path, 'static', 'uploads', filename)
        photo.save(upload_path)

        # Create and save complaint
        new_complaint = Complaint(
            user_id=current_user.id,
            description=form.description.data,
            photo_path=f'uploads/{filename}',
            location=form.location.data
        )
        db.session.add(new_complaint)
        db.session.commit()

        flash('Complaint submitted successfully!', 'success')
        return redirect(url_for('complaints.list_complaints'))

    # Fetch existing complaints for display
    user_complaints = Complaint.query.filter_by(user_id=current_user.id).all()
    return render_template('complaint_form.html', form=form, complaints=user_complaints)
