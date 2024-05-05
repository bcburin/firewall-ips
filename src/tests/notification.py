import logging

from src.models.enums import Action
from src.models.firewall_rule import FirewallRuleOutModel
from src.services.notification import FWRuleNotificationServiceManager


if __name__ == '__main__':
    """
    It is necessary to configure a running SMTP server in server.config in order to test this script.
    """

    logging.basicConfig(level=logging.DEBUG)
    fw_rule1 = FirewallRuleOutModel(src_port=100, des_port=567, action=Action.DROP)
    fw_rule2 = FirewallRuleOutModel(src_port=127, des_port=568, action=Action.BLOCK)
    nsm1 = FWRuleNotificationServiceManager()
    nsm2 = FWRuleNotificationServiceManager()
    nsm3 = FWRuleNotificationServiceManager()
    nsm1.enqueue_notification(fw_rule1)
    nsm2.enqueue_notification(fw_rule2)
    nsm3.send_notifications()
