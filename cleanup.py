#!/usr/bin/env python
import openstack

import env


def main() -> None:
    conn = openstack.connect()
    for server in conn.compute.servers(name=env.VM_NAME):
        conn.compute.delete_server(server)


if __name__ == "__main__":
    main()
