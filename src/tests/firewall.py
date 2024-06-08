from src.models.enums import Action
from src.models.firewall_rule import FirewallRule
from src.services.firewall import IPTablesWriter
from src.services.executor import LocalLinuxExecutor


if __name__ == '__main__':
    executor = LocalLinuxExecutor(admin=True, password="xxx")
    fw_writer = IPTablesWriter(command_executor=executor, chain="TEST", table="filter")
    # delete rules
    fw_writer.flush()
    # create rules
    fw1 = FirewallRule(protocol="tcp", des_port=80, src_port=3541, src_address="192.0.10.4", action=Action.DROP)
    fw2 = FirewallRule(protocol="tcp", src_port=22, des_address="192.0.5.9", action=Action.DROP)
    fw3 = FirewallRule(protocol="tcp", des_port=2469, src_port=22, src_address="192.0.10.5", action=Action.ALLOW)
    fw4 = FirewallRule(protocol="tcp", src_address="127.0.0.1", des_port=443, action=Action.DROP)
    fw5 = FirewallRule(protocol="tcp", des_address="0.0.0.0", des_port=5673, src_port=3458, action=Action.DROP)
    # add rules
    fw_writer.append_rule(fw2)
    fw_writer.append_rule(fw4)
    fw_writer.append_rule(fw5)
    fw_writer.append_rule(fw1)
    fw_writer.append_rule(fw3)
    # list rules
    rules = fw_writer.list_rules()
    print(rules)
