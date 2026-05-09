from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from source.utils.db import db

from datetime import datetime, timezone

Base = db.Model

class Account(db.Model):
    __tablename__ = "accounts"
    id = Column(Integer, primary_key=True)

    string_id = Column(String(30), nullable=False, unique=True)
    account_id = Column(Integer)
    workspace_id = Column(Integer, ForeignKey("workspaces.id"), nullable=False)

    # Date
    added_at = Column(DateTime, nullable=False, default=datetime.now(timezone.utc))

    # Relations
    workspace = relationship("Workspace", back_populates="accounts")

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
    
    def __init__(self, string_id:str, account_id:int):
        self.string_id = string_id
        self.account_id = account_id