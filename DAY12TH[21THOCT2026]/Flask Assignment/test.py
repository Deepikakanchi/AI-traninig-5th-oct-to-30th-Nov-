from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_get_products():

    #act
    response = client.get("/products")
    #assert
    assert response.status_code == 200
