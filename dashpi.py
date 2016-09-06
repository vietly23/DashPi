from flask import Flask, session, redirect, request, flash, render_template, url_for
from oauth2client import client
import urllib.parse

app = Flask(__name__)
app.secret_key = '3512a68c-3b77-474f-b807-0a24d73ac98b'
app.debug = True

SCOPE = ['https://www.googleapis.com/auth/calendar.readonly',
			'https://www.googleapis.com/auth/gmail.readonly',
			]

FLOW = client.flow_from_clientsecrets('../client_secret.json', SCOPE,
		redirect_uri='http://www.192.168.0.196.xip.io:5000/oauth2callback')

@app.route('/')
def index():
	if 'google_credentials' in session:
		return 'Hello World!'
	else:
		return redirect(url_for('login'), 302)

@app.route('/login')
def login():
	auth_uri = FLOW.step1_get_authorize_url()
	return render_template('login.html', auth_uri=auth_uri) 

@app.route('/oauth2callback')
def oauth2callback():
	if request.args.get('error') == 'access_denied':
		return redirect(url_for('login'))
	else:
		auth_code = request.args.get('code')
		credentials = FLOW.step2_exchange(auth_code)
		session['google_credentials'] = credentials.to_json()
		return redirect(url_for('index'))

@app.route('/logout')
def logout():
	session.clear()
	return "session cleared" 

if __name__ == '__main__':
	pass

