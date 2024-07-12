local_addrs = "${', '.join(cfg.get('local_addrs'))}";

control_socket = "$DBDIR/rspamd.sock mode=0600 owner=${cfg.get('user')}";

dns {
    nameserver = ${cfg.get('nameservers')};
}

neighbours {
% for name, server in cfg.get('neighbours').items():
    ${name} {
        host = "${server.get('host')}";
        % if server.get('path', False):
        path = "${server.get('path')}";
        % endif
    }
 % endfor
}