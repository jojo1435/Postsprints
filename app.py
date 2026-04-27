from flask import Flask
from dotenv import load_dotenv

from source.services.mailtrap import mail
from source.utils.db import db
from source.utils.login import login_manager

load_dotenv(".env.debug")

app = Flask(__name__, 
        static_url_path="",
        template_folder="source/templates", 
        static_folder="source/static")
app.config.from_object("config")

db.init_app(app)
login_manager.init_app(app)
mail.init_app(app)

from source.views.main import main
from source.views.auth import auth
from source.views.dashboard import dashboard
from source.utils.jinja import jinja_bp

app.register_blueprint(jinja_bp)
app.register_blueprint(main)
app.register_blueprint(auth)
app.register_blueprint(dashboard)