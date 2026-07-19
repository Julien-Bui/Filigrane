@echo off
cd /d "%~dp0"

:: Créer l'environnement virtuel s'il n'existe pas
if not exist ".venv\" (
    echo 🛠️ Creation de l'environnement virtuel pour la premiere fois...
    python -m venv .venv
    call .venv\Scripts\activate.bat
    pip install -r requirements.txt
) else (
    :: Activer l'environnement virtuel
    call .venv\Scripts\activate.bat
)

:: Lancer l'application
python main.py
pause
