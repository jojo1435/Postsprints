from sqlalchemy import Column, Integer, String

from source.utils.db import db

Base = db.Model

class Plan(Base):
    __tablename__ = "plans"
    id = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=False, unique=True)

    # Limits
    max_workplaces = Column(Integer, nullable=False)
    max_accounts = Column(Integer, nullable=False)
    max_posts_per_month = Column(Integer, nullable=False)
    max_media_storage = Column(Integer, nullable=False)
    max_file_upload_size = Column(Integer, nullable=False)
    max_files_per_upload = Column(Integer, nullable=False)

    @classmethod
    def free(cls):
        return cls.query.filter_by(name="free").first()
    
    @classmethod
    def starter(cls):
        return cls.query.filter_by(name="starter").first()
    
    @classmethod
    def growth(cls):
        return cls.query.filter_by(name="growth").first()
    
    @classmethod
    def pro(cls):
        return cls.query.filter_by(name="pro").first()

    @classmethod
    def enterprise(cls):
        return cls.query.filter_by(name="enterprise").first()
    
    def __init__(self, name:str, max_workplaces:int, max_accounts:int, max_posts_per_month:int, max_media_storage:int, max_file_upload_size:int, max_files_per_upload:int):
        self.name = name
        self.max_workplaces = max_workplaces
        self.max_accounts = max_accounts
        self.max_posts_per_month = max_posts_per_month
        self.max_media_storage = max_media_storage
        self.max_file_upload_size = max_file_upload_size
        self.max_files_per_upload = max_files_per_upload