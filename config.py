import os

VM_NAME = f"gitlab-builder-{os.getenv('CUSTOM_ENV_CI_RUNNER_ID')}-project-{os.getenv('CUSTOM_ENV_CI_PROJECT_ID')}-concurrent-{os.getenv('CUSTOM_ENV_CI_CONCURRENT_PROJECT_ID')}-job-{os.getenv('CUSTOM_ENV_CI_JOB_ID')}"  # noqa

FLAVOR = os.getenv("CUSTOM_ENV_FLAVOR") or os.getenv("FLAVOR")
BUILDER_IMAGE = os.getenv("CUSTOM_ENV_BUILDER_IMAGE") or os.getenv("BUILDER_IMAGE")
NETWORK = os.getenv("CUSTOM_ENV_NETWORK") or os.getenv("NETWORK")
KEY_PAIR_NAME = os.getenv("CUSTOM_ENV_KEY_PAIR_NAME") or os.getenv("KEY_PAIR_NAME")
SECURITY_GROUP = os.getenv("CUSTOM_ENV_SECURITY_GROUP") or os.getenv("SECURITY_GROUP")
USERNAME = os.getenv("CUSTOM_ENV_USERNAME") or os.getenv("USERNAME")
PRIVATE_KEY_PATH = f"{os.getenv('HOME')}/priv_key"
