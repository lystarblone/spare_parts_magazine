from unittest.mock import patch
from streamlit.testing.v1 import AppTest

@patch('requests.get')
@patch('requests.post')
@patch('requests.put')
def test_replacements_page(mock_put, mock_post, mock_get):
    mock_get.return_value.json.side_effect = [
        [{'id': 1, 'name': 'Excavator'}],
        [], [], [], []
    ]
    mock_post.return_value.status_code = 200
    mock_put.return_value.status_code = 200

    app = AppTest.from_file('frontend/pages/Replacements.py')
    app.run(timeout=5)

    assert 'Случаи замен запчастей' in app.title[0].value