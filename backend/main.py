from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from .database import init_db, get_db
from .crud import (
    create_equipment, get_equipments, get_equipment,
    create_part, get_parts, get_part,
    create_workshop, get_workshops, get_workshop,
    create_replacement_type, get_replacement_types, get_replacement_type,
    create_replacement, get_replacements, update_replacement,
    calculate_wear_for_equipment, calculate_procurement_plan
)
from .schemas import (
    EquipmentCreate, EquipmentResponse,
    PartCreate, PartResponse,
    WorkshopCreate, WorkshopResponse,
    ReplacementTypeCreate, ReplacementTypeResponse,
    ReplacementCreate, ReplacementResponse,
    WearResponse, ProcurementResponse
)
from typing import List, Optional
from datetime import date
import logging
from logging.handlers import RotatingFileHandler

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = RotatingFileHandler('app.log', maxBytes=1000000, backupCount=5)
handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logger.addHandler(handler)

app = FastAPI(title='Spare Parts Journal API')

init_db()

@app.get('/')
def read_root():
    logger.info('Root endpoint accessed')
    return {'message': 'Welcome to Spare Parts Journal API. Use /docs for API documentation.'}

@app.get('/health')
def health_check(db: Session = Depends(get_db)):
    try:
        db.execute('SELECT 1')
        logger.info('Health check: database is healthy')
        return {'status': 'healthy', 'database': 'connected'}
    except Exception:
        logger.exception('Health check failed: database connection error')
        raise HTTPException(status_code=500, detail='Database connection error')

@app.post('/equipment/', response_model=EquipmentResponse)
def api_create_equipment(equipment: EquipmentCreate, db: Session = Depends(get_db)):
    try:
        result = create_equipment(db, equipment)
        logger.info(f'Successfully created equipment: {equipment.name}')
        return result
    except Exception:
        logger.exception(f'Error creating equipment: {equipment.name}')
        raise HTTPException(status_code=500, detail='Internal server error')

@app.get('/equipment/', response_model=List[EquipmentResponse])
def api_get_equipments(db: Session = Depends(get_db)):
    try:
        equipments = get_equipments(db)
        logger.info(f'Fetched {len(equipments)} equipments')
        return equipments
    except Exception:
        logger.exception('Error fetching equipments')
        raise HTTPException(status_code=500, detail='Internal server error')

@app.get('/equipment/{equipment_id}', response_model=EquipmentResponse)
def api_get_equipment(equipment_id: int, db: Session = Depends(get_db)):
    try:
        db_equip = get_equipment(db, equipment_id)
        if not db_equip:
            logger.error(f'Equipment not found with ID: {equipment_id}')
            raise HTTPException(status_code=404, detail='Equipment not found')
        return db_equip
    except HTTPException:
        raise
    except Exception:
        logger.exception(f'Error fetching equipment with ID: {equipment_id}')
        raise HTTPException(status_code=500, detail='Internal server error')

@app.post('/parts/', response_model=PartResponse)
def api_create_part(part: PartCreate, db: Session = Depends(get_db)):
    try:
        result = create_part(db, part)
        logger.info(f'Successfully created part: {part.name}')
        return result
    except Exception:
        logger.exception(f'Error creating part: {part.name}')
        raise HTTPException(status_code=500, detail='Internal server error')

@app.get('/parts/', response_model=List[PartResponse])
def api_get_parts(equipment_id: Optional[int] = None, db: Session = Depends(get_db)):
    try:
        parts = get_parts(db, equipment_id)
        logger.info(f'Fetched {len(parts)} parts for equipment_id: {equipment_id}')
        return parts
    except Exception:
        logger.exception(f'Error fetching parts for equipment_id: {equipment_id}')
        raise HTTPException(status_code=500, detail='Internal server error')

@app.get('/parts/{part_id}', response_model=PartResponse)
def api_get_part(part_id: int, db: Session = Depends(get_db)):
    try:
        db_part = get_part(db, part_id)
        if not db_part:
            logger.error(f'Part not found with ID: {part_id}')
            raise HTTPException(status_code=404, detail='Part not found')
        return db_part
    except HTTPException:
        raise
    except Exception:
        logger.exception(f'Error fetching part with ID: {part_id}')
        raise HTTPException(status_code=500, detail='Internal server error')

@app.post('/workshops/', response_model=WorkshopResponse)
def api_create_workshop(workshop: WorkshopCreate, db: Session = Depends(get_db)):
    try:
        result = create_workshop(db, workshop)
        logger.info(f'Successfully created workshop: {workshop.name}')
        return result
    except Exception:
        logger.exception(f'Error creating workshop: {workshop.name}')
        raise HTTPException(status_code=500, detail='Internal server error')

@app.get('/workshops/', response_model=List[WorkshopResponse])
def api_get_workshops(db: Session = Depends(get_db)):
    try:
        workshops = get_workshops(db)
        logger.info(f'Fetched {len(workshops)} workshops')
        return workshops
    except Exception:
        logger.exception('Error fetching workshops')
        raise HTTPException(status_code=500, detail='Internal server error')

@app.get('/workshops/{workshop_id}', response_model=WorkshopResponse)
def api_get_workshop(workshop_id: int, db: Session = Depends(get_db)):
    try:
        db_workshop = get_workshop(db, workshop_id)
        if not db_workshop:
            logger.error(f'Workshop not found with ID: {workshop_id}')
            raise HTTPException(status_code=404, detail='Workshop not found')
        return db_workshop
    except HTTPException:
        raise
    except Exception:
        logger.exception(f'Error fetching workshop with ID: {workshop_id}')
        raise HTTPException(status_code=500, detail='Internal server error')

@app.post('/replacement_types/', response_model=ReplacementTypeResponse)
def api_create_replacement_type(replacement_type: ReplacementTypeCreate, db: Session = Depends(get_db)):
    try:
        result = create_replacement_type(db, replacement_type)
        logger.info(f'Successfully created replacement type: {replacement_type.name}')
        return result
    except Exception:
        logger.exception(f'Error creating replacement type: {replacement_type.name}')
        raise HTTPException(status_code=500, detail='Internal server error')

@app.get('/replacement_types/', response_model=List[ReplacementTypeResponse])
def api_get_replacement_types(db: Session = Depends(get_db)):
    try:
        types = get_replacement_types(db)
        logger.info(f'Fetched {len(types)} replacement types')
        return types
    except Exception:
        logger.exception('Error fetching replacement types')
        raise HTTPException(status_code=500, detail='Internal server error')

@app.get('/replacement_types/{type_id}', response_model=ReplacementTypeResponse)
def api_get_replacement_type(type_id: int, db: Session = Depends(get_db)):
    try:
        db_type = get_replacement_type(db, type_id)
        if not db_type:
            logger.error(f'Replacement type not found with ID: {type_id}')
            raise HTTPException(status_code=404, detail='Replacement type not found')
        return db_type
    except HTTPException:
        raise
    except Exception:
        logger.exception(f'Error fetching replacement type with ID: {type_id}')
        raise HTTPException(status_code=500, detail='Internal server error')

@app.post('/replacements/', response_model=ReplacementResponse)
def api_create_replacement(replacement: ReplacementCreate, db: Session = Depends(get_db)):
    try:
        result = create_replacement(db, replacement)
        logger.info(f'Successfully created replacement for part_id: {replacement.part_id}')
        return result
    except Exception:
        logger.exception(f'Error creating replacement for part_id: {replacement.part_id}')
        raise HTTPException(status_code=500, detail='Internal server error')

@app.get('/replacements/', response_model=List[ReplacementResponse])
def api_get_replacements(equipment_id: Optional[int] = None, db: Session = Depends(get_db)):
    try:
        replacements = get_replacements(db, equipment_id)
        logger.info(f'Fetched {len(replacements)} replacements for equipment_id: {equipment_id}')
        return replacements
    except Exception:
        logger.exception(f'Error fetching replacements for equipment_id: {equipment_id}')
        raise HTTPException(status_code=500, detail='Internal server error')

@app.put('/replacements/{replacement_id}', response_model=ReplacementResponse)
def api_update_replacement(replacement_id: int, replacement: ReplacementCreate, db: Session = Depends(get_db)):
    try:
        updated = update_replacement(db, replacement_id, replacement.model_dump())
        if not updated:
            logger.error(f'Replacement not found with ID: {replacement_id}')
            raise HTTPException(status_code=404, detail='Replacement not found')
        return updated
    except HTTPException:
        raise
    except Exception:
        logger.exception(f'Error updating replacement with ID: {replacement_id}')
        raise HTTPException(status_code=500, detail='Internal server error')

@app.get('/wear/{equipment_id}', response_model=List[WearResponse])
def api_get_wear(equipment_id: int, current_date: Optional[date] = None, db: Session = Depends(get_db)):
    try:
        if current_date is None:
            current_date = date.today()
        wear = calculate_wear_for_equipment(db, equipment_id, current_date)
        logger.info(f'Calculated wear for equipment_id: {equipment_id}')
        return wear
    except Exception:
        logger.exception(f'Error calculating wear for equipment_id: {equipment_id}')
        raise HTTPException(status_code=500, detail='Internal server error')

@app.get('/procurement/{part_id}', response_model=ProcurementResponse)
def api_get_procurement(part_id: int, end_date: date, db: Session = Depends(get_db)):
    try:
        procurement = calculate_procurement_plan(db, part_id, end_date)
        logger.info(f'Calculated procurement plan for part_id: {part_id}')
        return procurement
    except ValueError as ve:
        logger.error(f'Invalid input for procurement calculation: {ve}')
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception:
        logger.exception(f'Error calculating procurement for part_id: {part_id}')
        raise HTTPException(status_code=500, detail='Internal server error')