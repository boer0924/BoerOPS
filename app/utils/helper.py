# -*- coding: utf-8 -*-

__all__ = ['get_dynamic_inventory']

def get_dynamic_inventory(proj, environ):
    return {
        proj.name: {
            'hosts': [{
                'hostname': h.ip_address,
                'port': h.ssh_port,
                'username': h.username,
                'password': h.password
            } for h in proj.hosts if h.environ == int(environ)],
            'vars': {
                'ansible_user': 'boer',
                'ansible_become': True,
                'ansible_become_method': 'sudo',
                'ansible_become_user': 'root',
                'ansible_become_pass': 'Admin@123'
            }
        }
    }
