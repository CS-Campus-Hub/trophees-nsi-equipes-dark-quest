"""level_hacker.py – Niveau 2 : Le Labo de Z3r0 (5 missions)"""
from visual_style import *
from level_engine import run_level

MISSIONS = [
    # correct = 2 (droite)
    {
        "npc": "Premier test. Qu'est-ce qu'un malware ?",
        "opts": [
            "Un antivirus trop lent qui ralentit l'ordinateur.",
            "Une mise a jour automatique non desiree du systeme.",
            "Un logiciel malveillant concu pour nuire, espionner ou voler des donnees."
        ],
        "correct": 2,
        "replies": [
            "Non. Un antivirus protege, il ne nuit pas. Arrete de confondre.",
            "Non. Les mises a jour corrigent des failles de securite, elles protegent.",
            "Exact. Virus, ransomware, spyware, cheval de Troie... tous sont des malwares."
        ],
        "lesson": "Types : virus (se copie), ransomware (crypte les fichiers), spyware (espionne), trojan (se cache)."
    },
    # correct = 1 (milieu)
    {
        "npc": "Les Rossi ont chiffre les fichiers de ta famille avec un ransomware. Que faire ?",
        "opts": [
            "Payer la rancon rapidement pour recuperer les fichiers le plus vite possible.",
            "Contacter les autorites et restaurer les donnees depuis une sauvegarde offline.",
            "Formater completement l'ordinateur et perdre toutes les donnees definitivement."
        ],
        "correct": 1,
        "replies": [
            "JAMAIS payer ! Ca finance les criminels et ne garantit pas du tout la recuperation.",
            "Correct. Les sauvegardes regulieres sont la vraie et seule protection efficace.",
            "Trop extreme. Avec des sauvegardes, on recupere tout sans payer et sans tout perdre."
        ],
        "lesson": "Regle 3-2-1 : 3 copies de tes donnees, sur 2 supports differents, dont 1 hors ligne."
    },
    # correct = 0 (gauche)
    {
        "npc": "Quelqu'un se fait passer pour ton banquier au telephone pour obtenir ton code. C'est quoi ?",
        "opts": [
            "De l'ingenierie sociale (vishing) : manipulation psychologique par telephone.",
            "Du phishing classique envoye par e-mail deguise en message de banque.",
            "Un bug technique de l'application bancaire qui envoie de fausses alertes."
        ],
        "correct": 0,
        "replies": [
            "Exactement. On appelle ca du vishing. Ta banque ne demandera JAMAIS ton code.",
            "Non. Le phishing c'est par e-mail/SMS. Au telephone, c'est du vishing.",
            "Rien a voir avec un bug. C'est une attaque humaine deliberee."
        ],
        "lesson": "Aucune banque ne demandera jamais ton code ou mot de passe par telephone. Raccroche toujours."
    },
    # correct = 2 (droite)
    {
        "npc": "Ton navigateur affiche : 'VIRUS DETECTE ! Appelez ce numero immediatement !' Que fais-tu ?",
        "opts": [
            "J'appelle le numero affiche pour qu'on nettoie mon ordinateur.",
            "Je clique sur le bouton 'Nettoyer maintenant' dans la pop-up.",
            "J'ignore et je ferme l'onglet. C'est du scareware, une arnaque classique."
        ],
        "correct": 2,
        "replies": [
            "En appelant, tu donnes acces a ton ordi a des criminels. C'est leur piege !",
            "Ce bouton installe le vrai malware. La pop-up est un mensonge complet.",
            "Parfait ! C'est du scareware : une fausse alerte pour te faire paniquer et payer."
        ],
        "lesson": "Les vraies alertes de securite ne demandent jamais d'appeler un numero ou de payer."
    },
    # correct = 0 (gauche)
    {
        "npc": "Comment verifier qu'un site est securise avant d'entrer tes donnees personnelles ?",
        "opts": [
            "Verifier le HTTPS, le cadenas et lire l'URL complete du domaine.",
            "Si le design est beau et professionnel, le site est necessairement fiable.",
            "Si Google le met en premier resultat de recherche, il est forcement securise."
        ],
        "correct": 0,
        "replies": [
            "Excellent ! HTTPS + cadenas + URL exacte : les 3 verifications indispensables.",
            "Les faux sites peuvent etre tres bien faits. Le design ne prouve absolument rien.",
            "Les sites frauduleux peuvent apparaitre en pub en premier. Mefie-toi toujours."
        ],
        "lesson": "Toujours verifier : https://, le nom de domaine exact, et les mentions legales du site."
    },
]

CONFIG = {
    "draw_bg":    draw_hacker_interior,
    "npc_fn":     draw_hacker,
    "npc_name":   "Z3r0  [Hacker]",
    "border_col": HACK_ACCENT,
    "level_num":  2,
    "missions":   MISSIONS,
}

def run(screen, clock, char_tag):
    return run_level(screen, clock, char_tag, CONFIG)