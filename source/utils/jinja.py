from flask import Blueprint, g

jinja_bp = Blueprint("jinja_bp", __name__)

@jinja_bp.app_context_processor
def inject_workspace():
    return dict(current_workspace=g.get("current_workspace"))