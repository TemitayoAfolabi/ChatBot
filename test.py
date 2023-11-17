import pytest
from flask import Flask
from flask.testing import FlaskClient
from unittest.mock import patch

from app import app

@pytest.fixture
def client() -> FlaskClient:
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_chatbot(client: FlaskClient):
    with patch("openai.Completion.create") as mock_create:
        # Set up mock response from OpenAI
        mock_response = {
            "choices": [
                {
                    "text": "Chatbot response"
                }
            ]
        }
        mock_create.return_value = mock_response

        # Send POST request to /chatbot route
        response = client.post("/chatbot", data={"message": "User input"})

        # Assert response status code
        assert response.status_code == 200

        # Assert chatbot response in response text
        assert "Chatbot response" in response.get_data(as_text=True)

        # Assert user input in response text
        assert "User input" in response.get_data(as_text=True)
