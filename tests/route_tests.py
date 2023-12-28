#!/usr/bin/env python3

import pytest
from fastapi.testclient import TestClient
from src.main import app
from src.routes import get_retirement_savings

client = TestClient(app)

def test_get_retirement_savings():
    # Test with a valid user_id
    response = client.get("/retirement_calculator/1")
    assert response.status_code == 200
    assert isinstance(response.json(), str)  # assuming the function returns a string

    # Test with a non-existent user_id
    response = client.get("/retirement_calculator/999999")
    assert response.status_code == 400  # expecting a bad request error

    # Test with an invalid user_id (not an integer)
    response = client.get("/retirement_calculator/abc")
    assert response.status_code == 422  # expecting an unprocessable entity error

def test_get_retirement_savings_function():
    # Test the function directly with a valid user_id
    assert isinstance(get_retirement_savings(1), str)

    # Test the function with a non-existent user_id
    with pytest.raises(ValueError):
        get_retirement_savings(999999)

    # Test the function with an invalid user_id (not an integer)
    with pytest.raises(TypeError):
        get_retirement_savings("abc")