#!/usr/bin/env python
import openstack

import env


def main() -> None:
    print(f"Deleting instance {env.VM_NAME}")
    conn = openstack.connect()
    server = conn.compute.find_server(env.VM_NAME)
    conn.compute.delete_server(server)


if __name__ == "__main__":
    main()
