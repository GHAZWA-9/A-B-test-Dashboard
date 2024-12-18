from fastapi.testclient import TestClient
from src.a_btest.API.APIconfig import app
from src.a_btest.API.APIModels import *
import matplotlib

# Instead of displaying the plot , save it in a file
matplotlib.use("Agg")


client = TestClient(app)
duration_Parameter = DurationParameter(variant_allocations=[50])

payload = duration_Parameter.model_dump()
print(payload)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


def test_calculate_SZ():
    duration_Parameter = DurationParameter(variant_allocations=[50])

    payload = duration_Parameter.model_dump()
    response = client.get("/calculate_sample_size", params=payload)
    assert response.status_code == 200  # check if the request was successfully handled
    data = response.json()

    # Ensure that the response matches the CalculateResponseDuration structure
    assert "sample_size" in data
    assert "duration_days" in data

    # Add additional checks to ensure that the values are as expected
    assert isinstance(data["sample_size"], int)
    assert isinstance(data["duration_days"], int)


def test_vizualize():
    visualPa = VisualParameter()
    payload = visualPa.model_dump()
    response = client.get("/vizualize", params=payload)
    assert response.status_code == 200
    assert response.headers["content-type"] == "image/png"


# add more restrictions on the value of the responses
def test_get_table():
    mde_Parameter = Mde_Parameter()
    payload = mde_Parameter.model_dump()
    response = client.get("/get_table_mde", params=payload)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert all(isinstance(row, dict) for row in data)
    assert all(key in data[0] for key in ["week", "mde", "visitors"])
    assert all(isinstance(row["week"], int) for row in data)
    assert all(isinstance(row["mde"], float) for row in data)
    assert all(isinstance(row["visitors"], int) for row in data)
    assert len(data) == mde_Parameter.number_weeks
