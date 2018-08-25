from flask import Flask , request , redirect , render_template
import re , cgi , os , jinja2

templates_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(templates_dir), autoescape = True)

app = Flask(__name__)
#app.config['DEBUG'] = True

#route and handler of the original form
@app.route('/', methods = ['GET'])
def index():
    return render_template('index.html')

@app.route('/user_signup', methods = ['POST'] )
def validate_form():
	template = ''
	username = request.form['username']
	password = request.form['password']
	verify_password = request.form['verify-password']
	email = request.form['user-email']

	error_username = ''
	error_password = ''
	error_verify_password = ''
	error_email = ''

	if username == '':
		error_username = 'Missing username'

	if not re.match(r'^(?=.*[a-z])', password):
		error_password += 'Need lowercase letter'
	if not re.match(r'^(?=.*[A-Z])', password):
		error_password += '  |  Need uppercase letter'
	if not re.match(r'^(?=.*[0-9])', password):
		error_password += '  |  Need a number'
	if not re.match(r'^(?=.*[^A-z0-9])', password):
		error_password += '  |  Need special character'
	if not re.match(r'^(?=.{8,})', password):
		error_password += '  |  Need at least 8 characters'

	if verify_password != password:
		error_verify_password = 'Password verification failed'

	if (email) and ( not re.match(r'^(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)', email) ):
		error_email = 'Invalid email'

	if (error_username != '') or (error_password != '') or (error_verify_password != '') or (error_email != ''):
		template = render_template(
			'index.html',
			error_username = error_username,
			error_password = error_password,
			error_verify_password = error_verify_password,
			error_email = error_email,
			username = username,
			email = email
		)
	else:
		template = render_template(
			'/welcome.html',
			username = username,
			email = email
		)

	return template

if __name__ == '__main__':
	#app.run(host='0.0.0.0', debug=True) # Run with this in VirtualBox <-> Vagrant
	app.run(debug=True) # Run with this in AWS
