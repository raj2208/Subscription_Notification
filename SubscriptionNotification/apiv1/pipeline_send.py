from email.message import EmailMessage
import ssl
import smtplib
def send(to,sub,bod):
    email_sender='abhinavpandeyjee1@gmail.com'
    email_password='######'
    email_reciever=to
    subject=sub
    body=bod
    print("Executing the threads")
    em=EmailMessage()
    em['From']=email_sender
    em['To']=email_reciever
    em['Subject']=subject
    em.set_content(body)

    context=ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com',465,context=context) as smtp:
        smtp.login(email_sender,email_password)
        smtp.sendmail(email_sender,email_reciever,em.as_string())