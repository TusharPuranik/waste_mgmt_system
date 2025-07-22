from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import Pickup
from app import db

driver_bp = Blueprint('driver', __name__, url_prefix='/driver')

@driver_bp.before_request
@login_required
def ensure_driver():
    # Only users with role 'driver' can access these routes
    if current_user.role != 'driver':
        flash('Access denied: Drivers only.', 'danger')
        return redirect(url_for('dashboard.home'))

@driver_bp.route('/')
def list_pickups():
    # List all pickups assigned to this driver
    pickups = Pickup.query.filter_by(driver_id=current_user.id)\
                         .order_by(Pickup.pickup_date, Pickup.time_slot)\
                         .all()
    return render_template('driver_pickups.html', pickups=pickups)

@driver_bp.route('/update/<int:pickup_id>/<status>')
def update_pickup(pickup_id, status):
    # Allow the driver to update the status of their assigned pickup
    p = Pickup.query.get_or_404(pickup_id)
    if p.driver_id != current_user.id:
        flash('Unauthorized action.', 'danger')
        return redirect(url_for('driver.list_pickups'))

    # Only allow certain status transitions
    valid_statuses = ['On the Way', 'Arrived', 'Completed']
    if status not in valid_statuses:
        flash('Invalid status.', 'warning')
        return redirect(url_for('driver.list_pickups'))

    p.status = status
    db.session.commit()
    flash(f'Pickup {pickup_id} status updated to "{status}".', 'success')
    return redirect(url_for('driver.list_pickups'))
