"""level_bar.py – Niveau 1 : Le Bar du Détective Moreau (5 missions)"""
from visual_style import *
from level_engine import run_level

MISSIONS = [
    # correct = 1 (milieu)
    {
        "npc": "Ils ont pirate le compte de ton pere. Qu'aurais-il du faire pour proteger ses mots de passe ?",
        "opts": [
            "Utiliser son prenom et sa date de naissance, facile a retenir.",
            "Un mot de passe long et unique par compte, avec chiffres et symboles.",
            "Partager son mot de passe avec un proche de confiance pour s'en souvenir."
        ],
        "correct": 1,
        "replies": [
            "Terrible ! C'est la premiere combinaison qu'un hacker essaie. Jamais ca.",
            "Parfait. Un mot de passe fort et unique par compte : c'est la base absolue.",
            "Ne JAMAIS partager un mot de passe, meme avec quelqu'un de confiance."
        ],
        "lesson": "Regle : 1 compte = 1 mot de passe fort (12+ caracteres, majuscules, chiffres, symboles)."
    },
    # correct = 0 (gauche)
    {
        "npc": "Les Rossi ont envoye un faux e-mail a ton pere. Comment reconnaitre un e-mail de phishing ?",
        "opts": [
            "Adresse suspecte, lien bizarre, ton urgent, fautes d'orthographe.",
            "Le logo de l'entreprise ne ressemble pas exactement a l'original.",
            "L'e-mail arrive apres 22h, les vraies entreprises n'envoient pas si tard."
        ],
        "correct": 0,
        "replies": [
            "Exact ! Ce sont les quatre signes classiques d'une tentative de phishing.",
            "Les logos se copient en 10 secondes. Ca ne prouve absolument rien.",
            "Les hackers envoient a toute heure. L'horaire n'est pas un indicateur fiable."
        ],
        "lesson": "Ne clique JAMAIS sur un lien dans un e-mail non sollicite. Verifie l'adresse complete."
    },
    # correct = 2 (droite)
    {
        "npc": "Ton telephone recoit : 'Votre colis est bloque. Cliquez ici.' Tu attends un colis. Que fais-tu ?",
        "opts": [
            "Je clique pour verifier, c'est peut-etre vrai, j'attends un colis.",
            "Je transfere le message a mes amis pour les avertir du probleme.",
            "J'ignore et je signale le SMS comme spam. C'est du smishing."
        ],
        "correct": 2,
        "replies": [
            "Pieige ! En cliquant tu risques d'installer un malware sur ton telephone.",
            "En transferant, tu propages l'attaque. Tes amis pourraient aussi cliquer.",
            "Parfait ! Le smishing (phishing par SMS) est tres repandu. Toujours ignorer."
        ],
        "lesson": "En cas de doute, contacte directement l'expediteur via ses coordonnees officielles."
    },
    # correct = 1 (milieu)
    {
        "npc": "Les Rossi ont surveille ta connexion au WiFi du cafe. Comment te proteger sur un WiFi public ?",
        "opts": [
            "Je me connecte normalement, le mot de passe WiFi protege mes donnees.",
            "J'utilise un VPN qui chiffre toutes mes communications.",
            "J'evite seulement les achats en ligne, le reste c'est sans risque."
        ],
        "correct": 1,
        "replies": [
            "Faux. Le mot de passe WiFi protege l'acces au reseau, pas tes donnees en transit.",
            "Exact ! Un VPN chiffre tout ton trafic, meme sur un reseau non securise.",
            "Tout est risque sur un WiFi public : e-mails, connexions, messages prives..."
        ],
        "lesson": "Sur tout WiFi public, utilise TOUJOURS un VPN. Tes donnees voyagent a decouvert sinon."
    },
    # correct = 2 (droite)
    {
        "npc": "Avant d'aller chez le hacker : qu'est-ce que la double authentification (2FA) ?",
        "opts": [
            "Deux mots de passe differents tapes l'un apres l'autre pour se connecter.",
            "Un systeme qui double automatiquement la longueur de mon mot de passe.",
            "Un second facteur (code SMS ou appli) exige en plus du mot de passe."
        ],
        "correct": 2,
        "replies": [
            "Non. Le 2FA c'est un DEUXIEME TYPE de verification, pas un second mot de passe.",
            "Ca n'existe pas. Le 2FA est un systeme complementaire entierement separe.",
            "Exactement ! Le 2FA bloque 99% des piratages meme si ton mot de passe est vole."
        ],
        "lesson": "Active le 2FA partout ou c'est possible. C'est le meilleur bouclier contre le piratage de compte."
    },
]

CONFIG = {
    "draw_bg":    draw_bar_interior,
    "npc_fn":     draw_detective,
    "npc_name":   "Detective Moreau",
    "border_col": DLGBRD,
    "level_num":  1,
    "missions":   MISSIONS,
}

def run(screen, clock, char_tag):
    return run_level(screen, clock, char_tag, CONFIG)