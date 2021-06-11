#!/usr/bin/env python
import openstack
import paramiko

import config


def provision_server(conn: openstack.connection.Connection) -> openstack.compute.v2.server.Server:
    image = conn.compute.find_image(config.BUILDER_IMAGE)
    flavor = conn.compute.find_flavor(config.FLAVOR)
    network = conn.network.find_network(config.NETWORK)
    server = conn.compute.create_server(
        name=config.VM_NAME,
        flavor_id=flavor.id,
        image_id=image.id,
        key_name=config.KEY_PAIR_NAME,
        security_groups=[{"name": config.SECURITY_GROUP}],
        networks=[{"uuid": network.id}],
    )
    return conn.compute.wait_for_server(server, wait=600)


def get_server_ip(
    conn: openstack.connection.Connection, server: openstack.compute.v2.server.Server
) -> str:
    return list(conn.compute.server_ips(server))[0].address


def check_ssh(ip: str) -> None:
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
    ssh_client.close()


def main() -> None:
    print("Connecting to Openstack")
    conn = openstack.connect()
    print(f"Provisioning an instance '{config.VM_NAME}'")
    server = provision_server(conn)
    ip = get_server_ip(conn, server)
    print(f"Instance {config.VM_NAME} is running on address {ip}")
    conn.close()
    print("Checking SSH connection")
    check_ssh(ip)


if __name__ == "__main__":
    main()
