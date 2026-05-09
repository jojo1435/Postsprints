from sqlalchemy import Column, Integer, ForeignKey

from source.utils.db import db

from datetime import datetime, timezone

Base = db.Model

class Usage(Base):
    __tablename__ = "usages"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Data
    year = Column(Integer)
    month = Column(Integer)
    posts_count = Column(Integer, default=0)
    accounts_count = Column(Integer, default=0)

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
    def create_for_user(cls, user_id):
        now = datetime.now(timezone.utc)

        usage = cls(
            year=now.year,
            month=now.month,
            posts_count=0,
            accounts_count=0
        )
        usage.user_id = user_id
        return usage

    @classmethod
    def get_by_user_id(cls, user_id):
        return cls.query.filter_by(user_id=user_id)

    def __init__(self, year:int, month:int, posts_count:int, accounts_count:int):
        self.year = year
        self.month = month
        self.posts_count = posts_count
        self.accounts_count = accounts_count
