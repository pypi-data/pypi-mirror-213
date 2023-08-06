#################################################################
## Base
#################################################################
FROM python:3.8-slim as lab_base
ARG LAB_VERSION

ENV LAB_VERSION=$LAB_VERSION
ENV LAB_ROOT=/opt/lab
ENV LAB_DIST=${LAB_ROOT}/dist
ENV LAB_HOME=${LAB_ROOT}/home
ENV LAB_BUILD=${LAB_ROOT}/build

#################################################################
## Builds utils and plugins as packages
#################################################################
FROM lab_base as lab_packages

RUN apt-get update -y --allow-releaseinfo-change \
  && apt-get install -y \
    git \
    --no-install-recommends

COPY . ${LAB_BUILD}

RUN pip install --upgrade pip build \
    && mkdir -p ${LAB_DIST}

RUN cd ${LAB_BUILD} \
    && python -m build \
    && cp -R ${LAB_BUILD}/dist ${LAB_DIST}/init

#RUN cd ${LAB_BUILD} \
#    && python -m build utils \
#    && cp -R ${LAB_BUILD}/utils/dist ${LAB_DIST}/utils

#RUN cd ${LAB_BUILD}/tools \
#    && sed -i "s|^version.*|version = \"${LAB_VERSION}\"|" pyproject.toml \
#    && python -m build \
#    && cp -R ${LAB_BUILD}/tools/dist ${LAB_DIST}/tools

#################################################################
## CLI
#################################################################
FROM lab_base as lab_cli
ENV LANGUAGE en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LC_ALL en_US.UTF-8
ENV PATH ${PATH}:/opt/bin
ENV HOME=${LAB_HOME}
ENV USER ${USER}
ENV DOCKER_VERSION "23.0.2"
ENV DOCKER_COMPOSE_VERSION "2.17.2"
ENV ACT_VERSION "0.2.45"

RUN apt-get update -y --allow-releaseinfo-change \
  && apt-get install -y \
    apt-transport-https \
    openssl \
    locales \
    ca-certificates \
    curl \
    gnupg2 \
    bash-completion \
    vim \
    sudo \
    git \
    gettext-base \
    libc-bin \
    pv \
    unzip \
    jq \
    python3-pip \
    python3-wheel \
    dnsutils \
    net-tools \
    iputils-ping \
    openssh-client \
    --no-install-recommends \
  && echo "en_US.UTF-8 UTF-8" > /etc/locale.gen \
  && locale-gen \
  && mkdir -p /opt/bin

RUN echo "Installing Docker client" \
  && curl -sSL https://download.docker.com/linux/static/stable/$(uname -m)/docker-${DOCKER_VERSION}.tgz > /tmp/docker-latest.tgz \
  && tar -xf /tmp/docker-latest.tgz -C /tmp \
  && cp -R /tmp/docker/* /usr/bin \
  && rm -rf /tmp/docker*

COPY --from=docker/buildx-bin /buildx /usr/libexec/docker/cli-plugins/docker-buildx

RUN echo "Installing Docker Compose" \
  && curl -sSL https://github.com/docker/compose/releases/download/v${DOCKER_COMPOSE_VERSION}/docker-compose-$(uname -s)-$(uname -m) > /usr/bin/docker-compose \
  && chmod +x /usr/bin/docker-compose

RUN echo "Installing act to run github workflows locally" \
  && curl -sSL https://github.com/nektos/act/releases/download/v${ACT_VERSION}/act_$(uname -s)_$(uname -m).tar.gz > /tmp/act.tar.gz \
  && tar -xf /tmp/act.tar.gz -C /tmp \
  && mv /tmp/act /usr/bin/act \
  && rm -rf /tmp/act*

COPY images/cli/requirements.txt /tmp/cli-requirements.txt
RUN echo "Installing Python dependencies" \
  && pip install --upgrade pip \
  && pip install -r /tmp/cli-requirements.txt

#COPY --from=lab_packages ${LAB_DIST} ${LAB_DIST}
#RUN echo "Installing Lab Partner utilities" \
#    && pip install ${LAB_DIST}/utils/lab_partner_utils-${LAB_VERSION}-py3-none-any.whl

COPY images/cli/bashrc ${HOME}/.bashrc
COPY images/cli/start-cli.sh /opt/bin/
COPY environments/local /opt/lab/
COPY images/cli/cli_sudoers /etc/sudoers.d/

CMD ["/opt/bin/start-cli.sh"]


#################################################################
## Jupyter
#################################################################
FROM lab_cli as lab_jupyter
ENV NUMBA_CACHE_DIR=${HOME}

RUN apt-get update \
    && apt-get install -yq --no-install-recommends \
        libsm6 \
        libxext6 \
        libxrender-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && mkdir -p ${HOME}/.jupyter \
    && mkdir -p ${HOME}/.local/share/jupyter

COPY images/jupyter/requirements.txt /tmp/jupyter-requirements.txt
RUN pip install -r /tmp/jupyter-requirements.txt

COPY images/jupyter/jupyter_lab_config.py ${HOME}/.jupyter
COPY images/jupyter/start-jupyter.sh /opt/bin
CMD ["/opt/bin/start-jupyter.sh"]