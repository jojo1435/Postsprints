from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from source.utils.db import db

from datetime import datetime, timezone

Base = db.Model

class User(Base, UserMixin):
    __tablename__ = "users"

    # Basic info
    id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False)
    email = Column(String(254), nullable=False, unique=True)
    password = Column(String(255), nullable=False)

    # Relationships
    plan_id = Column(Integer, ForeignKey("plans.id"))

    plan = relationship("Plan", backref="user")
    usages = relationship("Usage", backref="user")
    memberships = relationship("WorkspaceMember", backref="user")

    # Status
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now(timezone.utc))
    verified_at = Column(DateTime)
    
    # Auth
    def set_password(self, password):
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password, password)
  
    def confirm_user(self):
        self.is_verified = True
        self.verified_at = datetime.now(timezone.utc)
        db.session.commit()
 
    # Database
    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

    def flush(self):
        db.session.add(self)
        db.session.flush()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_by_id(cls, id):
        return cls.query.get(id)
    
    @classmethod
    def get_by_email(cls, email):
        return cls.query.filter_by(email=email).first()
    
    # Billing
    def set_plan(self, plan):
        self.plan = plan
    
    # Workspaces
    @property
    def workspaces(self):
        return [m.workspace for m in self.memberships]
    
    def get_role(self, workspace_id):
        for m in self.memberships:
            if m.workspace_id == workspace_id:
                return m.role
        return None
    
    def get_owned_workspaces(self):
        return [m.workspace for m in self.memberships if m.role == "owner"]

    def get_admin_workspaces(self):
        return [m.workspace for m in self.memberships if m.role == "admin"]

    def is_owner(self, workspace_id):
        return self.get_role(workspace_id) == "owner"

    def is_admin(self, workspace_id):
        return self.get_role(workspace_id) in ["owner", "admin"]

    # Usage
    def get_current_usage(self):
        now = datetime.now(timezone.utc)
        return next(
            (u for u in self.usages if u.year == now.year and u.month == now.month),
            None
        )

    def get_posts_used(self):
        usage = self.get_current_usage()
        return usage.posts_count if usage else 0

    def get_posts_left(self):
        return max(0, self.plan.max_posts_per_month - self.get_posts_used())

    def can_create_post(self):
        return self.get_posts_left() > 0

    def __init__(self, name:str, email:str):
        self.name = name
        self.email = email