FROM debian:12-slim
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends \
    samba samba-dsdb-modules samba-vfs-modules krb5-user dnsutils \
    netcat-openbsd ca-certificates python3 && \
    rm -rf /var/lib/apt/lists/*
COPY entrypoint.sh /usr/local/bin/armor-dc-entrypoint
RUN chmod 755 /usr/local/bin/armor-dc-entrypoint
EXPOSE 53/tcp 53/udp 88/tcp 88/udp 135/tcp 139/tcp 389/tcp 389/udp 445/tcp 464/tcp 464/udp 3268/tcp
ENTRYPOINT ["/usr/local/bin/armor-dc-entrypoint"]
