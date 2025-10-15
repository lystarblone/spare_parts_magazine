from unittest.mock import patch
from streamlit.testing.v1 import AppTest

@patch('requests.get')
@patch('requests.post')
def test_directories_page(mock_post, mock_get):
    mock_get.return_value.json.side_effect = [
        [{'id': 1, 'name': 'Bulldozer', 'fleet_quantity': 2}],
        [{'id': 1, 'name': 'Bulldozer', 'fleet_quantity': 2}],
        [],
        [],
        []
    ]
    mock_post.return_value.status_code = 200

    app = AppTest.from_file('frontend/pages/Directories.py')
    app.run(timeout=5)

    assert app.title[0].value == 'Справочники'
    assert len(app.dataframe) > 0