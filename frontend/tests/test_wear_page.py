from unittest.mock import patch
from streamlit.testing.v1 import AppTest

@patch('requests.get')
def test_wear_page(mock_get):
    mock_get.return_value.json.side_effect = [
        [{'id': 1, 'name': 'Crane'}],
        [{'part_name': 'Hook', 'remaining_percentage': 80, 'zone': 'Green'}]
    ]

    app = AppTest.from_file('frontend/pages/Wear.py')
    app.run(timeout=5)

    assert app.title[0].value == 'Расчет степени износа'