"""level_mafia.py – Niveau 3 + scène famille (images mafia_boy/girl) + message 5 lignes"""
import pygame, math
from visual_style import *
from level_engine import run_level, W, H

MISSIONS = [
    {"npc":"Tu as paye l'entree. Qu'est-ce qu'un pare-feu (firewall) ?",
     "opts":["Un antivirus installe sur le telephone.",
             "Un systeme filtrant le trafic reseau contre les intrusions.",
             "Un logiciel qui accelere la connexion internet."],
     "correct":1,
     "replies":["Non. L'antivirus protege les fichiers, le pare-feu protege le reseau.",
                "Exact. Sans pare-feu, ton reseau est une porte ouverte aux hackers.",
                "Faux. Un pare-feu securise les connexions, pas la vitesse."],
     "lesson":"Un pare-feu surveille et filtre toutes les connexions entrant et sortant."},
    {"npc":"Mes hommes ont localise ta famille via leurs reseaux sociaux. Quelle erreur ont-ils commise ?",
     "opts":["Partager trop d'infos personnelles publiquement : adresse, photos, habitudes.",
             "Utiliser des emojis dans leurs publications.",
             "Se connecter depuis un ordinateur plutot que depuis un telephone."],
     "correct":0,
     "replies":["Exact. L'OSINT (collecte de donnees publiques) est l'outil prefere des espions.",
                "Les emojis n'ont rien a voir. C'est le CONTENU partage qui etait dangereux.",
                "L'appareil n'importe pas. C'est ce qu'on publie qui est dangereux."],
     "lesson":"Sur les reseaux sociaux : minimise les infos personnelles. Rien de prive n'est vraiment prive."},
    {"npc":"Mes hommes ont craque le mot de passe 'football92' en 3 secondes. Pourquoi ?",
     "opts":["Ils ont devine par chance.",
             "Ils ont achete illegalement les donnees.",
             "Attaque par dictionnaire : programme testant des milliers de mots courants."],
     "correct":2,
     "replies":["Impossible. Les bons systemes bloquent apres quelques tentatives ratees.",
                "Meme dans ce cas, un bon mot de passe rendrait les donnees inutilisables.",
                "Exactement. 'football92', 'azerty', 'password123' se craquent en secondes."],
     "lesson":"N'utilise jamais de mots du dictionnaire ni d'informations personnelles comme mot de passe."},
    {"npc":"Tes amis ont recu un faux e-mail pretendant venir de toi. Qu'auraient-ils du verifier ?",
     "opts":["La longueur du message.",
             "L'adresse e-mail complete de l'expediteur, pas seulement le nom affiche.",
             "L'heure d'envoi."],
     "correct":1,
     "replies":["Faux. Les e-mails de phishing peuvent etre tres longs et bien rediges.",
                "Parfait ! Le nom affiche peut dire ton prenom, mais l'adresse reelle sera suspecte.",
                "Faux. Les attaques se font a toute heure."],
     "lesson":"Toujours verifier l'adresse e-mail COMPLETE de l'expediteur, pas seulement le nom affiche."},
    {"npc":"Derniere question. Que signifie le RGPD ?",
     "opts":["Reglement General sur la Protection des Donnees : tu controles tes infos.",
             "Reseau General de Protection contre les Dangers du Partage.",
             "Registre General des Personnes Declarees sur internet."],
     "correct":0,
     "replies":["Exact ! Le RGPD te donne le droit d'acces, rectification et effacement de tes donnees.",
                "Ce sigle n'existe pas. Le RGPD est une loi europeenne tres precise.",
                "Completement invente. C'est un reglement qui protege les citoyens."],
     "lesson":"RGPD : tu as le droit de savoir quelles donnees une entreprise possede sur toi et de les supprimer."},
]


def _scene_fin(screen, clock, char_tag):
    """Affiche l'image mafia_boy ou mafia_girl plein écran puis le message."""
    # Charger l'image de la réunion famille
    img_name = "mafia_boy.png" if char_tag=="boy" else "mafia_girl.png"
    img = load_img(img_name, (W, H))

    t0 = pygame.time.get_ticks()
    phase = "REUNION"

    while True:
        t = pygame.time.get_ticks()-t0
        clicked=False
        for ev in pygame.event.get():
            if ev.type==pygame.QUIT: pygame.quit(); import sys; sys.exit()
            if ev.type==pygame.MOUSEBUTTONDOWN: clicked=True
            if ev.type==pygame.KEYDOWN and ev.key==pygame.K_SPACE: clicked=True

        if phase == "REUNION":
            # Afficher l'image plein écran
            if img:
                screen.blit(img,(0,0))
                # Overlay léger pour lisibilité du texte
                ov=pygame.Surface((W,H),pygame.SRCALPHA); ov.fill((0,0,0,80)); screen.blit(ov,(0,0))
            else:
                screen.fill((8,12,28))
            # Titre par-dessus l'image
            draw_textc(screen,"La famille est LIBEREE !",W//2,18,UI_GOLD,32)
            # Étoiles
            for i in range(6):
                ang=t*0.002+i*1.05
                draw_star(screen,int(W//2+220*math.cos(ang)),int(H//2-80+90*math.sin(ang)),10+i%3*5)
            draw_textc(screen,"ESPACE pour voir le message final",W//2,H-32,WHITE,16)
            if clicked and t>1200:
                phase="MESSAGE"; t0=pygame.time.get_ticks()

        elif phase == "MESSAGE":
            t=pygame.time.get_ticks()-t0
            screen.fill((8,12,28))
            import random; rng=random.Random(42)
            for _ in range(80):
                sx=rng.randint(0,W); sy=rng.randint(0,H)
                br=90+int(50*math.sin(t*0.001+sx*0.02))
                pygame.draw.circle(screen,(br,br,br),(sx,sy),1)
            # 5 lignes de sensibilisation
            lignes = [
                ("BRAVO – TA FAMILLE EST LIBEREE !",    UI_GOLD,       34, True),
                ("",                                     WHITE,          8, False),
                ("Dans la vraie vie, protege tes donnees :", (200,200,255), 20, True),
                ("  Mot de passe fort et unique par compte", (180,255,180), 18, False),
                ("  Active le 2FA, utilise un VPN, sauvegarde tes donnees", (180,255,180), 18, False),
                ("  Ne clique jamais sur un lien suspect", (180,255,180), 18, False),
                ("",                                     WHITE,          8, False),
                ("Tes donnees personnelles sont aussi precieuses", (255,220,100), 19, True),
                ("que les personnes que tu aimes.",               (255,220,100), 19, False),
            ]
            y=35
            for txt,col,sz,gras in lignes:
                if txt: draw_textc(screen,txt,W//2,y,col,sz,gras)
                y+=sz+12
            # barre de lecture
            prog=min(1.0,t/4000)
            pygame.draw.rect(screen,(30,40,80),(W//4,H-50,W//2,12),border_radius=6)
            pygame.draw.rect(screen,UI_GOLD,(W//4,H-50,int(W//2*prog),12),border_radius=6)
            if t<2500:
                draw_textc(screen,"Lis attentivement...",W//2,H-26,(130,130,180),14)
            else:
                draw_textc(screen,"ESPACE pour terminer",W//2,H-26,(180,180,240),16)
                if clicked: return

        pygame.display.flip()
        clock.tick(60)


CONFIG = {
    "draw_bg":    draw_mafia_interior,
    "npc_fn":     draw_mafioso,
    "npc_name":   "Don Rossi",
    "border_col": (165,38,38),
    "level_num":  3,
    "missions":   MISSIONS,
    "on_win":     _scene_fin,
}

def run(screen, clock, char_tag):
    return run_level(screen, clock, char_tag, CONFIG)