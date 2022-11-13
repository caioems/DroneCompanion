from G2Companion.database.configs.base import Base
from sqlalchemy import Column, Integer, Text

class Report(Base):
    #declarative base
    __tablename__='report'
    
    uid = Column(Integer, primary_key=True, nullable=False)
    #TODO: Create text column for timestamp
    motor_status = Column(Text)
    motor_feedback = Column(Text)
    imu_status = Column(Text)
    imu_feedback = Column(Text)
    
    def __repr__(self):
        return f"Total de registros: {self.uid}"
    
    #TODO: crud

