import pytest

@pytest.fixture(autouse=True)
def open_form(page):
    page.goto("http://127.0.0.1:8000/delivery.html")
