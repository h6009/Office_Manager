from flask import Flask, request, render_template, session, redirect, url_for, escape
import erppeek

# Config Odoo server 
DATABASE='tms_2112'
SERVER='https://cuongpv:Darkness1996@tms80-integration.trobz.com'
USERNAME='admin'
PASSWORD='songonight'


# Config for Webserver
app = Flask(__name__)
app.secret_key = 'b3zLyNfTgwMERvUg' #Random string for generate session

# Define for all url of application
@app.route('/')
def hello_world():
    return 'Hello, World!'

# Login form - verify by Slack
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        return slack_login_verify()
    else:
        return render_template('login.html')

# Dashboards features
@app.route('/dashboard')
def dashboard():
    client=erppeek.Client(SERVER, DATABASE, USERNAME,PASSWORD)
    data = { 
        'total_users': client.model('res.users').count(),
    }
    return render_template('dashboard.html', data=data)

# List functions library

## Function login by slack account
def slack_login_verify():
    print('test')