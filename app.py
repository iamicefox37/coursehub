from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm
app = Flask(__name__)

app.config['SECRET_KEY'] = '49766a12c794824c8fccdf75b5a71f77'
#git
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
	return render_template('login.html', form=form)

if __name__ == "__main__":
    app.run(debug=True)