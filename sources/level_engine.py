"""
level_engine.py
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CORRECTIF PRINCIPAL – bug « fermeture sur bonne réponse »
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Le bug venait des if/elif en Python : quand on changeait
phase = "LESSON" dans le bloc QUESTION, Python evaluait
encore elif phase == "LESSON" dans le MEME frame, avec
advance=True encore actif. Meme probleme LESSON→SCORE_SCREEN
qui causait un retour immediat avant meme d'afficher le score.

FIX : on capture `current_phase = phase` au debut du frame
et tous les if/elif utilisent `current_phase`. Ainsi les
transitions de phase n'ont d'effet qu'au frame suivant.

SYSTEME DE SCORE (tel que demande) :
  0-1  → INSUFFISANT   – 0 etoile  – rejouer obligatoire
  2    → ESSAYE ENCORE – 1 etoile  – rejouer obligatoire
  3-4  → BIEN          – 2 etoiles – rejouer obligatoire
  5    → NIVEAU COMPLET – 3 etoiles – passage au suivant
"""
import pygame, math
from visual_style import *
from visual_style import _font   # _font commence par _ → non exporté par import *
from visual_style import _font   # underscore → non exporte par import *, import explicite

W, H = 900, 600
CURRENT_LANG = "fr"   # main.py met a jour ce module-level avant chaque niveau

# ── LAYOUT FIXE ──────────────────────────────────────────
TOPBAR_H  = 48
PANEL_H   = 240
PANEL_Y   = H - PANEL_H       # 360
CONTENT_H = PANEL_Y - TOPBAR_H  # 312

NPC_ZONE  = pygame.Rect(0,       TOPBAR_H, 310, CONTENT_H)
PLAY_ZONE = pygame.Rect(W - 310, TOPBAR_H, 310, CONTENT_H)

# ── MESSAGES DE SCORE (3 langues) ────────────────────────
# (titre, sous-titre, peut_passer)
SCORE_MSGS = {
    "fr": {
        (0,1): ("INSUFFISANT",    "Tu dois rejouer pour passer ce niveau.",       False),
        (2,2): ("ESSAYE ENCORE",  "1 bonne reponse du 1er coup. Tu peux mieux !", False),
        (3,4): ("BIEN",           "Presque parfait ! Rejoue pour le maximum.",    False),
        (5,5): ("NIVEAU COMPLET", "",                                              True),
    },
    "en": {
        (0,1): ("INSUFFICIENT",   "You must replay to pass this level.",          False),
        (2,2): ("TRY AGAIN",      "1 first-try answer. You can do better!",       False),
        (3,4): ("GOOD",           "Almost perfect! Replay for the maximum.",      False),
        (5,5): ("LEVEL COMPLETE", "",                                              True),
    },
    "pt": {
        (0,1): ("INSUFICIENTE",   "Deves jogar novamente para passar.",           False),
        (2,2): ("TENTA DE NOVO",  "1 resposta certa. Podes fazer melhor!",        False),
        (3,4): ("BOM",            "Quase perfeito! Joga novamente para o maximo.",False),
        (5,5): ("NIVEL COMPLETO", "",                                              True),
    },
}
SCORE_STARS = {(0,1): 0, (2,2): 1, (3,4): 2, (5,5): 3}

REPLAY_BTN = {"fr":"REJOUER",   "en":"REPLAY",    "pt":"JOGAR NOVAMENTE"}
CONT_BTN   = {"fr":"CONTINUER", "en":"CONTINUE",  "pt":"CONTINUAR"}


def _get_score_info(score):
    """Retourne (titre, sous_titre, peut_passer, n_etoiles)."""
    lang = CURRENT_LANG if CURRENT_LANG in SCORE_MSGS else "fr"
    msgs  = SCORE_MSGS[lang]
    for (lo, hi), val in msgs.items():
        if lo <= score <= hi:
            n_stars = SCORE_STARS.get((lo, hi), 0)
            return (*val, n_stars)
    v = msgs[(5,5)]
    return (*v, 3)


# ── ANIMATION IDLE ────────────────────────────────────────
def _idle_frame(t_ms, offset=0):
    return int((t_ms + offset) / 600) % 3


# ── BARRE DE PROGRESSION ─────────────────────────────────
def _draw_progress(surface, done, total, border_col):
    pygame.draw.rect(surface,(10,12,28),(0,0,W,TOPBAR_H))
    pygame.draw.rect(surface,border_col,(0,0,W,TOPBAR_H),2)
    draw_textc(surface, f"Mission {done+1} / {total}", W//2, 14, WHITE, 18)
    for i in range(total):
        cx = W//2 - total*20 + i*40 + 20
        c  = UI_GOLD if i < done else (55,55,70)
        pygame.draw.circle(surface, c, (cx,40), 8)
        pygame.draw.circle(surface, border_col, (cx,40), 8, 2)
        if i < done:
            draw_textc(surface, "v", cx, 32, UI_GREEN, 12)


# ── CADRES NPC ET JOUEUR ──────────────────────────────────
def _draw_npc_frame(surface, npc_fn, border_col, npc_name, t_ms):
    zone = NPC_ZONE
    pygame.draw.rect(surface,(10,13,32,220),zone)
    pygame.draw.rect(surface,border_col,zone,2)
    frame = _idle_frame(t_ms)
    s = 6
    char_h = 16 * s
    cy = zone.bottom - char_h - 5
    npc_fn(surface, zone.left + zone.width//2 - 4*s, cy, scale=s, frame=frame)
    pygame.draw.rect(surface,(10,13,32),(zone.left,zone.bottom,zone.width,20))
    pygame.draw.rect(surface,border_col,(zone.left,zone.bottom,zone.width,20),1)
    draw_textc(surface, npc_name, zone.centerx, zone.bottom+3, border_col, 12)


def _draw_player_frame(surface, player_fn, t_ms):
    zone = PLAY_ZONE
    pygame.draw.rect(surface,(10,13,32,220),zone)
    pygame.draw.rect(surface,DLGBRD,zone,2)
    frame = _idle_frame(t_ms, offset=300)
    s = 6
    char_h = 16 * s
    cy = zone.bottom - char_h - 5
    player_fn(surface, zone.left + zone.width//2 - 4*s, cy, scale=s, frame=frame)


# ── BULLE CENTRALE ────────────────────────────────────────
def _draw_center_bubble(surface, text, size=13, border_col=DLGBRD, bg=(245,248,255)):
    cx = W // 2
    cy = TOPBAR_H + CONTENT_H // 2
    max_w = max(200, W - NPC_ZONE.width - PLAY_ZONE.width - 20)
    draw_speech_bubble(surface, cx, cy, text, size=size,
                       bg=bg, border=border_col, max_w=max_w)


# ── PANNEAU DE CHOIX ─────────────────────────────────────
def _draw_choice_panel(surface, opts, chosen, border_col, mouse,
                        locked, wrong_flash):
    pygame.draw.rect(surface,(6,8,22),(0,PANEL_Y,W,PANEL_H))
    pygame.draw.rect(surface,border_col,(0,PANEL_Y,W,PANEL_H),3)

    if wrong_flash:
        draw_textc(surface, "Ups..  Mauvaise reponse !",
                   W//2, PANEL_Y+8, UI_RED, 15)
    elif locked:
        draw_textc(surface, "CORRECT !", W//2, PANEL_Y+8, UI_GREEN, 16)
    else:
        draw_textc(surface, "Quelle est ta reponse ?",
                   W//2, PANEL_Y+8, UI_GOLD, 15)

    margin  = 10
    gap     = 8
    btn_w   = W - margin*2
    titre_h = 32
    avail_h = PANEL_H - titre_h - gap*2
    btn_h   = (avail_h - gap*2) // 3

    rects = []
    for i, opt in enumerate(opts):
        cx = W // 2
        cy = PANEL_Y + titre_h + gap + i*(btn_h+gap) + btn_h//2

        if locked and i == chosen:
            col = (25,92,30)
        elif locked:
            col = (36,36,52)
        elif wrong_flash:
            col = (36,36,52)
        else:
            hov = (abs(mouse[0]-cx) < btn_w//2 and abs(mouse[1]-cy) < btn_h//2)
            col = (62,98,165) if hov else (45,68,125)

        hov2 = (not locked and not wrong_flash and
                abs(mouse[0]-cx) < btn_w//2 and abs(mouse[1]-cy) < btn_h//2)
        r = draw_button(surface, opt, cx, cy, w=btn_w, h=btn_h,
                        col=col, hover=hov2, size=14)
        rects.append(r)

        if locked and i == chosen:
            draw_textc(surface, "CORRECT", cx, cy-btn_h//2-18, UI_GREEN, 12)

    return rects


# ── LEÇON ────────────────────────────────────────────────
def _draw_lesson(surface, lesson, border_col):
    pygame.draw.rect(surface,(6,8,22),(0,PANEL_Y,W,PANEL_H))
    pygame.draw.rect(surface,border_col,(0,PANEL_Y,W,PANEL_H),3)
    draw_textc(surface, "LECON :", W//2, PANEL_Y+10, UI_GOLD, 15)
    f = _font(14, bold=False)
    words = lesson.split(); lines = []; line = ""
    for w in words:
        t2 = (line+" "+w).strip()
        if f.size(t2)[0] > W-60:
            lines.append(line); line = w
        else:
            line = t2
    if line: lines.append(line)
    y0 = PANEL_Y + 34
    for i, ln in enumerate(lines):
        draw_textc(surface, ln, W//2, y0+i*22, WHITE, 14, bold=False)
    draw_textc(surface, "Clic ou ESPACE pour continuer...",
               W//2, H-18, (150,150,200), 13, bold=False)


# ── ÉCRAN DE SCORE ────────────────────────────────────────
def _draw_score_screen(surface, score, total, t_ms, on_win_done):
    titre, sous_titre, peut_passer, n_stars = _get_score_info(score)
    lang = CURRENT_LANG if CURRENT_LANG in REPLAY_BTN else "fr"

    # Fond sombre
    ov = pygame.Surface((W, H), pygame.SRCALPHA)
    ov.fill((0,0,0,185))
    surface.blit(ov, (0,0))

    # Couleur du titre
    if n_stars == 0:   titre_col = (222, 60, 60)
    elif n_stars == 1: titre_col = (220,180, 50)
    elif n_stars == 2: titre_col = (180,220, 80)
    else:              titre_col = UI_GOLD

    draw_textc(surface, titre, W//2, H//2-120, titre_col, 40)
    draw_textc(surface, f"Score : {score} / {total}", W//2, H//2-72, WHITE, 24)

    if sous_titre:
        draw_textc(surface, sous_titre, W//2, H//2-40, (200,200,255), 17)

    # ── Étoiles ──────────────────────────────────────────
    star_y    = H//2 + 20
    positions = [W//2 - 80, W//2, W//2 + 80]
    for i in range(3):
        cx2 = positions[i]
        if i < n_stars:
            # Étoile gagnée – animée
            sc = 1.0 + 0.15 * math.sin(t_ms*0.004 + i)
            draw_star(surface, cx2, star_y, int(32*sc))
        else:
            # Étoile manquante – grisée
            draw_star(surface, cx2, star_y, 28,
                      col=(55,55,65), border=(40,40,50))

    # ── Bouton action ────────────────────────────────────
    if peut_passer and on_win_done:
        btn_lbl = CONT_BTN.get(lang, "CONTINUER")
        btn_col = UI_GOLD
    else:
        btn_lbl = REPLAY_BTN.get(lang, "REJOUER")
        btn_col = (200,200,255)

    draw_textc(surface, btn_lbl, W//2, H-60, btn_col, 22)
    draw_textc(surface, "ESPACE  ou  CLIC",
               W//2, H-30, (120,120,160), 14, bold=False)


# ── BOUTON SORTIR ─────────────────────────────────────────
def _draw_exit_btn(surface, mouse):
    r = draw_button(surface, "SORTIR", W-72, 26, w=118, h=32,
                    col=(88,32,52),
                    hover=(abs(mouse[0]-(W-72)) < 59 and abs(mouse[1]-26) < 16))
    return r


# ═══════════════════════════════════════════════════════════
#  BOUCLE PRINCIPALE DU NIVEAU
# ═══════════════════════════════════════════════════════════
def run_level(screen, clock, char_tag, config):
    """
    Retourne True si score=5 (passage au niveau suivant).
    Retourne False si le joueur doit rejouer ou a quitte.
    """
    draw_bg   = config["draw_bg"]
    npc_fn    = config["npc_fn"]
    npc_name  = config["npc_name"]
    border    = config["border_col"]
    missions  = config["missions"]
    on_win    = config.get("on_win", None)
    player_fn = draw_charles if char_tag == "boy" else draw_celia

    total       = len(missions)
    mis_idx     = 0
    score       = 0
    phase       = "QUESTION"   # QUESTION | WRONG_FLASH | LESSON | SCORE_SCREEN
    chosen      = None
    phase_t     = 0
    on_win_done = False

    while True:
        t_ms  = pygame.time.get_ticks()
        mouse = pygame.mouse.get_pos()

        clicked  = False
        key_down = set()
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                import sys; sys.exit()
            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                clicked = True
            if ev.type == pygame.KEYDOWN:
                key_down.add(ev.key)

        advance = clicked or (pygame.K_SPACE in key_down)

        mis = missions[min(mis_idx, total-1)]

        # ── DESSIN ─────────────────────────────────────────
        draw_bg(screen)
        _draw_progress(screen, mis_idx, total, border)
        _draw_npc_frame(screen, npc_fn, border, npc_name, t_ms)
        _draw_player_frame(screen, player_fn, t_ms)
        r_exit = _draw_exit_btn(screen, mouse)

        # ══════════════════════════════════════════════════════
        # CORRECTIF CLÉ : capturer la phase au debut du frame.
        #
        # Sans ce correctif, si on fait `phase = "LESSON"` dans
        # le bloc `if phase == "QUESTION"`, Python evalue ensuite
        # `elif phase == "LESSON"` dans le MEME frame car `phase`
        # a change. Cela causait l'execution de LESSON avec
        # `advance=True` (le clic est encore actif) → puis
        # SCORE_SCREEN aussi dans le meme frame → return immediat.
        #
        # Avec `current_phase`, chaque branche est evaluee sur la
        # valeur de debut de frame, et les changements n'ont
        # d'effet qu'au frame suivant.
        # ══════════════════════════════════════════════════════
        current_phase = phase

        # ── QUESTION ───────────────────────────────────────
        if current_phase == "QUESTION":
            _draw_center_bubble(screen, mis["npc"], size=13, border_col=border)
            rects = _draw_choice_panel(screen, mis["opts"], None,
                                       border, mouse,
                                       locked=False, wrong_flash=False)
            if clicked:
                # Toujours verifier SORTIR en premier
                if r_exit.collidepoint(mouse):
                    return False
                else:
                    for i, r in enumerate(rects):
                        if r.collidepoint(mouse):
                            chosen = i
                            if i == mis["correct"]:
                                score  += 1          # 1 seule chance → toujours compté
                                phase   = "LESSON"
                                phase_t = t_ms
                            else:
                                phase   = "WRONG_FLASH"
                                phase_t = t_ms
                            break

        # ── FLASH ERREUR (1.5 s) ───────────────────────────
        # Mauvaise reponse : flash rapide puis question suivante.
        # On ne montre PAS la lecon ni la bonne reponse.
        elif current_phase == "WRONG_FLASH":
            _draw_center_bubble(screen, mis["npc"], size=13, border_col=border)
            _draw_choice_panel(screen, mis["opts"], None,
                               border, mouse, locked=False, wrong_flash=True)
            if clicked and r_exit.collidepoint(mouse):
                return False
            if (t_ms - phase_t) > 1500:
                # Passer directement a la question suivante sans lesson
                mis_idx += 1
                chosen   = None
                if mis_idx >= total:
                    if score == total and on_win:
                        on_win(screen, clock, char_tag)
                        on_win_done = True
                    phase   = "SCORE_SCREEN"
                    phase_t = t_ms
                else:
                    phase   = "QUESTION"
                    phase_t = t_ms

        # ── LEÇON ──────────────────────────────────────────
        elif current_phase == "LESSON":
            _draw_center_bubble(screen, mis["replies"][chosen], size=13,
                                border_col=UI_GREEN, bg=(215,248,215))
            draw_speech_bubble(screen,
                               cx=PLAY_ZONE.centerx, cy=PLAY_ZONE.top+18,
                               text=mis["opts"][chosen], size=12,
                               bg=(225,242,255), border=(70,120,200),
                               max_w=PLAY_ZONE.width-20)
            _draw_lesson(screen, mis["lesson"], border)

            # Sortir en PREMIER
            if clicked and r_exit.collidepoint(mouse):
                return False

            # Avancer la mission apres 600 ms
            if advance and (t_ms - phase_t) > 600:
                mis_idx  += 1
                chosen    = None
                if mis_idx >= total:
                    # Fin du niveau : declencher la scene de victoire si parfait
                    if score == total and on_win:
                        on_win(screen, clock, char_tag)
                        on_win_done = True
                    phase   = "SCORE_SCREEN"
                    phase_t = t_ms
                else:
                    phase = "QUESTION"

        # ── SCORE SCREEN ───────────────────────────────────
        elif current_phase == "SCORE_SCREEN":
            draw_bg(screen)
            _draw_score_screen(screen, score, total, t_ms, on_win_done)
            _, _, peut_passer, _ = _get_score_info(score)

            # Garde de 800 ms : evite que le clic/espace qui a
            # avance la derniere lecon ne valide aussi cet ecran
            # (grâce a current_phase ce cas ne se produit plus,
            # mais on garde la garde par securite).
            if advance and (t_ms - phase_t) > 800:
                return peut_passer

        pygame.display.flip()
        clock.tick(60)