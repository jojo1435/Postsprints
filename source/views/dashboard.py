from flask import Blueprint, render_template, redirect, g, url_for, session, abort
from flask_login import login_required, current_user
from sqlalchemy.orm import joinedload

from source.forms.workspace import CreateWorkspaceForm
from source.models.workspace_member import WorkspaceMember
from source.models.workspace import Workspace
from source.utils.decorators import active_user_required

import datetime

dashboard = Blueprint("dashboard", __name__)

@dashboard.before_request
def load_current_workspace():
    if not current_user.is_authenticated:
        g.current_workspace = None
        return

    workspace_id = session.get("workspace_id")

    if not workspace_id:
        membership = WorkspaceMember.query.filter_by(user_id=current_user.id).first()

        if membership:
            session["workspace_id"] = membership.workspace_id
            workspace_id = membership.workspace_id

    if workspace_id:
        workspace = Workspace.query.get(workspace_id)

        valid = WorkspaceMember.query.filter_by(
            user_id=current_user.id,
            workspace_id=workspace_id
        ).first()

        g.current_workspace = workspace if valid else None
    else:
        g.current_workspace = None

@dashboard.route("/dashboard", methods=["GET"])
@login_required
@active_user_required
def index():
    return render_template("pages/dashboard/index.html")

@dashboard.route("/dashboard/workspace", methods=["GET"])
@login_required
@active_user_required
def workspace():
    return render_template("pages/dashboard/workspace/index.html",
                           date=datetime.datetime.now())

@dashboard.route("/dashboard/workspace/create", methods=["GET", "POST"])
@login_required
@active_user_required
def workspace_create():
    form = CreateWorkspaceForm()

    current_workplaces = WorkspaceMember.query.filter_by(user_id=current_user.id, role="owner").count()
    max_workplaces = current_user.plan.max_workplaces
    
    user_can_create = current_workplaces < max_workplaces

    if form.validate_on_submit():
        if user_can_create:
            name = form.name.data
            description = form.description.data
            color = form.color.data
            icon = form.icon.data

            workspace = Workspace(name, description, color, icon)
            workspace.save()

            member = WorkspaceMember(current_user.id, workspace.id, "owner")
            member.save()

            session["workspace_id"] = workspace.id

            return redirect(url_for("dashboard.workspace"))
        else:
            return "number of max workplaces reached"

    return render_template("pages/dashboard/workspace/create.html",
                        form = form,
                        current_workplaces = current_workplaces,
                        user_can_create = user_can_create)

@dashboard.route("/dashboard/workspace/switch/<int:workspace_id>", methods=["GET"])
@login_required
@active_user_required
def workspace_switch(workspace_id):
    membership = WorkspaceMember.query.filter_by(
        user_id=current_user.id,
        workspace_id=workspace_id
    ).first()

    if not membership:
        abort(403)

    session["workspace_id"] = workspace_id

    return redirect(url_for("dashboard.workspace"))

@dashboard.route("/dashboard/calendar", methods=["GET", "POST"])
@login_required
@active_user_required
def calendar():
    return render_template("pages/dashboard/calendar.html")