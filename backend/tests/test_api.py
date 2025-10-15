from fastapi.testclient import TestClient
from backend.main import app
import uuid

client = TestClient(app)

def test_root():
    response = client.get('/')
    assert response.status_code == 200
    assert 'message' in response.json()

def test_create_and_get_equipment():
    unique_name = f'Тестовое оборудование {uuid.uuid4()}'
    new_equipment = {'name': unique_name, 'fleet_quantity': 3}
    response = client.post('/equipment/', json=new_equipment)
    assert response.status_code == 200
    data = response.json()
    assert data['name'] == new_equipment['name']

    equip_id = data['id']
    response = client.get(f'/equipment/{equip_id}')
    assert response.status_code == 200
    assert response.json()['id'] == equip_id

def test_create_and_get_part():
    equipment = client.get('/equipment/').json()[0]
    unique_name = f'Тестовая запчасть {uuid.uuid4()}'
    new_part = {
        'name': unique_name,
        'useful_life': 300,
        'equipment_id': equipment['id'],
        'quantity_per_equipment': 2,
        'stock_quantity': 10,
        'procurement_time': 15
    }
    response = client.post('/parts/', json=new_part)
    assert response.status_code == 200
    data = response.json()
    assert data['name'] == new_part['name']

def test_create_workshop_and_type():
    unique_workshop_name = f'Тестовая мастерская {uuid.uuid4()}'
    new_workshop = {'name': unique_workshop_name, 'address': 'Тестовая улица'}
    response = client.post('/workshops/', json=new_workshop)
    assert response.status_code == 200
    assert response.json()['name'] == new_workshop['name']

    unique_type_name = f'тестовая замена {uuid.uuid4()}'
    new_type = {'name': unique_type_name}
    response = client.post('/replacement_types/', json=new_type)
    assert response.status_code == 200
    assert response.json()['name'] == new_type['name']

def test_create_replacement_and_get():
    equipment = client.get('/equipment/').json()[0]
    part = client.get(f'/parts/?equipment_id={equipment["id"]}').json()[0]
    workshop = client.get('/workshops/').json()[0]
    rtype = client.get('/replacement_types/').json()[0]

    new_replacement = {
        'equipment_id': equipment['id'],
        'part_id': part['id'],
        'replacement_date': '2024-10-01',
        'replacement_type_id': rtype['id'],
        'workshop_id': workshop['id']
    }
    response = client.post('/replacements/', json=new_replacement)
    assert response.status_code == 200

def test_wear_calculation():
    equipment = client.get('/equipment/').json()[0]
    response = client.get(f'/wear/{equipment["id"]}')
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_procurement_plan():
    part = client.get('/parts/').json()[0]
    response = client.get(f'/procurement/{part["id"]}?end_date=2025-12-31')
    assert response.status_code == 200
    data = response.json()
    assert 'part_name' in data