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
        if not rule.protocol and (rule.src_port or rule.des_port):
            raise ValueError("source and destiny ports must specify a protocol")
        # write protocol, source and destiny
        if rule.protocol:
            rule_str += f"-p {rule.protocol} "
        if rule.src_address:
            rule_str += f"-s {rule.src_address} "
        if rule.des_address:
            rule_str += f"-d {rule.des_address} "
        if rule.protocol and rule.src_port:
            rule_str += f"--sport {rule.src_port} "
        if rule.protocol and rule.des_port:
            rule_str += f"--dport {rule.des_port} "
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
            if len(parts) < 5:
                continue
            action = parts[0]
            protocol = parts[1]
            src_address = parts[3]
            des_address = parts[4]
            src_port = None
            des_port = None
            for part in parts[5:]:
                if part.startswith('spt:'):
                    src_port = part.split(':')[1]
                elif part.startswith('dpt:'):
                    des_port = part.split(':')[1]
            rule = FirewallRule(
                protocol=protocol,
                src_address=cls._translate_address(src_address),
                des_address=cls._translate_address(des_address),
                src_port=cls._translate_port(src_port),
                des_port=cls._translate_port(des_port),
                action=cls._translate_action(action)
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
