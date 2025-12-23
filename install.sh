#!/bin/bash

echo "🛑 ARRÊT ET NETTOYAGE COMPLET..."
# 1. On supprime les conteneurs
docker-compose down

# 2. CRUCIAL : On supprime le volume de la base de données corrompue
# (Adaptez le nom si votre dossier ne s'appelle pas 'rapidpro-docker')
echo "🗑️ Suppression du volume de base de données..."
docker volume rm rapidpro-docker_postgres
docker volume rm rapidpro-docker_valkey
docker volume rm rapidpro-docker_static_content

echo "🚀 REDÉMARRAGE..."
docker-compose up -d

echo "⏳ Attente de 30 secondes pour l'initialisation de la DB..."
sleep 30

echo "📦 Génération des fichiers statiques (CSS/JS)..."
docker-compose exec -T rapidpro /rapidpro/.venv/bin/python manage.py collectstatic --noinput

echo "🏗️ CRÉATION DES DONNÉES (ADMIN + ORG + INITIALIZE)..."
docker-compose exec -T rapidpro /rapidpro/.venv/bin/python manage.py shell <<EOF
import sys
from django.contrib.auth import get_user_model
from temba.orgs.models import Org, OrgMembership

User = get_user_model()

try:
    # 1. ADMIN
    print(">> Création Admin...")
    admin, _ = User.objects.get_or_create(email="admin@gmail.com")
    admin.set_password("admin123")
    admin.is_superuser = True
    admin.is_staff = True
    admin.is_active = True
    admin.save()

    # 2. ORGANISATION (LA MÉTHODE CORRECTE)
    print(">> Création Organisation...")
    if not Org.objects.filter(name="Mon Organisation").exists():
        org = Org.objects.create(
            name="Mon Organisation",
            timezone="Africa/Bujumbura",
            language="fr",
            created_by=admin,
            modified_by=admin
        )
        
        # C'EST ICI QUE LA MAGIE OPÈRE
        print(">> INITIALISATION INTERNE (Création des groupes/champs)...")
        org.initialize()
        
        # Config Langues
        org.flow_languages = ["fra", "eng"]
        org.primary_language = "fra"
        org.save()
        
        # Droits Admin (Code 'A' pour v10)
        OrgMembership.objects.create(org=org, user=admin, role_code='A')
        
        # Org par défaut
        admin.org = org
        admin.save()
        print("✅ SUCCÈS : Organisation créée et initialisée proprement.")
    else:
        print("ℹ️ L'organisation existe déjà (bizarre après un reset).")

except Exception as e:
    print(f"❌ ERREUR : {e}")
    sys.exit(1)
EOF

echo "-----------------------------------------------"
echo "✅ TERMINÉ ! Connectez-vous sur http://100.42.186.218:81/"
echo "👤 User: admin@gmail.com"
echo "🔑 Pass: admin123"
echo "-----------------------------------------------"
