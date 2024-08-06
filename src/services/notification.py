import logging
from abc import ABC, abstractmethod
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from queue import Queue
from smtplib import SMTP
from typing import Generic, Type

from jinja2 import Environment, FileSystemLoader

from src.common.config import EmailNotificationConfig, NotificationConfig, ConfigurationManager
from src.common.notification import NotifiableObjectType, NotifiableObject
from src.common.utils import LoadableSingleton
from src.models.enums import Action
from src.models.firewall_rule import FirewallRuleOutModel


class NotificationService(Generic[NotifiableObjectType], ABC):

    def __init__(self, notifiable_object_class: Type[NotifiableObject]):
        self._cls = notifiable_object_class
        self._notifications = Queue(maxsize=ConfigurationManager().get_server_config().notification.max_queue_size)

    def enqueue_notification(self, notification: NotifiableObjectType):
        if not isinstance(notification, self._cls):
            logging.error(
                f"[{self.__class__.__name__}] notification to be enqueued must be of type {self._cls.__name__}. "
                f"Dropping notification.")
            return
        if self._notifications.full():
            logging.warning(f"[{self.__class__.__name__}] notification queue is full.")
        self._notifications.put(item=notification)

    def send_notifications(self):
        if self._notifications.empty():
            return
        notifications = []
        while not self._notifications.empty():
            notifications.append(self._notifications.get())
        try:
            self._send(notifications=notifications)
        except Exception as e:
            logging.error(f"[{self.__class__.__name__}] unexpected error while sending notifications: {e}")

    @abstractmethod
    def _send(self, notifications: list[NotifiableObjectType]):
        ...


class EmailNotificationService(Generic[NotifiableObjectType], NotificationService[NotifiableObjectType], ABC):

    def __init__(self, notifiable_object_class: Type[NotifiableObject], config: EmailNotificationConfig):
        super().__init__(notifiable_object_class=notifiable_object_class)
        self._config = config
        try:
            self._server = SMTP(self._config.smtp.server, self._config.smtp.port)
            if self._config.smtp.ehlo is not None:
                self._server.ehlo(self._config.smtp.ehlo)
            self._server.starttls()
            self._server.login(self._config.sender.email, self._config.sender.password)
            logging.info(f"[{self.__class__.__name__}] successfully connected to SMTP server.")
        except Exception as e:
            self._server = None
            logging.error(f"[{self.__class__.__name__}] unable to connect to SMTP server: {e}")

    def _send(self, notifications: list[NotifiableObjectType]):
        if self._server is None:
            logging.warning(
                f"[{self.__class__.__name__}] notifications of type {self._cls.__name__} will not be sent, "
                f"since there is not connection to SMTP server: {notifications}")
            return
        message = MIMEMultipart()
        message['From'] = self._config.sender.email
        message['To'] = ', '.join(self._config.mailing_list)
        message['Subject'] = self._config.subject.format(n=len(notifications))
        html_body = self._write_email_body(notifications)
        message.attach(MIMEText(html_body, 'html'))
        self._server.sendmail(self._config.sender.email, self._config.mailing_list, message.as_string())
        logging.info(
            f"[{self.__class__.__name__}] successfully sent email with notifications of type {self._cls.__name__}")

    @abstractmethod
    def _write_email_body(self, notifications: list[NotifiableObjectType]) -> str:
        ...

    def disconnect(self):
        self._server.quit()


class FWRuleEmailNotificationService(EmailNotificationService[FirewallRuleOutModel]):

    def __init__(self, config: EmailNotificationConfig):
        super().__init__(notifiable_object_class=FirewallRuleOutModel, config=config)
        self._env = Environment(loader=FileSystemLoader(self._config.resolved_template_path.parent))
        self._template = self._env.get_template(self._config.resolved_template_path.name)

    def _write_email_body(self, notifications: list[FirewallRuleOutModel]) -> str:
        context = {
            'num_rules': len(notifications),
            'firewall_rules': notifications
        }
        return self._template.render(context)


class FWRuleNotificationServiceManager(LoadableSingleton):

    def __init__(self):
        self._notification_services: list[NotificationService] = []
        self._config: NotificationConfig | None = None
        super().__init__()

    def _load(self):
        self._config = ConfigurationManager().get_notification_config()
        if self._config is None or not self._config.enable:
            return
        if self._config.methods.email is not None:
            self._notification_services.append(FWRuleEmailNotificationService(config=self._config.methods.email))

    def _loaded(self):
        return self._config is not None and (self._notification_services or not self._config.has_any_method())

    def enqueue_notification(self, notification: FirewallRuleOutModel):
        for service in self._notification_services:
            service.enqueue_notification(notification)

    def send_notifications(self):
        for service in self._notification_services:
            service.send_notifications()


if __name__ == '__main__':
    ConfigurationManager().load()
    manager = FWRuleNotificationServiceManager()
    manager.enqueue_notification(FirewallRuleOutModel(src_port=100, des_port=567, action=Action.DROP))
    manager.enqueue_notification(FirewallRuleOutModel(src_port=127, des_port=568, action=Action.BLOCK))
    manager.enqueue_notification(FirewallRuleOutModel(nat_src_port=100, nat_des_port=200, action=Action.BLOCK))
    manager.send_notifications()
