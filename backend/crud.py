from datetime import date, timedelta
from typing import List, Optional
import logging
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

logger = logging.getLogger(__name__)

def create_equipment(db: Session, equipment: EquipmentCreate) -> EquipmentResponse:
    try:
        db_equip = Equipment(**equipment.model_dump())
        db.add(db_equip)
        db.commit()
        db.refresh(db_equip)
        logger.info(f"Successfully created equipment: {equipment.name}")
        return EquipmentResponse(**db_equip.__dict__)
    except Exception as e:
        logger.exception(f"Failed to create equipment: {equipment.name}")
        raise

def get_equipments(db: Session) -> List[EquipmentResponse]:
    try:
        equipments = db.query(Equipment).all()
        logger.info(f"Fetched {len(equipments)} equipments")
        return [EquipmentResponse(**eq.__dict__) for eq in equipments]
    except Exception as e:
        logger.exception("Failed to fetch equipments")
        raise

def get_equipment(db: Session, equipment_id: int) -> Optional[EquipmentResponse]:
    try:
        db_equip = db.query(Equipment).filter(Equipment.id == equipment_id).first()
        if db_equip:
            logger.info(f"Fetched equipment with ID: {equipment_id}")
            return EquipmentResponse(**db_equip.__dict__)
        logger.warning(f"Equipment not found with ID: {equipment_id}")
        return None
    except Exception as e:
        logger.exception(f"Failed to fetch equipment with ID: {equipment_id}")
        raise

def create_part(db: Session, part: PartCreate) -> PartResponse:
    try:
        db_part = Part(**part.model_dump())
        db.add(db_part)
        db.commit()
        db.refresh(db_part)
        logger.info(f"Successfully created part: {part.name}")
        return PartResponse(**db_part.__dict__)
    except Exception as e:
        logger.exception(f"Failed to create part: {part.name}")
        raise

def get_parts(db: Session, equipment_id: Optional[int] = None) -> List[PartResponse]:
    try:
        query = db.query(Part)
        if equipment_id:
            query = query.filter(Part.equipment_id == equipment_id)
        parts = query.all()
        logger.info(f"Fetched {len(parts)} parts for equipment_id: {equipment_id}")
        return [PartResponse(**part.__dict__) for part in parts]
    except Exception as e:
        logger.exception(f"Failed to fetch parts for equipment_id: {equipment_id}")
        raise

def get_part(db: Session, part_id: int) -> Optional[PartResponse]:
    try:
        db_part = db.query(Part).filter(Part.id == part_id).first()
        if db_part:
            logger.info(f"Fetched part with ID: {part_id}")
            return PartResponse(**db_part.__dict__)
        logger.warning(f"Part not found with ID: {part_id}")
        return None
    except Exception as e:
        logger.exception(f"Failed to fetch part with ID: {part_id}")
        raise

def create_workshop(db: Session, workshop: WorkshopCreate) -> WorkshopResponse:
    try:
        db_workshop = Workshop(**workshop.model_dump())
        db.add(db_workshop)
        db.commit()
        db.refresh(db_workshop)
        logger.info(f"Successfully created workshop: {workshop.name}")
        return WorkshopResponse(**db_workshop.__dict__)
    except Exception as e:
        logger.exception(f"Failed to create workshop: {workshop.name}")
        raise

def get_workshops(db: Session) -> List[WorkshopResponse]:
    try:
        workshops = db.query(Workshop).all()
        logger.info(f"Fetched {len(workshops)} workshops")
        return [WorkshopResponse(**ws.__dict__) for ws in workshops]
    except Exception as e:
        logger.exception("Failed to fetch workshops")
        raise

def get_workshop(db: Session, workshop_id: int) -> Optional[WorkshopResponse]:
    try:
        db_workshop = db.query(Workshop).filter(Workshop.id == workshop_id).first()
        if db_workshop:
            logger.info(f"Fetched workshop with ID: {workshop_id}")
            return WorkshopResponse(**db_workshop.__dict__)
        logger.warning(f"Workshop not found with ID: {workshop_id}")
        return None
    except Exception as e:
        logger.exception(f"Failed to fetch workshop with ID: {workshop_id}")
        raise

def create_replacement_type(db: Session, replacement_type: ReplacementTypeCreate) -> ReplacementTypeResponse:
    try:
        db_type = ReplacementType(**replacement_type.model_dump())
        db.add(db_type)
        db.commit()
        db.refresh(db_type)
        logger.info(f"Successfully created replacement type: {replacement_type.name}")
        return ReplacementTypeResponse(**db_type.__dict__)
    except Exception as e:
        logger.exception(f"Failed to create replacement type: {replacement_type.name}")
        raise

def get_replacement_types(db: Session) -> List[ReplacementTypeResponse]:
    try:
        types = db.query(ReplacementType).all()
        logger.info(f"Fetched {len(types)} replacement types")
        return [ReplacementTypeResponse(**rt.__dict__) for rt in types]
    except Exception as e:
        logger.exception("Failed to fetch replacement types")
        raise

def get_replacement_type(db: Session, type_id: int) -> Optional[ReplacementTypeResponse]:
    try:
        db_type = db.query(ReplacementType).filter(ReplacementType.id == type_id).first()
        if db_type:
            logger.info(f"Fetched replacement type with ID: {type_id}")
            return ReplacementTypeResponse(**db_type.__dict__)
        logger.warning(f"Replacement type not found with ID: {type_id}")
        return None
    except Exception as e:
        logger.exception(f"Failed to fetch replacement type with ID: {type_id}")
        raise

def create_replacement(db: Session, replacement: ReplacementCreate) -> ReplacementResponse:
    try:
        db_repl = Replacement(**replacement.model_dump())
        db.add(db_repl)
        db.commit()
        db.refresh(db_repl)
        logger.info(f"Successfully created replacement for part_id: {replacement.part_id}")
        return ReplacementResponse(**db_repl.__dict__)
    except Exception as e:
        logger.exception(f"Failed to create replacement for part_id: {replacement.part_id}")
        raise

def get_replacements(db: Session, equipment_id: Optional[int] = None) -> List[ReplacementResponse]:
    try:
        query = db.query(Replacement)
        if equipment_id:
            query = query.filter(Replacement.equipment_id == equipment_id)
        replacements = query.all()
        logger.info(f"Fetched {len(replacements)} replacements for equipment_id: {equipment_id}")
        return [ReplacementResponse(**repl.__dict__) for repl in replacements]
    except Exception as e:
        logger.exception(f"Failed to fetch replacements for equipment_id: {equipment_id}")
        raise

def update_replacement(db: Session, replacement_id: int, data: dict) -> Optional[ReplacementResponse]:
    try:
        db_repl = db.query(Replacement).filter(Replacement.id == replacement_id).first()
        if db_repl:
            for key, value in data.items():
                setattr(db_repl, key, value)
            db.commit()
            db.refresh(db_repl)
            logger.info(f"Successfully updated replacement with ID: {replacement_id}")
            return ReplacementResponse(**db_repl.__dict__)
        logger.warning(f"Replacement not found with ID: {replacement_id}")
        return None
    except Exception as e:
        logger.exception(f"Failed to update replacement with ID: {replacement_id}")
        raise

def calculate_wear_for_equipment(db: Session, equipment_id: int, current_date: date = date.today()) -> List[WearResponse]:
    try:
        equipment = get_equipment(db, equipment_id)
        if not equipment:
            logger.warning(f"Equipment not found for wear calculation: {equipment_id}")
            return []
        parts = [get_part(db, part.id) for part in get_parts(db, equipment_id)]
        replacements = get_replacements(db, equipment_id)
        results = []
        for part in parts:
            if not part:
                continue
            part_reps = sorted(
                [r for r in replacements if r.part_id == part.id],
                key=lambda r: r.replacement_date,
                reverse=True
            )
            last_replacement_date = date.fromisoformat(part_reps[0].replacement_date) if part_reps else None
            if not last_replacement_date:
                logger.warning(f"No replacements found for part: {part.name}")
                results.append(WearResponse(part_name=part.name, zone='Unknown', remaining_percentage=0.0))
                continue
            days_used = (current_date - last_replacement_date).days
            remaining_days = max(0, part.useful_life - days_used)
            remaining_percentage = (remaining_days / part.useful_life * 100) if part.useful_life > 0 else 0
            zone = 'Green' if remaining_percentage > 25 else 'Yellow' if remaining_percentage > 10 else 'Red'
            if part.stock_quantity == 0 and remaining_days < part.procurement_time:
                zone = 'Critical'
            results.append(WearResponse(part_name=part.name, zone=zone, remaining_percentage=remaining_percentage))
        logger.info(f"Calculated wear for {len(results)} parts in equipment_id: {equipment_id}")
        return results
    except Exception as e:
        logger.exception(f"Failed to calculate wear for equipment_id: {equipment_id}")
        raise

def calculate_procurement_plan(db: Session, part_id: int, end_date: date) -> ProcurementResponse:
    try:
        if end_date < date.today():
            logger.error(f"End date {end_date} is in the past")
            raise ValueError("End date cannot be in the past")
        part = get_part(db, part_id)
        if not part:
            logger.warning(f"Part not found for procurement plan: {part_id}")
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
                    logger.info(f"Calculated procurement plan for part: {part.name}, latest init date: {candidate}")
                    return ProcurementResponse(part_name=part.name, latest_init_date=candidate)
            candidate -= timedelta(days=1)
        logger.warning(f"No valid procurement date found for part: {part.name}")
        return ProcurementResponse(part_name=part.name, latest_init_date=None)
    except Exception as e:
        logger.exception(f"Failed to calculate procurement plan for part_id: {part_id}")
        raise