from datetime import datetime
from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = '49766a12c794824c8fccdf75b5a71f77'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"

posts = [
	{
		'author': 'Chris Lwin',
		'title': 'Self Discipline',
		'content': 'The master key to lasting success is self discipline.',
		'date_posted': 'April 20, 2019'
	},
	{
		'author': 'John Doe',
		'title': 'My Awesome Article',
		'content': 'Lorem ipsum dolor sit amet consectetur adipisicing elit. In voluptatem at deserunt ducimus explicabo dignissimos quo ipsa! Eius sit fuga, nisi dolore id vero a, ex eaque libero, inventore explicabo.',
		'date_posted': 'June 11, 2018'
	}
]

@app.route("/")
@app.route("/home")
def home():
    return render_template('posts.html', posts=posts)

@app.route("/about")
def about():
	return render_template('about.html', title='About')

@app.route("/register", methods=['GET', 'POST'])
def register():
	form = RegistrationForm()
	if form.validate_on_submit():
		flash(f'Account has been created for {form.username.data}.', 'success')
		return redirect(url_for('home'))
	return render_template('register.html', title='register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		if form.email.data == 'admin@myblog.com' and form.password.data == 'pass':
			flash('Welcome back!', 'success')
			return redirect(url_for('home'))
		else:
			flash('Incorrect username/password.', 'danger')
	return render_template('login.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)