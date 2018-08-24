from flask import Flask, request
import os, jinja2

templates_dir = os.path.join(os.path.dirname(__file__),'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(templates_dir), autoescape=True)

app = Flask(__name__)
app.config['DEBUG'] = True

@app.route("/")
def index():
	template = jinja_env.get_template('index.html')
	return template.render()

@app.route("/welcome", methods=['POST'])
def welcome():
	form_username = request.form['username']
	template = jinja_env.get_template('welcome.html')
	return template.render(username=form_username)

if __name__ == '__main__':
    app.run()