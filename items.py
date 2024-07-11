global node, repo

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
    'actions.conf'
]

if config.get('mx_check').get('enabled'):
    config_files.append('mx_check.conf')

if config.get('rbl').get('enabled'):
    config_files.append('rbl.conf')

if config.get('greylist').get('enabled'):
    config_files.append('greylist.conf')

override_files = [
    'worker-fuzzy.inc',
]

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

files = {
    '/etc/apt/sources.list.d/rspamd.list': {
        'content': f"""
            deb [arch=amd64 signed-by=/etc/apt/keyrings/rspamd.gpg] https://rspamd.com/apt-stable/ {node.metadata.get('debian', {}).get('release_name', 'bullseye')} main
            deb-src [arch=amd64 signed-by=/etc/apt/keyrings/rspamd.gpg] https://rspamd.com/apt-stable/ {node.metadata.get('debian', {}).get('release_name', 'bullseye')} main
        """,
    },
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
        ]
    }
