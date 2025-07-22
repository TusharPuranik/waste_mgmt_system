from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import Pickup
from app.models import Complaint
from app import db
from sqlalchemy import func
from app.models import User
from flask import request



admin = Blueprint('admin', __name__, url_prefix='/admin')

@admin.before_request
@login_required
def ensure_admin():
    # Only allow users with role 'admin'
    if current_user.role != 'admin':
        flash('Access denied: Admins only.', 'danger')
        return redirect(url_for('dashboard.home'))

@admin.route('/pickups')
def view_pickups():
    pickups = Pickup.query.order_by(Pickup.created_at.desc()).all()
    # Fetch all drivers
    drivers = User.query.filter_by(role='driver').all()
    return render_template(
        'admin_pickups.html',
        pickups=pickups,
        drivers=drivers
    )


@admin.route('/pickups/assign/<int:pickup_id>', methods=['POST'])
def assign_pickup(pickup_id):
    driver_id = request.form.get('driver_id', type=int)
    p = Pickup.query.get_or_404(pickup_id)
    p.driver_id = driver_id if driver_id else None
    db.session.commit()
    flash(f'Pickup {pickup_id} assigned to driver {driver_id}', 'success')
    return redirect(url_for('admin.view_pickups'))

@admin.route('/update_pickup/<int:pickup_id>/<status>')
def update_pickup(pickup_id, status):
    # Update status of a pickup and redirect back
    pickup = Pickup.query.get_or_404(pickup_id)
    pickup.status = status
    db.session.commit()
    flash(f'Pickup {pickup_id} marked as {status}.', 'success')
    return redirect(url_for('admin.view_pickups'))

@admin.route('/complaints')
def view_complaints():
    # List all complaints for admin review
    complaints = Complaint.query.order_by(Complaint.created_at.desc()).all()
    return render_template('admin_complaints.html', complaints=complaints)

@admin.route('/update_complaint/<int:complaint_id>/<status>')
def update_complaint(complaint_id, status):
    # Update status of a complaint and redirect back
    complaint = Complaint.query.get_or_404(complaint_id)
    complaint.status = status
    db.session.commit()
    flash(f'Complaint {complaint_id} marked as {status}.', 'success')
    return redirect(url_for('admin.view_complaints'))

@admin.route('/reports')
def view_reports():
    # Pickups by waste type
    pickup_data = (
        db.session.query(Pickup.waste_type, func.count(Pickup.id))
        .group_by(Pickup.waste_type)
        .all()
    )
    pickup_labels = [wt for wt, _ in pickup_data]
    pickup_counts = [count for _, count in pickup_data]

    # Complaints by status
    complaint_data = (
        db.session.query(Complaint.status, func.count(Complaint.id))
        .group_by(Complaint.status)
        .all()
    )
    complaint_labels = [st for st, _ in complaint_data]
    complaint_counts = [count for _, count in complaint_data]

    return render_template(
        'admin_reports.html',
        pickup_labels=pickup_labels,
        pickup_counts=pickup_counts,
        complaint_labels=complaint_labels,
        complaint_counts=complaint_counts
    )

