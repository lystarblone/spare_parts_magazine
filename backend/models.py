from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date, Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Equipment(Base):
    __tablename__ = 'equipment'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    fleet_quantity = Column(Integer, nullable=False)
    parts = relationship('Part', back_populates='equipment')

class Part(Base):
    __tablename__ = 'parts'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    useful_life = Column(Integer, nullable=False)
    equipment_id = Column(Integer, ForeignKey('equipment.id'), nullable=False)
    quantity_per_equipment = Column(Integer, nullable=False)
    stock_quantity = Column(Integer, nullable=False)
    procurement_time = Column(Integer, nullable=False)
    equipment = relationship('Equipment', back_populates='parts')

    __table_args__ = (Index('idx_part_equipment_id', 'equipment_id'),)

class Workshop(Base):
    __tablename__ = 'workshops'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    address = Column(String, nullable=False)

class ReplacementType(Base):
    __tablename__ = 'replacement_types'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

class Replacement(Base):
    __tablename__ = 'replacements'
    id = Column(Integer, primary_key=True)
    equipment_id = Column(Integer, ForeignKey('equipment.id'), nullable=False)
    part_id = Column(Integer, ForeignKey('parts.id'), nullable=False)
    replacement_date = Column(Date, nullable=False)
    replacement_type_id = Column(Integer, ForeignKey('replacement_types.id'), nullable=False)
    workshop_id = Column(Integer, ForeignKey('workshops.id'), nullable=False)
    equipment = relationship('Equipment')
    part = relationship('Part')
    replacement_type = relationship('ReplacementType')
    workshop = relationship('Workshop')

    __table_args__ = (
        Index('idx_replacement_equipment_id', 'equipment_id'),
        Index('idx_replacement_part_id', 'part_id'),
    )