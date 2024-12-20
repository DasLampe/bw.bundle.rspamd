global node, repo

defaults = {
    'rspamd': {
        'user': '_rspamd',
        'group': '_rspamd',
        'worker_password': repo.vault.password_for(f'rspamd_worker_password_{node.name}').value,
        'redis_servers': {
            'redis': ['localhost'],
            # 'bayes': ['replication_master', 'localhost'],  # If Multiple, First is write, all other are read
            # 'fuzzy': ['localhost'],
            # 'greylist': ['localhost'],
            # 'mx_check': ['localhost'],
        },
        'mailserver_hostname': node.hostname,
        'extended_spam_headers': True,
        'skip_local': False,
        'skip_authenticated': True,
        'local_addrs': ['127.0.0.0/8', '::1'],
        'nameservers': ['127.0.0.1'],
        'mx_check': {
            'enabled': True,
            'exclude_domains': [
                "https://maps.rspamd.com/freemail/disposable.txt.zst",
                "https://maps.rspamd.com/freemail/free.txt.zst",
            ],
        },
        'rbl': {
            'enabled': True,
            'spamhaus_dqs_key': '',
        },
        'greylist': {
            'enabled': True,
            'whitelist': {
                'ips': [
                    '127.0.0.1',
                    '::1',
                ],
                'domains': [],
            },
        },
        'multimap': {
            'blacklist': {
                'subjects': [],
            }
        },
        'neighbours': {
            # 'server1': {'host': ''},
            # 'server2': {'host': 'localhost', 'path': '/rspamd'},
        },
        'dkim': {
            'enabled': False,
            'path': '/var/lib/rspamd/dkim',
            'selector': 'dkim',
            'domains':{},
        },
    },
    'apt': {
        'packages': {
            'wget': {},
            'gpg': {},
            'apt-transport-https': {},
            'rspamd': {
                'installed': True,
                'needs': [
                    'action:import_rspamd_apt_key',
                    'action:apt_update_cache',
                ],
            },
        },
    },
}
