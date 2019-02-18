from flask import Flask, request, render_template, session, redirect, url_for, escape
import erppeek
from unidecode import unidecode

# Config Odoo server 
DATABASE='tms_2112' 
SERVER='https://cuongpv:Darkness1996@tms80-integration.trobz.com'
USERNAME='admin'
PASSWORD='songonight'
domain='trobz.com' #use for genete email address

# Config for Webserver
app = Flask(__name__)
app.secret_key = 'b3zLyNfTgwMERvUg' #Random string for generate session

# Define for all url of application
@app.route('/')
def index():
    if is_user_session_exist():
        return redirect(url_for('dashboard'))
    else:
        return redirect(url_for('login'))

# Login form - verify by Slack
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        return slack_login_verify(request.form['slack_email'], request.form['slack_password'])
    else:
        return render_template('login.html')

# Dashboards features show
@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    client=erppeek.Client(SERVER, DATABASE, USERNAME,PASSWORD)
    data = { 
        'total_users': client.model('res.users').count(),
    }
    
    if request.method == 'POST' and \
       request.form['generate_user_information']:
       return render_template('generate_user_information.html')
       
    return render_template('dashboard.html', data=data)
    


# List functions library
@app.route('/generate_user_information', methods=['POST'])
def generate_user_information():
    if is_user_session_exist():
        data = cover_fullname_to_username(request.form['fullname'])
        print(data)
        return render_template('generate_user_information.html', data=data)
    else:
        return redirect(url_for('login'))

@app.route('/tms_add_user', methods=['POST'])
def tms_add_user():
    data = ''
    return data

@app.route('/logout')
def logout():
    session.pop('slack_username', None)
    return redirect(url_for('index'))

# List functions library
## Cover fullname to username
def cover_fullname_to_username(fullname):
    materials = split(fullname, ' ')
    firstname = materials[count(materials) -1]
    # last name
    raw_lastname = materials.pop(count(materials-1))
    lastname = ' '.join(raw_lastname)
    # username 
    username = ''.join(unidecode(firstname + lastname)).lower()
    email = username + "@" + domain
    data = { 'firstname': firstname,
        'lastname': lastname,
        'username': username,
        'email': email }
    return data

## Function login by slack account
def slack_login_verify(slack_email, slack_password):
    if True:
        # Set session and dashboard redirect
        return redirect(url_for('dashboard'))
    else:
        return redirect(url_for('login'))

def is_user_session_exist():
    if 'slack_email' in session:
        return True
    else:
        return False