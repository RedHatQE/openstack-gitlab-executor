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

`FLAVOR` - Default instance flavor reference

`BUILDER_IMAGE` - Default image to use for instance provisioning

`NETWORK` - Default network name

`KEY_PAIR_NAME` - Default SSH key pair name

`SECURITY_GROUP` - Default security group

`USERNAME` - Default username for SSH connection to instances

`PRIVATE_KEY` - Private key content

`PASSWORD`  - Password overrides a set PRIVATE_KEY (not recommended)

`PASSPHRASE` - Passphrase to your private key

### GitLab Runner variables

`RUNNER_TAG_LIST` - Tag list

`REGISTRATION_TOKEN` - Runner's registration token

`RUNNER_NAME` - Runner name

`CI_SERVER_URL` - Runner URL

`RUNNER_BUILDS_DIR` - Path to `builds` directory on the Openstack instance

`RUNNER_CACHE_DIR` - Path to `cache` directory on the Openstack instance

`CONCURRENT` - Limits how many jobs can run concurrently (default 1)

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

```sh
cat env.txt

RUNNER_TAG_LIST=<your value>
REGISTRATION_TOKEN=<your value>
RUNNER_NAME=<your value>
CI_SERVER_URL=<your value>
RUNNER_BUILDS_DIR=<your value>
RUNNER_CACHE_DIR=<your value>
CONCURRENT=<your value>

FLAVOR=<your value>
BUILDER_IMAGE=<your value>
NETWORK=<your value>
KEY_PAIR_NAME=<your value>
SECURITY_GROUP=<your value>
USERNAME=<your value>
PASSWORD=<your value>
PASSPHRASE=<your value>

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
           -e PRIVATE_KEY="$(cat <private key filename>)"
           --env-file=env.txt \
           quay.io/redhatqe/openstack-gitlab-runner:latest
```

You can override instance configuration defaults by providing environment variables in a GitLab CI
job config. For example, if you want to use another Openstack image to provision builder instance
you should provide the following:

```yaml
stages:
  - build

build:
  stage: build
  variables:
    BUILDER_IMAGE: my-custom-image
  tags:
    - some-tag
  script:
    - some command
```
