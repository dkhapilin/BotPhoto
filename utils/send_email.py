import smtplib
import os
import mimetypes

from config_date.config import EMAIL_ADDRESS, EMAIL_PASSWORD
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage


def send_email(to_email: str, path: str = None) -> None:
    sender = EMAIL_ADDRESS
    password = EMAIL_PASSWORD
    title = path.split('/')[-1]
    server = smtplib.SMTP_SSL('smtp.yandex.ru', 465)
    server.starttls()
    print(path)
    try:
        server.login(sender, password)
        message = MIMEMultipart()
        message['From'] = sender
        message['To'] = to_email
        message['Subject'] = title

        for file in os.listdir(path):
            print(file)
            file_name = os.path.basename(file)
            f_type, encoding = mimetypes.guess_type(file)
            file_type, subtype = f_type.split("/")

            if file_type == "image":
                with open(os.path.join(path, file), "rb") as image:
                    image = MIMEImage(image.read())

            file.add_header('content-disposition', 'attachment', filename=file_name)
            message.attach(image)

        server.sendmail(sender, to_email, message.as_string())

    except Exception as e:
        pass
