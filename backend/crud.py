from datetime import date, timedelta
from typing import List, Optional

from dateutil.relativedelta import relativedelta
from sqlalchemy.orm import Session

from .models import Equipment, Part, Workshop, ReplacementType, Replacement
from .schemas import (
    EquipmentCreate, EquipmentResponse,
    PartCreate, PartResponse,
    WorkshopCreate, WorkshopResponse,
    ReplacementTypeCreate, ReplacementTypeResponse,
    ReplacementCreate, ReplacementResponse,
    WearResponse, ProcurementResponse
)

def create_equipment(db: Session, equipment: EquipmentCreate) -> EquipmentResponse:
    db_equip = Equipment(**equipment.model_dump())
    db.add(db_equip)
    db.commit()
    db.refresh(db_equip)
    return EquipmentResponse(**db_equip.__dict__)

def get_equipments(db: Session) -> List[EquipmentResponse]:
    return [EquipmentResponse(**eq.__dict__) for eq in db.query(Equipment).all()]

def get_equipment(db: Session, equipment_id: int) -> Optional[EquipmentResponse]:
    db_equip = db.query(Equipment).filter(Equipment.id == equipment_id).first()
    return EquipmentResponse(**db_equip.__dict__) if db_equip else None

def create_part(db: Session, part: PartCreate) -> PartResponse:
    db_part = Part(**part.model_dump())
    db.add(db_part)
    db.commit()
    db.refresh(db_part)
    return PartResponse(**db_part.__dict__)

def get_parts(db: Session, equipment_id: Optional[int] = None) -> List[PartResponse]:
    query = db.query(Part)
    if equipment_id:
        query = query.filter(Part.equipment_id == equipment_id)
    return [PartResponse(**part.__dict__) for part in query.all()]

def get_part(db: Session, part_id: int) -> Optional[PartResponse]:
    db_part = db.query(Part).filter(Part.id == part_id).first()
    return PartResponse(**db_part.__dict__) if db_part else None

def create_workshop(db: Session, workshop: WorkshopCreate) -> WorkshopResponse:
    db_workshop = Workshop(**workshop.model_dump())
    db.add(db_workshop)
    db.commit()
    db.refresh(db_workshop)
    return WorkshopResponse(**db_workshop.__dict__)

def get_workshops(db: Session) -> List[WorkshopResponse]:
    return [WorkshopResponse(**ws.__dict__) for ws in db.query(Workshop).all()]

def get_workshop(db: Session, workshop_id: int) -> Optional[WorkshopResponse]:
    db_workshop = db.query(Workshop).filter(Workshop.id == workshop_id).first()
    return WorkshopResponse(**db_workshop.__dict__) if db_workshop else None

def create_replacement_type(db: Session, replacement_type: ReplacementTypeCreate) -> ReplacementTypeResponse:
    db_type = ReplacementType(**replacement_type.model_dump())
    db.add(db_type)
    db.commit()
    db.refresh(db_type)
    return ReplacementTypeResponse(**db_type.__dict__)

def get_replacement_types(db: Session) -> List[ReplacementTypeResponse]:
    return [ReplacementTypeResponse(**rt.__dict__) for rt in db.query(ReplacementType).all()]

def get_replacement_type(db: Session, type_id: int) -> Optional[ReplacementTypeResponse]:
    db_type = db.query(ReplacementType).filter(ReplacementType.id == type_id).first()
    return ReplacementTypeResponse(**db_type.__dict__) if db_type else None

def create_replacement(db: Session, replacement: ReplacementCreate) -> ReplacementResponse:
    db_repl = Replacement(**replacement.model_dump())
    db.add(db_repl)
    db.commit()
    db.refresh(db_repl)
    return ReplacementResponse(**db_repl.__dict__)

def get_replacements(db: Session, equipment_id: Optional[int] = None) -> List[ReplacementResponse]:
    query = db.query(Replacement)
    if equipment_id:
        query = query.filter(Replacement.equipment_id == equipment_id)
    return [ReplacementResponse(**repl.__dict__) for repl in query.all()]

def update_replacement(db: Session, replacement_id: int, data: dict) -> Optional[ReplacementResponse]:
    db_repl = db.query(Replacement).filter(Replacement.id == replacement_id).first()
    if db_repl:
        for key, value in data.items():
            setattr(db_repl, key, value)
        db.commit()
        db.refresh(db_repl)
        return ReplacementResponse(**db_repl.__dict__)
    return None

def calculate_wear_for_equipment(db: Session, equipment_id: int, current_date: date = date.today()) -> List[WearResponse]:
    equipment = get_equipment(db, equipment_id)
    if not equipment:
        return []
    parts = [get_part(db, part.id) for part in get_parts(db, equipment_id)]
    replacements = get_replacements(db, equipment_id)
    results = []
    for part in parts:
        if not part:
            continue
        part_reps = sorted([r for r in replacements if r.part_id == part.id], key=lambda r: r.replacement_date, reverse=True)
        last_replacement_date = date.fromisoformat(part_reps[0].replacement_date) if part_reps else None
        if not last_replacement_date:
            results.append(WearResponse(part_name=part.name, zone='Unknown', remaining_percentage=100.0))
            continue
        days_used = (current_date - last_replacement_date).days
        remaining_days = max(0, part.useful_life - days_used)
        remaining_percentage = (remaining_days / part.useful_life * 100) if part.useful_life > 0 else 0
        zone = 'Green' if remaining_percentage > 25 else 'Yellow' if remaining_percentage > 10 else 'Red'
        if part.stock_quantity == 0 and remaining_days < part.procurement_time:
            zone = 'Critical'
        results.append(WearResponse(part_name=part.name, zone=zone, remaining_percentage=remaining_percentage))
    return results

def calculate_procurement_plan(db: Session, part_id: int, end_date: date) -> ProcurementResponse:
    part = get_part(db, part_id)
    if not part:
        return ProcurementResponse(part_name='', latest_init_date=None)
    
    candidate = end_date - timedelta(days=int(part.procurement_time))
    while candidate >= date.today():
        next_month = candidate + relativedelta(months=1)
        next_month_start = next_month.replace(day=1)
        possible_proc_dates = [
            next_month_start.replace(day=10),
            next_month_start.replace(day=25)
        ]
        proc_date = min((d for d in possible_proc_dates if d > candidate), default=None)
        if proc_date:
            delivery_date = proc_date + timedelta(days=int(part.procurement_time))
            if delivery_date <= end_date:
                return ProcurementResponse(part_name=part.name, latest_init_date=candidate)
        candidate -= timedelta(days=1)
    return ProcurementResponse(part_name=part.name, latest_init_date=None)