import time

def Send_email(receiver_email, receiver_name, title, text,pics):
    import smtplib
    import os
    from email.mime.text import MIMEText
    from email.mime.image import MIMEImage
    from email.header import Header
    from email.mime.multipart import MIMEMultipart

    email_host = 'smtp.qq.com'
    email_user = '2287245796@qq.com'
    email_certificate = 'dxxqtwfuokjbdjjf'
    email_sender = '2287245796@qq.com'

    # message = MIMEText(text, 'plain', 'utf-8')
    message = MIMEMultipart('related')
    message['From'] = Header("Castamere", 'utf-8')
    message['To'] = Header(receiver_name, 'utf-8')
    message['Subject'] = Header(title, 'utf-8')


    
    pic_inline = '<p>A snapshort from your security camera:</p>'
    for index,pic_file in enumerate(pics):
            pic_file_name = os.path.basename(pic_file)
            with open(pic_file,'rb') as image:
                image_info = MIMEImage(image.read(),_subtype=False)
                image_info.add_header('Content-Id',f'<image{index+1}>')
                message.attach(image_info)
                tmp_pic_inline = f'''
                    <!-- <br>这是一段对图片进行描述的文本 {pic_file_name}:</br> -->
                    <br><img src="cid:image{index+1}" width="300" alt={pic_file_name}></br>
                    '''
                pic_inline += tmp_pic_inline

    message.attach(MIMEText(text + pic_inline , "html", "utf-8"))

    try:
        smtpObj = smtplib.SMTP()
        smtpObj.connect(email_host, 25)
        smtpObj.login(email_user, email_certificate)
        smtpObj.sendmail(email_sender, receiver_email, message.as_string())
        print("Alert success")
    except smtplib.SMTPException:
        
        print("Alert falied")


def alert():
    # receiver_email = 'castamerego@gmail.com'
    receiver_email = '2287245796@qq.com'
    receiver_name = 'Castamere'
    present_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
    text = f'Dear Castamere \n \n In {present_time}, an Alert in your house has been triggered, please check it out on www.castamerego.com/surveillance'
    pics = ['picture\camera_0.jpg','picture\camera_1.jpg']
    Send_email(receiver_email, receiver_name, 'Alert!', text,pics)

