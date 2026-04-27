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
    accounts = relationship("Account", backref="workspace")

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()  

    @classmethod
    def get_by_user_id(cls, user_id):
        return cls.query.filter_by(user_id=user_id)
    
    def __init__(self, name:str, description:str, color:str, icon:str):
        self.name = name
        self.description = description
        self.color = color
        self.icon = icon