import time

def Send_email(receiver_email, receiver_name, title, text):
    import smtplib
    from email.mime.text import MIMEText
    from email.header import Header

    email_host = 'smtp.qq.com'
    email_user = '2287245796@qq.com'
    email_certificate = 'dxxqtwfuokjbdjjf'
    email_sender = '2287245796@qq.com'

    message = MIMEText(text, 'plain', 'utf-8')
    message['From'] = Header("Castamere", 'utf-8')
    message['To'] = Header(receiver_name, 'utf-8')
    message['Subject'] = Header(title, 'utf-8')

    try:
        smtpObj = smtplib.SMTP()
        smtpObj.connect(email_host, 25)
        smtpObj.login(email_user, email_certificate)
        smtpObj.sendmail(email_sender, receiver_email, message.as_string())
        print("success")
    except smtplib.SMTPException:
        
        print("Falied")


def alert():
    # receiver_email = 'castamerego@gmail.com'
    receiver_email = '2287245796@qq.com'
    receiver_name = 'Castamere'
    present_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
    text = f'Dear Castamere\n\nIn {present_time}, an Alert in your house has been triggered, please check it out on www.castamerego.com/surveillance'
    Send_email(receiver_email, receiver_name, 'Alert!', text)

alert()