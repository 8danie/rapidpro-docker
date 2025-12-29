FROM debian:bullseye-slim

# 1. Installation de Kannel et Supervisor
RUN apt-get update && \
    apt-get install -y kannel supervisor procps && \
    rm -rf /var/lib/apt/lists/*

# 2. Création sécurisée de l'utilisateur (si manquant)
RUN (getent group kannel || groupadd -r kannel) && \
    (getent passwd kannel || useradd -r -g kannel kannel)

# 3. Préparation des dossiers
# On ajoute /var/run/kannel pour le PID de supervisor
RUN mkdir -p /var/log/kannel /var/spool/kannel /var/run/kannel && \
    touch /var/log/kannel/kannel.log /var/log/kannel/smsbox.log && \
    chown -R kannel:kannel /var/log/kannel /var/spool/kannel /var/run/kannel

# 4. Copie des configurations
COPY kannel.conf /etc/kannel/kannel.conf
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# 5. Sécurité
USER kannel

# 6. Lancement via Supervisor
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
