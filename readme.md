# Dark Quest 2D

**Trophées NSI 2025-2026 — Dossier n°2108**  
Lycée Français Alioune Blondin Beye — Luanda, Angola

## Présentation

Dark Quest 2D est un jeu éducatif développé en Python/Pygame. Le joueur est un adolescent dont la famille a été kidnappée par la mafia.Pour la libérer, il traverse 3 niveaux en répondant à des quiz sur la cybersécurité: mots de passe, phishing, malwares, ransomware et RGPD.

## Équipe

|Membre|Classe|Contributions|
|-|-|-|
|Yasmine Viegas|Terminale NSI|Scénario, questions cybersécurité, main.py|
|Rayan Haidar|Terminale NSI|level\_engine.py, level\_bar.py, level\_hacker.py, débogage|
|Alexandra Fontoura|Terminale NSI|visual\_style.py, level\_mafia.py, Organisation des fichiers du projet,Coordination technique de l'équipe|

## Installation

```bash
pip install -r requirements.txt
python sources/main.py
```

## Structure du projet

```
sources/        → Code source Python
data/           → Images et sprites
docs/           → Dossier technique PDF
```

## Fonctionnalités

* 2 personnages jouables : Charles ou Célia
* 3 niveaux : Bar du Détective Moreau, Labo de Z3r0, Repaire Don Rossi
* 15 questions de cybersécurité (5 par niveau)
* Système de 4 vies et score en étoiles
* 3 langues : français, anglais, portugais
* Personnages animés dessinés entièrement en Python

## Technologies

* Python 3
* Pygame 2.x
* Pillow (PIL)

