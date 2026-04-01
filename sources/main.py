"""
DARK QUEST 2D  –  main.py
Projet NSI  |  python main.py
Contrôles : Flèches/WASD  |  Approche porte = entrée auto  |  Espace/Clic = avancer

CORRECTIFS :
- Joueur ne sort plus de l'écran (clamp y ajusté : reste sous le HUD et
  au-dessus de la barre d'indices du bas).
- Personnage centré dans la carte de profil (draw_char_info).
"""
import pygame, sys, math, os
from visual_style import *
import level_bar, level_hacker, level_mafia

pygame.init()
W, H = 900, 600
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Dark Quest 2D")
clock = pygame.time.Clock()

# ── TEXTES (3 langues) ────────────────────────────────────────────────
TX = {
"fr": {"play":"JOUER","settings":"OPTIONS","back":"RETOUR","continue":"CONTINUER",
       "language":"LANGUE","lang_fr":"FRANCAIS","lang_en":"ENGLISH","lang_pt":"PORTUGUES",
       "story_title":"[ PROLOGUE ]",
       "story":["En dormant, ta famille a ete enlevee par un groupe",
                "mafieux a qui ton pere devait des services...",
                "Ils avaient fui pour commencer une vie nouvelle,",
                "mais les Rossi les ont retrouves.",
                "Suis les indices. Ne fais confiance a personne."],
       "hint1":"Va au BAR -- le detective t'attend !",
       "hint2":"Va chez le HACKER pour obtenir l'adresse exacte.",
       "hint3":"Rends-toi a la MAFIA (5 pieces necessaires) !",
       "enter":"Approche-toi de la porte pour entrer"},
"en": {"play":"PLAY","settings":"SETTINGS","back":"BACK","continue":"CONTINUE",
       "language":"LANGUAGE","lang_fr":"FRANCAIS","lang_en":"ENGLISH","lang_pt":"PORTUGUES",
       "story_title":"[ PROLOGUE ]",
       "story":["While you slept, your family was kidnapped",
                "by a mafia group your father owed favours...",
                "They had fled to start a new life,",
                "but the Rossi family tracked them down.",
                "Follow the clues. Trust no one."],
       "hint1":"Go to the BAR -- the detective is waiting!",
       "hint2":"Visit the HACKER to get the exact address.",
       "hint3":"Head to the MAFIA (need 5 coins)!",
       "enter":"Approach the door to enter automatically"},
"pt": {"play":"JOGAR","settings":"OPCOES","back":"VOLTAR","continue":"CONTINUAR",
       "language":"IDIOMA","lang_fr":"FRANCES","lang_en":"INGLES","lang_pt":"PORTUGUES",
       "story_title":"[ PROLOGO ]",
       "story":["Enquanto dormias, a tua familia foi raptada",
                "por um grupo mafioso a quem o pai devia favores...",
                "Tinham fugido para comecar uma vida nova,",
                "mas os Rossi encontraram-nos.",
                "Segue as pistas. Nao confies em ninguem."],
       "hint1":"Vai ao BAR -- o detetive espera!",
       "hint2":"Visita o HACKER para obter o endereco.",
       "hint3":"Dirige-te a MAFIA (precisas de 5 moedas)!",
       "enter":"Aproxima-te da porta para entrar"},
}

# ── ÉTAT DU JEU ───────────────────────────────────────────────────────
COIN_INIT = [
    [195,195,False],[255,248,False],[390,182,False],
    [345,315,False],[498,402,False],[598,252,False],
    [648,182,False],[748,302,False],[448,302,False],
    [298,402,False],[150,355,False],[550,355,False],
]

g = {"lang":"fr","char":None,"state":"menu","level":1,"coins":0,"lives":4,
     "px":float(W//2),"py":float(H//2+60),
     "map_coins":[list(c) for c in COIN_INIT],
     "near_bld":None,"_win_lvl":0}

SPEED = 3.5

# ── COLLISIONS (murs des bâtiments, portes ouvertes) ──────────────────
BX_B, BY_B = 22,     52
BX_H, BY_H = W-228,  52
BX_M, BY_M = W-228, 360

# Rectangles solides (laisser les ouvertures de porte libres)
# BAR    porte : BX_B+75, w=44, de BY_B+103
# HACKER porte : BX_H+73, w=48, de BY_H+99
# MAFIA  porte : BX_M+71, w=52, de BY_M+97
WALLS = [
    pygame.Rect(BX_B,       BY_B,       195, 103),
    pygame.Rect(BX_B,       BY_B+103,   75,  62),
    pygame.Rect(BX_B+119,   BY_B+103,   98,  62),
    pygame.Rect(BX_H,       BY_H,       195, 99),
    pygame.Rect(BX_H,       BY_H+99,    73,  66),
    pygame.Rect(BX_H+121,   BY_H+99,    74,  66),
    pygame.Rect(BX_M,       BY_M,       195, 97),
    pygame.Rect(BX_M,       BY_M+97,    71,  68),
    pygame.Rect(BX_M+123,   BY_M+97,    72,  68),
]

# Petites zones juste devant les portes (déclenchent l'entrée auto)
DOOR_BAR    = pygame.Rect(BX_B+72,  BY_B+150, 50, 32)
DOOR_HACKER = pygame.Rect(BX_H+70,  BY_H+148, 54, 32)
DOOR_MAFIA  = pygame.Rect(BX_M+68,  BY_M+150, 56, 32)

# Zones plus larges pour la flèche indicatrice
NEAR_BAR    = DOOR_BAR.inflate(65, 55)
NEAR_HACKER = DOOR_HACKER.inflate(65, 55)
NEAR_MAFIA  = DOOR_MAFIA.inflate(65, 55)

# ── LIMITES D'ÉCRAN DU JOUEUR ─────────────────────────────────────────
# Le sprite joueur scale=4 est dessiné à (px-14, py-52).
# Tête en haut : py - 52 doit rester sous le HUD (y=42) → py_min = 42+52+4 = 98
# Pieds en bas : py doit rester au-dessus de la barre d'indices (y=H-44=556) → py_max = 550
# Gauche/droite : marges de 18 px
MAP_X_MIN = 18
MAP_X_MAX = W - 18
MAP_Y_MIN = 98
MAP_Y_MAX = H - 50   # = 550

def collide_wall(nx, ny):
    foot = pygame.Rect(int(nx)-12, int(ny)-6, 24, 14)
    return any(foot.colliderect(w) for w in WALLS)

def resolve(ox, oy, nx, ny):
    if not collide_wall(nx, ny): return nx, ny
    if not collide_wall(nx, oy): return nx, oy
    if not collide_wall(ox, ny): return ox, ny
    return ox, oy

def check_door():
    foot = pygame.Rect(int(g["px"])-12, int(g["py"])-6, 24, 14)
    if foot.colliderect(DOOR_BAR):    return "bar"
    if foot.colliderect(DOOR_HACKER): return "hacker"
    if foot.colliderect(DOOR_MAFIA):  return "mafia"
    return None

def check_near():
    foot = pygame.Rect(int(g["px"])-12, int(g["py"])-6, 24, 14)
    if foot.colliderect(NEAR_BAR):    return "bar"
    if foot.colliderect(NEAR_HACKER): return "hacker"
    if foot.colliderect(NEAR_MAFIA):  return "mafia"
    return None

# ── UTILITAIRES ───────────────────────────────────────────────────────
def tx(k): return TX[g["lang"]].get(k, TX["fr"].get(k, k))
def go(s): g["state"] = s

def reset_center():
    """Remet le joueur au centre de la carte après sortie d'un niveau."""
    g["px"] = float(W//2); g["py"] = float(H//2+60)

def reset_map():
    g["map_coins"] = [list(c) for c in COIN_INIT]
    g["near_bld"]  = None
    reset_center()

def full_reset():
    g.update({"lang":"fr","char":None,"state":"menu","level":1,
               "coins":0,"lives":4,"_win_lvl":0})
    reset_map()

# ── NPCs SUR LA CARTE ─────────────────────────────────────────────────
NPC_DATA = [
    (BX_B+97,  BY_B+202, draw_detective, "J'ai des infos !",          1),
    (BX_H+97,  BY_H+202, draw_hacker,   "Teste tes connaissances !", 2),
    (BX_M+97,  BY_M+202, draw_mafioso,  "5 pieces pour entrer...",   3),
]

def draw_npcs(t_ms):
    for nx, ny, fn, bubble, lvl in NPC_DATA:
        if g["level"] >= lvl:
            bob = int(math.sin(t_ms*0.002+nx)*3)
            fn(screen, nx-14, ny-52+bob, scale=4)
            draw_speech_bubble(screen, nx, ny-56+bob, bubble,
                               size=12, bg=(245,245,255), border=(80,80,140), max_w=200)

# ── ÉCRANS ────────────────────────────────────────────────────────────
def draw_char_info():
    draw_cobble_bg(screen, W, H)
    ov = pygame.Surface((W,H),pygame.SRCALPHA); ov.fill((0,0,0,130)); screen.blit(ov,(0,0))
    ct = g["char"]; nm = "Charles" if ct=="boy" else "Celia"
    fn = draw_charles if ct=="boy" else draw_celia

    # ── Carte gauche (personnage) ──────────────────────────────────────
    pygame.draw.rect(screen,(22,28,52),(48,78,268,444),border_radius=8)
    pygame.draw.rect(screen,DLGBRD,(48,78,268,444),3,border_radius=8)

    # CORRECTION : personnage centré dans la carte (ne plus être trop en haut).
    # Centre horizontal de la carte : 48 + 268//2 = 182.
    # Le sprite a son centre visuel à x + 4*scale = x + 24 (à scale=6).
    # Donc x = 182 - 24 = 158.
    # Centre vertical de la zone image (entre y=78 et y=338) : 78 + (338-78)//2 = 208.
    # Sprite height ≈ 15*6 = 90 px → top à 208 - 45 = 163 → on arrondit à 155.
    fn(screen, 158, 155, scale=6)

    draw_textc(screen,nm,182,338,UI_GOLD,28)
    for i,(k,v) in enumerate([("Age","14 ans"),("Pays","France"),
                               ("Ecole","Lycee Victor Hugo"),("IP","192.168.0.1")]):
        draw_text(screen,f"  {k} : {v}",68,375+i*34,HACK_ACCENT if k=="IP" else WHITE,16)

    # ── Carte droite (profil détaillé) ────────────────────────────────
    pygame.draw.rect(screen,(22,28,52),(342,78,520,444),border_radius=8)
    pygame.draw.rect(screen,DLGBRD,(342,78,520,444),3,border_radius=8)
    draw_textc(screen,"PROFIL DETAILLE",W//2+102,94,UI_GOLD,22)
    stats=[("Famille","Parents + 1 soeur"),("Motivation","Retrouver sa famille"),
           ("Competences","Deduction, courage"),("Langues","Francais / Anglais"),
           ("Reseau","WiFi familial partage"),("Menace","Donnees exposees en ligne")]
    for i,(k,v) in enumerate(stats):
        y2=134+i*56
        pygame.draw.rect(screen,(30,38,68),(360,y2,484,48),border_radius=5)
        draw_text(screen,k,378,y2+8,HACK_ACCENT,16)
        draw_text(screen,v,378,y2+26,WHITE,15,bold=False)
    m=pygame.mouse.get_pos()
    return draw_button(screen,tx("continue"),W//2+102,H-44,w=200,h=42,
                       col=(48,78,155),hover=abs(m[1]-H+44)<21)

def draw_story():
    y0=H//2
    pygame.draw.rect(screen,(12,14,28),(0,0,W,y0))
    draw_textc(screen,tx("story_title"),W//2,18,UI_GOLD,28)
    for i,ln in enumerate(tx("story")):
        draw_textc(screen,ln,W//2,62+i*46,WHITE,16,bold=False)
    pygame.draw.line(screen,DLGBRD,(0,y0-2),(W,y0-2),3)
    pygame.draw.rect(screen,(6,6,14),(0,y0,W,H-y0))
    for sx,sh in [(130,28),(150,34),(170,26)]:
        pygame.draw.rect(screen,(15,10,10),(sx,y0+86-sh,11,sh))
    for mx,mh in [(308,45),(355,48)]:
        pygame.draw.rect(screen,(10,8,10),(mx,y0+H-y0-mh-10,18,mh))
        pygame.draw.rect(screen,(9,7,9),(mx-4,y0+H-y0-mh-17,26,8))
    fn=draw_charles if g["char"]=="boy" else draw_celia
    fn(screen,W*3//4+15,y0+52,scale=5)
    pygame.draw.circle(screen,(220,215,195),(W-52,y0+26),22)
    pygame.draw.circle(screen,(6,6,14),(W-41,y0+18),17)

# ── BOUCLE PRINCIPALE ─────────────────────────────────────────────────
while True:
    t_ms  = pygame.time.get_ticks()
    mouse = pygame.mouse.get_pos()
    clicked = False; key_down = set()
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT: pygame.quit(); sys.exit()
        if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1: clicked = True
        if ev.type == pygame.KEYDOWN: key_down.add(ev.key)
    keys    = pygame.key.get_pressed()
    advance = clicked or (pygame.K_SPACE in key_down)

    # ── MOUVEMENT ─────────────────────────────────────────────────────
    if g["state"] == "map":
        dx = dy = 0
        if keys[pygame.K_LEFT]  or keys[pygame.K_a]: dx -= SPEED
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]: dx += SPEED
        if keys[pygame.K_UP]    or keys[pygame.K_w]: dy -= SPEED
        if keys[pygame.K_DOWN]  or keys[pygame.K_s]: dy += SPEED
        ox, oy = g["px"], g["py"]

        # CORRECTION : clamp renforcé pour que le joueur reste dans la zone
        # visible (sous le HUD en haut, au-dessus de la barre d'indices en bas).
        nx = max(MAP_X_MIN, min(MAP_X_MAX, ox + dx))
        ny = max(MAP_Y_MIN, min(MAP_Y_MAX, oy + dy))

        g["px"], g["py"] = resolve(ox, oy, nx, ny)
        g["near_bld"] = check_near()
        for c in g["map_coins"]:
            if not c[2] and abs(g["px"]-c[0])<20 and abs(g["py"]-c[1])<20:
                c[2]=True; g["coins"]+=1

        # ── ENTRÉE AUTO DANS LES NIVEAUX ──────────────────────────────
        door = check_door()
        if door:
            import level_engine as _le; _le.CURRENT_LANG = g["lang"]
        if door == "bar" and g["level"] >= 1:
            result = level_bar.run(screen, clock, g["char"])
            if result:
                g["level"] = max(g["level"], 2); g["_win_lvl"] = 1; go("level_win")
            else:
                g["lives"] = max(0, g["lives"] - 1)
                if g["lives"] == 0: go("game_over")
            reset_center()
        elif door == "hacker" and g["level"] >= 2:
            result = level_hacker.run(screen, clock, g["char"])
            if result:
                g["level"] = max(g["level"], 3); g["_win_lvl"] = 2; go("level_win")
            else:
                g["lives"] = max(0, g["lives"] - 1)
                if g["lives"] == 0: go("game_over")
            reset_center()
        elif door == "mafia" and g["level"] >= 3:
            if g["coins"] >= 5:
                result = level_mafia.run(screen, clock, g["char"])
                if result:
                    go("victory")
                else:
                    g["lives"] = max(0, g["lives"] - 1)
                    if g["lives"] == 0: go("game_over")
            else:
                go("need_coins")
            reset_center()

    # ── DESSIN ────────────────────────────────────────────────────────
    screen.fill(DARK_BG)
    st = g["state"]

    if st == "menu":
        draw_menu_bg(screen, t_ms)
        r_opt = draw_button(screen,"OPT",44,24,w=66,h=34,col=(35,40,68),
                            hover=(mouse[0]<77 and mouse[1]<41))
        r_pl  = draw_button(screen,tx("play"),W//2,H*2//3,w=220,h=56,col=(48,78,155),
                            hover=(abs(mouse[0]-W//2)<110 and abs(mouse[1]-H*2//3)<28))
        r_st  = draw_button(screen,tx("settings"),W//2,H*2//3+74,w=220,h=48,col=(38,55,95),
                            hover=(abs(mouse[0]-W//2)<110 and abs(mouse[1]-H*2//3-74)<24))
        if clicked:
            if r_pl.collidepoint(mouse):  go("select")
            if r_st.collidepoint(mouse):  go("settings")
            if r_opt.collidepoint(mouse): go("settings")

    elif st == "settings":
        draw_menu_bg(screen, t_ms)
        draw_textc(screen,tx("language"),W//2,H//3-24,UI_GOLD,30)
        for i,(lk,lbl) in enumerate([("fr",tx("lang_fr")),("en",tx("lang_en")),("pt",tx("lang_pt"))]):
            cy2=H//2-28+i*70; sel=(g["lang"]==lk)
            r=draw_button(screen,lbl,W//2,cy2,w=248,h=52,
                          col=(52,108,65) if sel else (42,52,82),hover=abs(mouse[1]-cy2)<26)
            if sel: pygame.draw.rect(screen,UI_GOLD,r,2,border_radius=5)
            if clicked and r.collidepoint(mouse): g["lang"]=lk
        r_bk=draw_button(screen,tx("back"),W//2,H-65,w=180,h=44,col=(55,38,88),
                         hover=abs(mouse[1]-H+65)<22)
        if clicked and r_bk.collidepoint(mouse): go("menu")

    elif st == "select":
        rects = draw_char_select(screen, mouse)
        r_bk  = draw_button(screen,tx("back"),82,H-38,w=148,h=38,col=(55,38,88),
                            hover=(mouse[1]>H-57 and mouse[0]<156))
        if clicked:
            if rects[0].collidepoint(mouse): g["char"]="boy";  go("char_info")
            if rects[1].collidepoint(mouse): g["char"]="girl"; go("char_info")
            if r_bk.collidepoint(mouse): go("menu")

    elif st == "char_info":
        r_cont = draw_char_info()
        if (clicked and r_cont.collidepoint(mouse)) or pygame.K_RETURN in key_down:
            go("story")

    elif st == "story":
        draw_story()
        pygame.draw.line(screen,DLGBRD,(0,H//2-2),(W,H//2-2),3)
        r_cont = draw_button(screen,tx("continue"),W//2,H-36,w=200,h=40,col=(48,78,155),
                             hover=abs(mouse[1]-H+36)<20)
        if (clicked and r_cont.collidepoint(mouse)) or advance:
            reset_map(); go("map")

    elif st == "map":
        draw_map(screen,W,H,g["map_coins"],t_ms,g["level"])
        draw_npcs(t_ms)
        fn = draw_charles if g["char"]=="boy" else draw_celia
        fn(screen, int(g["px"])-14, int(g["py"])-52, scale=4)
        nb = g["near_bld"]
        if nb:
            acc = (nb=="bar") or (nb=="hacker" and g["level"]>=2) or (nb=="mafia" and g["level"]>=3)
            if acc:
                draw_arrow(screen, int(g["px"]), int(g["py"])-65, t_ms)
                draw_textc(screen, tx("enter"), W//2, H-28, UI_GOLD, 15)
        draw_hud(screen,W,g["lives"],g["coins"],g["level"])
        hints={1:tx("hint1"),2:tx("hint2"),3:tx("hint3")}
        pygame.draw.rect(screen,(15,18,42),(0,H-44,W,44))
        pygame.draw.rect(screen,HUD_BORDER,(0,H-44,W,44),1)
        draw_textc(screen,hints.get(g["level"],""),W//2,H-34,(185,185,235),15)

    elif st == "level_win":
        draw_level_complete_screen(screen, g["_win_lvl"], t_ms)
        if advance: go("map")

    elif st == "victory":
        fn = draw_charles if g["char"]=="boy" else draw_celia
        draw_victory_screen(screen, fn)
        if advance: full_reset()

    elif st == "game_over":
        # Charger l'image selon le personnage
        img_name = "game_over_boy.png" if g["char"]=="boy" else "game_over_girl.png"
        img = load_img(img_name, (W, H))
        if img:
            screen.blit(img, (0, 0))
        else:
            screen.fill((8, 4, 4))
            draw_textc(screen, "GAME OVER", W//2, H//2-40, (222,48,48), 54)
        # Overlay semi-transparent pour lisibilité du bouton
        ov = pygame.Surface((W, 60), pygame.SRCALPHA)
        ov.fill((0, 0, 0, 160))
        screen.blit(ov, (0, H-68))
        r_restart = draw_button(screen, "REJOUER DEPUIS LE DEBUT", W//2, H-38,
                                w=340, h=44, col=(140,28,28),
                                hover=abs(mouse[1]-H+38)<22)
        if clicked and r_restart.collidepoint(mouse):
            full_reset()

    elif st == "need_coins":
        draw_map(screen,W,H,g["map_coins"],t_ms,g["level"])
        draw_hud(screen,W,g["lives"],g["coins"],g["level"])
        ov=pygame.Surface((W-36,130),pygame.SRCALPHA); ov.fill((18,8,8,225))
        screen.blit(ov,(18,H//2-65))
        pygame.draw.rect(screen,(145,28,28),(18,H//2-65,W-36,130),3,border_radius=8)
        draw_textc(screen,"GARDE DES ROSSI",W//2,H//2-55,(255,80,80),22)
        draw_textc(screen,f"Il te faut 5 pieces ! ({g['coins']}/5)",W//2,H//2-14,WHITE,18)
        draw_textc(screen,"Continue a collecter les pieces dans la ville !",W//2,H//2+16,(200,200,200),15)
        r_bk=draw_button(screen,"Retour",W//2,H//2+56,w=180,h=40,col=(55,38,55),
                         hover=abs(mouse[1]-H//2-56)<20)
        if (clicked and r_bk.collidepoint(mouse)) or pygame.K_ESCAPE in key_down:
            go("map")

    pygame.display.flip()
    clock.tick(60)