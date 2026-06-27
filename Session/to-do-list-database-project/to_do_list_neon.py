from fastapi import FastAPI, status
from schemas import ToDoList, ToDoListResponse
from to_do import ToDo
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title='To Do List API',
    description='A mini project to create a to-do list',
    version='0.1.0'
)

DATABASE_URL = os.environ.get("DATABASE_URL")
engine = create_engine(DATABASE_URL)

@app.post('/add_task/', response_model=ToDoListResponse)
def add_new_task(task_info : ToDoList):
    with Session(engine) as session:
        task = ToDo(name=task_info.name, status=task_info.status, percentage=task_info.percentage)
        session.add(task)
        session.commit()
        return ToDoListResponse(status="successful", message="task inserted")
    return ToDoListResponse(status="unsuccessful", message="task not inserted")

@app.get('/get_task_by_id/')
def get_task_by_id(task_id: str):
    with Session(engine) as session:
        task = session.query(ToDo).where(ToDo.id == task_id).first()
        if task != None:
            return task
    raise Exception (
        status_code=status.HTTP_404_NOT_FOUND
    )

@app.get('/get_task_by_name/')
def get_task_by_name(task_name: str):
    with Session(engine) as session:
        task = session.query(ToDo).where(ToDo.name == task_name).all()
        if task != None:
            return task
    raise Exception (
        status_code=status.HTTP_404_NOT_FOUND
    )

@app.get('/get_task_by_status/')
def get_task_by_status(task_status: str):
    with Session(engine) as session:
        task = session.query(ToDo).where(ToDo.status == task_status).all()
        if task != None:
            return task
    raise Exception (
        status_code=status.HTTP_404_NOT_FOUND
    )

@app.get('/get_task_by_percentage/')
def get_task_by_percentage(task_percentage: str):
    with Session(engine) as session:
        task = session.query(ToDo).where(ToDo.percentage == task_percentage).all()
        if task != None:
            return task
    raise Exception (
        status_code=status.HTTP_404_NOT_FOUND
    )

@app.get('/get_all_tasks/')
def get_all():
    with Session(engine) as session:
        tasks = session.query(ToDo).all()
        if tasks != None:
            return tasks
    return "There are no tasks in the To Do list"

@app.put('/update_task/', response_model=ToDoListResponse)
def update_task(update_key : str, input_value : ToDoList) -> ToDoListResponse:
    with Session(engine) as session:
        task = session.query(ToDo).where(ToDo.id == update_key).first()
        if task != None:
            task.name = input_value.name
            task.status = input_value.status
            task.percentage = input_value.percentage
            session.commit()
            return ToDoListResponse(status="successful", message="Dictionary updated")
    raise Exception (
        status_code=status.HTTP_404_NOT_FOUND
    )

@app.put('/update_task_name/', response_model=ToDoListResponse)
def update_task_name(update_key : str, input_name : str) -> ToDoListResponse:
    with Session(engine) as session:
        task = session.query(ToDo).where(ToDo.id == update_key).first()
        if task != None:
            task.name = input_name
            session.commit()
            return ToDoListResponse(status="successful", message="Dictionary updated")
    raise Exception (
        status_code=status.HTTP_404_NOT_FOUND
    )

@app.put('/update_task_status/', response_model=ToDoListResponse)
def update_task_status(update_key : str, input_status : str) -> ToDoListResponse:
    with Session(engine) as session:
        task = session.query(ToDo).where(ToDo.id == update_key).first()
        if task != None:
            task.status = input_status
            if input_status == "completed":
                task.percentage = 100.0
            session.commit()
            return ToDoListResponse(status="successful", message="Dictionary updated")
    raise Exception (
        status_code=status.HTTP_404_NOT_FOUND
    )

@app.put('/update_task_percentage/', response_model=ToDoListResponse)
def update_task_percentage(update_key : str, input_percentage : float) -> ToDoListResponse:
    with Session(engine) as session:
        task = session.query(ToDo).where(ToDo.id == update_key).first()
        if task != None:
            task.percentage = input_percentage
            if input_percentage == 100:
                task.status = "completed"
            session.commit()
            return ToDoListResponse(status="successful", message="Dictionary updated")
    raise Exception (
        status_code=status.HTTP_404_NOT_FOUND
    )

@app.delete('/delete_task/', response_model=ToDoListResponse)
def delete_task(delete_key : str) -> ToDoListResponse:
    with Session(engine) as session:
        task = session.query(ToDo).where(ToDo.id == delete_key).first()
        if task != None:
            session.delete(task)
            session.commit()
            return ToDoListResponse(status="successful", message="Item deleted")
    raise Exception (
        status_code=status.HTTP_404_NOT_FOUND
    )

@app.delete('/delete_completed/', response_model=ToDoListResponse)
def delete_complete() -> ToDoListResponse:
    with Session(engine) as session:
        tasks = session.query(ToDo).where(ToDo.status == "completed").all()
        if tasks != None:
            for task in tasks:
                session.delete(task)
            session.commit()
            return ToDoListResponse(status="successful", message="Completed item(s) deleted")
    return ToDoListResponse(status="successful", message="No completed items")


