# GitLab CI Openstack executor

GitLab CI doesn't support Openstack as an executor but provides the ability to implement your own
executor by using scripts to provision, run, and clean up CI environment. This repository contains
such scripts as well as a Containerfile to build and configure a container image with Gitlab Runner
that uses custom Openstack executor.

## Building

```sh
git clone https://github.com/RedHatQE/openstack-gitlab-executor.git
cd openstack-gitlab-executor
podman build --build-arg GITLAB_RUNNER_VERSION=<version> -f Containerfile -t openstack-gitlab-runner
```

## Configuration

The container expects the following environment variables:

### Instance variables

`FLAVOR` - Instance flavor reference

`BUILDER_IMAGE` - Image to use for instance provisioning

`NETWORK` - Network name

`KEY_PAIR_NAME` - SSH key pair name

`SECURITY_GROUP` - Security group

`USERNAME` - Username for SSH connection to instances

`PRIVATE_KEY_PATH` - Path to private key of the `KEY_PAIR_NAME` inside the container.

### GitLab Runner variables

`RUNNER_TAG_LIST` - Tag list

`REGISTRATION_TOKEN` - Runner's registration token

`RUNNER_NAME` - Runner name

`CI_SERVER_URL` - Runner URL

### [Openstack variables](https://docs.openstack.org/python-openstackclient/latest/cli/man/openstack.html#environment-variables)

`OS_AUTH_URL` - Openstack authentication URL

`OS_PROJECT_NAME` - Project-level authentication scope (name or ID)

`OS_USERNAME` - Authentication username

`OS_PASSWORD` - Authentication password

`OS_PROJECT_DOMAIN_NAME` - Domain name or ID containing project

`OS_USER_DOMAIN_NAME` - Domain name or ID containing user

`OS_REGION_NAME` - Authentication region name

`OS_IDENTITY_API_VERSION` - Identity API version

`OS_INTERFACE` - Interface type

## Usage

Create an env file with all variables:

```text
RUNNER_TAG_LIST=<your value>
REGISTRATION_TOKEN=<your value>
RUNNER_NAME=<your value>
CI_SERVER_URL=<your value>

FLAVOR=<your value>
BUILDER_IMAGE=<your value>
NETWORK=<your value>
KEY_PAIR_NAME=<your value>
SECURITY_GROUP=<your value>
USERNAME=<your value>
PRIVATE_KEY_PATH=/mnt/private_key/<private key>

OS_AUTH_URL=<your value>
OS_PROJECT_NAME=<your value>
OS_USERNAME=<your value>
OS_PASSWORD=<your value>
OS_PROJECT_DOMAIN_NAME=<your value>
OS_USER_DOMAIN_NAME=<your value>
OS_REGION_NAME=<your value>
OS_IDENTITY_API_VERSION=<your value>
OS_INTERFACE=<your value>
```

Run a container:

```sh
podman run -it \
           --env-file=env \
           -v <dir with private key>:/mnt/private_key/ \
           localhost/openstack-gitlab-runner
```
