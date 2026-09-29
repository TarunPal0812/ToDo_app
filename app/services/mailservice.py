import base64
import mimetypes
import os
import mailtrap as mt
from app.config.config import setting

mailtrap_client = mt.MailtrapClient(
    token= setting.MAILTRAP_TOKEN,
    sandbox= True,
    inbox_id= "4934045"
)

def send_welcome_mail(recipent: str):
    print(f"Initiated sending welcome mail to {recipent}")
    try:
        mail = mt.Mail(
            sender= mt.Address(email="welcome@todo.com"),
            to= [mt.Address(email= recipent)],
            subject= "Welcome to the todo application",
            text= "Here you can listed your todo's..!!"
        )
        mailtrap_client.send(mail)
        print("Welcome mail sent successfully.")
    except Exception as e:
        print(f"Failed to send welcome mail: {e}")


def send_todos_mail(recipent: str, file_path: str):
    try:
        mail_attachments = []
        if file_path and os.path.exists(file_path):
            filename = os.path.basename(file_path)
            
            mimetype, _ = mimetypes.guess_type(file_path)
            mimetype = mimetype or "application/octet-stream"
            
            with open(file_path, "rb") as f:
                file_bytes = f.read()
                base64_content = base64.b64encode(file_bytes)
            
            mail_attachments.append(
                mt.Attachment(
                    content=base64_content,
                    filename=filename,
                    mimetype=mimetype,
                    disposition=mt.Disposition.ATTACHMENT 
                )
            )

        mail = mt.Mail(
            sender=mt.Address(email="welcome@todo.com"),
            to=[mt.Address(email=recipent)],
            subject="Welcome to the todo application",
            text="Here you can list your todos..!!",
            attachments=mail_attachments 
        )
        
        mailtrap_client.send(mail)
        print("Welcome mail sent successfully.")
    except Exception as e:
        print(f"Failed to send welcome mail: {e}")


