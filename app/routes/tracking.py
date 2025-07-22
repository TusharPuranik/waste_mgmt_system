from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import Pickup

tracking_bp = Blueprint('tracking', __name__, url_prefix='/tracking')

@tracking_bp.before_request
@login_required
def block_driver():
    if current_user.role == 'driver':
        flash('Drivers may only use their dashboard.', 'warning')
        return redirect(url_for('driver.list_pickups'))

@tracking_bp.route('/', methods=['GET'])
def track_home():
    # Fetch only this user's pickups, newest first
    pickups = (
        Pickup.query
              .filter_by(user_id=current_user.id)
              .order_by(Pickup.pickup_date.desc())
              .all()
    )
    return render_template('tracking.html', pickups=pickups)
