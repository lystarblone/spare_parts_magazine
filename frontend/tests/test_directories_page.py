import pytest
from unittest.mock import patch
from streamlit.testing.v1 import AppTest

@pytest.mark.timeout(5)
@patch('requests.get')
@patch('requests.post')
def test_directories_page(mock_post, mock_get):
    mock_get.return_value.json.return_value = [{'id': 1, 'name': 'Test Truck', 'fleet_quantity': 10}]
    mock_post.return_value.status_code = 200
    app = AppTest.from_file('frontend/pages/Directories.py')
    app.run()
    assert app.session_state is not None
    text_inputs = [ti for ti in app.text_input if ti.form_id == 'add_equipment' and ti.label == 'Наименование']
    assert len(text_inputs) > 0

@pytest.mark.timeout(5)
@patch('requests.get')
def test_replacements_page(mock_get):
    mock_get.side_effect = [
        [{'id': 1, 'name': 'Truck'}],
        [{'id': 1, 'part_name': 'Engine Belt', 'replacement_date': '2025-01-01'}],
        [{'id': 1, 'name': 'Engine Belt', 'equipment_id': 1}],
        [{'id': 1, 'name': 'Planned'}],
        [{'id': 1, 'name': 'Main Workshop'}],
    ]
    app = AppTest.from_file('frontend/pages/Replacements.py')
    app.run()
    assert app.session_state is not None
    assert app.title[0].value == 'Случаи замен запчастей'

@pytest.mark.timeout(5)
@patch('requests.get')
def test_procurement_page(mock_get):
    mock_get.side_effect = [
        [{'id': 1, 'name': 'Filter'}],
        {'part_name': 'Filter', 'latest_init_date': '2025-08-01'}
    ]
    app = AppTest.from_file('frontend/pages/Procurement.py')
    app.run()
    assert app.title[0].value == 'Формирование плана закупки'
    assert app.session_state is not None

@pytest.mark.timeout(5)
@patch('requests.get')
def test_wear_page(mock_get):
    mock_get.side_effect = [
        [{'id': 1, 'name': 'Excavator'}],
        [
            {'part_name': 'Track Belt', 'remaining_percentage': 80, 'zone': 'Green'},
            {'part_name': 'Hydraulic Pump', 'remaining_percentage': 50, 'zone': 'Yellow'}
        ]
    ]
    app = AppTest.from_file('frontend/pages/Wear.py')
    app.run()
    assert app.title[0].value == 'Расчет степени износа'
    assert app.session_state is not None