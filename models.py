from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from datetime import datetime
from .database import Base


class HCP(Base):
    __tablename__ = "hcp"

    hcp_id = Column(Integer, primary_key=True, index=True)
    hcp_name = Column(String(100))
    specialization = Column(String(100))
    hospital = Column(String(150))
    city = Column(String(100))


class Interaction(Base):
    __tablename__ = "interaction"

    interaction_id = Column(Integer, primary_key=True, index=True)
    hcp_id = Column(Integer, ForeignKey("hcp.hcp_id"))
    interaction_type = Column(String(50))
    notes = Column(Text)
    summary = Column(Text)
    interaction_date = Column(DateTime, default=datetime.utcnow)