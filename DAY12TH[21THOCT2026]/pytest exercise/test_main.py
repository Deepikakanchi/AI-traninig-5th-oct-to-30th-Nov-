from fastapi.testclient import TestClient
from main import app


#1. Create a TestClient for the FastAPI application

client = TestClient(app)


#2. Write a test for:
# GET /tasks
#Check that the status code is 200 .
def test_get_tasks():
    # Act
    response = client.get("/tasks")
    # Assert
    assert response.status_code == 200
#3. Check that the response from GET /tasks is a list
def test_get_task_list():
     response = client.get("/tasks")
     assert isinstance(response.json(),list)

# 4. Write a test for:
# GET /tasks/1
# Check:
# status code is 200
# returned id is 1
def test_get_task_single():
    response = client.get("/tasks/1")
    assert response.status_code == 200
    assert response.json().get("id") == 1


# 5. Test a task ID that does not exist.
# Example:
# GET /tasks/999
# Check that the API returns:
# 404
def test_get_invalid_task():
    response = client.get("/tasks/999")
    assert response.status_code == 404

# 6. Write a test for:
# POST /tasks
# Use:
# {
#   "id": 4,
#   "title": "Check server logs",
#   "status": "Pending"
# }
# Check:
# status code
# returned ID
# returned title

def test_add_task():
    response = client.post(
        "/tasks",
        json={
            "id": 4,
            "title": "check server logs",
            "status": "pending"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == 4
    assert data["title"] == "check server logs"


#7. Send invalid POST data by omitting one required field.
# Check that FastAPI returns a validation error.

def test_invalid_post():
    response = client.post(
        "/tasks",
        json={
            "id": 5,
            "title": "logs"
        }
    )
    assert response.status_code == 422

# 8. Write a test for:
# PUT /tasks/2
# Change the status to:
# Completed
# Verify the response.
def test_put_task():
    response = client.put(
        "/tasks/2",
        json={
            "id": 2,
            "title":"Review invoice",
            "status":"completed"
        }
    )

    assert response.status_code == 200

# 9. Write a test for:
# DELETE /tasks/3
# Verify that the response indicates successful deletion

def test_delete_complete():
    response = client.delete("/tasks/3")
    assert response.status_code == 200

# 10. After deleting Etask 3 , call:
# GET /tasks/3
# and verify that it returns 404 .
def test_get_deleted_task():
    response=client.get("/tasks/3")
    assert response.status_code == 404


# 11. Run all tests using:
# python -m pytest -v

