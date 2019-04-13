# Copyright (c) 2019 Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


class ModuleGroup(object):
    MODULES = [
        'docker_compose',
        'docker_config',
        'docker_container',
        'docker_container_info',
        'docker_host_info',
        'docker_image',
        'docker_image_facts',
        'docker_image_info',
        'docker_login',
        'docker_network',
        'docker_network_info',
        'docker_node',
        'docker_node_info',
        'docker_prune',
        'docker_secret',
        'docker_service',
        'docker_swarm',
        'docker_swarm_info',
        'docker_swarm_service',
        'docker_swarm_service_info',
        'docker_volume',
        'docker_volume_info',
    ]
