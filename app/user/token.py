def send_email(mail, to, subject, template, sender):
    """Send an email"""
    msg = Message(
        subject,
        recipients=[to],
        html=template,
        sender=sender
    )
    mail.send(msg)

if __name__ == '__main__':
    pass
