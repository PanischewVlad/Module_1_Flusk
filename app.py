from flask import Flask, render_template, flash, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField
from wtforms.validators import DataRequired, NumberRange, ValidationError

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def validate_integer(form, field):
    if field.data % 1 != 0:
        raise ValidationError("Please enter an integer.")

class YearForm(FlaskForm):
    year = IntegerField('Enter a year:', validators=[
        DataRequired(message="Field cannot be empty."),
        NumberRange(min=0, message="Year must be a positive integer."),
        validate_integer
    ])
    submit = SubmitField('Check Leap Year')

def is_leap_year(year):
    if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
        return True
    return False

@app.route('/', methods=['GET', 'POST'])
def home():
    form = YearForm()
    if form.validate_on_submit():
        year = form.year.data
        if is_leap_year(year):
            flash(f"{year} is a leap year!", "success")
            image = 'leap_year.png'
        else:
            flash(f"{year} is not a leap year.", "danger")
            image = 'non_leap_year.png'
        return render_template('result.html', year=year, image=image)
    return render_template('home.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)
