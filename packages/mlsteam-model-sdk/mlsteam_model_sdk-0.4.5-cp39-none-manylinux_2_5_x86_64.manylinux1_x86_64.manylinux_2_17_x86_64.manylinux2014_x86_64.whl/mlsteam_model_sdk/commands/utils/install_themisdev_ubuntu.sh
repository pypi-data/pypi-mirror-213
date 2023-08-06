#!/bin/bash

DEBIAN_FRONTEND=noninteractive
apt_update=0

install_apt_pkg () {
    if [ $apt_update -eq 0 ]; then
        apt-get update -y
        apt_update=1
    fi
    apt-get install -y "$1"
}

ensure_wget_exists () {
    wget --version
    if [ $? -ne 0 ]; then
        install_apt_pkg wget
    fi
}

ensure_lsb_release_exists () {
    lsb_release --help
    if [ $? -ne 0 ]; then
        install_apt_pkg lsb-release
    fi
}

install_apt_pkg apt-transport-https
install_apt_pkg ca-certificates
ensure_wget_exists
ensure_lsb_release_exists

wget -qO - https://pkgs-ce.cossacklabs.com/gpg | apt-key add - && \
RELEASE=$(lsb_release -cs) && \
OS_NAME=$(lsb_release -is) && \
OS_NAME=${OS_NAME,,} && \
echo "deb https://pkgs-ce.cossacklabs.com/stable/${OS_NAME} ${RELEASE} main" | \
    tee /etc/apt/sources.list.d/cossacklabs.list
apt-get update
apt-get install libthemis-dev -y
echo "Themis dev installation done."
