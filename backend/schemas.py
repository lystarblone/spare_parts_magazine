from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import date

class EquipmentBase(BaseModel):
    name: str = Field(..., min_length=1)
    fleet_quantity: int = Field(..., ge=0)

class EquipmentCreate(EquipmentBase):
    pass

class EquipmentResponse(EquipmentBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

class PartBase(BaseModel):
    name: str = Field(..., min_length=1)
    useful_life: int = Field(..., ge=1, description='Useful life in days')
    equipment_id: int = Field(..., ge=1)
    quantity_per_equipment: int = Field(..., ge=1)
    stock_quantity: int = Field(..., ge=0)
    procurement_time: int = Field(..., ge=1, description='Procurement time in days')

class PartCreate(PartBase):
    pass

class PartResponse(PartBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

class WorkshopBase(BaseModel):
    name: str = Field(..., min_length=1)
    address: str = Field(..., min_length=1)

class WorkshopCreate(WorkshopBase):
    pass

class WorkshopResponse(WorkshopBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

class ReplacementTypeBase(BaseModel):
    name: str = Field(..., min_length=1)

class ReplacementTypeCreate(ReplacementTypeBase):
    pass

class ReplacementTypeResponse(ReplacementTypeBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

class ReplacementBase(BaseModel):
    equipment_id: int = Field(..., ge=1)
    part_id: int = Field(..., ge=1)
    replacement_date: date
    replacement_type_id: int = Field(..., ge=1)
    workshop_id: int = Field(..., ge=1)

class ReplacementCreate(ReplacementBase):
    pass

class ReplacementResponse(ReplacementBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

class WearResponse(BaseModel):
    part_name: str
    zone: str
    remaining_percentage: float

class ProcurementResponse(BaseModel):
    part_name: str
    latest_init_date: Optional[date] = Field(None, description='Latest date to initiate procurement, None if not possible')