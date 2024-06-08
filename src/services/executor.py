import subprocess
from abc import ABC, abstractmethod


class CommandExecutor(ABC):
    @abstractmethod
    def execute(self, command: str) -> str:
        ...


class LocalLinuxExecutor(CommandExecutor):
    def __init__(self, password: str | None = None, admin: bool = False):
        if admin and not password:
            raise ValueError("password required for administrator privileges")
        self.admin = admin
        self.password = password

    def execute(self, command):
        if self.admin:
            command = f"echo '{self.password}' | sudo -S {command}"
        try:
            result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
            return result.decode()
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Failed to execute local command: {e.output.decode()}")


class SSHExecutor(CommandExecutor):
    def __init__(self, ssh_host, ssh_user, ssh_key_path):
        self.ssh_host = ssh_host
        self.ssh_user = ssh_user
        self.ssh_key_path = ssh_key_path

    def execute(self, command):
        ssh_command = [
            'ssh', '-i', self.ssh_key_path,
            f'{self.ssh_user}@{self.ssh_host}',
            command
        ]
        try:
            result = subprocess.check_output(ssh_command, stderr=subprocess.STDOUT)
            return result.decode()
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Failed to execute remote command: {e.output.decode()}")
