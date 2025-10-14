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
from typing import List
from datetime import date

app = FastAPI(title='Spare Parts Journal API')

init_db()

@app.post('/equipment/', response_model=EquipmentResponse)
def api_create_equipment(equipment: EquipmentCreate, db: Session = Depends(get_db)):
    return create_equipment(db, equipment)

@app.get('/equipment/', response_model=List[EquipmentResponse])
def api_get_equipments(db: Session = Depends(get_db)):
    return get_equipments(db)

@app.get('/equipment/{equipment_id}', response_model=EquipmentResponse)
def api_get_equipment(equipment_id: int, db: Session = Depends(get_db)):
    db_equip = get_equipment(db, equipment_id)
    if not db_equip:
        raise HTTPException(status_code=404, detail='Equipment not found')
    return db_equip

@app.post('/parts/', response_model=PartResponse)
def api_create_part(part: PartCreate, db: Session = Depends(get_db)):
    return create_part(db, part)

@app.get('/parts/', response_model=List[PartResponse])
def api_get_parts(equipment_id: int | None = None, db: Session = Depends(get_db)):
    return get_parts(db, equipment_id)

@app.get('/parts/{part_id}', response_model=PartResponse)
def api_get_part(part_id: int, db: Session = Depends(get_db)):
    db_part = get_part(db, part_id)
    if not db_part:
        raise HTTPException(status_code=404, detail='Part not found')
    return db_part

@app.post('/workshops/', response_model=WorkshopResponse)
def api_create_workshop(workshop: WorkshopCreate, db: Session = Depends(get_db)):
    return create_workshop(db, workshop)

@app.get('/workshops/', response_model=List[WorkshopResponse])
def api_get_workshops(db: Session = Depends(get_db)):
    return get_workshops(db)

@app.get('/workshops/{workshop_id}', response_model=WorkshopResponse)
def api_get_workshop(workshop_id: int, db: Session = Depends(get_db)):
    db_workshop = get_workshop(db, workshop_id)
    if not db_workshop:
        raise HTTPException(status_code=404, detail='Workshop not found')
    return db_workshop

@app.post('/replacement_types/', response_model=ReplacementTypeResponse)
def api_create_replacement_type(replacement_type: ReplacementTypeCreate, db: Session = Depends(get_db)):
    return create_replacement_type(db, replacement_type)

@app.get('/replacement_types/', response_model=List[ReplacementTypeResponse])
def api_get_replacement_types(db: Session = Depends(get_db)):
    return get_replacement_types(db)

@app.get('/replacement_types/{type_id}', response_model=ReplacementTypeResponse)
def api_get_replacement_type(type_id: int, db: Session = Depends(get_db)):
    db_type = get_replacement_type(db, type_id)
    if not db_type:
        raise HTTPException(status_code=404, detail='Replacement type not found')
    return db_type

@app.post('/replacements/', response_model=ReplacementResponse)
def api_create_replacement(replacement: ReplacementCreate, db: Session = Depends(get_db)):
    return create_replacement(db, replacement)

@app.get('/replacements/', response_model=List[ReplacementResponse])
def api_get_replacements(equipment_id: int | None = None, db: Session = Depends(get_db)):
    return get_replacements(db, equipment_id)

@app.put('/replacements/{replacement_id}', response_model=ReplacementResponse)
def api_update_replacement(replacement_id: int, replacement: ReplacementCreate, db: Session = Depends(get_db)):
    updated = update_replacement(db, replacement_id, replacement.model_dump())
    if not updated:
        raise HTTPException(status_code=404, detail='Replacement not found')
    return updated

@app.get('/wear/{equipment_id}', response_model=List[WearResponse])
def api_get_wear(equipment_id: int, current_date: date | None = None, db: Session = Depends(get_db)):
    if current_date is None:
        current_date = date.today()
    return calculate_wear_for_equipment(db, equipment_id, current_date)

@app.get('/procurement/{part_id}', response_model=ProcurementResponse)
def api_get_procurement(part_id: int, end_date: date, db: Session = Depends(get_db)):
    return calculate_procurement_plan(db, part_id, end_date)