from flask import Blueprint, render_template
from flask_login import login_required, current_user
from flask import redirect, url_for, flash


dashboard = Blueprint('dashboard', __name__)
@dashboard.before_request
@login_required
def block_driver():
    if current_user.role == 'driver':
        flash('Drivers may only use their dashboard.', 'warning')
        return redirect(url_for('driver.list_pickups'))


@dashboard.route('/')
@login_required
def home():
    # Render the dashboard.html template
    return render_template('dashboard.html')
