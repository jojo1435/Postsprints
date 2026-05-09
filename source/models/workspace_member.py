from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from source.utils.db import db

from datetime import datetime, timezone

Base = db.Model

class WorkspaceMember(Base):
    __tablename__ = "workspace_members"
    id = Column(Integer, primary_key=True)

    # Relation
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    workspace_id = Column(Integer, ForeignKey("workspaces.id"), nullable=False)

    # Data
    role = Column(String(20), default="member")  # owner, admin or member

    # Date
    added_at = Column(DateTime, nullable=False, default=datetime.now(timezone.utc))

    # Relations
    workspace = relationship("Workspace", back_populates="memberships")

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

    def __init__(self, user_id:int, workspace_id:int, role:str):
        self.user_id = user_id
        self.workspace_id = workspace_id
        self.role = role