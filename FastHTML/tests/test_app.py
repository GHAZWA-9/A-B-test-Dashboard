import pytest
from src.a_btest.FastHTML.app import app
from starlette.testclient import TestClient
from src.a_btest.FastHTML.app import app

# Initialize the test client
client = TestClient(app)


def test_root_route():
    """Test the root route returns correct HTML structure."""
    response = client.get("/")
    assert response.status_code == 200
    assert "Sample Size Estimator" in response.text
    assert "Traffic and Conversion Analysis" in response.text
    assert "Power Analysis Visualization" in response.text


def test_sample_size_calculator_route():
    """Test the sample size calculator route."""
    response = client.get("/sample-size-calculator")
    assert response.status_code == 200
    assert "Enter baseline conversion rate" in response.text
    assert "Daily visitors" in response.text


def test_visualization_route():
    """Test the visualization route."""
    response = client.get("/visualization")
    assert response.status_code == 200
    assert "Baseline Conversion Rate (%)" in response.text


def test_data_analysis_route():
    """Test the data analysis route."""
    response = client.get("/data-analysis")
    assert response.status_code == 200
    assert "Weekly Traffic" in response.text
