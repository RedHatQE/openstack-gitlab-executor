#!/usr/bin/env python
import openstack

import config


def main() -> None:
    print(f"Deleting instance {config.VM_NAME}")
    conn = openstack.connect()
    server = conn.compute.find_server(config.VM_NAME)
    conn.compute.delete_server(server)


if __name__ == "__main__":
    main()
