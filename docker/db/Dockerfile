FROM postgres:17-bullseye

RUN openssl req -new -x509 -days 365 -nodes -text -out /etc/postgresql/server.crt -keyout /etc/postgresql/server.key -subj '/CN=localhost' \
    && chown postgres:postgres /etc/postgresql/server.key \
    && chmod 600 /etc/postgresql/server.key

RUN chown postgres:postgres /etc/postgresql/server.key \
    && chmod 600 /etc/postgresql/server.key

CMD ["-c", "ssl=on", "-c", "ssl_cert_file=/etc/postgresql/server.crt", "-c", "ssl_key_file=/etc/postgresql/server.key"]
