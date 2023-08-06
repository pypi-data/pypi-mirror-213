import smtplib, ssl
from datetime import datetime
from email.message import EmailMessage
import os
import socket
import mimetypes
from pathlib import Path


class EmailAlerts:
    """
    Email management
    Attributes:
        smtp_address: configuration parameter
        email_port: port of server
        email_sender: snder address
        email_password: password
        email_receiver: receiver address
        environment (optional): name of the environment (used to identify application)
        attachments (optional): list of files to add to message. See add_attachment for individual files
        cooldown (optional): time in hours to wait between two emails
    """

    def __init__(self, smtp_address: str, email_port: int, email_sender: str, email_password: str,
                 email_receiver, environment: str = None, attachments: list = None, cooldown: int = None):
        self.attachments = attachments
        if attachments is None:
            self.attachments = []
        self.environment = environment
        self.message = None
        self.subject = None
        self.smtp_address = smtp_address
        self.email_password = email_password
        self.email_port = email_port
        self.email_sender = email_sender
        self.email_receiver = email_receiver
        if cooldown is not None and (cooldown <= 0 or type(cooldown) != int):
            raise ValueError('Cooldown must be an integer greater than 0')
        self.cooldown = cooldown
        self.last_update = None

    def send_email(self, subject=None, message=None):
        """
        Send an email alert. The subject and body of the email can be set by the user or leave blank to use the
        default values.
        args:
            subject: The subject of the email alert.
            body: The body of the email alert.
        """
        send_mail = True
        if self.cooldown is not None:
            # 1. Check last time an email was sent
            if self.last_update is None:
                self.read_last_message_timestamp()
            # 2. Compare times
            if self.last_update is not None:
                now = datetime.now()
                diff = (now - self.last_update).total_seconds() / 3600
                # 3. If diff less than cooldown, don't send email
                send_mail = False if diff < self.cooldown else True
        if send_mail:
            msg = EmailMessage()
            msg['From'] = self.email_sender
            msg['To'] = self.email_receiver
            if subject is None:
                msg['Subject'] = self.subject
            else:
                msg['Subject'] = subject
            if message is None:
                msg.set_content(self.message)
            else:
                msg.set_content(message)
            if self.attachments:
                for attachment in self.attachments:
                    self._add_attachment(attachment, msg)

            with smtplib.SMTP(self.smtp_address, self.email_port) as smtp:
                smtp.starttls(context=ssl.create_default_context())
                smtp.ehlo()
                smtp.login(self.email_sender, self.email_password)
                smtp.send_message(msg)
                print("Email sent successfully")
            self.last_update = datetime.now()
            self.write_message_timestamp()
            return True
        else:
            return False

    def set_message(self, message):
        self.message = message

    def set_subject(self, subject):
        self.subject = subject

    def set_environment(self, environment):
        self.environment = environment

    def set_email_alert_info(self, subject, message, environment):
        """
        Set the message, subject and environment for the email alert all in one function.
        """
        self.set_environment(environment)
        self.set_message(message)
        self.set_subject(subject)

    def set_attachments(self, attachments: list):
        failed = False
        for attachment in attachments:
            path = Path(attachment)
            if not path.is_file():
                print("File does not exist: {}".format(path.resolve()))
                attachments.remove(attachment)
                failed = True
        self.attachments = attachments
        if failed:
            return False
        return True

    def add_attachment(self, attachment):
        path = Path(attachment)
        if not path.is_file():
            print("File does not exist: {}".format(path.resolve()))
            return False
        self.attachments.append(attachment)
        return True

    def clear_attachments(self):
        self.attachments = []

    @staticmethod
    def _add_attachment(path, msg):
        """
        Add an attachment to the email alert as path to the file.
        """
        # Check if the file exists and is not a directory
        path = Path(path)
        if not path.is_file():
            print("File does not exist")
            return False
        filename = os.path.basename(path)
        ctype, encoding = mimetypes.guess_type(path)
        if ctype is None or encoding is not None:
            # No guess could be made, or the file is encoded (compressed), so
            # use a generic bag-of-bits type.
            ctype = 'application/octet-stream'
        maintype, subtype = ctype.split('/', 1)
        with open(path, 'rb') as fp:
            msg.add_attachment(fp.read(),
                               maintype=maintype,
                               subtype=subtype,
                               filename=filename)
        return True

    def reset_email_alert_info(self):
        """
        Reset the email alert info to default values.
        """
        self.set_message(None)
        self.set_subject(None)
        self.set_environment(None)

    def read_last_message_timestamp(self, filename='last_email_update.txt'):
        """
        Reads from file last time an email was sent
        """
        fle = Path(filename)
        fle.touch(exist_ok=True)
        with open(fle, mode='r+') as file:
            last_date = file.read()
            if last_date:
                last_date = datetime.strptime(last_date, "%d-%b-%Y (%H:%M:%S.%f)")
            else:
                last_date = None
        self.last_update = last_date

    def write_message_timestamp(self, filename='last_email_update.txt'):
        """
        Write in a file last time an email was sent
        """
        if self.last_update is not None:
            with open(filename, mode='w+') as file:
                file.write(f'{self.last_update.strftime("%d-%b-%Y (%H:%M:%S.%f)")}')
        else:
            print('No email was sent before')

    def email_alert_decorator(self, fnc):
        """
        Wrapper function for email alerts. The contents of the email can be set by the user
        using the set_message set_subject functions, and set_environment function.
        If None is passed to any of these functions, the default values will be used.
        """

        def wrapper(*args, **kwargs):
            try:
                return fnc(*args, **kwargs)
            except Exception as e:
                if self.environment is None:
                    self.environment = "Production"
                if self.message is None:
                    self.message = \
                        f"ERROR: {e}\n\
                        DEVICE: {socket.gethostname()}\n\
                        FILE: {os.path.abspath(__file__)}\n\
                        "
                if self.subject is None:
                    self.subject = f"Email alert: Error in: {self.environment}"

                self.send_email(self.subject, self.message)

        return wrapper
