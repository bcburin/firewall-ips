from abc import ABC, abstractmethod

from src.models.enums import Action
from src.models.firewall_rule import FirewallRule
from src.services.executor import CommandExecutor


class FirewallWriter(ABC):
    @abstractmethod
    def append_rule(self, rule: FirewallRule):
        ...

    @abstractmethod
    def prepend_rule(self, rule: FirewallRule):
        ...

    @abstractmethod
    def delete_rule(self, rule: FirewallRule):
        ...

    @abstractmethod
    def flush(self):
        ...

    @abstractmethod
    def list_rules(self) -> list[FirewallRule]:
        ...


class IPTablesWriter(FirewallWriter):
    def __init__(self, command_executor: CommandExecutor, chain: str, table: str):
        self.command_executor = command_executor
        self.chain = chain
        self.table = table

    @staticmethod
    def _write_iptables_rule(rule: FirewallRule) -> str:
        rule_str = ""
        # check whether rule is valid
        if not rule.protocol and (rule.dst_port):
            raise ValueError("port must specify a protocol")
        # write protocol, source and destiny
        if rule.protocol and rule.dst_port:
            rule_str += f"--dport {rule.dst_port} "

        if rule.min_fl_byt_s is not None and rule.max_fl_byt_s is not None:
            rule_str += f"-m connbytes --connbytes {rule.min_fl_byt_s}:{rule.max_fl_byt_s} --connbytes-dir both --connbytes-mode bytes "

        if rule.min_fl_pkt_s is not None and rule.max_fl_pkt_s is not None:
            rule_str += f"-m connbytes --connbytes {rule.min_fl_pkt_s}:{rule.max_fl_pkt_s} --connbytes-dir both --connbytes-mode packets "

        if rule.min_tot_fw_pk is not None and rule.max_tot_fw_pk is not None:
            rule_str += f"-m conntrack --ctdir ORIGINAL --ctbytes {rule.min_tot_fw_pk}:{rule.max_tot_fw_pk} "

        if rule.min_tot_bw_pk is not None and rule.max_tot_bw_pk is not None:
            rule_str += f"-m conntrack --ctdir REPLY --ctbytes {rule.min_tot_bw_pk}:{rule.max_tot_bw_pk} "

        # write action
        if rule.action == Action.ALLOW:
            rule_str += "-j ACCEPT"
        elif rule.action == Action.BLOCK:
            rule_str += "-j REJECT"
        return rule_str.strip()

    @classmethod
    def _read_iptables_rule(cls, rules_str: str) -> list[FirewallRule]:
        rules = []
        lines = rules_str.splitlines()
        for line in lines:
            if not line or line.startswith('target') or 'Chain' in line:
                continue
            parts = line.split()
            if len(parts) < 10:
                continue
            dst_port=parts[1]
            protocol= parts[2]
            min_fl_byt_s=parts[3]
            max_fl_byt_s=parts[4]
            min_fl_pkt_s=parts[5]
            max_fl_pkt_s=parts[6]
            min_tot_fw_pk=parts[7]
            max_tot_fw_pk=parts[8]
            min_tot_bw_pk=parts[9]
            max_tot_bw_pk=parts[10]
            action = parts[0]
            rule = FirewallRule(
                protocol=protocol,
                dst_port=dst_port,
                min_fl_byt_s=min_fl_byt_s,
                max_fl_byt_s=max_fl_byt_s,
                min_fl_pkt_s=min_fl_pkt_s,
                max_fl_pkt_s=max_fl_pkt_s,
                min_tot_fw_pk=min_tot_fw_pk,
                max_tot_fw_pk=max_tot_fw_pk,
                min_tot_bw_pk=min_tot_bw_pk,
                max_tot_bw_pk=max_tot_bw_pk,
                action=action
            )
            rules.append(rule)
        return rules

    _port_mappings = {
        "ssh": 22,
        "http": 80,
        "https": 443,
        "ftp": 21,
        "telnet": 23,
        "smtp": 25,
        "domain": 53,
        "pop3": 110,
        "imap": 143,
        "snmp": 161,
        "ldap": 389,
        "https-alt": 8443,
        "http-alt": 8080,
        "smtps": 465,
        "imaps": 993,
        "pop3s": 995,
        "rdp": 3389,
        "mysql": 3306,
        "postgres": 5432,
        "redis": 6379,
        "memcached": 11211
    }

    _address_mappings = {
        "localhost": "127.0.0.1",
        "anywhere": "0.0.0.0/0",
        "broadcast": "255.255.255.255",
        "localnet": "192.168.0.0/16",
        "multicast": "224.0.0.0/4"
    }

    @classmethod
    def _translate_port(cls, port: int | str | None) -> int | None:
        if port is None:
            return None
        if isinstance(port, int):
            return port
        if port.isdecimal():
            return int(port)
        return cls._port_mappings[port]

    @classmethod
    def _translate_address(cls, address: str | None) -> str | None:
        if address is None or address == "anywhere":
            return None
        if address in cls._address_mappings:
            return cls._address_mappings[address]
        return address

    @staticmethod
    def _translate_action(action_str) -> Action:
        if action_str == "ACCEPT":
            return Action.ALLOW
        if action_str == "REJECT":
            return Action.BLOCK

    def append_rule(self, rule: FirewallRule):
        command = f"iptables -t {self.table} -A {self.chain} {self._write_iptables_rule(rule)}"
        self.command_executor.execute(command)

    def prepend_rule(self, rule: FirewallRule):
        command = f"iptables -t {self.table} -I {self.chain} 1 {self._write_iptables_rule(rule)}"
        self.command_executor.execute(command)

    def delete_rule(self, rule: FirewallRule):
        command = f"iptables -t {self.table} -D {self.chain} {self._write_iptables_rule(rule)}"
        self.command_executor.execute(command)

    def flush(self):
        command = f"iptables -t {self.table} -F {self.chain}"
        self.command_executor.execute(command)

    def list_rules(self) -> list[FirewallRule]:
        command = f"iptables -t {self.table} -L {self.chain}"
        output = self.command_executor.execute(command)
        return self._read_iptables_rule(rules_str=output)
