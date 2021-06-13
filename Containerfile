ARG GITLAB_RUNNER_VERSION=master

FROM registry.access.redhat.com/ubi8:8.4 AS builder

ARG GITLAB_RUNNER_VERSION

ENV GITLAB_REPO=https://gitlab.com/gitlab-org/gitlab-runner.git \
    PATH=$PATH:/root/go/bin/

RUN dnf install -y git-core make go ncurses && \
    git clone --depth=1 --branch=${GITLAB_RUNNER_VERSION} ${GITLAB_REPO} && \
    cd gitlab-runner && \
    make runner-bin-host && \
    chmod a+x out/binaries/gitlab-runner && \
    out/binaries/gitlab-runner --version

FROM registry.access.redhat.com/ubi8:8.4

ARG GITLAB_RUNNER_VERSION

COPY --from=builder /gitlab-runner/out/binaries/gitlab-runner /usr/bin

ENV HOME=/home/gitlab-runner \
    VENV=/openstack_driver_venv

ENV PATH="$VENV/bin:$PATH"

LABEL maintainer="Dmitry Misharov <misharov@redhat.com>" \
      version="$GITLAB_RUNNER_VERSION" \
      io.openshift.tags="gitlab,ci,runner" \
      name="openstack-gitlab-runner" \
      io.k8s.display-name="GitLab runner" \
      summary="GitLab runner" \
      description="A GitLab runner image with openstack custom executor." \
      io.k8s.description="A GitLab runner image with openstack custom executor."

WORKDIR $HOME

COPY cleanup.py env.py config.sh prepare.py run.py requirements.txt start.sh .

RUN dnf install -y --nodocs python38-pip git-core && \
    python3.8 -m venv $VENV && \
    pip install wheel && \
    pip install -r requirements.txt && \
    dnf remove -y git-core && \
    dnf clean all -y

RUN chgrp -R 0 $HOME && \
    chmod +x cleanup.py config.sh prepare.py run.py start.sh && \
    chmod -R g=u $HOME

USER 1001

CMD ["./start.sh"]
