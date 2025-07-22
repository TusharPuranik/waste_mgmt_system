from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models import User
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import TextAreaField
from wtforms import StringField
from wtforms.validators import DataRequired, Length
from wtforms import SelectField
from wtforms.validators import DataRequired


from wtforms import SelectField, DateField
from wtforms.validators import DataRequired

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=50)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone', validators=[DataRequired(), Length(min=10, max=20)])
    role = SelectField(
    'I am a',
    choices=[
        ('user', 'Regular User'),
        ('driver', 'Driver')
    ],
    default='user',
    validators=[DataRequired()]
)
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is already registered.')

    def validate_phone(self, phone):
        user = User.query.filter_by(phone=phone.data).first()
        if user:
            raise ValidationError('That phone number is already registered.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class PickupForm(FlaskForm):
    pin_code = StringField('PIN Code', validators=[DataRequired(), Length(min=4, max=10)])
    waste_type = SelectField(
        'Waste Type',
        choices=[
            ('organic', 'Organic'),
            ('recyclable', 'Recyclable'),
            ('hazardous', 'Hazardous'),
            ('mixed', 'Mixed'),
        ],
        validators=[DataRequired()]
    )
    pickup_date = DateField('Pickup Date', format='%Y-%m-%d', validators=[DataRequired()])
    time_slot = SelectField(
        'Time Slot',
        choices=[
            ('9-11', '09:00 AM – 11:00 AM'),
            ('11-1', '11:00 AM – 01:00 PM'),
            ('1-3', '01:00 PM – 03:00 PM'),
            ('3-5', '03:00 PM – 05:00 PM'),
        ],
        validators=[DataRequired()]
    )
    submit = SubmitField('Request Pickup')

class ComplaintForm(FlaskForm):
    description = TextAreaField(
        'Description',
        validators=[DataRequired(), Length(min=10, max=500)]
    )
    photo = FileField(
        'Photo (JPEG/PNG)',
        validators=[
            FileRequired(),
            FileAllowed(['jpg', 'jpeg', 'png'], 'Images only!')
        ]
    )
    location = StringField(
        'Location',
        validators=[DataRequired(), Length(min=5, max=100)]
    )
    submit = SubmitField('Submit Complaint')
