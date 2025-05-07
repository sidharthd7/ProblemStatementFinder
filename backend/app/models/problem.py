from sqlalchemy import Column, Integer, String, JSON, DateTime
from ..db.base_class import Base
from datetime import datetime

class Problem(Base):
    __tablename__ = "problems"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    tech_stack = Column(JSON, nullable=False) 
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    source_file = Column(String, nullable=False)  