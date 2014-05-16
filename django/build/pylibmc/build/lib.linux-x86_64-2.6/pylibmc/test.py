# Copyright 2014 Open Connectome Project (http;//openconnecto.me)
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Test utils."""

import os
import socket
import _pylibmc, pylibmc
from textwrap import dedent

class NotAliveError(Exception):
    template = dedent("""
    test memcached %s:%s not alive

    consider setting MEMCACHED_HOST and/or MEMCACHED_PORT
    to something more appropriate.""").lstrip()

    def __init__(self, svr):
        (self.server_type, self.address, self.port) = svr

    def __str__(self):
        return self.template % (self.address, self.port)

def get_version(addr):
    (type_, host, port) = addr
    if (type_ != _pylibmc.server_type_tcp):
        raise NotImplementedError("test server can only be on tcp for now")
    else:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect((host, port))
            s.send("version\r\n")
            version = s.recv(4096)
        finally:
            s.close()
        if not version.startswith("VERSION ") or not version.endswith("\r\n"):
            raise ValueError("unexpected version return: %r" % (version,))
        else:
            version = version[8:-2]
        return version

def is_alive(addr):
    try:
        version = get_version(addr)
    except (ValueError, socket.error):
        version = None
    return (bool(version), version)

def make_test_client(cls=pylibmc.Client, env=None, server_type="tcp",
                     host="127.0.0.1", port=11211, **kwds):
    """Make a test client. `env` overrides keyword arguments.

    >>> make_test_client() is not None
    True
    """
    server_types = {"tcp": _pylibmc.server_type_tcp,
                    "udp": _pylibmc.server_type_udp,
                    "unix": _pylibmc.server_type_unix}

    if env is None:
        env = os.environ

    styp = env.get("MEMCACHED_TYPE", server_type)
    host = env.get("MEMCACHED_HOST", host)
    port = env.get("MEMCACHED_PORT", port)

    test_server = (server_types[styp], str(host), int(port))
    alive, version = is_alive(test_server)

    if alive:
        return cls([test_server], **kwds)
    else:
        raise NotAliveError(test_server)
