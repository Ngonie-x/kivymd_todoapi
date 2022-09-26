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
    complete_tasks, incomplete_tasks = db.get_tasks()

    context = {
        'complete': json.dumps(complete_tasks),
        'incomplete': json.dumps(incomplete_tasks)
    }

    return context


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
