#!/usr/bin/env python
import stat
import sys
from pathlib import Path

import openstack
import paramiko

import config


def get_server_ip(conn: openstack.connection.Connection) -> str:
    server = conn.compute.find_server(config.VM_NAME)
    return list(conn.compute.server_ips(server))[0].address


def execute_script_on_server(
    ssh: paramiko.client.SSHClient, sftp: paramiko.sftp_client.SFTPClient, script_path: str
) -> None:
    path = Path(script_path)
    sftpattrs = sftp.put(script_path, path.name)
    sftp.chmod(path.name, sftpattrs.st_mode | stat.S_IEXEC)
    _, stdout, _ = ssh.exec_command(f"./{path.name}")
    print(*stdout.readlines())
    sftp.remove(path.name)


def get_ssh_client(ip: str) -> paramiko.client.SSHClient:
    ssh_client = paramiko.client.SSHClient()
    pkey = paramiko.rsakey.RSASHA256Key.from_private_key_file(config.PRIVATE_KEY_PATH)
    ssh_client.set_missing_host_key_policy(paramiko.client.AutoAddPolicy())
    ssh_client.connect(
        hostname=ip,
        username=config.USERNAME,
        pkey=pkey,
        look_for_keys=False,
        allow_agent=False,
        timeout=60,
    )
    return ssh_client


def main() -> None:
    conn = openstack.connect()
    ip = get_server_ip(conn)
    ssh_client = get_ssh_client(ip)
    sftp_client = ssh_client.open_sftp()
    print(f"Executing {sys.argv[2]}")
    execute_script_on_server(ssh_client, sftp_client, sys.argv[1])
    sftp_client.close()
    ssh_client.close()


if __name__ == "__main__":
    main()
