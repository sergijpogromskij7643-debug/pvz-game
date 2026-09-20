# ==============================================================
#  PLANTS vs ZOMBIES v8.0 - Ultimate Edition
# ==============================================================
import pygame, random, math, sys, os, json

VERSION = "8.0"
GAME_TITLE = "PvZ: Ultimate"
AUTHOR = "Твоя власна гра"
EASTER_DAHSA = "Даша"

pygame.init()
RENDER_W, RENDER_H = 960, 540

info = pygame.display.Info()
DETECTED_W = info.current_w if info.current_w > 0 else 1280
DETECTED_H = info.current_h if info.current_h > 0 else 720
if DETECTED_H > DETECTED_W:
    DETECTED_W, DETECTED_H = DETECTED_H, DETECTED_W

SCREEN_W, SCREEN_H = RENDER_W, RENDER_H
FPS = 60
SCALE = RENDER_W / 1280.0
UI_HEIGHT = int(120 * SCALE)
GRID_COLS, GRID_ROWS = 9, 5
GRID_LEFT = int(110 * SCALE)
GRID_TOP = UI_HEIGHT
CELL_W = (SCREEN_W - GRID_LEFT - int(15 * SCALE)) // GRID_COLS
CELL_H = (SCREEN_H - UI_HEIGHT - int(15 * SCALE)) // GRID_ROWS
GRID_W = GRID_COLS * CELL_W
GRID_H = GRID_ROWS * CELL_H
MAX_PARTICLES = 150
WHITE = (255, 255, 255); BLACK = (20, 20, 20)

def S(v): return int(v * SCALE)
def cell_center(c, r): return (GRID_LEFT + c*CELL_W + CELL_W//2, GRID_TOP + r*CELL_H + CELL_H//2)
def pos_to_cell(x, y):
    if not (GRID_LEFT <= x < GRID_LEFT+GRID_W): return None
    if not (GRID_TOP <= y < GRID_TOP+GRID_H): return None
    return int((x-GRID_LEFT)//CELL_W), int((y-GRID_TOP)//CELL_H)
def draw_ts(surf, text, font, color, center, sh=(0,0,0), off=3):
    shs = font.render(text, True, sh); surf.blit(shs, shs.get_rect(center=(center[0]+off, center[1]+off)))
    t = font.render(text, True, color); surf.blit(t, t.get_rect(center=center))
def lerp(a, b, t): return a + (b-a)*t
_circle_cache = {}
def gsc(radius, color):
    key = (radius, color)
    if key in _circle_cache: return _circle_cache[key]
    r = max(2, radius); surf = pygame.Surface((r*2, r*2), pygame.SRCALPHA)
    for i in range(3):
        a = 90 + i*60; rad = r-i
        if rad > 0: pygame.draw.circle(surf, (color[0],color[1],color[2],min(255,a)), (r,r), rad)
    _circle_cache[key] = surf; return surf
_shadow_cache = {}
def get_shadow(w, h):
    key = (w, h)
    if key in _shadow_cache: return _shadow_cache[key]
    s = pygame.Surface((w, h), pygame.SRCALPHA)
    pygame.draw.ellipse(s, (0,0,0,80), (0,0,w,h))
    _shadow_cache[key] = s; return s

# ==============================================================
#  ПЕРЕКЛАДИ
# ==============================================================
LANG = {
    "uk": {"play":"ГРАТИ","tutorial":"НАВЧАННЯ","settings":"НАЛАШТУВАННЯ","exit":"ВИХІД",
        "back":"НАЗАД","restart":"ЩЕ РАЗ","levels":"РІВНІ","menu":"МЕНЮ","about":"ПРО ГРУ",
        "victory":"ПЕРЕМОГА!","gameover":"ГРУ ЗАВЕРШЕНО","paused":"ПАУЗА",
        "tap_continue":"Тап - продовжити","time":"Час","killed":"Вбито","location":"Локація",
        "select_location":"ВИБІР ЛОКАЦІЇ","version":"Версія","sound":"Звук","music":"Музика",
        "show_fps":"Показувати FPS","particles":"Частинки","screen_shake":"Тряска екрана",
        "auto_collect":"Авто-збір сонця","difficulty":"Складність","easy":"ЛЕГКА",
        "normal":"НОРМ","hard":"ВАЖКА","game_speed":"Швидкість","language":"Мова",
        "yes":"ТАК","no":"НІ","on":"УВІМК","off":"ВИКЛ","scroll_hint":"Прокрути вгору/вниз",
        "killed_label":"Знищено","sec":"с","loading":"ЗАВАНТАЖЕННЯ...","tap_anywhere":"Тап де завгодно далі",
        "player_name":"Ім'я гравця","credits":"Автор","made_with":"Зроблено з",
        "secret_found":"СЕКРЕТ ЗНАЙДЕНО!"},
    "ru": {"play":"ИГРАТЬ","tutorial":"ОБУЧЕНИЕ","settings":"НАСТРОЙКИ","exit":"ВЫХОД",
        "back":"НАЗАД","restart":"ЕЩЁ РАЗ","levels":"УРОВНИ","menu":"МЕНЮ","about":"О ИГРЕ",
        "victory":"ПОБЕДА!","gameover":"ИГРА ОКОНЧЕНА","paused":"ПАУЗА",
        "tap_continue":"Тап - продолжить","time":"Время","killed":"Убито","location":"Локация",
        "select_location":"ВЫБОР ЛОКАЦИИ","version":"Версия","sound":"Звук","music":"Музыка",
        "show_fps":"Показывать FPS","particles":"Частицы","screen_shake":"Тряска экрана",
        "auto_collect":"Авто-сбор солнца","difficulty":"Сложность","easy":"ЛЁГКАЯ",
        "normal":"НОРМ","hard":"ТЯЖЁЛАЯ","game_speed":"Скорость","language":"Язык",
        "yes":"ДА","no":"НЕТ","on":"ВКЛ","off":"ВЫКЛ","scroll_hint":"Прокрути вверх/вниз",
        "killed_label":"Уничтожено","sec":"с","loading":"ЗАГРУЗКА...","tap_anywhere":"Тап куда угодно",
        "player_name":"Имя игрока","credits":"Автор","made_with":"Сделано с",
        "secret_found":"СЕКРЕТ НАЙДЕН!"},
    "en": {"play":"PLAY","tutorial":"TUTORIAL","settings":"SETTINGS","exit":"EXIT",
        "back":"BACK","restart":"RETRY","levels":"LEVELS","menu":"MENU","about":"ABOUT",
        "victory":"VICTORY!","gameover":"GAME OVER","paused":"PAUSED",
        "tap_continue":"Tap to continue","time":"Time","killed":"Killed","location":"Location",
        "select_location":"SELECT LOCATION","version":"Version","sound":"Sound","music":"Music",
        "show_fps":"Show FPS","particles":"Particles","screen_shake":"Screen shake",
        "auto_collect":"Auto-collect sun","difficulty":"Difficulty","easy":"EASY",
        "normal":"NORMAL","hard":"HARD","game_speed":"Speed","language":"Language",
        "yes":"YES","no":"NO","on":"ON","off":"OFF","scroll_hint":"Scroll up/down",
        "killed_label":"Destroyed","sec":"s","loading":"LOADING...","tap_anywhere":"Tap anywhere",
        "player_name":"Player name","credits":"Author","made_with":"Made with",
        "secret_found":"SECRET FOUND!"},
}
LEVEL_NAMES = [
    ("Перший день","Первый день","First Day"),
    ("Полудень","Полдень","Noon"),
    ("Присмерк","Сумерки","Dusk"),
    ("Темна ніч","Тёмная ночь","Dark Night"),
    ("Місячна ніч","Лунная ночь","Moonlit Night"),
    ("Кінець світу","Конец света","End of World"),
    ("СЕКРЕТНА ЛОКАЦІЯ","СЕКРЕТНАЯ","SECRET LOCATION"),
]

LEVELS = [
    {"name_idx":0,"sun_start":250,"win_time":90,"spawn_base":10.0,"spawn_decay":0.03,
     "sky_sun_range":(5,8),"zombies":["normal","cone"],
     "sky_top":(135,206,235),"sky_bot":(200,230,240),
     "lawn_a":(104,176,76),"lawn_b":(86,156,62),"tint":None,"weather":"clear"},
    {"name_idx":1,"sun_start":200,"win_time":110,"spawn_base":8.5,"spawn_decay":0.04,
     "sky_sun_range":(5,8),"zombies":["normal","cone","flag"],
     "sky_top":(255,200,100),"sky_bot":(255,235,170),
     "lawn_a":(120,180,70),"lawn_b":(100,160,55),"tint":(255,220,120,30),"weather":"clear"},
    {"name_idx":2,"sun_start":175,"win_time":130,"spawn_base":7.5,"spawn_decay":0.05,
     "sky_sun_range":(5,7),"zombies":["normal","cone","runner","newspaper"],
     "sky_top":(200,100,140),"sky_bot":(255,180,130),
     "lawn_a":(90,150,70),"lawn_b":(75,130,55),"tint":(200,100,140,40),"weather":"clear"},
    {"name_idx":3,"sun_start":150,"win_time":150,"spawn_base":6.5,"spawn_decay":0.06,
     "sky_sun_range":(4,6),"zombies":["normal","cone","bucket","runner","flag","screendoor","toxic"],
     "sky_top":(20,25,60),"sky_bot":(60,70,120),
     "lawn_a":(60,100,60),"lawn_b":(45,80,45),"tint":(20,30,80,90),"weather":"stars"},
    {"name_idx":4,"sun_start":125,"win_time":180,"spawn_base":5.5,"spawn_decay":0.07,
     "sky_sun_range":(4,6),"zombies":["normal","cone","bucket","runner","football","balloon","electric","healer"],
     "sky_top":(40,50,100),"sky_bot":(100,130,180),
     "lawn_a":(60,110,80),"lawn_b":(45,90,60),"tint":(60,80,150,80),"weather":"moon"},
    {"name_idx":5,"sun_start":100,"win_time":200,"spawn_base":4.5,"spawn_decay":0.08,
     "sky_sun_range":(4,6),"zombies":["normal","cone","bucket","runner","football","giant",
                                       "dancing","invisible","bomber","shield","fire","ice"],
     "sky_top":(120,20,20),"sky_bot":(200,80,40),
     "lawn_a":(110,70,50),"lawn_b":(90,55,40),"tint":(200,40,40,50),"weather":"fire"},
    {"name_idx":6,"sun_start":500,"win_time":240,"spawn_base":3.0,"spawn_decay":0.02,
     "sky_sun_range":(2,4),"zombies":["normal","bucket","football","giant","dancing",
                                       "invisible","bomber","shield","fire","ice","toxic",
                                       "electric","healer","dahsa"],
     "sky_top":(255,100,200),"sky_bot":(255,200,255),
     "lawn_a":(200,100,200),"lawn_b":(180,80,180),"tint":(255,150,255,40),"weather":"clear"},
]

# ==============================================================
#  ЧАСТИНКИ
# ==============================================================
class Particle:
    __slots__ = ('x','y','vx','vy','color','size','life','max_life','gravity','remove')
    def __init__(self, x, y, vx, vy, color, size, life, gravity=0):
        self.x, self.y = x, y; self.vx, self.vy = vx, vy
        self.color = color; self.size = size
        self.life = life; self.max_life = life; self.gravity = gravity; self.remove = False
    def update(self, dt):
        self.x += self.vx*dt; self.y += self.vy*dt; self.vy += self.gravity*dt
        self.life -= dt
        if self.life <= 0: self.remove = True
    def draw(self, screen):
        a = max(0.0, self.life/self.max_life); sz = max(1, int(self.size*(0.3+0.7*a)))
        screen.blit(gsc(sz, self.color), (int(self.x-sz), int(self.y-sz)))

class FloatingText:
    __slots__ = ('x','y','vy','text','color','life','max_life','font','remove')
    def __init__(self, x, y, text, color, font, life=1.0):
        self.x, self.y = x, y; self.vy = -70*SCALE; self.text = text; self.color = color
        self.life = life; self.max_life = life; self.font = font; self.remove = False
    def update(self, dt):
        self.y += self.vy*dt; self.vy *= 0.93; self.life -= dt
        if self.life <= 0: self.remove = True
    def draw(self, screen):
        a = max(0, min(255, int(255*(self.life/self.max_life))))
        t = self.font.render(self.text, True, self.color); t.set_alpha(a)
        screen.blit(t, t.get_rect(center=(self.x, self.y)))

class FlyingSun:
    def __init__(self, x, y, tx, ty, value):
        self.sx, self.sy = x, y; self.tx, self.ty = tx, ty
        self.x, self.y = x, y; self.value = value
        self.t = 0.0; self.duration = 0.4; self.remove = False
    def update(self, dt):
        self.t += dt; p = min(1.0, self.t/self.duration); e = 1-(1-p)**2
        arc = math.sin(p*math.pi)*60*SCALE
        self.x = lerp(self.sx, self.tx, e); self.y = lerp(self.sy, self.ty, e)-arc
        if p >= 1.0: self.remove = True
    def draw(self, screen):
        cx, cy = int(self.x), int(self.y)
        pygame.draw.circle(screen, (255,205,30), (cx,cy), S(18))
        pygame.draw.circle(screen, (255,245,160), (cx,cy), S(10))

class Sun:
    RADIUS = S(30); TAP_RADIUS = S(60); LIFETIME = 12.0; VALUE = 25
    def __init__(self, x, y, ty, value=VALUE):
        self.x, self.y = x, y; self.target_y = ty; self.value = value
        self.life = self.LIFETIME; self.remove = False
        self.anim = random.uniform(0, math.tau); self.landed = False
    def update(self, dt):
        self.anim += dt*2
        if self.y < self.target_y: self.y = min(self.target_y, self.y+130*SCALE*dt)
        else:
            if not self.landed: self.landed = True
            self.life -= dt
            if self.life <= 0: self.remove = True
    def contains(self, pos):
        dx, dy = pos[0]-self.x, pos[1]-self.y
        return dx*dx+dy*dy <= self.TAP_RADIUS**2
    def draw(self, screen):
        r = int(self.RADIUS + math.sin(self.anim)*2); cx, cy = int(self.x), int(self.y)
        pygame.draw.circle(screen, (255,205,30), (cx,cy), r)
        pygame.draw.circle(screen, (255,240,140), (cx,cy), int(r*0.55))
        if self.landed and self.life < 3.0 and int(self.life*6)%2 == 0:
            pygame.draw.circle(screen, WHITE, (cx,cy), r+4, 3)

# ==============================================================
#  РОСЛИНИ
# ==============================================================
class Plant:
    cost = 0; max_hp = 100; base_cooldown = 5.0
    def __init__(self, col, row):
        self.col, self.row = col, row; self.x, self.y = cell_center(col, row)
        self.hp = self.max_hp; self.alive = True
        self.anim = random.uniform(0, math.tau); self.place_anim = 0.0
    def update(self, dt, game):
        self.anim += dt
        if self.place_anim < 1.0: self.place_anim = min(1.0, self.place_anim+dt*5)
    def take_damage(self, dmg):
        self.hp -= dmg
        if self.hp <= 0: self.hp = 0; self.alive = False
    def draw(self, screen): pass

class Sunflower(Plant):
    cost = 50; max_hp = 100; base_cooldown = 5.0; PI = 9.0
    def __init__(self, col, row):
        super().__init__(col, row); self.timer = random.uniform(3, 5)
    def update(self, dt, game):
        super().update(dt, game); self.timer -= dt
        if self.timer <= 0:
            self.timer = self.PI
            game.suns.append(Sun(self.x+random.randint(-S(15),S(15)), self.y-S(20),
                                 self.y+random.randint(S(15),S(35))))
    def draw(self, screen):
        sc = 0.3+0.7*self.place_anim; cx = int(self.x); cy = int(self.y+math.sin(self.anim*2)*2)
        pygame.draw.line(screen, (40,120,40), (cx,cy+S(26)), (cx,cy+S(10)), S(7))
        for i in range(8):
            a = i*math.tau/8+self.anim*0.4
            pygame.draw.circle(screen, (255,205,40),
                (int(cx+math.cos(a)*S(24)*sc), int(cy+math.sin(a)*S(24)*sc)), int(S(12)*sc))
        pygame.draw.circle(screen, (140,85,35), (cx,cy), int(S(18)*sc))
        pygame.draw.circle(screen, BLACK, (cx-S(6),cy-S(3)), S(2))
        pygame.draw.circle(screen, BLACK, (cx+S(6),cy-S(3)), S(2))

class Peashooter(Plant):
    cost = 100; max_hp = 100; base_cooldown = 6.0; FIRE_INTERVAL = 1.4
    def __init__(self, col, row):
        super().__init__(col, row); self.timer = 0.0; self.recoil = 0.0
    def update(self, dt, game):
        super().update(dt, game)
        if self.recoil > 0: self.recoil = max(0, self.recoil-dt*60)
        self.timer -= dt
        if self.timer <= 0 and game.zombie_in_row(self.row, self.x):
            self.timer = self.FIRE_INTERVAL; self.recoil = S(8)
            game.projectiles.append(Pea(self.x+S(24), self.y-S(12), self.row, "green"))
    def draw(self, screen):
        sc = 0.3+0.7*self.place_anim; cx = int(self.x); cy = int(self.y+math.sin(self.anim*2)*2)
        pygame.draw.line(screen, (40,120,40), (cx,cy+S(26)), (cx,cy+S(8)), S(7))
        bx = cx+S(18)-int(self.recoil)
        pygame.draw.circle(screen, (50,150,50), (bx,cy-S(8)), S(10))
        pygame.draw.circle(screen, (70,180,70), (cx,cy-S(5)), int(S(20)*sc))
        pygame.draw.circle(screen, WHITE, (cx+S(6),cy-S(10)), S(5))
        pygame.draw.circle(screen, BLACK, (cx+S(8),cy-S(10)), S(2))

class Repeater(Peashooter):
    cost = 200; base_cooldown = 8.0
    def __init__(self, col, row):
        super().__init__(col, row); self.burst = 0; self.bt = 0.0
    def update(self, dt, game):
        Plant.update(self, dt, game)
        if self.recoil > 0: self.recoil = max(0, self.recoil-dt*60)
        self.timer -= dt
        if self.burst > 0:
            self.bt -= dt
            if self.bt <= 0:
                self.bt = 0.15; self.burst -= 1
                game.projectiles.append(Pea(self.x+S(24), self.y-S(12), self.row, "green"))
                self.recoil = S(8)
        if self.timer <= 0 and game.zombie_in_row(self.row, self.x):
            self.timer = self.FIRE_INTERVAL; self.burst = 2; self.bt = 0.0
    def draw(self, screen):
        sc = 0.3+0.7*self.place_anim; cx = int(self.x); cy = int(self.y+math.sin(self.anim*2)*2)
        pygame.draw.line(screen, (40,120,40), (cx,cy+S(26)), (cx,cy+S(8)), S(7))
        bx = cx+S(20)-int(self.recoil)
        pygame.draw.circle(screen, (50,150,50), (bx,cy-S(16)), S(9))
        pygame.draw.circle(screen, (50,150,50), (bx,cy-S(2)), S(9))
        pygame.draw.circle(screen, (70,180,70), (cx,cy-S(5)), int(S(22)*sc))
        pygame.draw.circle(screen, WHITE, (cx+S(6),cy-S(10)), S(6))
        pygame.draw.circle(screen, BLACK, (cx+S(8),cy-S(10)), S(2))

class SnowPea(Peashooter):
    cost = 175; base_cooldown = 8.0; FIRE_INTERVAL = 1.5
    def update(self, dt, game):
        Plant.update(self, dt, game)
        if self.recoil > 0: self.recoil = max(0, self.recoil-dt*60)
        self.timer -= dt
        if self.timer <= 0 and game.zombie_in_row(self.row, self.x):
            self.timer = self.FIRE_INTERVAL; self.recoil = S(8)
            game.projectiles.append(Pea(self.x+S(24), self.y-S(12), self.row, "blue"))
    def draw(self, screen):
        sc = 0.3+0.7*self.place_anim; cx = int(self.x); cy = int(self.y+math.sin(self.anim*2)*2)
        pygame.draw.line(screen, (40,120,40), (cx,cy+S(26)), (cx,cy+S(8)), S(7))
        bx = cx+S(18)-int(self.recoil)
        pygame.draw.circle(screen, (100,180,220), (bx,cy-S(8)), S(10))
        pygame.draw.circle(screen, (140,210,240), (cx,cy-S(5)), int(S(20)*sc))
        pygame.draw.circle(screen, WHITE, (cx+S(6),cy-S(10)), S(5))
        pygame.draw.circle(screen, BLACK, (cx+S(8),cy-S(10)), S(2))

class Wallnut(Plant):
    cost = 50; max_hp = 800; base_cooldown = 20.0
    def draw(self, screen):
        sc = 0.3+0.7*self.place_anim; cx, cy = int(self.x), int(self.y)
        w = int(S(34)*sc); h = int(S(80)*sc)
        pygame.draw.ellipse(screen, (175,115,55), (cx-w, cy-h//2, w*2, h))
        pygame.draw.ellipse(screen, (115,68,25), (cx-w, cy-h//2, w*2, h), 3)
        r = self.hp/self.max_hp
        if r < 0.66: pygame.draw.line(screen, (100,55,20), (cx-S(12),cy-S(22)), (cx-S(4),cy-S(6)), 2)
        if r < 0.33: pygame.draw.line(screen, (100,55,20), (cx+S(10),cy-S(18)), (cx+S(2),cy+S(6)), 2)
        pygame.draw.circle(screen, WHITE, (cx-S(10),cy-S(5)), S(6))
        pygame.draw.circle(screen, WHITE, (cx+S(10),cy-S(5)), S(6))
        pygame.draw.circle(screen, BLACK, (cx-S(8),cy-S(5)), S(2))
        pygame.draw.circle(screen, BLACK, (cx+S(8),cy-S(5)), S(2))

class CherryBomb(Plant):
    cost = 150; max_hp = 100; base_cooldown = 25.0
    def __init__(self, col, row):
        super().__init__(col, row); self.fuse = 0.9
    def update(self, dt, game):
        super().update(dt, game); self.fuse -= dt
        if self.fuse <= 0:
            cx, cy = self.x, self.y
            game.trigger_shake(0.4, S(14)); game.flash_screen(255, (255,200,80), 0.2)
            for _ in range(40):
                a = random.uniform(0, math.tau); s = random.uniform(150, 450)
                c = random.choice([(255,200,50),(255,130,40),(255,80,30)])
                game.particles.append(Particle(cx,cy,math.cos(a)*s,math.sin(a)*s,c,
                    random.randint(8,16),random.uniform(0.5,1.0),gravity=200))
            for z in game.zombies:
                if not z.alive: continue
                if abs(z.row-self.row) <= 1 and abs(z.x-cx) < CELL_W*1.7:
                    z.take_damage(1800); game.spawn_death_particles(z.x,z.y); game.zombies_killed += 1
            self.alive = False
    def draw(self, screen):
        sc = 0.3+0.7*self.place_anim; cx, cy = int(self.x), int(self.y)
        fl = int(self.fuse*12)%2 == 0 and self.fuse < 0.6
        b = (255,80,80) if fl else (180,30,30)
        pygame.draw.circle(screen, b, (cx-S(10),cy+S(8)), int(S(22)*sc))
        pygame.draw.circle(screen, b, (cx+S(10),cy+S(8)), int(S(22)*sc))
        pygame.draw.line(screen, (60,100,40), (cx,cy-S(10)), (cx,cy-S(28)), 3)
        pygame.draw.circle(screen, (255,220,50), (cx,cy-S(30)), S(4))

class Chomper(Plant):
    cost = 150; max_hp = 100; base_cooldown = 22.0
    RANGE = S(120); CHEW_TIME = 14.0
    def __init__(self, col, row):
        super().__init__(col, row); self.chew_timer = 0.0
    def update(self, dt, game):
        super().update(dt, game)
        if self.chew_timer > 0: self.chew_timer -= dt; return
        target = None
        for z in game.zombies:
            if not z.alive: continue
            if z.row == self.row and 0 < z.x-self.x < self.RANGE:
                if target is None or z.x < target.x: target = z
        if target is not None:
            target.take_damage(99999); game.spawn_death_particles(target.x,target.y); game.zombies_killed += 1
            game.floating_texts.append(FloatingText(self.x,self.y-S(35),"YUM!",
                (255,200,80),game.f_med,life=1.0))
            self.chew_timer = self.CHEW_TIME
    def draw(self, screen):
        sc = 0.3+0.7*self.place_anim; cx = int(self.x); cy = int(self.y+math.sin(self.anim*1.5)*2)
        pygame.draw.line(screen, (40,100,40), (cx,cy+S(26)), (cx,cy+S(8)), S(7))
        mo = 1.0 if self.chew_timer <= 0 else 0.2
        pygame.draw.ellipse(screen, (90,160,60),
            (cx-int(S(26)*sc),cy-int(S(18)*sc),int(S(52)*sc),int(S(44)*sc)))
        mh = int(S(18)*sc*mo)
        pygame.draw.ellipse(screen, (150,40,60), (cx+int(S(6)*sc),cy-mh//2,int(S(26)*sc),mh))
        pygame.draw.circle(screen, WHITE, (cx-S(8),cy-S(6)), S(4))
        pygame.draw.circle(screen, BLACK, (cx-S(8),cy-S(6)), S(2))

# НОВІ РОСЛИНИ
class Threepeater(Peashooter):
    cost = 325; base_cooldown = 12.0
    def update(self, dt, game):
        Plant.update(self, dt, game)
        if self.recoil > 0: self.recoil = max(0, self.recoil-dt*60)
        self.timer -= dt
        if self.timer <= 0:
            fired = False
            for dr in (-1, 0, 1):
                nr = self.row + dr
                if 0 <= nr < GRID_ROWS and game.zombie_in_row(nr, self.x):
                    game.projectiles.append(Pea(self.x+S(24), self.y-S(12)+dr*S(20), nr, "green"))
                    fired = True
            if fired:
                self.timer = self.FIRE_INTERVAL; self.recoil = S(8)
    def draw(self, screen):
        sc = 0.3+0.7*self.place_anim; cx = int(self.x); cy = int(self.y)
        pygame.draw.line(screen, (40,120,40), (cx,cy+S(26)), (cx,cy+S(8)), S(7))
        for dy in (-S(14), 0, S(14)):
            pygame.draw.circle(screen, (50,150,50), (cx+S(18),cy-S(5)+dy), S(9))
        pygame.draw.circle(screen, (70,180,70), (cx,cy-S(5)), int(S(24)*sc))
        pygame.draw.circle(screen, BLACK, (cx-S(7),cy-S(8)), S(2))
        pygame.draw.circle(screen, BLACK, (cx+S(7),cy-S(8)), S(2))

class Jalapeno(Plant):
    cost = 125; max_hp = 100; base_cooldown = 30.0
    def __init__(self, col, row):
        super().__init__(col, row); self.fuse = 1.0
    def update(self, dt, game):
        super().update(dt, game); self.fuse -= dt
        if self.fuse <= 0:
            game.trigger_shake(0.5, S(18)); game.flash_screen(255, (255,120,20), 0.3)
            for _ in range(60):
                a = random.uniform(-math.pi/2, math.pi/2)
                s = random.uniform(200, 600)
                game.particles.append(Particle(self.x, self.y,
                    math.cos(a)*s, math.sin(a)*s*0.3, (255,150,40),
                    random.randint(10,20), random.uniform(0.6,1.0), gravity=-100))
            for z in game.zombies:
                if z.alive and z.row == self.row:
                    z.take_damage(2000); game.spawn_death_particles(z.x,z.y); game.zombies_killed += 1
            self.alive = False
    def draw(self, screen):
        sc = 0.3+0.7*self.place_anim; cx, cy = int(self.x), int(self.y)
        fl = int(self.fuse*15)%2 == 0 and self.fuse < 0.7
        c = (255,220,80) if fl else (220,50,30)
        pygame.draw.ellipse(screen, c, (cx-S(14), cy-S(28), S(28), S(56)))
        pygame.draw.line(screen, (40,100,40), (cx,cy-S(28)), (cx,cy-S(38)), 3)

class Garlic(Plant):
    cost = 75; max_hp = 400; base_cooldown = 15.0
    def draw(self, screen):
        sc = 0.3+0.7*self.place_anim; cx, cy = int(self.x), int(self.y)
        pygame.draw.circle(screen, (240,230,215), (cx,cy-S(8)), int(S(30)*sc))
        pygame.draw.circle(screen, (200,190,175), (cx,cy-S(8)), int(S(30)*sc), 3)
        for i in range(5):
            a = -math.pi/2 + (i-2)*0.3
            x2 = cx + math.cos(a)*S(30)*sc
            y2 = cy-S(8) + math.sin(a)*S(30)*sc
            pygame.draw.line(screen, (180,170,155), (cx,cy-S(8)), (x2,y2), 2)
        pygame.draw.circle(screen, WHITE, (cx-S(8),cy-S(12)), S(4))
        pygame.draw.circle(screen, WHITE, (cx+S(8),cy-S(12)), S(4))
        pygame.draw.circle(screen, BLACK, (cx-S(8),cy-S(12)), S(2))
        pygame.draw.circle(screen, BLACK, (cx+S(8),cy-S(12)), S(2))

class Pea:
    SPEED = 500*SCALE; DAMAGE = 20
    def __init__(self, x, y, row, kind="green"):
        self.x, self.y, self.row = x, y, row; self.kind = kind; self.alive = True; self.tt = 0.0
    def update(self, dt, game):
        self.x += self.SPEED*dt; self.tt -= dt
        if self.tt <= 0:
            self.tt = 0.05
            c = (180,240,255) if self.kind == "blue" else (150,220,150)
            game.particles.append(Particle(self.x, self.y, -30, random.uniform(-10,10), c, S(4), 0.2))
        if self.x > SCREEN_W+30: self.alive = False; return
        for z in game.zombies:
            if z.alive and z.row == self.row and z.x-S(24) <= self.x <= z.x+S(26):
                z.take_damage(self.DAMAGE)
                if self.kind == "blue": z.slow_timer = 5.0
                self.alive = False; game.spawn_hit_particles(self.x, self.y); return
    def draw(self, screen):
        cx, cy = int(self.x), int(self.y)
        if self.kind == "blue":
            pygame.draw.circle(screen, (120,200,240), (cx,cy), S(7))
            pygame.draw.circle(screen, (60,130,190), (cx,cy), S(7), 2)
        else:
            pygame.draw.circle(screen, (60,170,60), (cx,cy), S(7))
            pygame.draw.circle(screen, (35,120,35), (cx,cy), S(7), 2)

# ==============================================================
#  ЗОМБІ (багато типів!)
# ==============================================================
class Zombie:
    max_hp = 100; speed = 25.0; damage = 45.0
    hat = None; body_color = (72,92,92); head_color = (150,180,130)
    scale = 1.0; has_flag = False; glow = None
    def __init__(self, row):
        self.row = row
        self.x = GRID_LEFT + GRID_W + S(70) + random.randint(0, S(90))
        self.y = GRID_TOP + row*CELL_H + CELL_H//2
        self.hp = self.max_hp; self.alive = True; self.eating = False
        self.anim = random.uniform(0, math.tau); self.eat_timer = 0.0; self.slow_timer = 0.0
    def take_damage(self, dmg):
        self.hp -= dmg
        if self.hp <= 0: self.hp = 0; self.alive = False
    def update(self, dt, game):
        self.anim += dt*4
        if self.slow_timer > 0: self.slow_timer -= dt
        mx = self.x - S(30)*self.scale
        p = game.plant_at_world(mx, self.y)
        sm = 1.0
        if self.slow_timer > 0: sm *= 0.5
        sm *= game.settings.diff_multiplier() * game.settings.game_speed
        if p is not None:
            self.eating = True; p.take_damage(self.damage*dt)
            self.eat_timer -= dt
            if self.eat_timer <= 0:
                self.eat_timer = 0.2
                game.particles.append(Particle(mx, self.y-S(20),
                    random.uniform(-40,40), random.uniform(-100,-50),
                    (120,80,40), 4, 0.5, gravity=400))
        else:
            self.eating = False; self.x -= self.speed*SCALE*dt*sm
        if self.x < GRID_LEFT - S(50): game.game_over(won=False)
    def draw(self, screen):
        cx, cy = int(self.x), int(self.y); s = self.scale
        walk = math.sin(self.anim)*3*s
        sh = get_shadow(int(S(50)*s), int(S(12)*s))
        screen.blit(sh, (cx-int(S(25)*s), cy+int(S(40)*s)))
        if self.glow:
            gsurf = pygame.Surface((int(S(80)*s), int(S(80)*s)), pygame.SRCALPHA)
            pygame.draw.circle(gsurf, (*self.glow, 60), (int(S(40)*s), int(S(40)*s)), int(S(35)*s))
            screen.blit(gsurf, (cx-int(S(40)*s), cy-int(S(40)*s)))
        pygame.draw.line(screen, (45,55,45), (cx-int(S(5)*s), cy+int(S(20)*s)),
                         (cx-int(S(9)*s)-int(walk), cy+int(S(44)*s)), max(2, int(S(7)*s)))
        pygame.draw.line(screen, (45,55,45), (cx+int(S(5)*s), cy+int(S(20)*s)),
                         (cx+int(S(9)*s)+int(walk), cy+int(S(44)*s)), max(2, int(S(7)*s)))
        body = pygame.Rect(cx-int(S(16)*s), cy-int(S(8)*s), int(S(32)*s), int(S(40)*s))
        pygame.draw.rect(screen, self.body_color, body, border_radius=int(S(6)*s))
        ay = cy-S(2)+int(walk*0.5)
        pygame.draw.line(screen, (115,155,115), (cx-int(S(8)*s), ay),
                         (cx-int(S(36)*s), ay-3), max(2, int(S(8)*s)))
        hy = cy-int(S(28)*s)
        pygame.draw.circle(screen, self.head_color, (cx,hy), int(S(18)*s))
        pygame.draw.circle(screen, (90,120,80), (cx,hy), int(S(18)*s), 2)
        pygame.draw.circle(screen, (240,240,220), (cx-int(S(7)*s), hy-int(S(4)*s)), int(S(4)*s))
        pygame.draw.circle(screen, (240,240,220), (cx+int(S(3)*s), hy-int(S(4)*s)), int(S(4)*s))
        pygame.draw.circle(screen, BLACK, (cx-int(S(8)*s), hy-int(S(4)*s)), max(1, S(2)))
        pygame.draw.circle(screen, BLACK, (cx+int(S(2)*s), hy-int(S(4)*s)), max(1, S(2)))
        # шапки
        if self.hat == "cone":
            pts = [(cx,hy-int(S(38)*s)),(cx-int(S(14)*s),hy-int(S(12)*s)),(cx+int(S(14)*s),hy-int(S(12)*s))]
            pygame.draw.polygon(screen, (230,130,40), pts); pygame.draw.polygon(screen, (180,90,20), pts, 2)
        elif self.hat == "bucket":
            r = pygame.Rect(cx-int(S(20)*s), hy-int(S(28)*s), int(S(40)*s), int(S(24)*s))
            pygame.draw.rect(screen, (155,155,165), r, border_radius=3)
            pygame.draw.rect(screen, (85,85,95), r, 2, border_radius=3)
        elif self.hat == "football":
            r = pygame.Rect(cx-int(S(22)*s), hy-int(S(22)*s), int(S(44)*s), int(S(20)*s))
            pygame.draw.rect(screen, (200,30,30), r, border_radius=5)
            pygame.draw.rect(screen, (100,10,10), r, 2, border_radius=5)
        elif self.hat == "newspaper":
            r = pygame.Rect(cx-int(S(5)*s), hy-int(S(4)*s), int(S(26)*s), int(S(18)*s))
            pygame.draw.rect(screen, (245,240,220), r); pygame.draw.rect(screen, (60,60,60), r, 1)
        elif self.hat == "screendoor":
            r = pygame.Rect(cx-int(S(30)*s), cy-int(S(35)*s), int(S(10)*s), int(S(60)*s))
            pygame.draw.rect(screen, (120,130,130), r, border_radius=2)
            pygame.draw.rect(screen, (60,70,70), r, 2, border_radius=2)
        elif self.hat == "balloon":
            pygame.draw.circle(screen, (230,80,80), (cx,cy-int(S(60)*s)), int(S(22)*s))
            pygame.draw.circle(screen, (180,50,50), (cx,cy-int(S(60)*s)), int(S(22)*s), 2)
        elif self.hat == "spike":
            for i in range(5):
                pygame.draw.polygon(screen, (200,200,210),
                    [(cx-int(S(15)*s)+i*int(S(7)*s), hy-int(S(20)*s)),
                     (cx-int(S(12)*s)+i*int(S(7)*s), hy-int(S(30)*s)),
                     (cx-int(S(9)*s)+i*int(S(7)*s), hy-int(S(20)*s))])
        elif self.hat == "crown":
            pygame.draw.polygon(screen, (255,215,60),
                [(cx-int(S(16)*s),hy-int(S(20)*s)),(cx-int(S(10)*s),hy-int(S(34)*s)),
                 (cx-int(S(4)*s),hy-int(S(22)*s)),(cx+S(2),hy-int(S(36)*s)),
                 (cx+int(S(8)*s),hy-int(S(22)*s)),(cx+int(S(14)*s),hy-int(S(34)*s)),
                 (cx+int(S(18)*s),hy-int(S(20)*s))])
        if self.has_flag:
            pygame.draw.line(screen, (100,70,40), (cx+int(S(20)*s), hy-int(S(26)*s)),
                             (cx+int(S(20)*s), hy+int(S(10)*s)), 3)
            pygame.draw.polygon(screen, (220,30,30),
                [(cx+int(S(20)*s),hy-int(S(26)*s)),(cx+int(S(44)*s),hy-int(S(20)*s)),
                 (cx+int(S(20)*s),hy-int(S(14)*s))])
        if self.hp < self.max_hp:
            w = int(S(42)*s); r = self.hp/self.max_hp
            bar = pygame.Rect(cx-w//2, hy-int(S(44)*s), w, 4)
            pygame.draw.rect(screen, (60,20,20), bar)
            col = (90,220,90) if r > 0.4 else (240,160,60)
            pygame.draw.rect(screen, col, (bar.x, bar.y, int(w*r), 4))
        if self.slow_timer > 0:
            ov = pygame.Surface((int(S(60)*s), int(S(90)*s)), pygame.SRCALPHA)
            pygame.draw.ellipse(ov, (120,200,255,70), (0,0,int(S(60)*s),int(S(90)*s)))
            screen.blit(ov, (cx-int(S(30)*s), cy-int(S(45)*s)))

class NormalZombie(Zombie): max_hp = 100; speed = 25.0
class ConeZombie(Zombie): max_hp = 220; speed = 24.0; hat = "cone"
class BucketZombie(Zombie): max_hp = 380; speed = 22.0; hat = "bucket"
class RunnerZombie(Zombie):
    max_hp = 70; speed = 55.0
    body_color = (100,100,140); head_color = (180,180,140)
class FlagZombie(Zombie): max_hp = 110; speed = 32.0; has_flag = True
class NewspaperZombie(Zombie):
    max_hp = 180; speed = 22.0; hat = "newspaper"; body_color = (100,80,60)
class FootballZombie(Zombie):
    max_hp = 500; speed = 30.0; damage = 60.0; hat = "football"
    body_color = (60,60,100); scale = 1.15
class GiantZombie(Zombie):
    max_hp = 700; speed = 16.0; damage = 90.0; scale = 1.45
    body_color = (60,80,80); head_color = (130,160,110); hat = "bucket"
class ScreenDoorZombie(Zombie):
    max_hp = 350; speed = 22.0; hat = "screendoor"
    def take_damage(self, dmg):
        if dmg <= 25: dmg *= 0.5
        super().take_damage(dmg)
class BalloonZombie(Zombie):
    max_hp = 120; speed = 30.0; hat = "balloon"
    def __init__(self, row):
        super().__init__(row); self.airborne = True
    def update(self, dt, game):
        if self.airborne:
            self.anim += dt*4
            self.x -= self.speed*SCALE*dt*0.8*game.settings.diff_multiplier()*game.settings.game_speed
            if self.x < GRID_LEFT + GRID_W*0.5:
                self.airborne = False; self.hat = None
            if self.x < GRID_LEFT-S(50): game.game_over(won=False)
            return
        super().update(dt, game)
    def draw(self, screen):
        if self.airborne:
            cy_save = self.y; self.y += -S(30); super().draw(screen); self.y = cy_save
        else: super().draw(screen)
class DancingZombie(Zombie):
    max_hp = 300; speed = 24.0; body_color = (140,80,130)
    def __init__(self, row):
        super().__init__(row); self.spawn_timer = 3.0
    def update(self, dt, game):
        super().update(dt, game); self.spawn_timer -= dt
        if self.spawn_timer <= 0 and self.alive:
            self.spawn_timer = 6.0
            for dr in (-1, 1):
                nr = self.row+dr
                if 0 <= nr < GRID_ROWS:
                    z = NormalZombie(nr); z.x = self.x + S(20); game.zombies.append(z)

# НОВІ МУТАНТИ
class ToxicZombie(Zombie):
    max_hp = 200; speed = 22.0
    body_color = (60,140,60); head_color = (100,200,100); glow = (100,255,100)
    def update(self, dt, game):
        super().update(dt, game)
        if random.random() < dt*2:
            game.particles.append(Particle(self.x, self.y, random.uniform(-30,30),
                random.uniform(-60,-20), (120,255,120), S(6), 0.6, gravity=100))

class ElectricZombie(Zombie):
    max_hp = 180; speed = 28.0
    body_color = (200,200,60); head_color = (255,240,120); glow = (255,255,100)
    def update(self, dt, game):
        super().update(dt, game)
        if random.random() < dt*4:
            a = random.uniform(0, math.tau)
            game.particles.append(Particle(self.x, self.y, math.cos(a)*80, math.sin(a)*80,
                (255,255,150), S(4), 0.3))

class InvisibleZombie(Zombie):
    max_hp = 150; speed = 26.0
    body_color = (140,140,140); head_color = (170,170,170)
    def __init__(self, row):
        super().__init__(row); self.opacity = 60
    def draw(self, screen):
        if self.x > GRID_LEFT + GRID_W*0.7:
            save_alpha = self.opacity
            surf = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
            old_screen = screen
            super().draw(surf)
            surf.set_alpha(self.opacity)
            old_screen.blit(surf, (0, 0))
        else:
            self.opacity = 255
            super().draw(screen)

class HealerZombie(Zombie):
    max_hp = 250; speed = 20.0
    body_color = (150,220,180); head_color = (200,255,220); glow = (150,255,180)
    def __init__(self, row):
        super().__init__(row); self.heal_timer = 2.0
    def update(self, dt, game):
        super().update(dt, game); self.heal_timer -= dt
        if self.heal_timer <= 0:
            self.heal_timer = 5.0
            for z in game.zombies:
                if z is self or not z.alive: continue
                if abs(z.x - self.x) < S(120) and abs(z.row - self.row) <= 1:
                    z.hp = min(z.max_hp, z.hp + 50)
                    game.particles.append(Particle(z.x, z.y-S(30),
                        random.uniform(-40,40), -80, (150,255,180), S(6), 0.7))

class BomberZombie(Zombie):
    max_hp = 220; speed = 24.0
    body_color = (60,60,80); head_color = (100,100,120)
    def __init__(self, row):
        super().__init__(row); self.tick = 3.0
    def update(self, dt, game):
        super().update(dt, game); self.tick -= dt
        if self.tick <= 0:
            self.tick = 4.0
            # вибух — ушкоджує рослини на 3x3
            game.trigger_shake(0.3, S(10)); game.flash_screen(180, (255,100,40), 0.15)
            for _ in range(30):
                a = random.uniform(0, math.tau); s = random.uniform(100, 300)
                game.particles.append(Particle(self.x, self.y, math.cos(a)*s, math.sin(a)*s,
                    (255,150,60), random.randint(8,16), 0.6, gravity=200))
            for r in range(GRID_ROWS):
                for c in range(GRID_COLS):
                    p = game.grid[r][c]
                    if p is None or not p.alive: continue
                    if abs(r-self.row) <= 1 and abs(p.x - self.x) < CELL_W*1.5:
                        p.take_damage(200)
            self.take_damage(200)

class ShieldZombie(Zombie):
    max_hp = 400; speed = 20.0
    body_color = (90,90,120); head_color = (140,140,170)
    def take_damage(self, dmg):
        # щит блокує першу половину шкоди
        if self.hp > self.max_hp * 0.5: dmg *= 0.3
        super().take_damage(dmg)
    def draw(self, screen):
        super().draw(screen)
        cx, cy = int(self.x), int(self.y)
        if self.hp > self.max_hp * 0.5:
            pygame.draw.arc(screen, (200,200,220),
                (cx-S(35), cy-S(50), S(20), S(80)), -math.pi/2, math.pi/2, 5)

class FireZombie(Zombie):
    max_hp = 260; speed = 26.0
    body_color = (180,60,30); head_color = (255,120,60); glow = (255,100,30)
    def update(self, dt, game):
        super().update(dt, game)
        if random.random() < dt*5:
            game.particles.append(Particle(self.x+random.uniform(-15,15),
                self.y-S(20), random.uniform(-20,20), random.uniform(-80,-30),
                (255,140,40), S(6), 0.5))

class IceZombie(Zombie):
    max_hp = 260; speed = 20.0
    body_color = (100,180,220); head_color = (180,230,255); glow = (150,220,255)
    def update(self, dt, game):
        super().update(dt, game)
        # сповільнює рослини навколо
        for row in range(GRID_ROWS):
            for col in range(GRID_COLS):
                p = game.grid[row][col]
                if p and p.alive and p.row == self.row and abs(p.x-self.x) < S(60):
                    if random.random() < dt*0.3:
                        game.particles.append(Particle(p.x, p.y-S(20),
                            random.uniform(-30,30), -50, (180,230,255), S(5), 0.6))

# 🥚 ПАСХАЛКА: зомбі "Даша"
class DahsaZombie(Zombie):
    max_hp = 1500; speed = 18.0; damage = 80.0
    body_color = (255,150,200); head_color = (255,200,220)
    hat = "crown"; scale = 1.3; glow = (255,180,220)
    def __init__(self, row):
        super().__init__(row)
        self.special_timer = 5.0
    def update(self, dt, game):
        super().update(dt, game)
        self.special_timer -= dt
        if self.special_timer <= 0:
            self.special_timer = 8.0
            # спавнить міні-зомбі
            for _ in range(3):
                nr = random.randint(0, GRID_ROWS-1)
                z = NormalZombie(nr); z.x = self.x; game.zombies.append(z)
            game.floating_texts.append(FloatingText(self.x, self.y-S(50),
                "ДАША!", (255,200,220), game.f_big, life=1.5))

ZOMBIE_MAP = {
    "normal":NormalZombie,"cone":ConeZombie,"bucket":BucketZombie,
    "runner":RunnerZombie,"flag":FlagZombie,"newspaper":NewspaperZombie,
    "football":FootballZombie,"giant":GiantZombie,"screendoor":ScreenDoorZombie,
    "balloon":BalloonZombie,"dancing":DancingZombie,
    "toxic":ToxicZombie,"electric":ElectricZombie,"invisible":InvisibleZombie,
    "healer":HealerZombie,"bomber":BomberZombie,"shield":ShieldZombie,
    "fire":FireZombie,"ice":IceZombie,"dahsa":DahsaZombie,
}

class Lawnmower:
    IDLE, RUNNING, GONE = 0, 1, 2
    def __init__(self, row):
        self.row = row; self.x = GRID_LEFT - S(50)
        self.y = GRID_TOP + row*CELL_H + CELL_H//2 + S(14)
        self.state = self.IDLE; self.speed = 1300*SCALE; self.anim = 0.0
    def update(self, dt, game):
        self.anim += dt*25
        if self.state == self.IDLE:
            for z in game.zombies:
                if z.alive and z.row == self.row and z.x < GRID_LEFT+S(20):
                    self.state = self.RUNNING
                    if game.settings.screen_shake: game.trigger_shake(0.5, S(10))
                    for _ in range(15):
                        game.particles.append(Particle(self.x+random.uniform(-S(15),S(15)),
                            self.y-S(10), random.uniform(-250,-80), random.uniform(-150,40),
                            (230,220,200), random.randint(8,16), random.uniform(0.5,1.0), gravity=200))
                    break
        elif self.state == self.RUNNING:
            self.x += self.speed*dt
            game.particles.append(Particle(self.x-S(20), self.y,
                random.uniform(-180,-60), random.uniform(-60,40),
                (220,220,200), random.randint(4,10), random.uniform(0.3,0.7), gravity=50))
            for z in game.zombies:
                if z.alive and z.row == self.row and abs(z.x-self.x) < S(55):
                    z.take_damage(99999); game.spawn_death_particles(z.x,z.y); game.zombies_killed += 1
            if self.x > SCREEN_W+100: self.state = self.GONE
    def draw(self, screen):
        if self.state == self.GONE: return
        x, y = int(self.x), int(self.y)
        if self.state == self.RUNNING:
            for i in range(6):
                a = self.anim*1.5 + i*math.tau/6
                pygame.draw.line(screen, (200,200,200), (x,y),
                    (x+math.cos(a)*S(24), y+math.sin(a)*S(12)), 3)
        for wx in (x-S(15), x+S(15)):
            pygame.draw.circle(screen, (30,30,30), (wx,y+S(16)), S(10))
            pygame.draw.circle(screen, (60,60,60), (wx,y+S(16)), S(3))
        body = pygame.Rect(x-S(28), y-S(12), S(56), S(30))
        pygame.draw.rect(screen, (200,60,50), body, border_radius=S(6))
        pygame.draw.rect(screen, (120,30,25), body, 2, border_radius=S(6))

def draw_house(screen):
    by = GRID_TOP + GRID_H; ht = GRID_TOP - S(25)
    pygame.draw.rect(screen, (180,140,90), (0, ht+S(50), GRID_LEFT-S(8), by-ht-S(50)))
    for i in range(ht+S(50), by, S(20)):
        pygame.draw.line(screen, (150,115,70), (0, i), (GRID_LEFT-S(8), i), 1)
    pygame.draw.polygon(screen, (140,60,40),
        [(0,ht+S(50)),(GRID_LEFT//2-S(4), ht-S(10)),(GRID_LEFT-S(8), ht+S(50))])
    win = pygame.Rect(S(20), ht+S(90), S(45), S(50))
    pygame.draw.rect(screen, (135,200,220), win); pygame.draw.rect(screen, (60,40,20), win, 2)
    door = pygame.Rect(S(28), by-S(90), S(40), S(80))
    pygame.draw.rect(screen, (100,60,30), door, border_radius=3)
    pygame.draw.rect(screen, (60,35,15), door, 2, border_radius=3)

class Card:
    W = S(104); H = S(114)
    def __init__(self, pc, x, y):
        self.plant_cls = pc; self.rect = pygame.Rect(x, y, self.W, self.H)
        self.cooldown = 0.0; self.ghost = pc(0, 0); self.press_t = 0.0
    @property
    def ready(self): return self.cooldown <= 0.0
    def update(self, dt):
        if self.cooldown > 0: self.cooldown = max(0, self.cooldown-dt)
        if self.press_t > 0: self.press_t = max(0, self.press_t-dt*4)
    def draw(self, screen, font, sel, aff):
        r = self.rect
        bg = (235,222,175) if aff else (165,158,140)
        pygame.draw.rect(screen, bg, r, border_radius=S(10))
        if sel: pygame.draw.rect(screen, (255,230,60), r, 4, border_radius=S(10))
        else: pygame.draw.rect(screen, (90,70,40), r, 2, border_radius=S(10))
        self.ghost.x = r.centerx; self.ghost.y = r.centery-S(12); self.ghost.place_anim = 1.0
        self.ghost.draw(screen)
        cs = font.render(str(self.plant_cls.cost), True, (40,30,10))
        strip = pygame.Rect(r.x+3, r.bottom-S(24), r.width-6, S(20))
        pygame.draw.rect(screen, (250,240,200), strip, border_radius=S(5))
        screen.blit(cs, cs.get_rect(center=strip.center))
        if self.cooldown > 0:
            ratio = self.cooldown/self.plant_cls.base_cooldown
            h = int(r.height*ratio)
            ov = pygame.Surface((r.width, h), pygame.SRCALPHA)
            ov.fill((0,0,0,150)); screen.blit(ov, (r.x, r.y))

class Button:
    def __init__(self, text, center, size, color, tc=WHITE, fs=None):
        self.text = text; self.rect = pygame.Rect(0,0,size[0],size[1]); self.rect.center = center
        self.color = color; self.text_color = tc
        self.font = pygame.font.Font(None, fs if fs else int(38*SCALE)); self.press_t = 0.0
    def update(self, dt):
        if self.press_t > 0: self.press_t = max(0, self.press_t-dt*4)
    def press(self): self.press_t = 1.0
    def draw(self, screen):
        sc = 1.0 - self.press_t*0.06
        r = pygame.Rect(0,0,int(self.rect.w*sc),int(self.rect.h*sc)); r.center = self.rect.center
        sh = pygame.Surface((r.w, r.h), pygame.SRCALPHA)
        pygame.draw.rect(sh, (0,0,0,100), (0,0,r.w,r.h), border_radius=S(14))
        screen.blit(sh, (r.x+4, r.y+5))
        pygame.draw.rect(screen, self.color, r, border_radius=S(14))
        pygame.draw.rect(screen, WHITE, r, 3, border_radius=S(14))
        t = self.font.render(self.text, True, self.text_color)
        screen.blit(t, t.get_rect(center=r.center))
    def hit(self, pos): return self.rect.collidepoint(pos)

class Settings:
    def __init__(self):
        self.sound_on = True; self.music_on = True; self.difficulty = "normal"
        self.show_fps = False; self.particles_on = True; self.screen_shake = True
        self.auto_collect = False; self.game_speed = 1.0; self.language = "uk"
        self.player_name = "Гравець"
    def diff_multiplier(self):
        return {"easy":0.75,"normal":1.0,"hard":1.35}[self.difficulty]

class Tutorial:
    def __init__(self): self.step = 0; self.done = False
    STEPS_UK = [
        ("Вітаємо!", "Ти захищаєш будинок від зомбі."),
        ("Сонечко", "Тапни по сонечку, щоб зібрати."),
        ("Соняшник", "Постав Соняшник за 50 сонця."),
        ("Горохостріл", "Постав Горохостріл за 100 сонця."),
        ("Горіх", "800 HP, затримує зомбі."),
        ("Газонокосилка", "Останній захист!"),
        ("Готово!", "Удачі!"),
    ]
    def draw(self, screen, fm, fs, w, h, t):
        if self.done: return
        idx = self.step+1
        # беремо з LANG якщо є, інакше з STEPS_UK
        try: title = t("tut_title_"+str(idx)); text = t("tut_text_"+str(idx))
        except: title, text = self.STEPS_UK[self.step] if self.step < len(self.STEPS_UK) else ("","")
        ph = S(90); panel = pygame.Rect(S(20), h-ph-S(15), w-S(40), ph)
        ov = pygame.Surface((panel.w, panel.h), pygame.SRCALPHA)
        ov.fill((20,20,30,220)); screen.blit(ov, panel.topleft)
        pygame.draw.rect(screen, (255,220,60), panel, 3, border_radius=S(14))
        draw_ts(screen, title, fm, (255,240,180), (panel.centerx, panel.y+S(28)), (0,0,0), 2)
        tt = fs.render(text, True, WHITE); screen.blit(tt, tt.get_rect(center=(panel.centerx, panel.y+S(58))))
        skip = fs.render(t("tap_anywhere"), True, (200,200,200))
        screen.blit(skip, skip.get_rect(center=(panel.centerx, panel.bottom-S(10))))
    def advance(self):
        self.step += 1
        if self.step >= 7: self.done = True

# ==============================================================
#  ГРА
# ==============================================================
class Game:
    LOADING, MENU, SETTINGS, LEVELS, PLAYING, PAUSED, GAMEOVER, VICTORY, TUTORIAL, ABOUT = range(10)

    def __init__(self, screen):
        self.screen = screen; self.settings = Settings()
        self.f_huge = pygame.font.Font(None, int(100*SCALE))
        self.f_big  = pygame.font.Font(None, int(66*SCALE))
        self.f_med  = pygame.font.Font(None, int(40*SCALE))
        self.f_small= pygame.font.Font(None, int(28*SCALE))
        self.f_tiny = pygame.font.Font(None, int(20*SCALE))

        self.settings_scroll = 0.0; self.settings_max_scroll = S(400)
        self.settings_drag_start = None; self.settings_drag_scroll = 0
        self.opt_rects = {}; self.btn_back_settings = None; self.lang_buttons = {}

        self.state = self.LOADING
        self.loading_t = 0.0
        self.loading_done = False
        self.loading_steps = [
            "Завантаження рослин...",
            "Завантаження зомбі...",
            "Компіляція мутантів...",
            "Завантаження пасхалок...",
            "Побудова газону...",
            "Готово!",
        ]
        self.loading_idx = 0

        self.current_level = 0; self.completed_levels = set()
        self.menu_time = 0.0
        self.clouds = [{"x":random.randint(0,SCREEN_W),"y":random.randint(S(30),S(150)),
                        "s":random.uniform(0.7,1.5)} for _ in range(5)]
        self._last_tap_t = -1000; self._last_tap_pos = (-999,-999); self.touch_mode = False
        self.shake_amp = 0; self.shake_t = 0.0
        self.flash_t = 0.0; self.flash_max = 0.0; self.flash_color = (255,255,255)
        self._menu_bg_cache = {}; self._lawn_bg_cache = {}
        self.tutorial = Tutorial()
        self.secret_unlocked = False
        self.tap_times = []  # для чит-коду

        self._build_buttons()
        self.reset_game()

    def t(self, key): return LANG[self.settings.language].get(key, key)

    def _build_buttons(self):
        cx = SCREEN_W//2
        self.btn_play     = Button(self.t("play"),(cx,int(SCREEN_H*0.44)),(S(500),S(78)),(60,165,60),fs=int(44*SCALE))
        self.btn_tutorial = Button(self.t("tutorial"),(cx,int(SCREEN_H*0.57)),(S(500),S(60)),(200,140,60),fs=int(30*SCALE))
        self.btn_about    = Button(self.t("about"),(cx,int(SCREEN_H*0.68)),(S(500),S(60)),(140,90,180),fs=int(30*SCALE))
        self.btn_settings = Button(self.t("settings"),(cx,int(SCREEN_H*0.79)),(S(500),S(60)),(60,120,200),fs=int(30*SCALE))
        self.btn_exit     = Button(self.t("exit"),(cx,int(SCREEN_H*0.90)),(S(500),S(54)),(150,60,60),fs=int(28*SCALE))

        self.btn_restart = Button(self.t("restart"),(cx-S(210),int(SCREEN_H*0.78)),(S(280),S(74)),(60,165,60),fs=int(38*SCALE))
        self.btn_levels  = Button(self.t("levels"),(cx,int(SCREEN_H*0.78)),(S(280),S(74)),(60,120,200),fs=int(38*SCALE))
        self.btn_menu    = Button(self.t("menu"),(cx+S(210),int(SCREEN_H*0.78)),(S(280),S(74)),(150,100,60),fs=int(38*SCALE))

        self.btn_levels_back = Button(self.t("back"),(SCREEN_W//2,SCREEN_H-S(45)),(S(280),S(66)),(150,100,60),fs=int(34*SCALE))
        self.btn_back_settings = Button(self.t("back"),(SCREEN_W//2,SCREEN_H-S(35)),(S(240),S(56)),(150,100,60),fs=int(30*SCALE))
        self.btn_about_back = Button(self.t("back"),(SCREEN_W//2,SCREEN_H-S(45)),(S(280),S(66)),(150,100,60),fs=int(34*SCALE))

        self.btn_pause = pygame.Rect(SCREEN_W-S(70), S(10), S(58), S(58))

        self.level_buttons = []
        cpr = 3; lw, lh = S(280), S(180); gx, gy = S(20), S(20)
        tw = cpr*lw + (cpr-1)*gx; sx = (SCREEN_W-tw)//2
        for i in range(len(LEVELS)):
            col = i%cpr; row = i//cpr
            self.level_buttons.append(pygame.Rect(sx+col*(lw+gx), S(140)+row*(lh+gy), lw, lh))

    def _build_menu_bg(self, idx):
        lvl = LEVELS[idx]
        surf = pygame.Surface((SCREEN_W, SCREEN_H)).convert()
        st, sb = lvl["sky_top"], lvl["sky_bot"]; step = 3
        for i in range(0, SCREEN_H, step):
            t = i/SCREEN_H
            c = (int(lerp(st[0],sb[0],t)),int(lerp(st[1],sb[1],t)),int(lerp(st[2],sb[2],t)))
            pygame.draw.rect(surf, c, (0,i,SCREEN_W,step))
        sx, sy = SCREEN_W-S(160), S(110)
        if lvl["weather"] in ("stars","moon"):
            for _ in range(60):
                pygame.draw.circle(surf, (255,255,240),
                    (random.randint(0,SCREEN_W),random.randint(0,SCREEN_H-S(200))), 1)
            pygame.draw.circle(surf, (240,240,200), (sx,sy), S(45))
            pygame.draw.circle(surf, (245,245,220), (sx+S(8),sy-S(4)), S(36))
        else:
            pygame.draw.circle(surf, (255,235,130), (sx,sy), S(60))
            pygame.draw.circle(surf, (255,250,200), (sx,sy), S(42))
        return surf

    def _build_lawn_bg(self, idx):
        lvl = LEVELS[idx]
        surf = pygame.Surface((GRID_W, GRID_H)).convert()
        for r in range(GRID_ROWS):
            for c in range(GRID_COLS):
                col = lvl["lawn_a"] if (r+c)%2 == 0 else lvl["lawn_b"]
                pygame.draw.rect(surf, col, (c*CELL_W, r*CELL_H, CELL_W, CELL_H))
        return surf

    def reset_game(self):
        lvl = LEVELS[self.current_level]
        self.sun = lvl["sun_start"]
        self.grid = [[None]*GRID_COLS for _ in range(GRID_ROWS)]
        self.zombies = []; self.projectiles = []; self.suns = []
        self.flying_suns = []; self.particles = []; self.floating_texts = []
        self.mowers = [Lawnmower(r) for r in range(GRID_ROWS)]
        self.selected_card = None; self.elapsed = 0.0
        sr = lvl["sky_sun_range"]; self.sky_sun_timer = random.uniform(sr[0],sr[1])
        self.zombie_timer = lvl["spawn_base"]*0.7
        self.zombies_killed = 0; self.won = False
        self.shake_amp = 0; self.shake_t = 0.0; self.flash_t = 0.0
        self.cards = []
        start_x = S(140)
        for cls in (Sunflower,Peashooter,Wallnut,SnowPea,Repeater,
                    CherryBomb,Chomper,Threepeater,Jalapeno,Garlic):
            self.cards.append(Card(cls, start_x, S(6)))
            start_x += Card.W + S(6)

    def plant_at_world(self, x, y):
        cell = pos_to_cell(x, y)
        if cell is None: return None
        c, r = cell; p = self.grid[r][c]
        return p if p is not None and p.alive else None

    def zombie_in_row(self, row, x):
        return any(z.alive and z.row == row and z.x > x-S(20) for z in self.zombies)

    def trigger_shake(self, time, amp):
        if not self.settings.screen_shake: return
        self.shake_t = max(self.shake_t, time); self.shake_amp = max(self.shake_amp, amp)
    def flash_screen(self, intensity, color, duration):
        self.flash_t = duration; self.flash_max = duration; self.flash_color = color
    def spawn_hit_particles(self, x, y):
        if not self.settings.particles_on: return
        for _ in range(4):
            a = random.uniform(0, math.tau); s = random.uniform(80, 200)
            self.particles.append(Particle(x,y,math.cos(a)*s,math.sin(a)*s,
                (150,230,100),random.randint(4,7),random.uniform(0.3,0.5),gravity=250))
    def spawn_death_particles(self, x, y):
        if not self.settings.particles_on: return
        for _ in range(12):
            a = random.uniform(0, math.tau); s = random.uniform(80, 250)
            color = random.choice([(120,180,80),(100,140,70),(160,200,120),(200,100,100)])
            self.particles.append(Particle(x,y,math.cos(a)*s,math.sin(a)*s-80,
                color,random.randint(6,12),random.uniform(0.5,1.0),gravity=500))
    def spawn_sun_collect_particles(self, x, y):
        if not self.settings.particles_on: return
        for _ in range(6):
            a = random.uniform(0, math.tau); s = random.uniform(100, 200)
            self.particles.append(Particle(x,y,math.cos(a)*s,math.sin(a)*s,
                (255,220,80),random.randint(5,9),random.uniform(0.4,0.7),gravity=120))
    def game_over(self, won=False):
        if self.state == self.PLAYING:
            self.state = self.VICTORY if won else self.GAMEOVER
            self.won = won
            if won:
                self.completed_levels.add(self.current_level)
                self.flash_screen(255,(255,255,150),0.5)
            else:
                self.flash_screen(255,(255,80,80),0.5); self.trigger_shake(0.6, S(14))

    def handle_event(self, event):
        if event.type == pygame.FINGERDOWN:
            self.touch_mode = True
            self._dispatch_tap((event.x*SCREEN_W, event.y*SCREEN_H))
        elif event.type == pygame.FINGERMOTION:
            pos = (event.x*SCREEN_W, event.y*SCREEN_H)
            if self.state == self.SETTINGS and self.settings_drag_start is not None:
                dy = self.settings_drag_start[1]-pos[1]
                self.settings_scroll = max(0, min(self.settings_max_scroll, self.settings_drag_scroll+dy))
        elif event.type == pygame.FINGERUP:
            self.settings_drag_start = None
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.touch_mode: return
            self._dispatch_tap(event.pos)
        elif event.type == pygame.MOUSEMOTION:
            if self.state == self.SETTINGS and self.settings_drag_start is not None:
                dy = self.settings_drag_start[1]-event.pos[1]
                self.settings_scroll = max(0, min(self.settings_max_scroll, self.settings_drag_scroll+dy))
        elif event.type == pygame.MOUSEBUTTONUP:
            self.settings_drag_start = None
        elif event.type == pygame.MOUSEWHEEL:
            if self.state == self.SETTINGS:
                self.settings_scroll = max(0, min(self.settings_max_scroll,
                    self.settings_scroll - event.y*S(40)))
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            if self.state == self.PLAYING: self.state = self.PAUSED
            elif self.state == self.PAUSED: self.state = self.PLAYING
            elif self.state in (self.SETTINGS, self.LEVELS, self.TUTORIAL, self.ABOUT): self.state = self.MENU

    def _dispatch_tap(self, pos):
        now = pygame.time.get_ticks()
        if now - self._last_tap_t < 45:
            lx, ly = self._last_tap_pos
            if abs(pos[0]-lx) < 40 and abs(pos[1]-ly) < 40: return
        self._last_tap_t = now; self._last_tap_pos = pos
        # чит-код: 5 швидких тапів у верхній лівий кут
        if pos[0] < S(80) and pos[1] < S(80):
            self.tap_times.append(now)
            self.tap_times = [t for t in self.tap_times if now-t < 2000]
            if len(self.tap_times) >= 5:
                self.tap_times = []
                if not self.secret_unlocked:
                    self.secret_unlocked = True
                    self.flash_screen(255, (255,180,255), 1.0)
        self._on_tap(pos)

    def _on_tap(self, pos):
        if self.state == self.LOADING:
            if self.loading_done:
                self.state = self.MENU
            return
        if self.state == self.TUTORIAL:
            self.tutorial.advance()
            if self.tutorial.done: self.state = self.PLAYING
            return
        if self.state == self.SETTINGS:
            self.settings_drag_start = pos; self.settings_drag_scroll = self.settings_scroll
            self._tap_settings(pos); return
        for b in [self.btn_play,self.btn_tutorial,self.btn_about,self.btn_settings,self.btn_exit,
                  self.btn_restart,self.btn_levels,self.btn_menu,self.btn_levels_back,
                  self.btn_back_settings,self.btn_about_back]:
            if b and b.hit(pos): b.press()
        if self.state == self.PLAYING:
            for c in self.cards:
                if c.rect.collidepoint(pos): c.press_t = 1.0

        if self.state == self.MENU: self._tap_menu(pos)
        elif self.state == self.LEVELS: self._tap_levels(pos)
        elif self.state == self.PLAYING: self._tap_play(pos)
        elif self.state == self.PAUSED: self.state = self.PLAYING
        elif self.state in (self.GAMEOVER, self.VICTORY): self._tap_gameover(pos)
        elif self.state == self.ABOUT:
            if self.btn_about_back.hit(pos): self.state = self.MENU

    def _tap_menu(self, pos):
        if self.btn_play.hit(pos):
            # якщо секрет відкрито - показуємо всі рівні
            self.state = self.LEVELS
        elif self.btn_tutorial.hit(pos):
            self.tutorial = Tutorial(); self.current_level = 0
            self.reset_game(); self.state = self.TUTORIAL
        elif self.btn_about.hit(pos): self.state = self.ABOUT
        elif self.btn_settings.hit(pos): self.settings_scroll = 0; self.state = self.SETTINGS
        elif self.btn_exit.hit(pos): pygame.event.post(pygame.event.Event(pygame.QUIT))

    def _tap_settings(self, pos):
        if self.btn_back_settings and self.btn_back_settings.hit(pos):
            self.state = self.MENU; return
        for lc, r in self.lang_buttons.items():
            rr = pygame.Rect(r.x, r.y-int(self.settings_scroll), r.w, r.h)
            if rr.collidepoint(pos):
                self.settings.language = lc; self._build_buttons(); return
        for k, r in self.opt_rects.items():
            rr = pygame.Rect(r.x, r.y-int(self.settings_scroll), r.w, r.h)
            if rr.collidepoint(pos): self._toggle_option(k); return

    def _toggle_option(self, key):
        s = self.settings
        if key == "sound": s.sound_on = not s.sound_on
        elif key == "music": s.music_on = not s.music_on
        elif key == "fps": s.show_fps = not s.show_fps
        elif key == "particles": s.particles_on = not s.particles_on
        elif key == "shake": s.screen_shake = not s.screen_shake
        elif key == "auto": s.auto_collect = not s.auto_collect
        elif key == "diff_easy": s.difficulty = "easy"
        elif key == "diff_normal": s.difficulty = "normal"
        elif key == "diff_hard": s.difficulty = "hard"
        elif key == "sp_05": s.game_speed = 0.5
        elif key == "sp_10": s.game_speed = 1.0
        elif key == "sp_15": s.game_speed = 1.5
        elif key == "sp_20": s.game_speed = 2.0

    def _tap_levels(self, pos):
        for i, r in enumerate(self.level_buttons):
            if r.collidepoint(pos):
                if i == 6 and not self.secret_unlocked:
                    # секретна локація закрита
                    self.flash_screen(150, (255,100,100), 0.3)
                    return
                self.current_level = i; self.reset_game(); self.state = self.PLAYING; return
        if self.btn_levels_back.hit(pos): self.state = self.MENU

    def _tap_gameover(self, pos):
        if self.btn_restart.hit(pos): self.reset_game(); self.state = self.PLAYING
        elif self.btn_levels.hit(pos): self.state = self.LEVELS
        elif self.btn_menu.hit(pos): self.state = self.MENU

    def _tap_play(self, pos):
        if self.btn_pause.collidepoint(pos): self.state = self.PAUSED; return
        for s in reversed(self.suns):
            if s.contains(pos):
                s.remove = True; self.spawn_sun_collect_particles(s.x, s.y)
                self.flying_suns.append(FlyingSun(s.x, s.y, S(80), S(60), s.value)); return
        for c in self.cards:
            if c.rect.collidepoint(pos):
                if not c.ready: return
                self.selected_card = None if self.selected_card is c else c; return
        if self.selected_card is not None:
            cell = pos_to_cell(pos[0], pos[1])
            if cell is None: return
            col, row = cell
            if self.grid[row][col] is not None: return
            cost = self.selected_card.plant_cls.cost
            if self.sun < cost: return
            self.sun -= cost
            self.grid[row][col] = self.selected_card.plant_cls(col, row)
            self.selected_card.cooldown = self.selected_card.plant_cls.base_cooldown
            self.selected_card = None
            px, py = cell_center(col, row)
            for _ in range(6):
                a = random.uniform(math.pi, math.tau); s = random.uniform(60, 150)
                self.particles.append(Particle(px+random.uniform(-S(20),S(20)),py+S(30),
                    math.cos(a)*s, math.sin(a)*s-80, (90,60,30),
                    random.randint(4,7), random.uniform(0.4,0.7), gravity=400))

    def update(self, dt):
        self.menu_time += dt
        # loading
        if self.state == self.LOADING:
            self.loading_t += dt
            if self.loading_t > 0.4 and self.loading_idx < len(self.loading_steps):
                self.loading_idx += 1; self.loading_t = 0.0
            if self.loading_idx >= len(self.loading_steps): self.loading_done = True
            return
        for c in self.clouds:
            c["x"] += dt*15*c["s"]
            if c["x"] > SCREEN_W+S(100):
                c["x"] = -S(100); c["y"] = random.randint(S(30),S(150))
        for b in [self.btn_play,self.btn_tutorial,self.btn_about,self.btn_settings,self.btn_exit,
                  self.btn_restart,self.btn_levels,self.btn_menu,self.btn_levels_back,
                  self.btn_back_settings,self.btn_about_back]:
            if b: b.update(dt)
        if self.shake_t > 0:
            self.shake_t -= dt
            if self.shake_t <= 0: self.shake_amp = 0
        if self.flash_t > 0: self.flash_t -= dt
        if self.state == self.TUTORIAL: return
        if self.state != self.PLAYING: return

        lvl = LEVELS[self.current_level]
        self.elapsed += dt
        if self.elapsed >= lvl["win_time"]:
            self.game_over(won=True); return
        self.sky_sun_timer -= dt
        if self.sky_sun_timer <= 0:
            sr = lvl["sky_sun_range"]; self.sky_sun_timer = random.uniform(sr[0],sr[1])
            x = random.randint(GRID_LEFT+S(40), GRID_LEFT+GRID_W-S(40))
            ty = random.randint(GRID_TOP+S(60), GRID_TOP+GRID_H-S(50))
            self.suns.append(Sun(x, GRID_TOP-S(40), ty))
        self.zombie_timer -= dt
        if self.zombie_timer <= 0:
            base = max(2.0, lvl["spawn_base"] - self.elapsed*lvl["spawn_decay"])
            self.zombie_timer = random.uniform(base, base+2.5)
            row = random.randint(0, GRID_ROWS-1)
            zt = random.choice(lvl["zombies"])
            self.zombies.append(ZOMBIE_MAP[zt](row))
        for c in self.cards: c.update(dt)
        for r in range(GRID_ROWS):
            for c in range(GRID_COLS):
                p = self.grid[r][c]
                if p is not None: p.update(dt, self)
        for m in self.mowers: m.update(dt, self)
        for z in self.zombies: z.update(dt, self)
        for pr in self.projectiles: pr.update(dt, self)
        for s in self.suns: s.update(dt)
        for fs in self.flying_suns:
            fs.update(dt)
            if fs.remove: self.sun += fs.value
        for pt in self.particles: pt.update(dt)
        for ft in self.floating_texts: ft.update(dt)
        if self.settings.auto_collect:
            for s in self.suns:
                if s.landed:
                    s.remove = True
                    self.flying_suns.append(FlyingSun(s.x, s.y, S(80), S(60), s.value))
        for z in self.zombies:
            if not z.alive: continue
            mower = self.mowers[z.row]
            if z.x < GRID_LEFT-S(50) and mower.state == Lawnmower.GONE:
                self.game_over(won=False); return
        for r in range(GRID_ROWS):
            for c in range(GRID_COLS):
                p = self.grid[r][c]
                if p is not None and not p.alive:
                    px, py = cell_center(c, r)
                    for _ in range(5):
                        a = random.uniform(0, math.tau); s = random.uniform(50, 120)
                        self.particles.append(Particle(px,py,math.cos(a)*s,math.sin(a)*s-50,
                            (120,160,90),random.randint(4,7),random.uniform(0.4,0.7),gravity=350))
                    self.grid[r][c] = None
        killed = sum(1 for z in self.zombies if not z.alive)
        self.zombies_killed += killed
        self.zombies = [z for z in self.zombies if z.alive]
        self.projectiles = [p for p in self.projectiles if p.alive]
        self.suns = [s for s in self.suns if not s.remove]
        self.flying_suns = [fs for fs in self.flying_suns if not fs.remove]
        self.particles = [p for p in self.particles if not p.remove]
        self.floating_texts = [ft for ft in self.floating_texts if not ft.remove]
        if len(self.particles) > MAX_PARTICLES: self.particles = self.particles[-MAX_PARTICLES:]

    def draw(self):
        if self.state == self.LOADING: self._draw_loading()
        elif self.state == self.MENU: self._draw_menu()
        elif self.state == self.SETTINGS: self._draw_settings()
        elif self.state == self.LEVELS: self._draw_levels()
        elif self.state == self.ABOUT: self._draw_about()
        else:
            self._draw_world()
            if self.state == self.TUTORIAL:
                self.tutorial.draw(self.screen, self.f_med, self.f_small, SCREEN_W, SCREEN_H, self.t)
            if self.state == self.PAUSED: self._draw_paused()
            elif self.state in (self.GAMEOVER, self.VICTORY): self._draw_gameover()
        if self.flash_t > 0:
            a = int(220*(self.flash_t/self.flash_max))
            fl = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
            fl.fill((self.flash_color[0], self.flash_color[1], self.flash_color[2], a))
            self.screen.blit(fl, (0, 0))

    def _draw_loading(self):
        s = self.screen
        # фон з градієнта
        for i in range(SCREEN_H):
            t = i/SCREEN_H
            c = (int(20+40*t), int(60+80*t), int(30+40*t))
            pygame.draw.line(s, c, (0,i), (SCREEN_W,i))
        # логотип
        cx, cy = SCREEN_W//2, SCREEN_H//2 - S(60)
        logo_bob = math.sin(self.menu_time*2)*4
        # намальований логотип
        pygame.draw.circle(s, (255,205,30), (cx-S(80), cy+logo_bob), S(40))
        for i in range(8):
            a = i*math.tau/8 + self.menu_time
            pygame.draw.circle(s, (255,205,40),
                (int(cx-S(80)+math.cos(a)*S(35)), int(cy+logo_bob+math.sin(a)*S(35))), S(12))
        pygame.draw.circle(s, (140,85,35), (cx-S(80), cy+logo_bob), S(22))
        # зомбі-лого
        pygame.draw.circle(s, (150,180,130), (cx+S(80), cy+logo_bob), S(28))
        pygame.draw.circle(s, (90,120,80), (cx+S(80), cy+logo_bob), S(28), 3)
        pygame.draw.circle(s, BLACK, (cx+S(72), cy+logo_bob-S(5)), S(3))
        pygame.draw.circle(s, BLACK, (cx+S(88), cy+logo_bob-S(5)), S(3))
        # заголовок
        draw_ts(s, GAME_TITLE, self.f_huge, WHITE, (cx, cy+S(80)), (0,0,0), 5)
        ver = self.f_small.render("v"+VERSION, True, (200,200,180))
        s.blit(ver, ver.get_rect(center=(cx, cy+S(120))))
        # прогрес
        bar_w = S(500); bar_h = S(20)
        bar_x = cx-bar_w//2; bar_y = SCREEN_H-S(100)
        pygame.draw.rect(s, (30,30,30), (bar_x,bar_y,bar_w,bar_h), border_radius=S(10))
        prog = (self.loading_idx)/len(self.loading_steps)
        pygame.draw.rect(s, (100,220,100),
            (bar_x+2, bar_y+2, int((bar_w-4)*prog), bar_h-4), border_radius=S(8))
        # текст кроку
        if self.loading_idx < len(self.loading_steps):
            step_text = self.loading_steps[self.loading_idx]
        else:
            step_text = self.t("tap_anywhere")
        txt = self.f_small.render(step_text, True, WHITE)
        s.blit(txt, txt.get_rect(center=(cx, bar_y-S(25))))

    def _draw_menu(self):
        s = self.screen
        if 0 not in self._menu_bg_cache: self._menu_bg_cache[0] = self._build_menu_bg(0)
        s.blit(self._menu_bg_cache[0], (0,0))
        for c in self.clouds: self._draw_cloud(s, c["x"], c["y"], c["s"])
        bounce = math.sin(self.menu_time*2)*5; cx = SCREEN_W//2
        draw_ts(s, GAME_TITLE, self.f_big, WHITE, (cx, S(90)+bounce), (30,80,30), 4)
        sub = self.f_med.render("v"+VERSION, True, (255,240,180))
        s.blit(sub, sub.get_rect(center=(cx, S(135)+bounce)))
        self.btn_play.draw(s); self.btn_tutorial.draw(s)
        self.btn_about.draw(s); self.btn_settings.draw(s); self.btn_exit.draw(s)
        v = self.f_tiny.render(GAME_TITLE+" v"+VERSION, True, (60,50,30))
        s.blit(v, v.get_rect(midbottom=(cx, SCREEN_H-S(6))))

    def _draw_cloud(self, s, x, y, scale):
        w = int(S(80)*scale); h = int(S(36)*scale)
        for dx, dy, r in [(0,0,h),(w*0.4,-h*0.3,h*0.9),(w*0.75,0,h*0.8)]:
            pygame.draw.ellipse(s, (250,250,250), (x+dx,y+dy,int(r*2),int(r*1.6)))

    def _draw_settings(self):
        s = self.screen
        if 0 not in self._menu_bg_cache: self._menu_bg_cache[0] = self._build_menu_bg(0)
        s.blit(self._menu_bg_cache[0], (0,0))
        ov = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA); ov.fill((0,0,0,160)); s.blit(ov,(0,0))
        cx_btn = SCREEN_W-S(180); cx_lab = S(60); rh = S(66); ys = S(140)
        ct = ys - int(self.settings_scroll)
        self.opt_rects = {}; self.lang_buttons = {}
        # мова
        y = ct
        if -rh < y < SCREEN_H+rh:
            t = self.f_small.render(self.t("language")+":", True, (255,255,220)); s.blit(t, (cx_lab,y))
            bx = SCREEN_W-S(360)
            for code, label in [("uk","УКР"),("ru","РУС"),("en","ENG")]:
                r = pygame.Rect(bx, y-S(6), S(100), S(46))
                act = self.settings.language == code
                c = (220,170,60) if act else (90,110,140)
                pygame.draw.rect(s, c, r, border_radius=S(10)); pygame.draw.rect(s, WHITE, r, 2, border_radius=S(10))
                tt = self.f_small.render(label, True, (20,20,20) if act else WHITE)
                s.blit(tt, tt.get_rect(center=r.center))
                self.lang_buttons[code] = pygame.Rect(r.x, r.y+int(self.settings_scroll), r.w, r.h)
                bx += S(110)
        opts = [("sound",self.t("sound")),("music",self.t("music")),("fps",self.t("show_fps")),
                ("particles",self.t("particles")),("shake",self.t("screen_shake")),
                ("auto",self.t("auto_collect"))]
        for i, (k, label) in enumerate(opts):
            y = ct + (i+1)*rh
            if -rh < y < SCREEN_H+rh:
                t = self.f_small.render(label+":", True, (255,255,220)); s.blit(t, (cx_lab,y))
                val = self._gov(k)
                br = pygame.Rect(cx_btn-S(90), y-S(6), S(180), S(46))
                c = (60,160,60) if val in (self.t("yes"),self.t("on")) else (140,60,60)
                pygame.draw.rect(s, c, br, border_radius=S(10)); pygame.draw.rect(s, WHITE, br, 2, border_radius=S(10))
                vt = self.f_small.render(val, True, WHITE); s.blit(vt, vt.get_rect(center=br.center))
                self.opt_rects[k] = pygame.Rect(br.x, br.y+int(self.settings_scroll), br.w, br.h)
        # diff
        y = ct + 7*rh + S(15)
        if -rh < y < SCREEN_H+rh:
            t = self.f_small.render(self.t("difficulty")+":", True, (255,255,220)); s.blit(t, (cx_lab,y))
            bx = SCREEN_W-S(400)
            for k, label in [("diff_easy",self.t("easy")),("diff_normal",self.t("normal")),("diff_hard",self.t("hard"))]:
                r = pygame.Rect(bx, y-S(6), S(120), S(46))
                act = self.settings.difficulty == k.replace("diff_","")
                c = (220,170,60) if act else (150,140,120)
                pygame.draw.rect(s, c, r, border_radius=S(10)); pygame.draw.rect(s, WHITE, r, 2, border_radius=S(10))
                tt = self.f_tiny.render(label, True, (20,20,20)); s.blit(tt, tt.get_rect(center=r.center))
                self.opt_rects[k] = pygame.Rect(r.x, r.y+int(self.settings_scroll), r.w, r.h)
                bx += S(125)
        # speed
        y = ct + 8*rh + S(15)
        if -rh < y < SCREEN_H+rh:
            t = self.f_small.render(self.t("game_speed")+":", True, (255,255,220)); s.blit(t, (cx_lab,y))
            bx = SCREEN_W-S(400)
            for k, label in [("sp_05","0.5x"),("sp_10","1x"),("sp_15","1.5x"),("sp_20","2x")]:
                r = pygame.Rect(bx, y-S(6), S(85), S(46))
                val = float(label.replace("x",""))
                act = abs(self.settings.game_speed - val) < 0.01
                c = (220,170,60) if act else (150,140,120)
                pygame.draw.rect(s, c, r, border_radius=S(10)); pygame.draw.rect(s, WHITE, r, 2, border_radius=S(10))
                tt = self.f_tiny.render(label, True, (20,20,20)); s.blit(tt, tt.get_rect(center=r.center))
                self.opt_rects[k] = pygame.Rect(r.x, r.y+int(self.settings_scroll), r.w, r.h)
                bx += S(95)
        draw_ts(s, self.t("settings"), self.f_big, WHITE, (SCREEN_W//2, S(50)), (0,0,0), 4)
        ver = self.f_small.render(self.t("version")+" "+VERSION, True, (255,240,180))
        s.blit(ver, ver.get_rect(center=(SCREEN_W//2, S(90))))
        self.btn_back_settings.draw(s)
        hint = self.f_tiny.render(self.t("scroll_hint"), True, (200,200,200))
        s.blit(hint, hint.get_rect(center=(SCREEN_W//2, SCREEN_H-S(80))))

    def _gov(self, key):
        s = self.settings
        if key == "sound": return self.t("on") if s.sound_on else self.t("off")
        if key == "music": return self.t("on") if s.music_on else self.t("off")
        if key == "fps": return self.t("yes") if s.show_fps else self.t("no")
        if key == "particles": return self.t("on") if s.particles_on else self.t("off")
        if key == "shake": return self.t("on") if s.screen_shake else self.t("off")
        if key == "auto": return self.t("on") if s.auto_collect else self.t("off")
        return ""

    def _draw_about(self):
        s = self.screen
        if 0 not in self._menu_bg_cache: self._menu_bg_cache[0] = self._build_menu_bg(0)
        s.blit(self._menu_bg_cache[0], (0,0))
        ov = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA); ov.fill((0,0,0,180)); s.blit(ov,(0,0))
        cx = SCREEN_W//2
        draw_ts(s, self.t("about").upper(), self.f_big, WHITE, (cx, S(70)), (0,0,0), 4)
        # логотип
        pygame.draw.circle(s, (255,205,40), (cx, S(160)), S(40))
        for i in range(8):
            a = i*math.tau/8 + self.menu_time
            pygame.draw.circle(s, (255,205,40),
                (int(cx+math.cos(a)*S(35)), int(S(160)+math.sin(a)*S(35))), S(12))
        pygame.draw.circle(s, (140,85,35), (cx, S(160)), S(22))
        lines = [
            GAME_TITLE + " v" + VERSION,
            self.t("credits") + ": " + AUTHOR,
            self.t("made_with") + " pygame + Python",
            "",
            "LOL v8.0",
            "",
            "Зомбі: 19 типів",
            "Рослини: 10 видів",
            "Локацій: 7 (1 секретна)",
        ]
        for i, line in enumerate(lines):
            color = (255,240,180) if i == 0 else WHITE
            t = self.f_med.render(line, True, color)
            s.blit(t, t.get_rect(center=(cx, S(240)+i*S(30))))
        self.btn_about_back.draw(s)

    def _draw_levels(self):
        s = self.screen
        if 0 not in self._menu_bg_cache: self._menu_bg_cache[0] = self._build_menu_bg(0)
        s.blit(self._menu_bg_cache[0], (0,0))
        ov = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA); ov.fill((0,0,0,120)); s.blit(ov,(0,0))
        draw_ts(s, self.t("select_location"), self.f_big, WHITE, (SCREEN_W//2, S(50)), (30,50,80), 4)
        li = {"uk":0,"ru":1,"en":2}[self.settings.language]
        for i, lvl in enumerate(LEVELS):
            r = self.level_buttons[i]; comp = i in self.completed_levels
            locked = (i == 6 and not self.secret_unlocked)
            sh = pygame.Surface((r.w+8, r.h+8), pygame.SRCALPHA)
            pygame.draw.rect(sh, (0,0,0,120), (0,0,r.w,r.h), border_radius=S(16))
            s.blit(sh, (r.x+5, r.y+5))
            if not locked:
                pv = pygame.Rect(r.x+S(10), r.y+S(10), r.w-S(20), S(80))
                for rr in range(3):
                    for cc in range(4):
                        c = lvl["lawn_a"] if (rr+cc)%2 == 0 else lvl["lawn_b"]
                        pygame.draw.rect(s, c, (pv.x+cc*(pv.w//4), pv.y+rr*(pv.h//3),
                            pv.w//4+1, pv.h//3+1))
                pygame.draw.rect(s, (40,30,20), r, 4, border_radius=S(16))
                name = LEVEL_NAMES[lvl["name_idx"]][li]
                ns = self.f_med.render(name, True, WHITE)
                s.blit(ns, ns.get_rect(center=(r.centerx, r.y+S(115))))
                info = self.f_small.render(
                    self.t("time")+": "+str(lvl["win_time"])+"  Sun: "+str(lvl["sun_start"]),
                    True, (255,235,150))
                s.blit(info, info.get_rect(center=(r.centerx, r.y+S(145))))
            else:
                pygame.draw.rect(s, (60,50,60), r, border_radius=S(16))
                pygame.draw.rect(s, (100,80,100), r, 4, border_radius=S(16))
                lock = self.f_huge.render("?", True, (200,150,200))
                s.blit(lock, lock.get_rect(center=r.center))
                hint = self.f_tiny.render("Секрет...", True, (200,150,200))
                s.blit(hint, hint.get_rect(center=(r.centerx, r.y+S(150))))
            if comp and not locked:
                star = self.f_big.render("V", True, (100,255,100))
                s.blit(star, star.get_rect(center=(r.right-S(25), r.y+S(25))))
        self.btn_levels_back.draw(s)

    def _draw_world(self):
        s = self.screen
        lvl = LEVELS[self.current_level]
        ox, oy = 0, 0
        if self.shake_t > 0 and self.shake_amp > 0:
            ox = random.randint(-self.shake_amp, self.shake_amp)
            oy = random.randint(-self.shake_amp, self.shake_amp)
        s.fill(lvl["lawn_b"], (0,0,SCREEN_W,SCREEN_H))
        if self.current_level not in self._lawn_bg_cache:
            self._lawn_bg_cache[self.current_level] = self._build_lawn_bg(self.current_level)
        s.blit(self._lawn_bg_cache[self.current_level], (GRID_LEFT+ox, GRID_TOP+oy))
        draw_house(s)
        if self.selected_card is not None:
            mx, my = pygame.mouse.get_pos()
            cell = pos_to_cell(mx, my)
            if cell:
                col, row = cell
                if self.grid[row][col] is None:
                    hl = pygame.Surface((CELL_W, CELL_H), pygame.SRCALPHA)
                    hl.fill((255,255,255,70)); pygame.draw.rect(hl, (255,255,255,160), (0,0,CELL_W,CELL_H), 2)
                    s.blit(hl, (GRID_LEFT+col*CELL_W, GRID_TOP+row*CELL_H))
        for m in self.mowers: m.draw(s)
        for r in range(GRID_ROWS):
            for c in range(GRID_COLS):
                p = self.grid[r][c]
                if p is not None: p.draw(s)
        for z in sorted(self.zombies, key=lambda zz: zz.row): z.draw(s)
        for pr in self.projectiles: pr.draw(s)
        for sun in self.suns: sun.draw(s)
        for pt in self.particles: pt.draw(s)
        for fs in self.flying_suns: fs.draw(s)
        for ft in self.floating_texts: ft.draw(s)
        if lvl["tint"] is not None:
            t = lvl["tint"]
            tint = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
            tint.fill((t[0],t[1],t[2],t[3])); s.blit(tint, (0,0))
        self._draw_ui(s)

    def _draw_ui(self, s):
        pygame.draw.rect(s, (78,54,32), (0,0,SCREEN_W,UI_HEIGHT))
        pygame.draw.rect(s, (120,85,50), (0,UI_HEIGHT-S(5),SCREEN_W,S(5)))
        panel = pygame.Rect(S(10),S(6),S(140),UI_HEIGHT-S(12))
        pygame.draw.rect(s, (215,195,145), panel, border_radius=S(10))
        pygame.draw.rect(s, (110,80,45), panel, 3, border_radius=S(10))
        pygame.draw.circle(s, (255,210,40), (S(44),UI_HEIGHT//2), S(22))
        pygame.draw.circle(s, (255,245,160), (S(44),UI_HEIGHT//2), S(13))
        txt = self.f_med.render(str(int(self.sun)), True, (40,30,10))
        s.blit(txt, txt.get_rect(midleft=(S(76),UI_HEIGHT//2)))
        for c in self.cards:
            c.draw(s, self.f_small, c is self.selected_card, self.sun >= c.plant_cls.cost)
        lvl = LEVELS[self.current_level]
        rem = max(0.0, lvl["win_time"]-self.elapsed)
        t1 = self.f_small.render(self.t("time")+": "+str(int(rem)), True, WHITE)
        s.blit(t1, (SCREEN_W-S(140)-t1.get_width(), S(12)))
        t2 = self.f_tiny.render(self.t("killed")+": "+str(self.zombies_killed), True, (230,225,180))
        s.blit(t2, (SCREEN_W-S(140)-t2.get_width(), S(42)))
        pygame.draw.rect(s, (100,70,40), self.btn_pause, border_radius=S(10))
        pygame.draw.rect(s, (60,40,20), self.btn_pause, 3, border_radius=S(10))
        cx, cy = self.btn_pause.center
        pygame.draw.rect(s, WHITE, (cx-S(10),cy-S(12),S(7),S(24)))
        pygame.draw.rect(s, WHITE, (cx+S(3),cy-S(12),S(7),S(24)))

    def _draw_paused(self):
        s = self.screen
        ov = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA); ov.fill((0,0,0,180)); s.blit(ov,(0,0))
        draw_ts(s, self.t("paused"), self.f_huge, WHITE, (SCREEN_W//2, SCREEN_H//2-S(40)), (0,0,0), 5)
        draw_ts(s, self.t("tap_continue"), self.f_med, (230,230,200),
                (SCREEN_W//2, SCREEN_H//2+S(40)), (0,0,0), 2)

    def _draw_gameover(self):
        s = self.screen
        ov = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA); ov.fill((0,0,0,200)); s.blit(ov,(0,0))
        if self.won: title, color = self.t("victory"), (120,255,120)
        else: title, color = self.t("gameover"), (255,95,95)
        draw_ts(s, title, self.f_huge, color, (SCREEN_W//2, S(140)), (0,0,0), 5)
        info = self.f_med.render(
            self.t("killed_label")+": "+str(self.zombies_killed)+"   |   "+
            self.t("time")+": "+str(int(self.elapsed))+" "+self.t("sec"), True, WHITE)
        s.blit(info, info.get_rect(center=(SCREEN_W//2, S(230))))
        self.btn_restart.draw(s); self.btn_levels.draw(s); self.btn_menu.draw(s)


def main():
    flags = pygame.SCALED | pygame.FULLSCREEN | pygame.DOUBLEBUF
    try:
        screen = pygame.display.set_mode((RENDER_W, RENDER_H), flags, vsync=1)
    except pygame.error:
        try: screen = pygame.display.set_mode((RENDER_W, RENDER_H), pygame.SCALED | pygame.FULLSCREEN)
        except pygame.error: screen = pygame.display.set_mode((RENDER_W, RENDER_H), pygame.SCALED)

    pygame.display.set_caption(GAME_TITLE+" v"+VERSION)
    clock = pygame.time.Clock()
    game = Game(screen)
    running = True
    while running:
        dt = clock.tick(FPS)/1000.0
        dt = min(dt, 0.04)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: running = False
            else: game.handle_event(event)
        game.update(dt)
        game.draw()
        if game.settings.show_fps:
            fps = int(clock.get_fps())
            fs = game.f_small.render("FPS: "+str(fps), True, (0,255,0))
            game.screen.blit(fs, (5, SCREEN_H-20))
        pygame.display.flip()
    pygame.quit(); sys.exit()

if __name__ == "__main__":
    main()