# Présentation — Dark Quest 2D

**Trophées NSI 2025-2026 — Dossier n°2108**  
Lycée Français Alioune Blondin Beye — Luanda, Angola

\---

## 1\. Résumé

Dark Quest 2D est un jeu éducatif en Python/Pygame où le joueur incarne un adolescent dont la famille est kidnappée par la mafia. Pour la libérer, il traverse 3 niveaux (bar, labo hacker, repaire mafia) en répondant à des quiz sur la cybersécurité. Mots de passe, phishing, malwares et RGPD sont abordés de façon ludique, avec personnages animés, système de vies et score en étoiles.

\---

## 2\. Description détaillée

Dark Quest 2D est développé entièrement en Python 3 avec Pygame. Le joueur choisit son personnage (Charles ou Célia), découvre le prologue de l'enlèvement de sa famille par les Rossi, puis explore une carte en vue du dessus. Il doit entrer dans trois bâtiments dans l'ordre pour progresser.

### Structure des fichiers

|Fichier|Rôle|
|-|-|
|main.py|Boucle principale, gestion de la carte, mouvements, états du jeu, Game Over|
|level\_engine.py|Moteur commun à tous les niveaux : phases QUESTION / WRONG\_FLASH / LESSON / SCORE|
|level\_bar.py|Niveau 1 — Bar du Détective Moreau (5 questions sur mots de passe, phishing)|
|level\_hacker.py|Niveau 2 — Labo de Z3r0 (5 questions sur malwares, ransomware, vishing)|
|level\_mafia.py|Niveau 3 — Repaire Don Rossi (5 questions sur firewall, OSINT, RGPD) + scène finale|
|visual\_style.py|Tous les visuels dessinés en Python pur : personnages pixel-art, décors, HUD, bulles|

### Mécanique de jeu

* 1 seule chance par question : bonne réponse → leçon affichée ; mauvaise réponse → flash rouge
* Score de 0 à 5 étoiles par niveau
* Système de 4 vies (cœurs) : chaque niveau raté retire 1 vie → Game Over à 0 vie
* Collecte de 12 pièces sur la carte pour débloquer le niveau 3 (seuil : 5 pièces)
* 3 langues disponibles : français, anglais, portugais
* Personnages animés dessinés entièrement en Python

\---

## 3\. Nature du code et répartition du travail

Le projet est une création originale. L'ensemble de la logique de jeu a été conçu et écrit par l'équipe à partir de zéro, sans copie de tutoriel.

### Yasmine Viegas

Conception du scénario complet et rédaction des 15 questions de cybersécurité (5 par niveau) avec leurs 3 options, réponses et leçons associées. Développement de main.py : boucle principale, gestion des états (menu, map, niveaux, victoire, game over), déplacement du joueur, collecte de pièces, système de 4 vies.

### Rayan Haidar

Architecture du projet et développement de level\_engine.py : moteur de niveaux, machine à états (QUESTION → WRONG\_FLASH → LESSON → SCORE\_SCREEN), correction du bug de fermeture, système de score multi-étoiles et multi-langue. Développement de level\_bar.py et level\_hacker.py.

### Alexandra Fontoura

Développement de visual\_style.py : fonctions de dessin des décors intérieurs, HUD avec 4 cœurs, bulles de dialogue, effets visuels. Remplacement des personnages pixel-art Python par des sprites Itch.io animés via spritesheets. Développement de level\_mafia.py et de la scène finale de libération.Coordination technique de l'équipe et Organisation des fichiers du projet.

\---

## 4\. Utilisation de l'Intelligence Artificielle

Conformément aux règles du concours, l'équipe déclare avec transparence tous les usages de l'IA dans ce projet.

**Claude (Anthropic) — Aide au débogage (\~30 % du code)**

* Identification et correction du bug de fermeture du jeu lors d'un clic sur une bonne réponse
* Aide à la correction de l'ordre de vérification du bouton SORTIR
* Explication du fonctionnement de `import \*` en Python

**IA conversationnelle — Reformulation pédagogique (\~5 % du contenu)**

* Certaines formulations de questions et de leçons ont été vérifiées et améliorées pour garantir leur exactitude technique. Les 15 questions ont été entièrement conçues par l'équipe, puis validées.

### Bilan global

|Élément|Équipe|IA|
|-|-|-|
|Code Python|70 % original|30 % débogage assisté|
|Contenu pédagogique|95 % original|5 % reformulation|
|Visuels / assets|100 % originaux|0 %|
|Scénario / game design|100 % original|0 %|

L'équipe certifie que le code, le scénario et le contenu pédagogique constituent une production originale, et que tous les usages de l'IA ont été limités, réfléchis et transparents.

