from asyncio import Task
import json
from typing import Union
from datetime import date
from fastapi import FastAPI
from pydantic import BaseModel


from db import Database

app = FastAPI()

db = Database()


class Todo(BaseModel):
    task: str
    due_date: Union[date, None] = None
    completed: bool = False


@app.get("/")
async def root():
    tasks = db.get_tasks()
    todos = []

    for todo in tasks:
        todos.append(
            {
                'id': todo[0],
                'task': todo[1],
                'due_date': todo[2],
                'completed': todo[3]
            }
        )

    return todos


@app.post("/create-task/")
async def create_task(todo: Todo):
    task = db.create_task(
        task=todo.task,
        due_date=todo.due_date
    )

    context = {
        'task': json.dumps(task)
    }

    return context


@app.post("/task/{task_id}")
async def get_task(task_id):
    task = db.get_task(task_id)

    todo = {
        'id': task[0],
        'task': task[1],
        'due_date': task[2],
        'completed': task[3]
    }

    return todo


@app.put("/task/mark-complete/{task_id}")
async def mark_complete(task_id):
    db.mark_task_as_complete(task_id)

    return {
        "status": "Success"
    }


@app.put("/task/mark-incomplete/{task_id}")
async def mark_incomplete(task_id):
    db.mark_task_as_incomplete(task_id)

    return {
        "status": "Success"
    }


@app.put("/task/update/{task_id}")
async def update_task(task_id: int, task: str):
    db.update_task(task_id, task)

    return {
        "status": "Success"
    }


@app.delete('/delete-task/{task_id}')
async def delete_task(task_id):
    db.delete_task(task_id)

    return {
        "status": "Success"
    }
