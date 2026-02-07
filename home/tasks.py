from celery import shared_task
import time
from datetime import datetime

# @shared_task
# def long_task():
#     print("Task started...")
#     time.sleep(10)
#     print("Task finished...")
#     return "Task completed successfully"

@shared_task
def delayed_task():
    print("Task executed after 10 seconds")
    return "Printed successfully"