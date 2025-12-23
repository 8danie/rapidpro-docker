#!/bin/bash

# ==========================================
# CONFIGURATION DE L'UTILISATEUR SIMPLE
# ==========================================
USER_EMAIL="user@gmail.com"
USER_PASS="user123"
ORG_NAME="Mon Organisation"

# Rôle souhaité :
# 'E' = Éditeur (Peut voir et modifier les flux/contacts) -> Recommandé pour les employés
# 'V' = Visiteur (Lecture seule, ne peut rien modifier)
# 'A' = Administrateur (Tous les droits)
USER_ROLE="E"
# ==========================================

echo "--------------------------------------------"
echo "👤 CRÉATION D'UN UTILISATEUR STANDARD"
echo "--------------------------------------------"

docker-compose exec -T rapidpro /rapidpro/.venv/bin/python manage.py shell <<EOF
import sys
from django.contrib.auth import get_user_model
from temba.orgs.models import Org, OrgMembership

# --- 1. TRANSFERT DES VARIABLES BASH VERS PYTHON ---
p_email = "$USER_EMAIL"
p_password = "$USER_PASS"
p_org_name = "$ORG_NAME"
p_role = "$USER_ROLE"

User = get_user_model()

print(f"🔹 Traitement pour : {p_email}")

try:
    # --- 2. RÉCUPÉRATION DE L'ORGANISATION ---
    # On cherche l'organisation exacte
    try:
        org = Org.objects.get(name=p_org_name)
    except Org.DoesNotExist:
        # Si on ne trouve pas par nom, on prend la première (mode secours)
        print(f"⚠️ Organisation '{p_org_name}' introuvable. Recherche d'une autre...")
        org = Org.objects.first()
        
    if not org:
        print("❌ ERREUR : Aucune organisation n'existe. Lancez d'abord install_rapidpro.sh")
        sys.exit(1)
        
    print(f"   🏢 Organisation cible : {org.name}")

    # --- 3. CRÉATION DE L'UTILISATEUR ---
    user, created = User.objects.get_or_create(email=p_email)
    
    # Configuration "User Simple" (Pas de barre rouge)
    user.set_password(p_password)
    user.is_active = True
    user.is_staff = False       # Important : Pas d'accès technique
    user.is_superuser = False   # Important : Pas d'accès global
    user.save()
    
    if created:
        print("   ✅ Compte utilisateur créé.")
    else:
        print("   ℹ️ Compte utilisateur mis à jour.")

    # --- 4. ATTRIBUTION DU RÔLE (MEMBERSHIP) ---
    # On lie l'utilisateur à l'organisation avec le rôle choisi
    membership, mem_created = OrgMembership.objects.update_or_create(
        org=org,
        user=user,
        defaults={'role_code': p_role}
    )
    
    role_name = "ÉDITEUR" if p_role == 'E' else "VISITEUR"
    print(f"   🔑 Rôle attribué : {role_name} (Code: {p_role})")

    # --- 5. FINALISATION ---
    # On définit cette org comme l'org par défaut à la connexion
    user.org = org
    user.save()
    
    print("\n🎉 SUCCÈS : Utilisateur prêt !")
    print(f"👉 Login : {p_email}")
    print(f"👉 Pass  : {p_password}")

except Exception as e:
    print(f"\n❌ ERREUR PYTHON : {e}")
    sys.exit(1)
EOF
