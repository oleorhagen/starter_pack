#!/usr/bin/env python3

import sys
import logging
import json
from collections import OrderedDict

import invoke
import fabric
from paramiko.ssh_exception import AuthenticationException

from cf_remote.utils import os_release, column_print, pretty

log = logging.getLogger(__name__)

def ssh_cmd(c, cmd):
    try:
        log.debug("'{}'".format(cmd))
        result = c.run(cmd, hide=True)
        return result.stdout.strip()
    except invoke.exceptions.UnexpectedExit:
        return None

def print_info(data):
    log.debug(pretty(data))
    output = OrderedDict()

    os_release = data["os_release"]
    os = like = None
    if os_release:
        if "ID" in os_release:
            os = os_release["ID"]
        if "ID_LIKE" in os_release:
            like = os_release["ID_LIKE"]
    if not os:
        os = data["uname"]
    if os and like:
        output["OS"] = "{} ({})".format(os, like)
    elif os:
        output["OS"] = "{}".format(os)
    else:
        output["OS"] = "Unknown"

    agent_version = data["agent_version"]
    if agent_version:
        output["CFEngine"] = agent_version
    else:
        output["CFEngine"] = "Not installed"

    column_print(output)

def info(hosts, users=None):
    host = hosts[0]
    if not users:
        users =  ["root", "ubuntu", "vagrant"]
    for user in users:
        try:
            c = fabric.Connection(host=host, user=user)
            break
        except AuthenticationException:
            continue
    data = OrderedDict()
    data["ssh_user"] = user
    data["ssh_host"] = host
    data["whoami"] = ssh_cmd(c, "whoami")
    data["uname"] = ssh_cmd(c, 'uname')
    data["os_release"] = os_release(ssh_cmd(c, "cat /etc/os-release"))
    data["agent_location"] = ssh_cmd(c, "which cf-agent")
    data["agent_version"] = ssh_cmd(c, "cf-agent --version")
    data["dpkg_location"] = ssh_cmd(c, "which dpkg")
    data["bin"] = {}
    for bin in ["dpkg", "rpm", "yum", "apt", "pkg"]:
        path = ssh_cmd(c, "which {}".format(bin))
        if path:
            data["bin"][bin] = path
    print_info(data)
