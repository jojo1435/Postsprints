from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.orm import relationship

from source.utils.db import db

from datetime import datetime, timezone

Base = db.Model

class Workspace(Base):
    __tablename__ = "workspaces"
    id = Column(Integer, primary_key=True)

    # Data
    name = Column(String(50), nullable=False)
    description = Column(Text)

    # UI
    color = Column(String(20), default="violet")
    icon = Column(String(50), default="letter")

    # Date
    created_at = Column(DateTime, nullable=False, default=datetime.now(timezone.utc))
    
    # Relations
    memberships = relationship("WorkspaceMember", back_populates="workspace", cascade="all, delete-orphan")
    accounts = relationship("Account", back_populates="workspace", cascade="all, delete-orphan")

    # Database
    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

    def flush(self):
        db.session.add(self)
        db.session.flush()

    def update(self, **kwargs):
        allowed_fields = {"name", "description", "color", "icon"}
        for key, value in kwargs.items():
            if key in allowed_fields and value is not None:
                setattr(self, key, value)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_by_user_id(cls, user_id):
        return cls.query.filter_by(user_id=user_id)
    
    def __init__(self, name:str, description:str, color:str, icon:str):
        self.name = name
        self.description = description
        self.color = color
        self.icon = icon