FEATURES:
* Collecting mac address of phone and laptop devices in internal network
* Checking amanda and barman backups
* Monitoring network and users connection
* Check TMS variables of node, hosts and instances
* Send requests http authentication and SSH to sysadmin
* Create account such as slack, google and gitlab for new-commer
* Revoking accounts such as slack, google and gitlab for leave user

INSTALLATION
Requirement:
* Internal tools:
- trobz package
- anhoi package

* Python tools
- flask
- requests

Development:
export FLASK_ENV=development
export FLASK_APP=trobzoi.py

flask run
or
python -m flask run

Production:
export FLASK_APP=trobzoi.py

flask run
or
python -m flask run

=> localhost:5000

HOW IT WORKS

Ourside: 
- Nginx
- Let's Encrypt

Reverse Proxy port 5000 to 443 for https

Inside:
* Front-end
- Semantic UI
- Datatables 
- HTML, CSS, Javascript

* Back-end
- python
- Slack API
- Anhoi and Trobz packages.

* Databases
- text files as a tables.

