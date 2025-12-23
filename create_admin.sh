#!/bin/bash

# Configuration de l'admin
EMAIL="admin@gmail.com"
PASSWORD="admin123"

echo "----------------------------------------------------------------"
echo "Gestion du superutilisateur : $EMAIL"
echo "----------------------------------------------------------------"

# On exécute un script Python directement dans le conteneur via stdin
docker-compose exec -T rapidpro /rapidpro/.venv/bin/python manage.py shell <<EOF
from django.contrib.auth import get_user_model
import sys

User = get_user_model()
email = "$EMAIL"
password = "$PASSWORD"

# Vérification si l'utilisateur existe
if User.objects.filter(email=email).exists():
    print(f"L'utilisateur {email} existe déjà.")
    
    # --- AJOUT : On force l'activation même s'il existait déjà ---
    u = User.objects.get(email=email)
    if not u.is_active or not u.is_superuser:
        print("Mise à jour des droits et validation de l'email...")
        u.is_active = True      # <--- C'est ici que la vérification est annulée
        u.is_staff = True
        u.is_superuser = True
        u.save()
        print("CORRIGÉ : L'utilisateur existant est maintenant actif et superadmin.")
    else:
        print("L'utilisateur est déjà correctement configuré.")

else:
    try:
        print(f"Création de l'utilisateur {email}...")
        # Création manuelle
        u = User(email=email)
        u.set_password(password)
        
        # --- CONFIGURATION DES DROITS ET VALIDATION ---
        u.is_active = True      # <--- Active le compte immédiatement (pas d'email de vérif)
        u.is_superuser = True   # <--- Donne tous les droits
        u.is_staff = True       # <--- Donne accès à l'admin /staff/
        
        u.save()
        print(f"SUCCÈS : Superutilisateur {email} créé et ACTIVÉ !")
    except Exception as e:
        print(f"ERREUR CRITIQUE : {e}")
        sys.exit(1)
EOF
