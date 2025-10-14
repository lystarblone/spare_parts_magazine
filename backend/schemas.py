from pydantic import BaseModel
from typing import Optional
from datetime import date

class EquipmentBase(BaseModel):
    name: str
    fleet_quantity: int

class EquipmentCreate(EquipmentBase):
    pass

class EquipmentResponse(EquipmentBase):
    id: int
    class Config:
        from_attributes = True

class PartBase(BaseModel):
    name: str
    useful_life: float
    equipment_id: int
    quantity_per_equipment: int
    stock_quantity: int
    procurement_time: float

class PartCreate(PartBase):
    pass

class PartResponse(PartBase):
    id: int
    class Config:
        from_attributes = True

class WorkshopBase(BaseModel):
    name: str
    address: str

class WorkshopCreate(WorkshopBase):
    pass

class WorkshopResponse(WorkshopBase):
    id: int
    class Config:
        from_attributes = True

class ReplacementTypeBase(BaseModel):
    name: str

class ReplacementTypeCreate(ReplacementTypeBase):
    pass

class ReplacementTypeResponse(ReplacementTypeBase):
    id: int
    class Config:
        from_attributes = True

class ReplacementBase(BaseModel):
    equipment_id: int
    part_id: int
    replacement_date: str
    replacement_type_id: int
    workshop_id: int

class ReplacementCreate(ReplacementBase):
    pass

class ReplacementResponse(ReplacementBase):
    id: int
    class Config:
        from_attributes = True

class WearResponse(BaseModel):
    part_name: str
    zone: str
    remaining_percentage: float

class ProcurementResponse(BaseModel):
    part_name: str
    latest_init_date: Optional[date]