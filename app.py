from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, length
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)
app.config['SECRET_KEY'] = 'LATTER'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/abdalrhmn/PycharmProjects/finalProject/databes.db'
Bootstrap(app)
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    password = db.Column(db.String(6), unique=True)





class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), length(min=3, max=15)])
    password = PasswordField('password', validators=[InputRequired(), length(min=3, max=6)])

class RegisterForm(FlaskForm):
    username = StringField('user Name', validators=[InputRequired(), length(min=3, max=15)])
    password = PasswordField('Password', validators=[InputRequired(), length(min=3, max=6)])


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login',methods=['GET','POST'])
def login():
    form =LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if user.password == form.password.data:
                return redirect(url_for('dashboard'))
        return '<h1>invaled inuser or passwor </h1>'



        #return '<h1> Hello (' + form.username.data + ' ) and your pass (' + form.password.data + ' )</h1>'

    return render_template('login.html', form=form)

@app.route('/signup',methods=['GET','POST'])
def signup():
    form = RegisterForm()
    if form.validate_on_submit():
        new_user = User(username=form.username.data, password=form.password.data)
        db.session.add(new_user)
        db.session.commit()

        return '<h1>New user created!</h1>'


        #return '<h1> Hello (' + form.username.data + ' ) and your pass (' + form.password.data + ' )</h1>'

    return render_template('signup.html', form=form)

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

if __name__ == '__main__':
    app.run(debug=True)