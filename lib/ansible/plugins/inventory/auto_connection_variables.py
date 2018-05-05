# Copyright (c) 2018 Paul Arthur
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = '''
  name: auto_connection_variables
  plugin_type: inventory
  short_description: Sets ansible_host based on reachability
  description:
    - Checks a list of connection candidates and sets ansible_host and ansible_port to the first one that's reachable.
    - Uses a <name>.yaml (or <name>.yml) YAML configuration file.
  options:
    connection_candidates:
      description: Ordered list of connection candidates as either plain strings or mappings with 'host' and (optionally) 'port'.
                   If no port is provided, the default is 22.
      required: yes
    connection_timeout:
      description: Socket connection timeout, in seconds. Low values may fail to detect open ports, high values may cause very slow inventory loads.
      default: 1
'''

EXAMPLES = '''
plugin: auto_connection_variables
connection_timeout: 0.5
connection_candidates:
  - host: private_ip_address
    port: 8822
  - private_ip_address
  - public_ip_address
'''

import os
import socket

from collections import Mapping

from ansible import constants as C
from ansible.errors import AnsibleParserError
from ansible.inventory.helpers import get_group_vars
from ansible.module_utils._text import to_native
from ansible.plugins.inventory import BaseInventoryPlugin, Constructable
from ansible.utils.vars import combine_vars


class InventoryModule(BaseInventoryPlugin, Constructable):
    NAME = 'auto_connection_variables'

    def __init__(self):
        super(InventoryModule, self).__init__()

    def verify_file(self, path):
        if super(InventoryModule, self).verify_file(path):
            file_name, ext = os.path.splitext(path)
            if ext in C.YAML_FILENAME_EXTENSIONS:
                return True
        return False

    def parse(self, inventory, loader, path, cache=False):
        super(InventoryModule, self).parse(inventory, loader, path)

        config_data = self._read_config_data(path)
        if 'connection_candidates' not in config_data:
            raise AnsibleParserError("failed to parse %s: no connection_candidates" % to_native(path))
        connect_timeout = config_data.get('connection_timeout', 1)

        for hostname in inventory.hosts:
            hostvars = combine_vars(get_group_vars(inventory.hosts[hostname].get_groups()), inventory.hosts[hostname].get_vars())
            for candidate in config_data['connection_candidates']:
                if 'ansible_port' in hostvars:
                    port = hostvars['ansible_port']
                else:
                    port = 22
                if isinstance(candidate, Mapping):
                    if 'host' not in candidate:
                        raise AnsibleParserError("failed to parse %s: connection_candidates contains a mapping without 'host'" % to_native(path))
                    host = self._compose(candidate['host'], hostvars)
                    if 'port' in candidate:
                        port = self._compose(candidate['port'], hostvars)
                else:
                    host = self._compose(candidate, hostvars)

                try:
                    connection = socket.create_connection((host, int(port)), connect_timeout)
                except socket.error:
                    pass
                else:
                    try:
                        connection.shutdown(socket.SHUT_RDWR)
                    except socket.error:
                        pass
                    else:
                        connection.close()

                    self.inventory.set_variable(hostname, 'ansible_host', host)
                    self.inventory.set_variable(hostname, 'ansible_port', int(port))
                    break
