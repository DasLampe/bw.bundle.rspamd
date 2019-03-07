local_addrs = "127.0.0.0/8, ::1";

dns {
    nameserver = ["${nameserver}:10"];
}