import os
from app.services.mailservice import send_todos_mail

def process_export_mail(recipient: str, filepath: str):
    try:
        send_todos_mail(recipient, filepath)
    finally:
        if os.path.exists(filepath):
            os.remove(filepath)
        # print(filepath)