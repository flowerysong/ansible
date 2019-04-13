# Copyright (c) 2019 Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


class ModuleGroup(object):
    MODULES = [
        'k8s',
        'k8s_auth',
        'k8s_facts',
        'k8s_info',
        'k8s_scale',
        'k8s_service',
        'kubevirt_cdi_upload',
        'kubevirt_preset',
        'kubevirt_pvc',
        'kubevirt_rs',
        'kubevirt_template',
        'kubevirt_vm',
    ]
