# Project SafeCity

## Prérequis
- Windows / Linux / macOS
- Python **3.11.14**
- Git
- PowerShell (Windows)

---

## Installation du projet (méthode officielle)

### 1️⃣ Cloner le repository
```bash
git clone https://github.com/mariamenni/project_safecity.git
cd project_safecity

🔹 2. Installer Python 3.11.14 (version OBLIGATOIRE pour streamlitcloud)
Vérifier d’abord :
python --version


🔹 3. Installer uv (gestionnaire d’environnement)
Windows (PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

🔹 4. Créer l’environnement 
uv sync

🔹 5. Activer l’environnement
Windows
.venv\Scripts\activate

Linux / macOS
source .venv/bin/activate

