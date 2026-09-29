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
