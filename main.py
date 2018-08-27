from flask import Flask , request , redirect , render_template
import re , cgi , os , jinja2

templates_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(templates_dir), autoescape = True)

app = Flask(__name__)
app.config['DEBUG'] = True

#route and handler of the original form
@app.route('/', methods = ['GET','POST'])
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
		error_username = ' [ Missing ] '
	if not re.match(r'^(?=.{3,20}$)', username):
		error_username = ' [ Need 3 to 20 characters ] '
	if re.match(r'^(?=.*[A-z0-9] ?)', username):
		error_username = ' [ No spaces allowed ] '

	if not re.match(r'^(?=.*[a-z])', password):
		error_password += ' [ Need lowercase letter ] \n'
	if not re.match(r'^(?=.*[A-Z])', password):
		error_password += ' [ Need uppercase letter ] \n'
	if not re.match(r'^(?=.*[0-9])', password):
		error_password += ' [ Need a number ] \n'
	if not re.match(r'^(?=.*[^A-z0-9])', password):
		error_password += ' [ Need special character ] \n'
	if not re.match(r'^(?=.{8,20}$)', password):
		error_password += ' [ Need 8 to 20 characters ] \n'

	if verify_password != password:
		error_verify_password = ' [ Password verification failed ] '

	if (email) and ( not re.match(r'^(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)', email) ):
		error_email = ' [ Invalid email ] '

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
	app.run(host='0.0.0.0', debug=True)
