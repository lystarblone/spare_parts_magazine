from unittest.mock import patch
from streamlit.testing.v1 import AppTest
from datetime import date

@patch('requests.get')
def test_procurement_page(mock_get):
    mock_get.return_value.json.side_effect = [
        [{'id': 1, 'name': 'Bearing'}],
        {'latest_init_date': str(date.today()), 'part_name': 'Bearing'},
        {'latest_init_date': str(date.today()), 'part_name': 'Bearing'}
    ]

    app = AppTest.from_file('frontend/pages/Procurement.py')
    app.run(timeout=5)

    assert app.title[0].value == 'Формирование плана закупки'