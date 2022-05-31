import uvicorn
from fastapi import FastAPI, BackgroundTasks
from send_email import send_email_background, send_email_async, Envs


def send_email_backgroundtasks(background_tasks: BackgroundTasks):
    send_email_background(background_tasks, 'Hello World', 'hazelhandrata@gmail.com', {
        'title': 'Hello World',
        'name': 'John Doe'
    })
    return 'Success'