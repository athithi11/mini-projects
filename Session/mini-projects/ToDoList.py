from fastapi import FastAPI, status
from schemas import ToDoList, ToDoListResponse
import json

app = FastAPI(
    title='To Do List API',
    description='A mini project to create a to-do list',
    version='0.1.0'
)

file_path = "/Users/athithiarulshanhar/Session/mini-projects/to_do_list.json"

with open(file=file_path) as json_file:
    tasks = json.load(json_file)

@app.post('/add_task/')
def add_new_task(task_info : ToDoList):
    task_id = len(tasks) + 1
    tasks.update({f"T{task_id}" : dict(task_info)})
    save_tasks()
    return {"received_data" : tasks}

@app.get('/get_task_by_id/', response_model=ToDoListResponse)
def get_task_by_id(task_id: str) -> ToDoListResponse:
    if task_id in tasks.keys():
        return ToDoListResponse(status="successful", message=tasks[task_id])
    raise Exception (
        status_code=status.HTTP_404_NOT_FOUND
    )

@app.get('/get_task_by_name/')
def get_task_by_name(task_name: str):
    task_list = {}
    for task_id, task in tasks.items():
        if task["name"] == task_name:
            task_list.update({task_id : task})
    if task_list != {}:
        return task_list
    else:
        raise Exception (
            status_code=status.HTTP_404_NOT_FOUND
        )

@app.get('/get_task_by_status/')
def get_task_by_status(task_status: str):
    task_list = {}
    for task_id, task in tasks.items():
        if task["status"] == task_status:
            task_list.update({task_id : task})
    if task_list != {}:
        return task_list
    else:
        raise Exception (
            status_code=status.HTTP_404_NOT_FOUND
        )

@app.get('/get_task_by_percentage/')
def get_task_by_percentage(task_percentage: str):
    task_list = {}
    for task_id, task in tasks.items():
        if task["percentage"] == task_percentage:
            task_list.update({task_id : task})
    if task_list != {}:
        return task_list
    else:
        raise Exception (
            status_code=status.HTTP_404_NOT_FOUND
        )

@app.get('/get_all_tasks/')
def get_all():
    return tasks

@app.put('/update_task/', response_model=ToDoListResponse)
def update_task(update_key : str, input_value : ToDoList) -> ToDoListResponse:
    if update_key in tasks.keys():
        tasks.update({update_key : input_value})
        save_tasks()
        return ToDoListResponse(status="successful", message="Dictionary updated")
    raise Exception (
        status_code=status.HTTP_404_NOT_FOUND
    )

@app.put('/update_task_name/', response_model=ToDoListResponse)
def update_task_name(update_key : str, input_name : str) -> ToDoListResponse:
    if update_key in tasks.keys():
        tasks[update_key]["name"] = input_name
        save_tasks()
        return ToDoListResponse(status="successful", message="Dictionary updated")
    raise Exception (
        status_code=status.HTTP_404_NOT_FOUND
    )

@app.put('/update_task_status/', response_model=ToDoListResponse)
def update_task_status(update_key : str, input_status : str) -> ToDoListResponse:
    if update_key in tasks.keys():
        tasks[update_key]["status"] = input_status
        if input_status == "completed":
            tasks[update_key]["percentage"] = 100.0
        save_tasks()
        return ToDoListResponse(status="successful", message="Dictionary updated")
    raise Exception (
        status_code=status.HTTP_404_NOT_FOUND
    )

@app.put('/update_task_percentage/', response_model=ToDoListResponse)
def update_task_percentage(update_key : str, input_percentage : float) -> ToDoListResponse:
    if update_key in tasks.keys():
        tasks[update_key]["percentage"] = input_percentage
        if input_percentage == 100:
            tasks[update_key]["status"] = "completed"
        save_tasks()
        return ToDoListResponse(status="successful", message="Dictionary updated")
    raise Exception (
        status_code=status.HTTP_404_NOT_FOUND
    )

@app.delete('/delete_task/', response_model=ToDoListResponse)
def delete_task(delete_key : str) -> ToDoListResponse:
    if delete_key in tasks.keys():
        tasks.pop(delete_key)
        save_tasks()
        return ToDoListResponse(status="successful", message="Item deleted")
    raise Exception (
        status_code=status.HTTP_404_NOT_FOUND
    )

@app.delete('/delete_completed/', response_model=ToDoListResponse)
def delete_complete() -> ToDoListResponse:
    deleted = False
    for task_id, task in tasks.items():
        if task["status"] == "completed":
            tasks.pop(task_id)
            deleted = True
    if deleted:
        save_tasks()
        return ToDoListResponse(status="successful", message="Completed item(s) deleted")
    else:
        return ToDoListResponse(status="successful", message="No completed items")

def save_tasks():
    with open(file_path, "w") as json_file:
        json.dump(tasks, json_file, indent=4)
