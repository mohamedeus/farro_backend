import sys
import os

# Add the parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from app import create_app

from flask import json

@pytest.fixture()
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
    })

    yield app

@pytest.fixture()
def client(app):
    return app.test_client()

@pytest.fixture()
def runner(app):
    return app.test_cli_runner()

def test_example(client):
    response = client.get("/hello")
    assert response.status_code == 200
    assert b"Hello, World!" in response.data
    

def test_get_product(client):
    
    response = client.get('/product/1')

    assert response.status_code == 200

    data = json.loads(response.data)

    assert "product_id" in data
    assert "product_name" in data
    assert "category" in data
    assert "description" in data
    assert "unit" in data
    assert "news" in data

    assert isinstance(data["news"], list)