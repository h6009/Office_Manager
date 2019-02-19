from flask import Flask, request, render_template, session, redirect, url_for, escape
import erppeek, random, string
from unidecode import unidecode

# Config Odoo server 
DATABASE='tms_2112' 
SERVER='https://cuongpv:Darkness1996@tms80-integration.trobz.com'
USERNAME='admin'
PASSWORD='songonight'
domain='trobz.com' #use for generate email address

# Config for Webserver
app = Flask(__name__)
app.secret_key = 'b3zLyNfTgwMERvUg' #Random string for generate session
client=erppeek.Client(SERVER, DATABASE, USERNAME,PASSWORD)

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
    if not is_user_session_exist():
        return redirect(url_for('login'))
    data = { 
        'total_users': client.model('res.users').count(),
    }
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
    # show fields
    print(client.model('res.users').keys())
    data = {}
    # get partner_id if exist or create an account
    if len(client.model('res.partner').browse(['email =' + request.form['email']]).id) == 1:
        data['create_odoo_partner'] = "Partner has already exist, ignore this step."
        data['partner_id'] = client.model('res.partner').browse(['email =' + request.form['email']]).id
    else:
        data['create_odoo_partner'] = "Look like email partner doesn't exist, created!"
        # Let's create partner
        data['partner_id'] = client.model('res.partner').create({
            'email': request.form['email'],
            'name': request.form['fullname'],
            'parent_id': 1
        }).id

    # Create user for login TMS
    print(data['partner_id'][0])
    client.model('res.users').create({
        'employer_id': 1, # equal 1 - mean trobz partner (company)
        'partner_id': data['partner_id'][0],
        'email': request.form['email'],
        'login': request.form['username'],
        'new_password': request.form['password'],
        'daily_hour': 8,
        'must_input_working_hour': True,
        'group_profile_id': 53, #53: fc | dev: 55
    })
    return "User has created! "

@app.route('/logout')
def logout():
    session.pop('slack_username', None)
    return redirect(url_for('index'))

# List functions library
## Cover fullname to username
def cover_fullname_to_username(fullname):
    tmp = unidecode(fullname).split(' ')
    # username 
    username = tmp[-1].lower() + ''.join([i[0] for i in tmp[:-1]]).lower()
    # email
    email = username + "@" + domain
    # fullname
    raw_fullname = fullname.split()
    #example: Phan Văn Cường => Cường (Phan Văn)
    fullname_rule = raw_fullname[-1] + ' ' + '(' + ' '.join(raw_fullname[:-1]) + ')'
    data = { 'username': username,
        'email': email,
        'fullname': fullname_rule,
        'password': randomString(12),
        'http_auth': username,
        'http_pass': randomString(12),}
    return data

## Function login by slack account
def slack_login_verify(slack_email, slack_password):
    if True:
        # Set session and dashboard redirect
        session['slack_email'] = slack_email
        return redirect(url_for('dashboard'))
    else:
        return redirect(url_for('login'))

def randomString(stringLength):
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(stringLength))


def is_user_session_exist():
    if 'slack_email' in session:
        return True
    else:
        return False