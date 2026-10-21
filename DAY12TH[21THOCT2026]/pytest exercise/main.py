from fastapi import FastAPI,HTTPException
from pydantic import BaseModel

app = FastAPI()

class Tasks(BaseModel):
    id: int
    title: str
    status: str

tasks = [
    Tasks(id=1,title="Prepare report",status="pending"),
    Tasks(id=2,title="Review invoice",status="completed"),
    Tasks(id=3,title="update dashboard",status="pending")
]

#GET    /tasks
@app.get("/tasks")
def get_tasks():
    return tasks

#GET    /tasks/{task_id}
@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    for task in tasks:
        if task.id == task_id:
            return task
    # return {"error": "task not found"}
    raise HTTPException(status_code=404, detail="task not found")

#POST   /tasks
@app.post("/tasks")
def add_task(task: Tasks):
    tasks.append(task)
    return task

#PUT    /tasks/{task_id}
@app.put("/tasks/{task_id}")
def update_task(task_id: int, updated_task: Tasks):
    for task in tasks:
        if task.id == task_id:
            task.title = updated_task.title
            task.status = updated_task.status
            return task

    return {"error": "task not found"}

#DELETE /tasks/{task_id}
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    for i,task in enumerate(tasks):
        if task.id == task_id:
            tasks.pop(i)
            return task
    return {"error": "task not found"}