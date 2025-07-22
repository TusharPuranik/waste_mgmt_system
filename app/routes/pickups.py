from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app.forms import PickupForm
from app import db
from app.models import Pickup
from datetime import date

# — Serviceable PIN codes (update this list as needed) —
serviceable_pin_codes = [
    '560001',
    '560002',
    '560003',
    # add more PINs here
]

# — Upcoming municipal holidays (YYYY-MM-DD) —
holidays = [
    '2025-07-15',
    '2025-08-15',
    '2025-10-02',
    # add more dates as needed
]

pickups_bp = Blueprint('pickups', __name__, url_prefix='/pickups')

@pickups_bp.before_request
@login_required
def block_driver():
    if current_user.role == 'driver':
        flash('Drivers may only use their dashboard.', 'warning')
        return redirect(url_for('driver.list_pickups'))

@pickups_bp.route('/', methods=['GET', 'POST'])
@login_required
def list_pickups():
    form = PickupForm()
    min_date = date.today().isoformat()

    if form.validate_on_submit():
        # Prevent picking a past date
        if form.pickup_date.data < date.today():
            flash('Pickup date cannot be in the past.', 'warning')
            return redirect(url_for('pickups.list_pickups'))

        # Check if service is available for this PIN code
        if form.pin_code.data not in serviceable_pin_codes:
            flash(
                'Service not available for this PIN code. '
                'Please choose a different area or contact support.',
                'warning'
            )
            return redirect(url_for('pickups.list_pickups'))

        # Check for municipal holiday
        selected = form.pickup_date.data.isoformat()
        if selected in holidays:
            flash(
                'Scheduled pickup overlaps with a municipal holiday. '
                'Please choose a different date.',
                'warning'
            )
            return redirect(url_for('pickups.list_pickups'))

        # Prevent double-booking of the same slot
        existing_slot = Pickup.query.filter_by(
            pin_code=form.pin_code.data,
            pickup_date=form.pickup_date.data,
            time_slot=form.time_slot.data
        ).first()
        if existing_slot:
            flash(
                'That time slot is already booked for your area. '
                'Please choose a different slot.',
                'warning'
            )
            return redirect(url_for('pickups.list_pickups'))

        # Create and save the pickup request
        new_pickup = Pickup(
            user_id=current_user.id,
            pin_code=form.pin_code.data,
            waste_type=form.waste_type.data,
            pickup_date=form.pickup_date.data,
            time_slot=form.time_slot.data
        )
        db.session.add(new_pickup)
        db.session.commit()
        flash('Pickup scheduled successfully!', 'success')
        return redirect(url_for('pickups.list_pickups'))

    # Fetch current user's pickups to display
    user_pickups = Pickup.query.filter_by(user_id=current_user.id).all()
    return render_template(
        'pickup_form.html',
        form=form,
        pickups=user_pickups,
        min_date=min_date
    )
