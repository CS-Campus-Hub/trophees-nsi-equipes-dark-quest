"""visual_style.py – couleurs, personnages animés, décors"""
import pygame, math, os

# ── COULEURS ──────────────────────────────────────────────
WHITE=(255,255,255);BLACK=(0,0,0);DARK_BG=(12,12,22)
HUD_BG=(20,20,38);HUD_BORDER=(70,90,160)
COBBLE_L=(145,135,118);COBBLE_D=(105,96,82);COBBLE_LINE=(78,70,58)
GRASS_L=(72,148,70);GRASS_D=(52,112,48)
BRICK_R=(158,68,52);BRICK_D=(118,48,36);BRICK_M=(82,66,54)
SIGN_GRN=(28,138,68);SIGN_TXT=(235,235,50);WIN_BLUE=(98,162,225)
DOOR_BR=(88,52,28);ROOF_G=(58,122,58)
WALL_D=(48,48,58);WALL_G=(78,78,92)
HACK_ACCENT=(0,220,240);HACK_CODE=(0,255,128);HACK_GG=(0,205,225)
MAF_DARK=(30,18,18);MAF_MID=(50,38,38);MAF_RED=(145,28,28)
COIN_GOLD=(255,200,30);COIN_DARK=(200,140,10);COIN_SHINE=(255,245,130)
SKIN_L=(242,198,158);HAIR_BR=(100,65,28)
# Garçon – calqué sur boy.png : veste bleue, jean marine, boots bruns
BOY_J=(35,88,200);BOY_JL=(65,130,230);BOY_JC=(90,200,240)  # cyan trim
BOY_P=(38,44,82);BOY_SH=(105,65,30);BOY_TEE=(100,108,120)
# Fille – calqué sur girl.png : veste rose, jean marine, baskets roses
GIRL_J=(215,45,120);GIRL_JL=(240,98,158);GIRL_P=(38,44,82)
GIRL_SH=(220,48,130);GIRL_BOW=(255,70,155);GIRL_HAIR=(100,65,28)
GIRL_SHOE=(220,48,130);GIRL_TEE=(140,148,158)
HACK_SK=(208,168,128);HACK_HAIR=(28,162,60);HACK_JK=(28,28,40)
DET_SK=(212,168,128);DET_COAT=(128,98,58);DET_COUTL=(158,128,82)
DET_HAT=(108,82,48);DET_BOOT=(70,42,18)
MAF_SK=(232,188,148);MAF_SUIT=(52,52,58);MAF_SUITL=(68,68,78)
MAF_SHIRT=(242,242,242);MAF_TIE=(202,28,28);MAF_HAT=(42,42,48);MAF_BOOT=(28,28,32)
MAF_GUN=(78,78,82)
UI_GOLD=(255,212,30);UI_RED=(222,48,48);UI_GREEN=(58,202,78)
DLGBG=(18,22,44);DLGBRD=(78,152,222);ARROW_Y=(255,232,0);STAR_Y=(255,212,0)
LAMP_POST=(78,78,68);LAMP_GLOW=(255,222,98)
TREE_D=(38,102,38);TREE_M=(52,132,52);TREE_L=(72,162,68);TREE_TR=(108,72,38)
BUSH_D=(34,90,34);BUSH_L=(58,130,52)
BAR_WOOD=(108,68,32);BAR_WOODL=(138,92,48)
COMP_BODY=(32,32,44);COMP_SCR=(0,18,38);DESK_COL=(48,38,28)

# ── CHARGEMENT D'IMAGE ────────────────────────────────────
_IMG_CACHE = {}
def load_img(name, size=None):
    """Charge une image depuis le même dossier que le script."""
    if name in _IMG_CACHE: return _IMG_CACHE[name]
    base = os.path.dirname(os.path.abspath(__file__))
    p = os.path.join(base, name)
    if not os.path.exists(p): return None
    try:
        img = pygame.image.load(p).convert_alpha()
        if size: img = pygame.transform.smoothscale(img, size)
        _IMG_CACHE[name] = img
        return img
    except Exception: return None

# ── TEXTE ─────────────────────────────────────────────────
def _font(size, bold=True):
    try: return pygame.font.SysFont("monospace", size, bold=bold)
    except: return pygame.font.Font(None, size)

def draw_text(surface, msg, x, y, color=WHITE, size=16, bold=True):
    s = _font(size, bold).render(str(msg), True, color)
    surface.blit(s, (x, y)); return s.get_rect(topleft=(x, y))

def draw_textc(surface, msg, cx, y, color=WHITE, size=16, bold=True):
    s = _font(size, bold).render(str(msg), True, color)
    x = cx - s.get_width()//2; surface.blit(s, (x, y))
    return s.get_rect(topleft=(x, y))

def _b(sur, x, y, rx, ry, rw, rh, col, s):
    pygame.draw.rect(sur, col, (x+rx*s, y+ry*s, rw*s, rh*s))

# ── BOUTON (wrapping + taille de police auto) ────────────
def draw_button(surface, msg, cx, cy, w=190, h=52,
                col=(55,78,145), hover=False, text_col=WHITE, size=15):
    bx, by = cx-w//2, cy-h//2
    bg = tuple(min(c+38,255) for c in col) if hover else col
    pygame.draw.rect(surface, bg, (bx,by,w,h), border_radius=6)
    border = tuple(min(c+90,255) for c in col)
    pygame.draw.rect(surface, border, (bx,by,w,h), 2, border_radius=6)
    if hover: pygame.draw.rect(surface,(255,255,200),(bx+1,by+1,w-2,7),border_radius=5)
    # Réduire la taille de police si nécessaire pour tenir dans la hauteur
    pad_x = 14; pad_y = 6
    max_text_w = w - pad_x*2
    max_text_h = h - pad_y*2
    for sz in [size, size-1, size-2, size-3, 11, 10]:
        if sz < 10: sz=10
        f = _font(sz, bold=False)
        # Wrapping
        words = msg.split(); lines = []; line = ""
        for word in words:
            test = (line+" "+word).strip()
            if f.size(test)[0] > max_text_w:
                if line: lines.append(line)
                line = word
            else: line = test
        if line: lines.append(line)
        lh = f.get_height()+3
        total_h = len(lines)*lh
        if total_h <= max_text_h or sz<=10: break
    # Affichage centré verticalement
    start_y = by + h//2 - total_h//2
    for i, ln in enumerate(lines):
        img = f.render(ln, True, text_col)
        # Clamp horizontal au cas où un mot serait trop long
        x_txt = cx - img.get_width()//2
        x_txt = max(bx+4, x_txt)
        surface.blit(img, (x_txt, start_y + i*lh))
    return pygame.Rect(bx, by, w, h)

# ── BULLE DE DIALOGUE (taille auto, jamais hors écran) ───
def draw_speech_bubble(surface, cx, cy, text, size=13,
                        bg=WHITE, border=(80,80,120), max_w=260):
    W_scr, _ = surface.get_size()
    f = _font(size, bold=False)
    words = text.split(); lines = []; line = ""
    for w in words:
        t2 = (line+" "+w).strip()
        if f.size(t2)[0] > max_w: lines.append(line); line=w
        else: line=t2
    if line: lines.append(line)
    if not lines: return
    lh = f.get_height()+4
    bw = max(f.size(l)[0] for l in lines)+20
    bh = len(lines)*lh+14
    bx = max(6, min(W_scr-bw-6, cx-bw//2))
    by = max(6, cy-bh-18)
    pygame.draw.rect(surface,bg,(bx,by,bw,bh),border_radius=8)
    pygame.draw.rect(surface,border,(bx,by,bw,bh),2,border_radius=8)
    qcx = max(bx+12, min(bx+bw-12, cx))
    pts = [(qcx-7,by+bh),(qcx+7,by+bh),(qcx,by+bh+14)]
    pygame.draw.polygon(surface,bg,pts); pygame.draw.polygon(surface,border,pts,2)
    for i, ln in enumerate(lines):
        surface.blit(f.render(ln,True,(25,25,45)),(bx+10,by+7+i*lh))

# ── PERSONNAGES ANIMÉS ────────────────────────────────────
# frame=0 → debout, frame=1 → jambe droite levée, frame=2 → jambe gauche levée

def draw_charles(surface, x, y, scale=4, frame=0):
    """Charles – veste bleue avec liseré cyan, jean marine, boots bruns."""
    s = scale; b = lambda rx,ry,rw,rh,col: _b(surface,x,y,rx,ry,rw,rh,col,s)
    # Animation : décalage des pieds
    loff = s if frame==1 else (-s if frame==2 else 0)
    roff = -s if frame==1 else (s if frame==2 else 0)
    pygame.draw.ellipse(surface,BLACK,(x+s,y+14*s,6*s,s))
    # Boots
    b(0,13,3,2,BOY_SH); b(4,13,3,2,BOY_SH)
    # Semelle
    pygame.draw.rect(surface,(62,38,15),(x-s,y+14*s+loff,4*s,s))
    pygame.draw.rect(surface,(62,38,15),(x+3*s,y+14*s+roff,4*s,s))
    # Jean
    b(0,9,3,4,BOY_P); b(4,9,3,4,BOY_P)
    b(3,9,1,4,(28,34,68))  # couture
    # Veste bleue
    b(0,4,7,5,BOY_J)
    b(0,4,1,5,BOY_JL); b(6,4,1,5,BOY_JL)  # reflets
    b(3,4,1,5,BOY_JC)                        # fermeture éclair cyan
    b(1,4,2,1,BOY_JC); b(4,4,2,1,BOY_JC)   # col
    # T-shirt visible
    b(2,5,3,4,BOY_TEE)
    # Bras (légère animation)
    arm_off = s//2 if frame==1 else (-s//2 if frame==2 else 0)
    pygame.draw.rect(surface,BOY_J,(x-s,y+5*s-arm_off,s,4*s))
    pygame.draw.rect(surface,BOY_J,(x+7*s,y+5*s+arm_off,s,4*s))
    # Mains
    b(-1,8,1,2,SKIN_L); b(7,8,1,2,SKIN_L)
    # Cou
    b(2,2,3,2,SKIN_L)
    # Tête
    b(1,0,5,3,SKIN_L)
    # Cheveux bruns (comme boy.png : arrondi, épais)
    b(1,0,5,1,HAIR_BR); b(1,0,1,2,HAIR_BR); b(5,0,1,2,HAIR_BR)
    b(2,0,3,1,(80,48,18))  # mèche frontale
    # Yeux
    b(2,1,1,1,(55,30,12)); b(4,1,1,1,(55,30,12))
    b(2,1,1,1,(180,155,130)); b(4,1,1,1,(180,155,130))  # reflet
    b(2,1,1,1,(55,30,12)); b(4,1,1,1,(55,30,12))
    # Bouche
    b(2,2,3,1,(185,128,98))

def draw_celia(surface, x, y, scale=4, frame=0):
    """Célia – veste rose avec liseré blanc, jean marine, baskets roses."""
    s = scale; b = lambda rx,ry,rw,rh,col: _b(surface,x,y,rx,ry,rw,rh,col,s)
    loff = s if frame==1 else (-s if frame==2 else 0)
    roff = -s if frame==1 else (s if frame==2 else 0)
    pygame.draw.ellipse(surface,BLACK,(x+s,y+14*s,6*s,s))
    # Baskets roses (comme girl.png)
    b(0,13,3,2,GIRL_SHOE); b(4,13,3,2,GIRL_SHOE)
    pygame.draw.rect(surface,WHITE,(x-s,y+14*s+loff,4*s,s))
    pygame.draw.rect(surface,WHITE,(x+3*s,y+14*s+roff,4*s,s))
    # Jean
    b(0,9,3,4,GIRL_P); b(4,9,3,4,GIRL_P)
    b(3,9,1,4,(28,34,68))
    # Veste rose
    b(0,4,7,5,GIRL_J)
    b(0,4,1,5,GIRL_JL); b(6,4,1,5,GIRL_JL)
    b(3,4,1,5,WHITE)      # fermeture (comme girl.png – trait blanc)
    b(1,4,2,1,WHITE); b(4,4,2,1,WHITE)  # col
    b(2,5,3,4,GIRL_TEE)  # t-shirt
    # Bras
    arm_off = s//2 if frame==1 else (-s//2 if frame==2 else 0)
    pygame.draw.rect(surface,GIRL_J,(x-s,y+5*s-arm_off,s,4*s))
    pygame.draw.rect(surface,GIRL_J,(x+7*s,y+5*s+arm_off,s,4*s))
    b(-1,8,1,2,SKIN_L); b(7,8,1,2,SKIN_L)
    # Cou
    b(2,2,3,2,SKIN_L)
    # Tête
    b(1,0,5,3,SKIN_L)
    # Cheveux bruns + queue de cheval + nœud rose (comme girl.png)
    b(1,0,5,1,GIRL_HAIR); b(1,0,1,3,GIRL_HAIR)
    b(5,0,4,3,GIRL_HAIR)   # queue de cheval
    b(6,0,3,2,GIRL_BOW)    # nœud rose
    b(6,0,1,1,(255,120,190))  # reflet nœud
    # Yeux (légèrement plus grands pour girl)
    b(2,1,1,2,(72,38,38)); b(4,1,1,2,(72,38,38))
    b(2,1,1,1,(190,150,150))  # reflet
    # Joues
    b(1,2,1,1,(255,178,178)); b(5,2,1,1,(255,178,178))
    # Sourire
    b(2,2,3,1,(185,128,98))

def draw_hacker(surface, x, y, scale=4, frame=0):
    s=scale; b=lambda rx,ry,rw,rh,col:_b(surface,x,y,rx,ry,rw,rh,col,s)
    loff=s if frame==1 else(-s if frame==2 else 0)
    roff=-s if frame==1 else(s if frame==2 else 0)
    pygame.draw.ellipse(surface,BLACK,(x+s,y+14*s,6*s,s))
    b(0,13,3,2,(18,18,28)); b(4,13,3,2,(18,18,28))
    pygame.draw.rect(surface,(12,12,22),(x-s,y+14*s+loff,4*s,s))
    pygame.draw.rect(surface,(12,12,22),(x+3*s,y+14*s+roff,4*s,s))
    b(0,9,3,4,(22,22,34)); b(4,9,3,4,(22,22,34))
    b(0,4,7,5,HACK_JK)
    b(0,4,1,5,HACK_ACCENT); b(6,4,1,5,HACK_ACCENT); b(3,4,1,5,(35,35,48))
    arm_off=s//2 if frame==1 else(-s//2 if frame==2 else 0)
    pygame.draw.rect(surface,HACK_JK,(x-s,y+5*s-arm_off,s,4*s))
    pygame.draw.rect(surface,HACK_JK,(x+7*s,y+5*s+arm_off,s,4*s))
    b(-1,8,1,2,HACK_SK); b(7,8,1,2,HACK_SK)
    b(2,8,2,2,HACK_ACCENT)  # gadget main droite
    b(2,2,3,2,HACK_SK); b(1,0,5,3,HACK_SK)
    b(1,0,5,1,HACK_HAIR); b(2,0,3,1,(18,128,48))
    b(1,1,2,1,HACK_GG); b(4,1,2,1,HACK_GG); b(3,1,1,1,(0,85,105))
    b(3,0,1,1,HACK_ACCENT)

def draw_detective(surface, x, y, scale=4, frame=0):
    s=scale; b=lambda rx,ry,rw,rh,col:_b(surface,x,y,rx,ry,rw,rh,col,s)
    loff=s if frame==1 else(-s if frame==2 else 0)
    roff=-s if frame==1 else(s if frame==2 else 0)
    pygame.draw.ellipse(surface,BLACK,(x+s,y+15*s,6*s,s))
    b(0,13,3,3,DET_BOOT); b(4,13,3,3,DET_BOOT)
    pygame.draw.rect(surface,(50,30,12),(x-s,y+15*s+loff,4*s,s))
    pygame.draw.rect(surface,(50,30,12),(x+3*s,y+15*s+roff,4*s,s))
    b(0,4,7,9,DET_COAT); b(0,4,2,9,DET_COUTL); b(3,4,3,5,DET_COUTL)
    arm_off=s//2 if frame==1 else(-s//2 if frame==2 else 0)
    pygame.draw.rect(surface,DET_COAT,(x-s,y+5*s-arm_off,s,8*s))
    pygame.draw.rect(surface,DET_COAT,(x+7*s,y+5*s+arm_off,s,8*s))
    pygame.draw.rect(surface,DET_COUTL,(x-s,y+5*s-arm_off,s,8*s))
    # loupe
    pygame.draw.circle(surface,(138,212,255),(x-s,y+3*s),3*s)
    pygame.draw.circle(surface,(95,168,218),(x-s,y+3*s),2*s)
    pygame.draw.circle(surface,WHITE,(x-2*s,y+2*s),s)
    pygame.draw.rect(surface,(48,48,48),(x-3*s,y+5*s,s,3*s))
    b(-1,8,1,2,DET_SK)
    b(2,2,3,2,DET_SK); b(1,0,5,3,DET_SK)
    b(-1,0,9,1,DET_HAT); b(1,0,5,2,(70,52,28))
    b(2,2,3,1,(88,62,38)); b(2,1,1,1,(52,32,18)); b(4,1,1,1,(52,32,18))

def draw_mafioso(surface, x, y, scale=4, frame=0):
    s=scale; b=lambda rx,ry,rw,rh,col:_b(surface,x,y,rx,ry,rw,rh,col,s)
    loff=s if frame==1 else(-s if frame==2 else 0)
    roff=-s if frame==1 else(s if frame==2 else 0)
    pygame.draw.ellipse(surface,BLACK,(x+s,y+14*s,6*s,s))
    b(0,12,3,3,MAF_BOOT); b(4,12,3,3,MAF_BOOT)
    pygame.draw.rect(surface,(18,18,22),(x-s,y+14*s+loff,4*s,s))
    pygame.draw.rect(surface,(18,18,22),(x+3*s,y+14*s+roff,4*s,s))
    b(0,9,3,3,MAF_SUIT);  b(4,9,3,3,MAF_SUIT)
    b(0,4,7,5,MAF_SUIT); b(0,4,2,5,MAF_SUITL); b(5,4,2,5,MAF_SUITL)
    b(3,4,1,5,MAF_SHIRT); b(3,5,1,3,MAF_TIE)
    arm_off=s//2 if frame==1 else(-s//2 if frame==2 else 0)
    pygame.draw.rect(surface,MAF_SUIT,(x-s,y+5*s-arm_off,s,7*s))
    pygame.draw.rect(surface,MAF_SUIT,(x+7*s,y+5*s+arm_off,s,7*s))
    pygame.draw.rect(surface,MAF_SUITL,(x-s,y+5*s-arm_off,s,7*s))
    pygame.draw.rect(surface,MAF_GUN,(x-3*s,y+10*s,4*s,2*s))
    pygame.draw.rect(surface,(58,58,62),(x-5*s,y+10*s,3*s,s))
    b(-1,9,1,2,MAF_SK)
    b(2,2,3,2,MAF_SK); b(1,0,5,3,MAF_SK)
    b(-1,0,9,1,MAF_HAT); b(1,0,5,2,(33,33,38)); b(1,1,5,1,(18,18,22))
    b(1,1,2,1,(18,18,18)); b(4,1,2,1,(18,18,18)); b(3,1,1,1,(8,8,8))

# ── DÉCORS INTÉRIEURS ────────────────────────────────────
def draw_bar_interior(surface):
    W,H=surface.get_size(); surface.fill((22,12,8))
    for i in range(0,W,24):
        for j in range(0,H*3//5,15):
            c=BRICK_R if (i+j)%3!=0 else BRICK_D
            pygame.draw.rect(surface,c,(i+1,j+1,22,13))
            pygame.draw.rect(surface,(60,35,20),(i,j,23,14),1)
    for lx in [W//5,W//2,W*4//5]:
        for r,a in [(160,18),(100,32),(55,52)]:
            gl=pygame.Surface((r*2,r*2),pygame.SRCALPHA)
            pygame.draw.circle(gl,(255,170,50,a),(r,r),r)
            surface.blit(gl,(lx-r,0))
        pygame.draw.rect(surface,(55,32,10),(lx-2,0,4,22))
        pygame.draw.rect(surface,(200,155,55),(lx-15,19,30,18))
        pygame.draw.rect(surface,(255,220,110),(lx-11,21,22,14))
    for i in range(0,W,65):
        c=(82,46,18) if i%130==0 else BAR_WOOD
        pygame.draw.rect(surface,c,(i,H*3//5,63,H))
        pygame.draw.line(surface,BAR_WOODL,(i,H*3//5),(i,H),1)
        pygame.draw.line(surface,(72,38,14),(i+32,H*3//5),(i+32,H),1)
    pygame.draw.rect(surface,(52,30,10),(W//5,H//5-5,W*3//5,8))
    pygame.draw.rect(surface,(52,30,10),(W//5,H//4+5,W*3//5,8))
    bottle_cols=[(58,98,148),(142,58,58),(58,142,98),(102,78,142),(200,158,40),
                 (180,80,30),(50,120,160),(160,50,80),(80,160,80),(140,100,50)]
    for i,c in enumerate(bottle_cols):
        bx=W//5+18+i*48; by=H//5-56
        pygame.draw.rect(surface,c,(bx,by,20,54))
        pygame.draw.rect(surface,tuple(min(v+55,255) for v in c),(bx+3,by+4,9,18))
        pygame.draw.rect(surface,(200,200,200),(bx+6,by-8,8,10))
    pygame.draw.rect(surface,(62,35,12),(0,H*3//5-6,W,12))
    pygame.draw.rect(surface,(105,62,26),(0,H*3//5+6,W,38))
    pygame.draw.rect(surface,BAR_WOODL,(0,H*3//5+6,W,8))
    for gx in [W//6,W//3,W//2,W*2//3,W*5//6]:
        pygame.draw.rect(surface,(170,215,240),(gx-9,H*3//5-38,18,34))
        pygame.draw.line(surface,(210,235,255),(gx-7,H*3//5-36),(gx-3,H*3//5-16),1)
    for sx in [W//8,W//4,W*3//8,W*5//8,W*3//4,W*7//8]:
        pygame.draw.circle(surface,(90,50,20),(sx,H*3//5+30),17)
        pygame.draw.circle(surface,(120,72,36),(sx,H*3//5+28),15)
        pygame.draw.rect(surface,(72,40,14),(sx-5,H*3//5+45,10,36))
        pygame.draw.ellipse(surface,(52,28,8),(sx-18,H*3//5+76,36,10))
    pygame.draw.rect(surface,(18,30,20),(W//2-90,H//3,180,55))
    pygame.draw.rect(surface,(30,50,28),(W//2-90,H//3,180,55),2)
    draw_textc(surface,"MENU DU JOUR",W//2,H//3+6,(160,220,140),13)
    draw_textc(surface,"Biere : 4 eur",W//2,H//3+24,(200,240,180),11,bold=False)
    draw_textc(surface,"Whisky: 7 eur",W//2,H//3+38,(200,240,180),11,bold=False)

def draw_hacker_interior(surface):
    W,H=surface.get_size(); surface.fill((4,6,14))
    for i in range(0,W,36): pygame.draw.line(surface,(12,18,28),(i,0),(i,H),1)
    for j in range(0,H,36): pygame.draw.line(surface,(12,18,28),(0,j),(W,j),1)
    for r in [260,190,120]:
        gl=pygame.Surface((r*2,r*2),pygame.SRCALPHA)
        pygame.draw.circle(gl,(0,180,220,max(0,22-r//14)),(r,r),r)
        surface.blit(gl,(W//2-r,H//2-r-50))
    pygame.draw.rect(surface,(8,12,26),(W//2-215,10,430,85))
    pygame.draw.rect(surface,HACK_ACCENT,(W//2-215,10,430,85),2)
    draw_textc(surface,"[ SYSTEM ACCESS GRANTED ]",W//2,18,HACK_ACCENT,14)
    for row in range(5):
        for col in range(10):
            cw=14+(row+col)%3*8; cl=HACK_CODE if (row+col)%4!=0 else HACK_ACCENT
            pygame.draw.rect(surface,cl,(W//2-200+col*43,34+row*10,cw,4))
    pygame.draw.rect(surface,(6,8,18),(0,H*3//5,W,H))
    for dkx,dky in [(22,H*2//5),(W-295,H*2//5)]:
        pygame.draw.rect(surface,(28,22,40),(dkx,dky,270,20))
        pygame.draw.rect(surface,HACK_ACCENT,(dkx,dky,270,20),1)
        pygame.draw.rect(surface,(20,16,32),(dkx,dky+20,270,H))
        for mi in range(2):
            mx=dkx+10+mi*134
            pygame.draw.rect(surface,COMP_BODY,(mx,dky-130,122,128))
            pygame.draw.rect(surface,COMP_SCR,(mx+4,dky-126,114,112))
            pygame.draw.rect(surface,HACK_ACCENT,(mx,dky-130,122,128),2)
            for li in range(10):
                cw=18+(li*11)%64; cl=HACK_CODE if li%3!=0 else HACK_ACCENT
                pygame.draw.rect(surface,cl,(mx+6,dky-120+li*11,cw,4))
            pygame.draw.rect(surface,COMP_BODY,(mx+52,dky-4,18,10))
            pygame.draw.rect(surface,(22,22,38),(mx+4,dky+4,114,14))
            for ki in range(11):
                pygame.draw.rect(surface,(32,32,50),(mx+8+ki*10,dky+6,8,10))
    for i in range(4):
        pts=[(W//2-48+i*34,H*2//5+10)]
        for j in range(5): pts.append((pts[-1][0]+(-1)**j*18,pts[-1][1]+26))
        pygame.draw.lines(surface,(0,110,140),False,pts,2)
    pygame.draw.rect(surface,HACK_ACCENT,(0,H//3,4,H//4))
    pygame.draw.rect(surface,HACK_CODE,(0,H*2//3,4,H//6))
    pygame.draw.rect(surface,HACK_ACCENT,(W-4,H//4,4,H//3))
    for px2,py2,pt,pc in [(W-90,H//3,"PASSWD?",(200,185,80)),(W-148,H//3+5,"TODO",(80,200,130))]:
        pygame.draw.rect(surface,pc,(px2,py2,60,40))
        draw_text(surface,pt,px2+6,py2+12,(30,30,30),11)
    pygame.draw.rect(surface,(42,28,18),(W//2-18,H*2//5-25,36,25))
    pygame.draw.rect(surface,(80,52,32),(W//2-14,H*2//5-23,28,20))

def draw_mafia_interior(surface):
    W,H=surface.get_size(); surface.fill((14,7,7))
    for i in range(0,W,24):
        for j in range(0,H*3//5,14):
            c=(42,24,22) if (i+j)%3!=0 else (30,16,15)
            pygame.draw.rect(surface,c,(i+1,j+1,22,12))
    for a in range(7):
        gl=pygame.Surface((W,H*3//5),pygame.SRCALPHA)
        lx=W//2-40+a*14
        pts=[(lx,0),(lx+80,0),(lx+80+a*20,H*3//5),(lx-a*12,H*3//5)]
        pygame.draw.polygon(gl,(210,170,70,max(0,32-a*4)),pts)
        surface.blit(gl,(0,0))
    pygame.draw.rect(surface,(10,8,6),(W//2-45,14,90,68))
    pygame.draw.rect(surface,(75,60,30),(W//2-45,14,90,68),3)
    pygame.draw.rect(surface,(125,105,55),(W//2-41,18,82,60))
    pygame.draw.line(surface,(75,60,30),(W//2,18),(W//2,78),2)
    pygame.draw.line(surface,(75,60,30),(W//2-41,50),(W//2+41,50),2)
    pygame.draw.rect(surface,(75,60,28),(W//2-3,0,6,H//5+5))
    for cx2 in [W//2-60,W//2-22,W//2+18,W//2+56]:
        pygame.draw.line(surface,(75,60,28),(W//2,H//5),(cx2,H//5+28),2)
        pygame.draw.rect(surface,(200,155,38),(cx2-5,H//5+25,10,20))
        pygame.draw.ellipse(surface,(255,175,38),(cx2-5,H//5+16,10,14))
        pygame.draw.ellipse(surface,(255,235,100),(cx2-3,H//5+18,6,9))
    pygame.draw.rect(surface,(20,12,12),(0,H*3//5,W,H))
    for i in range(0,W,58):
        c=(26,16,14) if i%116==0 else (22,13,12)
        pygame.draw.rect(surface,c,(i,H*3//5,56,H))
        pygame.draw.line(surface,(16,9,9),(i,H*3//5),(i,H),1)
    tw=400; tx2,ty2=W//2-tw//2,H*3//5-32
    pygame.draw.rect(surface,(52,28,16),(tx2,ty2,tw,24))
    pygame.draw.rect(surface,(68,38,20),(tx2,ty2,tw,8))
    pygame.draw.rect(surface,(38,20,10),(tx2,ty2,tw,24),2)
    for leg in [tx2+22,tx2+tw-30]:
        pygame.draw.rect(surface,(42,22,10),(leg,ty2+24,20,H//2))
    pygame.draw.rect(surface,(38,18,18),(W//2-40,H//2-85,80,H//2+25))
    pygame.draw.rect(surface,(58,28,28),(W//2-40,H//2-85,80,26))
    pygame.draw.rect(surface,(28,12,12),(W//2-40,H//2-85,80,H//2+25),2)
    for rx2 in [0,W-46]:
        pygame.draw.rect(surface,(76,16,16),(rx2,0,46,H*2//3))
        pygame.draw.rect(surface,(55,10,10),(rx2,0,46,H*2//3),2)
        for pli in range(0,46,10):
            pygame.draw.line(surface,(38,8,8),(rx2+pli,0),(rx2+pli,H*2//3),1)
    for sx2 in [30,W-52]:
        pygame.draw.rect(surface,(36,18,18),(sx2,H//5,14,H*2//5))
        pygame.draw.rect(surface,(48,26,26),(sx2,H//5,14,H*2//5),1)

# ── CARTE ─────────────────────────────────────────────────
def draw_cobble_bg(surface,W,H):
    surface.fill(COBBLE_D)
    sw,sh=48,30
    for row in range(H//sh+2):
        off=(row%2)*(sw//2)
        for col in range(W//sw+2):
            sx,sy=col*sw-off,row*sh
            c=COBBLE_L if (row+col)%3!=0 else (132,122,106)
            pygame.draw.rect(surface,c,(sx+1,sy+1,sw-2,sh-2))
            pygame.draw.rect(surface,COBBLE_LINE,(sx,sy,sw,sh),1)
def draw_grass_patch(surface,x,y,w,h):
    pygame.draw.rect(surface,GRASS_D,(x,y,w,h))
    for i in range(0,w,10):
        for j in range(0,h,10):
            c=GRASS_L if (i+j)%20==0 else GRASS_D
            pygame.draw.rect(surface,c,(x+i,y+j,8,8))
    pygame.draw.rect(surface,(42,92,40),(x,y,w,h),2)
def draw_bush(surface,cx,y,size=18):
    pygame.draw.circle(surface,BUSH_D,(cx,y+size//2),size)
    pygame.draw.circle(surface,BUSH_L,(cx-size//3,y+size//3),size*2//3)
    pygame.draw.circle(surface,BUSH_L,(cx+size//3,y+size//4),size//2)
    pygame.draw.circle(surface,(88,160,68),(cx,y),size//3)
def draw_tree(surface,cx,y):
    pygame.draw.rect(surface,TREE_TR,(cx-5,y+22,10,16))
    pygame.draw.circle(surface,TREE_D,(cx,y+10),22)
    pygame.draw.circle(surface,TREE_M,(cx+4,y+6),16)
    pygame.draw.circle(surface,TREE_L,(cx-6,y+10),12)
def draw_flower_patch(surface,cx,cy):
    import random; rng=random.Random(cx*7+cy)
    cols=[(255,80,80),(255,210,40),(200,100,255),(255,160,80)]
    for _ in range(6):
        fx=cx+rng.randint(-14,14); fy=cy+rng.randint(-8,8)
        c=cols[rng.randint(0,3)]
        pygame.draw.circle(surface,c,(fx,fy),3)
        pygame.draw.circle(surface,(255,245,150),(fx,fy),1)
def draw_lamp(surface,x,y):
    pygame.draw.rect(surface,LAMP_POST,(x-2,y+8,4,55))
    pygame.draw.rect(surface,LAMP_POST,(x-2,y+8,18,4))
    pygame.draw.rect(surface,(195,175,78),(x+12,y+2,12,12))
    pygame.draw.rect(surface,LAMP_GLOW,(x+13,y+3,10,10))
def draw_coin(surface,cx,cy,r=10):
    pygame.draw.circle(surface,COIN_DARK,(cx,cy),r)
    pygame.draw.circle(surface,COIN_GOLD,(cx,cy),r-1)
    pygame.draw.circle(surface,COIN_SHINE,(cx-r//3,cy-r//3),r//3)
    draw_textc(surface,"$",cx,cy-6,COIN_DARK,10)
def draw_bench(surface,x,y):
    pygame.draw.rect(surface,(108,72,38),(x,y+8,50,6))
    pygame.draw.rect(surface,(88,58,28),(x+4,y+14,8,10))
    pygame.draw.rect(surface,(88,58,28),(x+38,y+14,8,10))
    pygame.draw.rect(surface,(108,72,38),(x,y,50,5))
def draw_fountain(surface,cx,cy,time_ms=0):
    pygame.draw.circle(surface,(125,158,178),(cx,cy+12),28)
    pygame.draw.circle(surface,(155,188,205),(cx,cy+12),22)
    pygame.draw.circle(surface,(125,158,178),(cx,cy+12),28,2)
    pygame.draw.rect(surface,(145,178,198),(cx-5,cy-8,10,20))
    pygame.draw.circle(surface,(135,205,255),(cx,cy-10),5)
    for i in range(5):
        ang=time_ms*0.003+i*1.26
        pygame.draw.circle(surface,(185,235,255),(cx+int(6*math.cos(ang)),cy-10+int(4*math.sin(ang))),2)
def draw_fake_shop(surface,x,y,w=110,h=90,sign_color=(55,88,145),sign_text="SHOP"):
    for row in range(h//12+1):
        for col in range(w//18+1):
            bx=x+col*18+(row%2)*9; by=y+row*12
            c=BRICK_R if (row+col)%3!=0 else BRICK_D
            pygame.draw.rect(surface,c,(bx,by,16,10))
            pygame.draw.rect(surface,BRICK_M,(bx,by,16,10),1)
    pygame.draw.rect(surface,BRICK_M,(x,y,w,h),2)
    pygame.draw.rect(surface,ROOF_G,(x-4,y-10,w+8,14))
    wx2=x+w//2-22
    pygame.draw.rect(surface,WIN_BLUE,(wx2,y+14,44,36))
    pygame.draw.rect(surface,(55,95,155),(wx2,y+14,44,36),2)
    pygame.draw.line(surface,(55,95,155),(wx2+22,y+14),(wx2+22,y+50),1)
    pygame.draw.line(surface,(55,95,155),(wx2,y+32),(wx2+44,y+32),1)
    pygame.draw.rect(surface,sign_color,(x+w//2-36,y-8,72,22))
    pygame.draw.rect(surface,tuple(min(c+60,255) for c in sign_color),(x+w//2-36,y-8,72,22),2)
    draw_textc(surface,sign_text,x+w//2,y-6,SIGN_TXT,14)
def draw_bar_building(surface,x,y,w=195,h=165):
    for row in range(h//12+1):
        for col in range(w//20+1):
            bx=x+col*20+(row%2)*10; by=y+row*12
            c=BRICK_R if (row+col)%3!=0 else BRICK_D
            pygame.draw.rect(surface,c,(bx,by,18,10)); pygame.draw.rect(surface,BRICK_D,(bx,by,18,10),1)
    pygame.draw.rect(surface,BRICK_M,(x,y,w,h),3)
    pygame.draw.rect(surface,ROOF_G,(x-6,y-12,w+12,16))
    door_x=x+w//2-22; door_y=y+h-62
    pygame.draw.rect(surface,DOOR_BR,(door_x,door_y,44,62))
    pygame.draw.rect(surface,(65,38,12),(door_x,door_y,44,62),2)
    pygame.draw.circle(surface,COIN_GOLD,(door_x+38,door_y+27),4)
    for wx2 in [x+20,x+w-52]:
        pygame.draw.rect(surface,WIN_BLUE,(wx2,y+22,32,32))
        pygame.draw.rect(surface,(55,95,155),(wx2,y+22,32,32),2)
    pygame.draw.rect(surface,SIGN_GRN,(x+w//2-42,y-10,84,28))
    draw_textc(surface,"BAR",x+w//2,y-6,SIGN_TXT,22)
def draw_hacker_building(surface,x,y,w=195,h=165):
    surface.fill(WALL_D,(x,y,w,h))
    for i in range(0,h,22): pygame.draw.line(surface,WALL_G,(x,y+i),(x+w,y+i),1)
    for i in range(0,w,22): pygame.draw.line(surface,WALL_G,(x+i,y),(x+i,y+h),1)
    pygame.draw.rect(surface,(38,38,52),(x,y,w,h),3)
    pygame.draw.rect(surface,(28,28,42),(x-5,y-12,w+10,16))
    pygame.draw.rect(surface,HACK_ACCENT,(x-5,y-12,w+10,16),1)
    door_x=x+w//2-24; door_y=y+h-66
    pygame.draw.rect(surface,(12,12,22),(door_x,door_y,48,66))
    pygame.draw.rect(surface,HACK_ACCENT,(door_x,door_y,48,66),2)
    for wxi,wyi in [(x+14,y+22),(x+w-54,y+22),(x+14,y+82),(x+w-54,y+82)]:
        pygame.draw.rect(surface,COMP_SCR,(wxi,wyi,40,30))
        pygame.draw.rect(surface,HACK_ACCENT,(wxi,wyi,40,30),1)
        for li in range(3): pygame.draw.rect(surface,HACK_CODE,(wxi+4,wyi+7+li*8,16+li*4,3))
    pygame.draw.rect(surface,(18,18,32),(x+w//2-52,y-10,104,28))
    pygame.draw.rect(surface,HACK_ACCENT,(x+w//2-52,y-10,104,28),2)
    draw_textc(surface,"HACKER",x+w//2,y-6,HACK_ACCENT,20)
def draw_mafia_building(surface,x,y,w=195,h=165):
    pygame.draw.rect(surface,MAF_DARK,(x,y,w,h))
    for row in range(h//14+1):
        for col in range(w//22+1):
            bx=x+col*22+(row%2)*11; by=y+row*14
            pygame.draw.rect(surface,MAF_MID,(bx,by,20,12))
            pygame.draw.rect(surface,(22,15,15),(bx,by,20,12),1)
    pygame.draw.rect(surface,(22,14,14),(x,y,w,h),3)
    pygame.draw.rect(surface,(28,18,18),(x-5,y-12,w+10,16))
    pygame.draw.rect(surface,MAF_RED,(x-5,y-12,w+10,16),2)
    door_x=x+w//2-26; door_y=y+h-68
    pygame.draw.rect(surface,(18,12,12),(door_x,door_y,52,68))
    pygame.draw.rect(surface,(62,18,18),(door_x,door_y,52,68),3)
    for wxi in [x+18,x+w-42]:
        pygame.draw.rect(surface,(16,10,10),(wxi,y+26,24,48))
        pygame.draw.rect(surface,MAF_RED,(wxi,y+26,24,48),2)
    pygame.draw.rect(surface,(58,12,12),(x+w//2-46,y-10,92,28))
    pygame.draw.rect(surface,(145,28,28),(x+w//2-46,y-10,92,28),2)
    draw_textc(surface,"MAFIA",x+w//2,y-6,(255,98,98),20)
def draw_map(surface,W,H,coins,time_ms,level_unlocked):
    draw_cobble_bg(surface,W,H)
    draw_grass_patch(surface,18,80,210,135); draw_grass_patch(surface,18,295,175,195)
    draw_grass_patch(surface,W-230,295,215,195); draw_grass_patch(surface,248,H-72,408,55)
    for bx,by,bsz in [(42,88,20),(88,88,16),(135,95,22),(52,310,18),(92,310,20),
                      (W-188,305,20),(W-138,305,16),(W-82,310,22),
                      (260,H-68,14),(320,H-68,16),(380,H-68,12),(430,H-68,18),(490,H-68,14)]:
        draw_bush(surface,bx,by,bsz)
    for fx,fy in [(70,175),(115,185),(W-165,175),(W-115,185),(305,H-55),(415,H-55),(470,H-55)]:
        draw_flower_patch(surface,fx,fy)
    for tx,ty in [(50,88),(95,88),(148,88),(45,305),(98,305),(W-185,305),(W-135,305),(W-82,305)]:
        draw_tree(surface,tx,ty)
    draw_lamp(surface,28,215); draw_lamp(surface,W-42,215); draw_lamp(surface,W//2-10,255)
    draw_fountain(surface,W//2,H//2+20,time_ms)
    draw_bench(surface,W//2-65,H//2+50); draw_bench(surface,W//2+15,H//2+50)
    draw_fake_shop(surface,240,H-165,108,88,(42,72,128),"CAFE")
    draw_fake_shop(surface,373,H-165,108,88,(72,42,108),"BOOKS")
    draw_fake_shop(surface,506,H-165,108,88,(32,92,58),"MARKET")
    bob=int(math.sin(time_ms*0.003)*4)
    for c in coins:
        if not c[2]: draw_coin(surface,c[0],c[1]+bob,10)
    draw_bar_building(surface,22,52)
    draw_hacker_building(surface,W-228,52)
    draw_mafia_building(surface,W-228,360)
    if level_unlocked<2:
        s2=pygame.Surface((195,165),pygame.SRCALPHA); s2.fill((0,0,0,145)); surface.blit(s2,(W-228,52))
        draw_textc(surface,"[ VERROUILLE ]",W-130,132,(180,80,80),14)
    if level_unlocked<3:
        s2=pygame.Surface((195,165),pygame.SRCALPHA); s2.fill((0,0,0,145)); surface.blit(s2,(W-228,360))
        draw_textc(surface,"[ VERROUILLE ]",W-130,440,(180,80,80),14)
def draw_menu_bg(surface,time_ms):
    W,H=surface.get_size(); surface.fill(DARK_BG)
    import random; rng=random.Random(7)
    for _ in range(100):
        sx=rng.randint(0,W); sy=rng.randint(0,H)
        br=130+int(60*math.sin(time_ms*0.001+sx*0.02))
        pygame.draw.circle(surface,(br,br,br),(sx,sy),rng.randint(1,2))
    pulse=int(math.sin(time_ms*0.0018)*22)
    draw_textc(surface,"DARK  QUEST",W//2,H//3-12,(222+pulse,198,28),68)
    draw_textc(surface,"-- 2 D --",W//2,H//3+60,(148,138,98),26)
    pygame.draw.line(surface,(78,58,18),(W//2-185,H//3+95),(W//2+185,H//3+95),2)
def draw_hud(surface,W,lives=4,coins=0,level=1):
    pygame.draw.rect(surface,HUD_BG,(0,0,W,42))
    pygame.draw.rect(surface,HUD_BORDER,(0,0,W,42),2)
    for i in range(4): draw_heart(surface,14+i*32,11,filled=(i<lives))
    draw_textc(surface,"Dark Quest 2D",W//2,12,WHITE,20)
    draw_coin(surface,W-115,21,9)
    draw_text(surface,f"x {coins}",W-102,13,UI_GOLD,16)
    draw_text(surface,f"Niv.{level}",W-52,13,(178,178,228),15)
def draw_heart(surface,x,y,size=20,filled=True):
    c=(222,48,48) if filled else (75,38,38)
    pts=[(x+size//2,y+size-2),(x+2,y+size//3),(x+2,y+size//6),
         (x+size//2,y),(x+size-2,y+size//6),(x+size-2,y+size//3)]
    pygame.draw.polygon(surface,c,pts)
    pygame.draw.circle(surface,c,(x+size//4+1,y+size//4),size//4)
    pygame.draw.circle(surface,c,(x+3*size//4-1,y+size//4),size//4)
    if filled: pygame.draw.circle(surface,(255,125,125),(x+size//4,y+size//4-1),size//8)
def draw_arrow(surface,x,y,time_ms):
    bob=int(math.sin(time_ms*0.004)*7); ay=y+bob
    pts=[(x,ay+18),(x-10,ay+6),(x-5,ay+6),(x-5,ay-8),(x+5,ay-8),(x+5,ay+6),(x+10,ay+6)]
    pygame.draw.polygon(surface,ARROW_Y,pts); pygame.draw.polygon(surface,(198,158,0),pts,2)
def draw_star(surface,cx,cy,r,col=STAR_Y,border=(198,158,0)):
    pts=[]
    for i in range(10):
        ang=math.pi/2+i*math.pi/5; rad=r if i%2==0 else r//2
        pts.append((cx+int(rad*math.cos(ang)),cy-int(rad*math.sin(ang))))
    pygame.draw.polygon(surface,col,pts); pygame.draw.polygon(surface,border,pts,2)
def draw_level_complete_screen(surface,level,time_ms):
    W,H=surface.get_size()
    ov=pygame.Surface((W,H),pygame.SRCALPHA); ov.fill((0,0,0,168)); surface.blit(ov,(0,0))
    draw_textc(surface,f"NIVEAU {level} TERMINE !",W//2,H//2-90,UI_GOLD,34)
    for i in range(3):
        sc=1.0+0.18*math.sin(time_ms*0.004+i)
        draw_star(surface,W//2-80+i*80,H//2-15,int(36*sc))
    draw_textc(surface,"ESPACE pour retourner a la carte",W//2,H//2+55,WHITE,20)
def draw_victory_screen(surface,char_fn=None):
    W,H=surface.get_size(); surface.fill((8,18,8))
    if char_fn: char_fn(surface,W//2-14,H//2-30,scale=5)
    ov=pygame.Surface((W,H),pygame.SRCALPHA); ov.fill((0,50,0,100)); surface.blit(ov,(0,0))
    for i in range(7):
        draw_star(surface,80+i*120,H//5,22+i%3*8,col=(255,212+i*5,0) if i%2==0 else (255,165,0))
    draw_textc(surface,"VICTOIRE !",W//2,H//5+30,UI_GOLD,54)
    draw_textc(surface,"Ta famille est liberee !",W//2,H//5+95,(155,235,155),24)
    draw_textc(surface,"ESPACE pour rejouer",W//2,H-55,(155,155,155),18)
def draw_char_select(surface,mouse):
    W,H=surface.get_size()
    draw_cobble_bg(surface,W,H)
    ov=pygame.Surface((W,H),pygame.SRCALPHA); ov.fill((0,0,0,135)); surface.blit(ov,(0,0))
    draw_textc(surface,"CHOISIS TON PERSONNAGE",W//2,44,UI_GOLD,30)
    # Essaie de charger les vraies images
    boy_img  = load_img("boy.png",  (130, 170))
    girl_img = load_img("girl.png", (130, 170))
    rects=[]
    for idx,(name,fn,cx,img) in enumerate([("CHARLES",draw_charles,W//4,boy_img),
                                             ("CELIA",  draw_celia,  3*W//4,girl_img)]):
        hov=abs(mouse[0]-cx)<108 and 85<mouse[1]<480
        pygame.draw.rect(surface,(38,52,88) if hov else (22,28,52),(cx-108,85,216,395),border_radius=8)
        pygame.draw.rect(surface,DLGBRD if hov else HUD_BORDER,(cx-108,85,216,395),3,border_radius=8)
        if img:
            surface.blit(img,(cx-65,105))
        else:
            fn(surface,cx-14,108,scale=6)
        draw_textc(surface,name,cx,335,WHITE,24)
        draw_textc(surface,"Age : 14 ans",cx,365,(175,175,175),16)
        draw_textc(surface,"Nationalite : Francaise",cx,390,(175,175,175),16)
        draw_textc(surface,"IP : 192.168.0.1",cx,415,HACK_ACCENT,15)
        r=draw_button(surface,"CHOISIR",cx,460,w=160,h=42,col=(75,118,195) if hov else (55,88,155),hover=hov)
        rects.append(r)
    return rects