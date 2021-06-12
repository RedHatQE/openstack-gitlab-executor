#!/usr/bin/env python
import sys

import openstack
import paramiko

import config


def get_server_ip(conn: openstack.connection.Connection) -> str:
    server = conn.compute.find_server(config.VM_NAME)
    return list(conn.compute.server_ips(server))[0].address


def execute_script_on_server(ssh: paramiko.client.SSHClient, script_path: str) -> int:
    stdin, stdout, _ = ssh.exec_command("/bin/bash")
    with open(script_path) as f:
        stdin.channel.send(f.read())
        stdin.channel.shutdown_write()
    print(*stdout.readlines())
    return stdout.channel.recv_exit_status()


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
    print(f"Executing {sys.argv[2]}")
    exit_status = execute_script_on_server(ssh_client, sys.argv[1])
    ssh_client.close()
    sys.exit(exit_status)


if __name__ == "__main__":
    main()
