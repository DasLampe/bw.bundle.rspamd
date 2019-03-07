# Rspamd via Bundlewrap
Install and configure Rspamd via Bundlewrap.

Config based on [Mailserver mit Dovecot, Postfix, MySQL und Rspamd unter Debian 9 Stretch](https://thomas-leister.de/mailserver-debian-stretch)

## Config
```python
'rspamd': {
    'nameserver': '127.0.0.1',
    'worker_password': '[generated]'
}
```

## Dependencies
- redis, e.g. [redis via Bundlewrap](https://github.com/DasLampe/bw.bundle.redis)
- [pkg_wrapper for Bundlewrap](https://github.com/DasLampe/bw.item.pkg_wrapper)

## Suggestions
- [Dovecot via Bundlewrap](https://github.com/DasLampe/bw.bundle.dovecot)
- [Postfix via Bundlewrap](https://github.com/DasLampe/bw.bundle.postfix)

## Known issues
- Hardcoded "stretch" in Repository file

## Author
André Flemming <daslampe@lano-crew.org>