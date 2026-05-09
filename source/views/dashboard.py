from flask import Blueprint, render_template, redirect, url_for, session, request, flash, abort, g
from flask_login import current_user, login_required

from source.forms.workspace import *
from source.models.workspace_member import WorkspaceMember
from source.models.workspace import Workspace
from source.utils.db import db
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

""" Workspaces Routes """

@dashboard.route("/dashboard/workspace", methods=["GET"])
@login_required
@active_user_required
def workspace():
    form = SwitchWorkspaceForm()

    return render_template("pages/dashboard/workspace/index.html",
                           form=form,
                           date=datetime.datetime.now())

@dashboard.route("/dashboard/workspace/create", methods=["GET", "POST"])
@login_required
@active_user_required
def workspace_create():
    current_workplaces = WorkspaceMember.query.filter_by(
        user_id=current_user.id, role="owner"
    ).count()

    current_max = current_user.plan.max_workplaces
    user_can_create = current_workplaces < current_max

    form = CreateWorkspaceForm()

    if form.validate_on_submit():
        name = form.name.data.strip()
        description = (form.description.data or "").strip()
        color = form.color.data
        icon = form.icon.data

        ALLOWED_COLORS = {"violet", "blue", "green", "amber", "pink", "red", "teal", "stone", "slate"}
        ALLOWED_ICONS = {"letter", "business", "team", "marketing", "analytics", "store", "favourite", "startup"}

        if color not in ALLOWED_COLORS or icon not in ALLOWED_ICONS:
            abort(400)

        fresh_count = WorkspaceMember.query.filter_by(
            user_id=current_user.id, role="owner"
        ).count()

        if fresh_count >= current_max:
            abort(403)
        
        try:
            workspace = Workspace(name, description, color, icon)
            workspace.flush()

            member = WorkspaceMember(current_user.id, workspace.id, "owner")
            member.save()

            session["workspace_id"] = workspace.id

            flash(f"Workspace created successfully||{name} has created successfully", "success")
            return redirect(url_for("dashboard.workspace"))
        except Exception:
            db.session.rollback()
            flash("Error||Something happend while creating your workspace. Please try again.", "error")

    return render_template("pages/dashboard/workspace/create.html",
                        form = form,
                        current_workplaces = current_workplaces,
                        user_can_create = user_can_create)

@dashboard.route("/dashboard/workspace/settings/<int:workspace_id>", methods=["GET", "POST"])
@login_required
@active_user_required
def workspace_settings(workspace_id):
    workspace = Workspace.query.get_or_404(workspace_id)

    current_workplaces = WorkspaceMember.query.filter_by(
        user_id=current_user.id, role="owner"
    ).count()

    WorkspaceMember.query.filter_by(
        user_id=current_user.id,
        workspace_id=workspace_id,
        role="owner"
    ).first_or_404()

    member_count = WorkspaceMember.query.filter_by(workspace_id=workspace_id).count()

    form = UpdateWorkspaceForm(obj=workspace)
    delete_form = DeleteWorkspaceForm()

    if form.validate_on_submit():
        name = form.name.data.strip()
        description = (form.description.data or "").strip()
        color = form.color.data
        icon = form.icon.data

        ALLOWED_COLORS = {"violet", "blue", "green", "amber", "pink", "red", "teal", "stone", "slate"}
        ALLOWED_ICONS = {"letter", "business", "team", "marketing", "analytics", "store", "favourite", "startup"}

        if color not in ALLOWED_COLORS or icon not in ALLOWED_ICONS:
            abort(400)

        try:
            workspace.update(name=name, description=description, color=color, icon=icon)
            flash(f"Workspace updated||{name} has been updated successfully", "success")
            return redirect(url_for("dashboard.workspace"))
        except Exception:
            db.session.rollback()
            flash("Error||Something happened while updating your workspace. Please try again.", "error")

    return render_template("pages/dashboard/workspace/settings.html",
                           form=form,
                           delete_form=delete_form,
                           workspace=workspace,
                           current_workplaces=current_workplaces,
                           member_count=member_count)

@dashboard.route("/dashboard/workspace/switch/<int:workspace_id>", methods=["POST"])
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

    return redirect(request.referrer or url_for("dashboard.workspace"))

@dashboard.route("/dashboard/workspace/settings/<int:workspace_id>/delete", methods=["POST"])
@login_required
@active_user_required
def workspace_delete(workspace_id):
    workspace = Workspace.query.get_or_404(workspace_id)

    WorkspaceMember.query.filter_by(
        user_id=current_user.id,
        workspace_id=workspace_id,
        role="owner"
    ).first_or_404()

    delete_form = DeleteWorkspaceForm()

    if delete_form.validate_on_submit():
        if delete_form.workspace_name.data.strip() != workspace.name:
            flash("Error||The workspace name you entered does not match.", "error")
            return redirect(url_for("dashboard.workspace_settings", workspace_id=workspace_id))
        try:
            workspace.delete()
            flash(f"Workspace deleted||{workspace.name} has been permanently deleted.", "success")
            return redirect(url_for("dashboard.workspace"))
        except Exception as e:
            db.session.rollback()
            flash(f"Error||Something went wrong while deleting your workspace. Please try again. {e}", "error")
            return redirect(url_for("dashboard.workspace_settings", workspace_id=workspace_id))

    flash("Error||Invalid form submission.", "error")
    return redirect(url_for("dashboard.workspace_settings", workspace_id=workspace_id))

""" Calendar Routes """

@dashboard.route("/dashboard/calendar", methods=["GET", "POST"])
@login_required
@active_user_required
def calendar():
    return render_template("pages/dashboard/calendar.html")