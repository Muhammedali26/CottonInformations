import datetime
from sys import exc_info
import pandas as pd
import csv
import ssl, smtplib
import csv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from csv import DictWriter



def log_error(file_name,code, message, notes):
    with open(f'{file_name}.csv', 'a') as f_object:
        print()

        field_names = ['Date','Error Code','Error Message',
               'Notes']
    
        dictwriter_object = DictWriter(f_object, fieldnames=field_names)

        log_dict = {
            'Date': datetime.datetime.strftime(datetime.datetime.today(), "%Y-%m-%d-%X")+" UTC",
            'Error Code': str(code),
            'Error Message': str(message),
            'Notes': str(notes)
        }
        dictwriter_object.writerow(log_dict)
        f_object.close()
    
    # log = log.append(log_dict, ignore_index=True)
    # log.to_csv("log.csv", index=False)

def mail_log_document(custom_error_text,error,basename,directory):

  html = f"""\
    <html>

    <body>
    <style>
        .dashed {{
        border-style: dashed;
        color: red;
        }}
    </style>
    <p>
    <div class="dashed">
        <p style="text-align:center; position: relative;"><strong>{custom_error_text}</strong></p>
        <br><strong>Error:{error}</strong><br>
        <br><strong>File name:{basename}</strong><br>
        <br><strong>Directory:{directory} </strong><br>
        <br>

    </div>
    </p>
    </body>

    </html>
    """
  sender_email = "****"
  password = "****"
  context = ssl.create_default_context()
  f = open("mail.csv")
  reader = csv.reader(f)
  next(reader)  # Skip header row
  # data = list(reader)
  # print(data)
  for name, email in reader:
      print(email)
      print(f"Sending email to {name}")
      # Send email here

      message = MIMEMultipart()

      message["Subject"] = "Error"
      message["From"] = sender_email
      message["To"] = email

      part = MIMEText(html, "html")
      message.attach(part)

      with smtplib.SMTP_SSL("smtp.yandex.com.tr", 465, context=context) as server:
          server.login(sender_email, password)
          server.sendmail(
              sender_email, email, message.as_string()
          )

def mail_log_url(custom_error_text,error,url):
  
  html = f"""\
    <html>

    <body>
    <style>
        .dashed {{
        border-style: dashed;
        color: red;
        }}
    </style>
    <p>
    <div class="dashed">
        <p style="text-align:center; position: relative;"><strong>{custom_error_text}</strong></p>
        <br><strong>Error:{error}</strong><br>
        <br><strong>URL:{url}</strong><br>
        <br>

    </div>
    </p>
    </body>

    </html>
    """
  sender_email = "****"
  password = "****"
  context = ssl.create_default_context()
  f = open("mail.csv")
  reader = csv.reader(f)
  next(reader)  # Skip header row
  # data = list(reader)
  # print(data)
  for name, email in reader:
      print(email)
      print(f"Sending email to {name}")
      # Send email here

      message = MIMEMultipart()

      message["Subject"] = "Error"
      message["From"] = sender_email
      message["To"] = email

      part = MIMEText(html, "html")
      message.attach(part)

      with smtplib.SMTP_SSL("smtp.yandex.com.tr", 465, context=context) as server:
          server.login(sender_email, password)
          server.sendmail(
              sender_email, email, message.as_string()
          )