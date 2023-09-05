local_addrs = "${', '.join(cfg.get('local_addrs'))}";

control_socket = "$DBDIR/rspamd.sock mode=0600 owner=${cfg.get('user')}";

dns {
    nameserver = ${cfg.get('nameservers')};
}