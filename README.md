# Image & PDF Watermarker

Un utilitaire Python autonome et robuste pour transformer n'importe quelle image ou document PDF en y appliquant un filigrane textuel personnalisé. 

## Fonctionnalités

- **Agnostique au format d'entrée** : Supporte les documents PDF ainsi que les images (PNG, JPEG, WEBP, BMP, etc.).
- **Filigrane Répété (Motif)** : Le texte est automatiquement répété en diagonale pour couvrir l'intégralité de la page ou de l'image (motif en quinconce).
- **Taille de Police Adaptative** : La taille du texte du filigrane s'adapte intelligemment à la longueur de votre phrase pour que tout reste lisible et esthétique.
- **Conversion PDF Standard** : Génère un fichier `.pdf` standardisé, utilisant les librairies industrielles de référence (`pypdf` + `reportlab`) pour garantir une compatibilité maximale.
- **Structure Claire** : Dossier d'entrée (`images/`) et dossier de sortie (`res/`) pour garder votre espace de travail propre.

## Installation

1. Clonez ce dépôt.
2. Créez un environnement virtuel pour isoler les dépendances :
   ```bash
   python -m venv .venv
   ```
3. Activez l'environnement virtuel :
   - **Linux/macOS** : `source .venv/bin/activate`
   - **Windows** : `.\.venv\Scripts\activate`
4. Installez les dépendances requises :
   ```bash
   pip install -r requirements.txt
   ```

## Utilisation

Le script est conçu pour être facile d'utilisation avec des raccourcis à la racine.

### Préparation

1. Placez vos images source ou vos fichiers PDF dans le dossier `images/`.

### Lancement via les scripts raccourcis (Recommandé)

Ces scripts s'occupent d'activer l'environnement virtuel pour vous :

- **Linux / macOS / WSL** :
  ```bash
  bash run.sh
  ```

- **Windows** :
  ```cmd
  .\run.bat
  ```

### Lancement manuel (Bash classique)

Si vous préférez lancer l'outil vous-même, sans utiliser les scripts raccourcis :

```bash
# Activation de l'environnement
source .venv/bin/activate

# Lancement du script principal
python main.py
```

L'application listera automatiquement les fichiers présents dans le dossier `images/` et vous demandera :
1. **Le numéro du fichier** que vous souhaitez traiter.
2. **Le texte** : le message à afficher en filigrane (ex: "CONFIDENTIEL", "Copie", etc.).
3. **Le fichier de sortie** : le nom du document PDF final (facultatif, par défaut le même nom que le fichier source).

Le fichier final protégé sera alors généré dans le dossier `res/` !

> [!WARNING]
> **Important : Compatibilité Adobe Acrobat**
> En raison des techniques de calques utilisées pour incruster le filigrane, il est déconseillé d'ouvrir le fichier PDF de sortie avec le logiciel Adobe Acrobat (qui peut parfois le bloquer ou le considérer comme corrompu). Privilégiez n'importe quel autre lecteur PDF standard (Aperçu sur Mac, votre navigateur web Chrome/Edge/Firefox, etc.).
