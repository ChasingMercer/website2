from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, csrf
from wtforms import Form, BooleanField, StringField, PasswordField, validators, TextAreaField
from wtforms.validators import InputRequired
from flask import Flask
from wtforms.widgets import TextArea
import smtplib




app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = 'True'
db = SQLAlchemy(app)
Bootstrap(app)

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=False, nullable=False)
    email = db.Column(db.String, unique=False, nullable=False)
    company = db.Column(db.String, unique=False, nullable=False)
    note = db.Column(db.String, unique=False, nullable=False)

    def __init__(self, name, email, company, note):
        self.name = name
        self.email = email
        self.company = company
        self.note = note

    def __repr__(self):
        return f"{self.name}, {self.company},{self.note}, {self.email}"

class ContactForm(FlaskForm):
    name = StringField('Name', [validators.Length(min=4, max=20)])
    email = StringField('Email Address', [validators.Length(min=6, max=50)])
    company = StringField('Company', [InputRequired()])
    note = StringField('Note', widget=TextArea())
    submit = SubmitField('Submit')


@app.route("/")
@app.route("/home", methods=['GET', 'POST'])
def home():
    form = ContactForm()


    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        company = form.company.data
        note = form.note.data
        user = User(name, email, company, note)
        db.session.add(user)
        db.session.commit()
        message = f"Hey {name}\n Thank you for contacting Mercer Consulting." \
                  f"\n I will get back to you shortly.\n\n Felix Morgan \n"
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login("mercerconsults@gmail.com", "19Criminals")
        server.sendmail("mercerconsults@gmail.com", email, message)
        server.sendmail("mercerconsults@gmail.com", "mercerconsults@gmail.com",f"New Message alert, {name}\n\n, {email}\n"
                                                                               f", {company}\n, {note}")
        return redirect(url_for('home'))
    else:
        flash('Unsuccessful Try Again')

    return render_template("index.html", form=form)

if __name__ == "__main__":
    app.run(debug=True)
