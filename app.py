from flask import Flask
from dotenv import load_dotenv

from source.forms.csfr import csfr
from source.services.mailtrap import mail
from source.utils.assets import hash_static_assets
from source.utils.db import db
from source.utils.login import login_manager
from source.utils.processors import inject_asset_version

load_dotenv(".env.debug")

app = Flask(__name__, 
        static_url_path="",
        template_folder="source/templates", 
        static_folder="source/static")
app.config.from_object("config")

csfr.init_app(app)
mail.init_app(app)
db.init_app(app)
login_manager.init_app(app)

app.context_processor(inject_asset_version)

with app.app_context():
    hash_static_assets(app)

from source.views.main import main
from source.views.auth import auth
from source.views.dashboard import dashboard
from source.utils.jinja import jinja_bp

app.register_blueprint(main)
app.register_blueprint(auth)
app.register_blueprint(dashboard)
app.register_blueprint(jinja_bp)