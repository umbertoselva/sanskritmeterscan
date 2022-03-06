from flask import Flask
from flask_session import Session
from tempfile import mkdtemp # to create temp dir to store session file
import os
import json # to create config json for the secret key

# initialize app
app = Flask(__name__)

# Configure app

# Configure secret key
with open('/etc/meterscan_config.json') as config_file:
	config = json.load(config_file)
app.config['SECRET_KEY'] = config.get("SECRET_KEY")
# Configure upload folder
app.config['UPLOAD_FOLDER'] = os.path.abspath("meterscan/static/files")
# Configure allowed extensions (only .txt)
app.config["ALLOWED_EXT"] = ["TXT"]
# Configure max filesize (2MB)
app.config["MAX_FILESIZE"] = 2 * 1024 * 1024

# Ensure templates are auto-reloaded
# app.jinja_env.auto_reload = True
app.config["TEMPLATES_AUTO_RELOAD"] = True
# this monitors changes in all related template files. 
# And if any of template files were edited after program was loaded 
# flask will reload the program/server to represent the changes.

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()	# this makes a dir temp to save the session info into (Otherwise default to use flask_session directory under current working directory.)
app.config["SESSION_PERMANENT"] = False 	# this makes the session expire (otherwise default is True)
app.config["SESSION_TYPE"] = "filesystem"	# this saves the session info on disk (in the temp dir)
Session(app)

from meterscan import routes