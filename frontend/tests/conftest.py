import pytest
from streamlit.testing.v1 import AppTest

@pytest.fixture
def run_app():
    def _run(script_path):
        return AppTest.from_file(script_path)
    return _run