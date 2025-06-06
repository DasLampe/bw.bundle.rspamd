global node, repo
from bundlewrap.utils import get_file_contents
from os.path import join

files = {}
directories = {}

config = node.metadata.get('rspamd', {})

config_files = [
    'redis.conf',
    'classifier-bayes.conf',
    'milter_headers.conf',
    'logging.inc',
    'worker-controller.inc',
    'worker-proxy.inc',
    'worker-normal.inc',
    'logging.inc',
    'options.inc',
    'actions.conf',
    'rbl_group.conf',
    'settings.conf',
    'multimap.conf',
]

override_files = [
    'worker-fuzzy.inc',
    'dkim_signing.conf',
]

if config.get('mx_check').get('enabled'):
    config_files.append('mx_check.conf')

if config.get('rbl').get('enabled'):
    config_files.append('rbl.conf')

if config.get('greylist').get('enabled'):
    config_files.append('greylist.conf')

if config.get('dkim').get('enabled'):
    config_files.append('dkim_signing.conf')
    config_files.append('arc.conf')

    # Copy key files per domain
    dkim_conf = config.get('dkim')
    directories[dkim_conf.get('path')] = {
        'owner': config.get('user'),
        'group': config.get('group'),
        'needs': [
            'pkg_apt:rspamd',
        ]
    }
    for domain, domain_config in dkim_conf.get('domains').items():
        selector = domain_config.get('selector', dkim_conf.get('selector'))

        files[f"{dkim_conf.get('path')}/{domain}.{selector}.key"] = {
            'content': repo.vault.decrypt_file(
                join(repo.path, 'data', 'dkim_keys', config.get('key', f'{domain}.{selector}.key'))
            ),
            'content_type': 'text',
            'owner': config.get('user'),
            'group': config.get('group'),
            'mode': '0400',
            'needs': [
                f'directory:{dkim_conf.get('path')}',
            ]
        }

map_files = {
    'greylist-whitelist-ip.inc': config.get('greylist').get('whitelist').get('ips'),
    'greylist-whitelist-domains.inc': config.get('greylist').get('whitelist').get('domains'),
    'multimap-blacklist-subjects.inc': config.get('multimap').get('blacklist').get('subjects'),
}

svc_systemd = {
    'rspamd': {
        'enabled': True,
        'running': True,
        'needs': [
            'action:import_rspamd_apt_key',
            'pkg_apt:rspamd',
        ]
    }
}

actions = {
    'import_rspamd_apt_key': {
        'command': 'wget -O- https://rspamd.com/apt-stable/gpg.key | gpg --dearmor > /etc/apt/keyrings/rspamd.gpg',
        'unless': 'test -f  /etc/apt/keyrings/rspamd.gpg',
        'needs': [
            'pkg_apt:gpg',
            'pkg_apt:wget',
        ],
        'triggers': [
            'action:apt_update_cache',
        ]
    },

    'apt_update_cache': {
        'command': 'apt update',
        'needs': [
            'file:/etc/apt/sources.list.d/rspamd.list',
        ],
        'triggered': True
    },
}

files['/etc/apt/sources.list.d/rspamd.list'] = {
    'content': f"""
        deb [arch=amd64 signed-by=/etc/apt/keyrings/rspamd.gpg] https://rspamd.com/apt-stable/ {node.metadata.get('debian', {}).get('release_name', 'bullseye')} main
        deb-src [arch=amd64 signed-by=/etc/apt/keyrings/rspamd.gpg] https://rspamd.com/apt-stable/ {node.metadata.get('debian', {}).get('release_name', 'bullseye')} main
    """,
}

for file in config_files:
    files[f'/etc/rspamd/local.d/{file}'] = {
        'source': f'etc/rspamd/local.d/{file}',
        'content_type': 'mako',
        'context': {
            'cfg': config,
        },
        'triggers': [
            'svc_systemd:rspamd:restart',
        ],
        'needs': [
            'pkg_apt:rspamd'
        ]
    }

for file in override_files:
    files[f'/etc/rspamd/override.d/{file}'] = {
        'source': f'etc/rspamd/override.d/{file}',
        'content_type': 'mako',
        'context': {
            'cfg': config,
        },
        'triggers': [
            'svc_systemd:rspamd:restart',
        ],
        'needs': [
            'pkg_apt:rspamd'
        ]
    }

for file_name, content in map_files.items():
    files[f'/etc/rspamd/maps.d/{file_name}'] = {
        'content': "\n".join(content) + "\n",
        'owner': config.get('user'),
        'group': config.get('group'),
        'triggers': [
            'svc_systemd:rspamd:restart',
        ],
        'needs': [
            'pkg_apt:rspamd'
        ]
    }
