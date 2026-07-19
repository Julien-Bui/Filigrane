#!/bin/bash
# Aller dans le répertoire du script
cd "$(dirname "$0")"

# Créer l'environnement virtuel s'il n'existe pas
if [ ! -d ".venv" ]; then
    echo "🛠️ Création de l'environnement virtuel pour la première fois..."
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
else
    # Activer l'environnement virtuel
    source .venv/bin/activate
fi

# Lancer l'application
python main.py
