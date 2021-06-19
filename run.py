#!/usr/bin/env python
import sys

import openstack
import paramiko

import env


def get_server_ip(conn: openstack.connection.Connection) -> str:
    server = list(conn.compute.servers(name=env.VM_NAME, status="ACTIVE"))[0]
    return list(conn.compute.server_ips(server))[0].address


def execute_script_on_server(ssh: paramiko.client.SSHClient, script_path: str) -> int:
    stdin, stdout, stderr = ssh.exec_command("/bin/bash")
    with open(script_path) as f:
        stdin.channel.send(f.read())
        stdin.channel.shutdown_write()
    for line in iter(lambda: stdout.readline(2048), ""):
        print(line, sep="", end="", flush=True)
    exit_status = stdout.channel.recv_exit_status()
    if exit_status != 0:
        for line in iter(lambda: stderr.readline(2048), ""):
            print(line, sep="", end="", flush=True)
    return exit_status


def get_ssh_client(ip: str) -> paramiko.client.SSHClient:
    ssh_client = paramiko.client.SSHClient()
    pkey = paramiko.rsakey.RSASHA256Key.from_private_key_file(env.PRIVATE_KEY_PATH)
    ssh_client.set_missing_host_key_policy(paramiko.client.AutoAddPolicy())
    ssh_client.connect(
        hostname=ip,
        username=env.USERNAME,
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
    exit_status = execute_script_on_server(ssh_client, sys.argv[1])
    ssh_client.close()
    if exit_status != 0:
        sys.exit(int(env.BUILD_FAILURE_EXIT_CODE))


if __name__ == "__main__":
    main()
