FROM debian:bullseye-slim

# 1. Installation de Kannel et des outils système
# On installe 'procps' pour le debug et on nettoie après
RUN apt-get update && \
    apt-get install -y kannel procps && \
    rm -rf /var/lib/apt/lists/*

# 2. CORRECTION CRITIQUE : Création forcée de l'utilisateur/groupe
# Si le paquet ne l'a pas fait, on le fait manuellement ici
RUN (getent group kannel || groupadd -r kannel) && \
    (getent passwd kannel || useradd -r -g kannel -s /bin/false -d /var/lib/kannel kannel)

# 3. Création des dossiers et attribution des permissions
# Maintenant que l'utilisateur 'kannel' existe à 100%, cette commande va marcher
RUN mkdir -p /var/log/kannel /var/spool/kannel && \
    touch /var/log/kannel/kannel.log /var/log/kannel/bearerbox.log /var/log/kannel/smsbox.log && \
    chown -R kannel:kannel /var/log/kannel /var/spool/kannel

# 4. Copie de la configuration
COPY kannel.conf /etc/kannel/kannel.conf

# 5. Script de démarrage robuste (Séquentiel)
RUN echo '#!/bin/bash\n\
touch /var/log/kannel/kannel.log /var/log/kannel/smsbox.log\n\
\n\
echo "--- Démarrage de Bearerbox ---"\n\
# On lance en arrière-plan (&) mais on garde la sortie visible\n\
/usr/sbin/bearerbox -v 0 /etc/kannel/kannel.conf &\n\
\n\
echo "--- Attente de 5 secondes ---"\n\
sleep 5\n\
\n\
echo "--- Démarrage de Smsbox ---"\n\
/usr/sbin/smsbox -v 0 /etc/kannel/kannel.conf\n\
' > /start.sh && chmod +x /start.sh
# 6. Sécurité : On passe en utilisateur kannel
USER kannel

CMD ["/start.sh"]
