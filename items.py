global node, repo

pkg = {
    'curl': {},
    'apt-transport-https': {},
    'rspamd': {
        'installed': True,
        'needs': [
            'action:apt_update_cache',
        ],
    }
}

actions = {}
files = {}
config = node.metadata.get('rspamd', {})

actions['import_rspamd_apt_key'] = {
    'command': 'curl https://rspamd.com/apt-stable/gpg.key | apt-key --no-tty add -',
    'needs': [
        'pkg:curl',
    ]
}

actions['apt_update_cache'] = {
    'command': 'apt update',
    'needs': [
        'import_rspamd_apt_key',
        'file:/etc/apt/sources.list/rspamd.list',
    ]
}

actions['rpamd_woker_password'] = {
    'command':  'worker_password=$(rspamadm pw -p {worker_password}) && sed -s "/worker_password/$worker_password/g"'
                .format(worker_password=config.get('worker_password', repo.vault.password_for(
                    'rspamd_worker_password_{}'.format(node.name)))
                ),
    'needs': [
        'file:/etc/rspamd/local.d/worker-controller.inc',
    ],
}

files['/etc/apt/sources.list/rspamd.list'] = {
    'content': """
        deb http://rspamd.com/apt-stable/ stretch main
        deb-src http://rspamd.com/apt-stable/ stretch main
    """,
}

files['/etc/rspamd/local.d/options.inc'] = {
    'source': 'etc/rspamd/local.d/options.inc',
    'content_type': 'mako',
    'context': {
        'nameserver': config.get('nameserver'),
    }
}

files['/etc/rspamd/local.d/worker-normal.inc'] = {
    'source': 'etc/rspamd/local.d/worker-normal.inc',
}

files['/etc/rspamd/local.d/worker-controller.inc'] = {
    'source': 'etc/rspamd/local.d/worker-controller.inc',
}

files['/etc/rspamd/local.d/worker-proxy.inc'] = {
    'source': 'etc/rspamd/local.d/worker-proxy.inc',
}

files['/etc/rspamd/local.d/logging.inc'] = {
    'source': 'etc/rspamd/local.d/logging.inc',
}

files['/etc/rspamd/local.d/worker-controller.inc'] = {
    'source': 'etc/rspamd/local.d/milter_headers.conf',
}

files['/etc/rspamd/local.d/classifier-bayes.conf'] = {
    'source': 'etc/rspamd/local.d/classifier-bayes.conf',
}

files['/etc/rspamd/local.d/redis.conf'] = {
    'source': 'etc/rspamd/local.d/redis.conf',
}
