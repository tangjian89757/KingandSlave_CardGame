import pygame
import random
import sys
import os
import time

# 初始化
pygame.init()
pygame.mixer.init()
WIDTH, HEIGHT = 1000, 700  # 增大窗口尺寸
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.DOUBLEBUF)
pygame.display.set_caption("King & Slave 卡牌游戏")
pygame.display.set_icon(pygame.Surface((32, 32)))

# 字体设置 - 使用高质量字体和抗锯齿
try:
    # 尝试使用更高质量的字体
    font_large = pygame.font.Font(None, 48)
    font_medium = pygame.font.Font(None, 32)
    font_small = pygame.font.Font(None, 24)
    font_tiny = pygame.font.Font(None, 20)
    # 不使用粗体，保持字体美观
except:
    # 备选方案
    font_large = pygame.font.SysFont("arial", 48)
    font_medium = pygame.font.SysFont("arial", 32)
    font_small = pygame.font.SysFont("arial", 24)
    font_tiny = pygame.font.SysFont("arial", 20)

# 颜色定义
COLORS = {
    'bg': (245, 245, 250),  # 淡灰蓝色背景
    'card_bg': (250, 250, 255),  # 淡蓝白色卡牌背景
    'card_border': (70, 130, 180),  # 钢蓝色边框
    'text_dark': (25, 25, 112),  # 深蓝色文字
    'text_light': (100, 149, 237),  # 浅蓝色文字
    'king_color': (220, 20, 60),  # 深红色（King）
    'slave_color': (34, 139, 34),  # 森林绿（Slave）
    'soldier_color': (105, 105, 105),  # 暗灰色（Soldier）
    'unknown_bg': (220, 220, 220),  # 浅灰色（未知卡牌）
    'button_bg': (80, 140, 190),
    'button_hover': (110, 159, 247),
    'shadow': (0, 0, 0, 50),
    'panel_bg': (235, 240, 250),  # 面板背景色
    'accent_bg': (230, 235, 245)  # 强调背景色
}

clock = pygame.time.Clock()

# 封面图加载
def load_cover_image():
    base_dir = os.path.dirname(__file__)
    name_candidates = [
        # 明确支持当前封面命名
        "King&Slave_GameCoverImage.png",
        # 兼容旧命名
        "cover.png", "cover.jpg", "cover.jpeg",
        "gamecover.png", "gamecover.jpg", "gamecover.jpeg",
        "gamecover.png.jpg"
    ]
    search_paths = []
    for n in name_candidates:
        search_paths.append(os.path.join(base_dir, n))
        search_paths.append(os.path.join(base_dir, "assets", n))
    for path in search_paths:
        if os.path.exists(path):
            try:
                img = pygame.image.load(path)
                # 依窗口比例平滑缩放
                w, h = img.get_size()
                scale = min(WIDTH / w, HEIGHT / h)
                new_size = (int(w * scale), int(h * scale))
                return pygame.transform.smoothscale(img, new_size)
            except:
                pass
    # 无封面时返回浅色背景
    fallback = pygame.Surface((WIDTH, HEIGHT))
    fallback.fill(COLORS['bg'])
    return fallback

# 音效和背景音乐
def load_sound(filename):
    try:
        base_dir = os.path.dirname(__file__)
        # 优先尝试根目录
        sound_path = os.path.join(base_dir, filename)
        if os.path.exists(sound_path):
            return pygame.mixer.Sound(sound_path)
        # 再尝试 assets 目录
        assets_path = os.path.join(base_dir, "assets", filename)
        if os.path.exists(assets_path):
            return pygame.mixer.Sound(assets_path)
    except:
        pass
    return None

# 背景音乐（兼容 assets 目录与新文件名）
_base_dir = os.path.dirname(__file__)
music_candidates = [
    os.path.join(_base_dir, "background_music.mp3"),
    os.path.join(_base_dir, "assets", "background_music.mp3"),
    os.path.join(_base_dir, "assets", "King&Slave_BGM.mp3"),
]
music_path = next((p for p in music_candidates if os.path.exists(p)), None)
if music_path and os.path.exists(music_path):
    try:
        pygame.mixer.music.load(music_path)
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.2)
    except:
        pass

# 音效
sounds = {
    "card_flip": load_sound("card_flip.wav"),
    "victory": load_sound("victory.wav"),
    "defeat": load_sound("defeat.wav"),
    "draw": load_sound("draw.wav")
}

# 工具：获取 assets 下的资源路径
def _asset_path(filename):
    return os.path.join(os.path.dirname(__file__), "assets", filename)

# 加载图像 - 高分辨率版本（自动在根目录与 assets 下查找）
def load_card(filename, size=(120, 180)):
    try:
        base_dir = os.path.dirname(__file__)
        # 依次尝试：绝对/相对给定路径、根目录、assets 目录
        candidate_paths = [
            filename,
            os.path.join(base_dir, filename),
            os.path.join(base_dir, "assets", filename)
        ]
        img_path = next((p for p in candidate_paths if os.path.exists(p)), None)
        img = pygame.image.load(img_path) if img_path else pygame.image.load(filename)
        # 使用高质量缩放
        scaled_img = pygame.transform.smoothscale(img, size)
        # 确保图像有正确的格式
        if not scaled_img.get_flags() & pygame.SRCALPHA:
            scaled_img = scaled_img.convert_alpha()
        return scaled_img
    except Exception as e:
        print(f"⚠️ 图像加载失败: {filename} - {e}")
        # 创建美观的占位符
        surface = pygame.Surface(size, pygame.SRCALPHA)
        surface.fill(COLORS['card_bg'])
        
        # 绘制边框
        pygame.draw.rect(surface, COLORS['card_border'], surface.get_rect(), 4)
        pygame.draw.rect(surface, COLORS['text_light'], surface.get_rect(), 2)
        
        # 绘制文字
        text = font_medium.render(filename.replace('.png', ''), True, COLORS['text_dark'])
        rect = text.get_rect(center=(size[0]//2, size[1]//2))
        surface.blit(text, rect)
        
        return surface

def create_unknown_card(size=(120, 180)):
    surface = pygame.Surface(size, pygame.SRCALPHA)
    
    # 扑克牌风格的深蓝色背景
    surface.fill((25, 25, 112))  # 深蓝色
    
    # 绘制边框
    pygame.draw.rect(surface, (255, 255, 255), surface.get_rect(), 3)
    pygame.draw.rect(surface, (70, 130, 180), surface.get_rect(), 1)
    
    # 绘制扑克牌风格的花纹
    w, h = size
    
    # 四个角的装饰
    corner_size = 20
    for x, y in [(0, 0), (w-corner_size, 0), (0, h-corner_size), (w-corner_size, h-corner_size)]:
        # 绘制小方块装饰
        pygame.draw.rect(surface, (255, 255, 255), (x+2, y+2, corner_size-4, corner_size-4), 2)
        pygame.draw.rect(surface, (100, 149, 237), (x+4, y+4, corner_size-8, corner_size-8), 1)
    
    # 中心花纹 - 绘制对称的几何图案
    center_x, center_y = w//2, h//2
    
    # 绘制中心菱形
    points = [
        (center_x, center_y - 15),
        (center_x + 15, center_y),
        (center_x, center_y + 15),
        (center_x - 15, center_y)
    ]
    pygame.draw.polygon(surface, (255, 255, 255), points, 2)
    pygame.draw.polygon(surface, (100, 149, 237), points, 1)
    
    # 绘制四个小圆点
    for dx, dy in [(0, -25), (25, 0), (0, 25), (-25, 0)]:
        pygame.draw.circle(surface, (255, 255, 255), (center_x + dx, center_y + dy), 3)
        pygame.draw.circle(surface, (100, 149, 237), (center_x + dx, center_y + dy), 2)
    
    # 绘制边框装饰线
    for i in range(3):
        y = 30 + i * 40
        pygame.draw.line(surface, (100, 149, 237), (10, y), (w-10, y), 1)
    
    return surface

# 预加载所有图像（适配重命名后的资源文件）
CARD_SIZE = (120, 180)

# 名称到实际文件名映射
CARD_FILE_MAP = {
    "King": "King&Slave_RoleCard_King.png",
    "Soldier": "King&Slave_RoleCard_Soldier.png",
    "Slave": "King&Slave_RoleCard_Slave.png",
}

card_images = {
    "King": load_card(CARD_FILE_MAP["King"], CARD_SIZE),
    "Soldier": load_card(CARD_FILE_MAP["Soldier"], CARD_SIZE),
    "Slave": load_card(CARD_FILE_MAP["Slave"], CARD_SIZE),
    "Unknown": create_unknown_card(CARD_SIZE)
}

class Card:
    def __init__(self, name, x, y):
        self.name = name
        self.image = card_images[name]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.dragging = False
        self.offset_x = 0
        self.offset_y = 0
        self.original_y = y
        self.original_x = x
        self.scale = 1.0

    def draw(self, surface):
        if self.dragging:
            # 拖拽时放大并添加阴影
            scaled_image = pygame.transform.smoothscale(self.image, 
                (int(CARD_SIZE[0] * 1.1), int(CARD_SIZE[1] * 1.1)))
            
            # 绘制阴影
            shadow_rect = scaled_image.get_rect(topleft=(self.rect.x + 3, self.rect.y + 3))
            shadow_surface = pygame.Surface(shadow_rect.size, pygame.SRCALPHA)
            shadow_surface.fill(COLORS['shadow'])
            surface.blit(shadow_surface, shadow_rect.topleft)
            
            surface.blit(scaled_image, (self.rect.x - 6, self.rect.y - 6))
        else:
            surface.blit(self.image, self.rect.topleft)

    def set_position(self, x, y):
        self.rect.topleft = (x, y)
        self.original_y = y
        self.original_x = x

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

class Game:
    def __init__(self):
        self.phase = "cover"  # cover, choose, arrange, battle, end
        self.deck_type = None
        self.player_cards = []
        self.computer_cards = []
        self.dragging_card = None
        self.battle_index = 0
        self.winner = None
        self.animating = False
        self.animation_step = 0
        self.battle_result = ""
        self.waiting_for_next = False
        self.wait_timer = 0
        self.card_spacing = 130
        # 当前对战缓存，避免渲染使用下一轮卡牌
        self.current_p_card = None
        self.current_c_card = None
        # 按钮区域存储
        self.king_button_rect = None
        self.slave_button_rect = None
        # 封面图
        self.cover_image = load_cover_image()

    def play_sound(self, sound_name):
        if sounds[sound_name]:
            try:
                sounds[sound_name].play()
            except:
                pass

    def draw_text(self, text, x, y, color=COLORS['text_dark'], font_type="medium", center=True):
        font_to_use = font_large if font_type == "large" else font_medium if font_type == "medium" else font_small if font_type == "small" else font_tiny
        # 使用抗锯齿渲染
        rendered = font_to_use.render(text, True, color)
        if center:
            rect = rendered.get_rect(center=(x, y))
        else:
            rect = rendered.get_rect(topleft=(x, y))
        screen.blit(rendered, rect)

    def draw_button(self, text, x, y, width, height, color=COLORS['button_bg'], hover_color=COLORS['button_hover']):
        mouse_pos = pygame.mouse.get_pos()
        is_hover = (x <= mouse_pos[0] <= x + width and y <= mouse_pos[1] <= y + height)
        
        button_color = hover_color if is_hover else color
        
        # 绘制按钮
        pygame.draw.rect(screen, button_color, (x, y, width, height))
        pygame.draw.rect(screen, COLORS['text_dark'], (x, y, width, height), 3)
        
        # 绘制文字
        self.draw_text(text, x + width//2, y + height//2, COLORS['card_bg'], "medium")
        
        return is_hover, (x, y, width, height)

    def choose_deck(self, deck_type):
        self.deck_type = deck_type
        
        # 重新设计布局 - 确保卡牌完全在面板内
        panel_margin = 50  # 面板边距
        card_width = CARD_SIZE[0]  # 120
        card_height = CARD_SIZE[1]  # 180
        
        # 面板尺寸
        panel_width = WIDTH - 2 * panel_margin  # 900
        panel_height = 200  # 面板高度
        
        # 计算卡牌间距，确保5张卡牌完全在面板内
        # 需要为卡牌留出边距
        card_margin = 20  # 卡牌与面板边缘的最小距离
        available_width = panel_width - 2 * card_margin - card_width  # 740
        self.card_spacing = available_width // 4  # 185
        
        # 计算起始位置，使卡牌在面板内居中
        start_x = panel_margin + card_margin + (available_width - 4 * self.card_spacing) // 2
        
        # 电脑面板位置
        computer_panel_y = 50
        computer_y = computer_panel_y + (panel_height - card_height) // 2  # 居中在面板内
        
        # 玩家面板位置
        player_panel_y = 300
        player_y = player_panel_y + (panel_height - card_height) // 2  # 居中在面板内
        
        # 创建玩家卡组：1张主卡 + 4张士兵
        self.player_cards = []
        for i in range(5):
            card_name = deck_type if i == 0 else "Soldier"
            x = start_x + i * self.card_spacing
            self.player_cards.append(Card(card_name, x, player_y))
        
        # 创建电脑卡组：相反的卡组
        opponent_type = "Slave" if deck_type == "King" else "King"
        self.computer_cards = []
        for i in range(5):
            card_name = opponent_type if i == 0 else "Soldier"
            x = start_x + i * self.card_spacing
            self.computer_cards.append(Card(card_name, x, computer_y))
        
        # 电脑卡组随机排序
        random.shuffle(self.computer_cards)
        for i, card in enumerate(self.computer_cards):
            card.set_position(start_x + i * self.card_spacing, computer_y)
        
        self.phase = "arrange"
        self.battle_index = 0

    def handle_drag(self, event):
        if self.phase != "arrange":
            return
        
        for card in self.player_cards:
            if card.is_clicked(event.pos):
                card.dragging = True
                card.offset_x = card.rect.x - event.pos[0]
                card.offset_y = card.rect.y - event.pos[1]
                self.dragging_card = card
                # 将拖拽的卡牌移到最前面
                self.player_cards.remove(card)
                self.player_cards.append(card)
                break

    def handle_motion(self, event):
        if self.dragging_card and self.dragging_card.dragging:
            self.dragging_card.rect.x = event.pos[0] + self.dragging_card.offset_x
            self.dragging_card.rect.y = event.pos[1] + self.dragging_card.offset_y

    def handle_drop(self):
        if self.dragging_card and self.dragging_card.dragging:
            self.dragging_card.dragging = False
            self.dragging_card = None
            # 重新排序卡牌
            self.player_cards.sort(key=lambda c: c.rect.x)
            # 使用与初始化时相同的布局计算
            panel_margin = 50
            card_width = CARD_SIZE[0]
            card_height = CARD_SIZE[1]
            panel_width = WIDTH - 2 * panel_margin
            panel_height = 200
            card_margin = 20
            available_width = panel_width - 2 * card_margin - card_width
            self.card_spacing = available_width // 4
            start_x = panel_margin + card_margin + (available_width - 4 * self.card_spacing) // 2
            player_panel_y = 300
            player_y = player_panel_y + (panel_height - card_height) // 2
            for i, card in enumerate(self.player_cards):
                card.set_position(start_x + i * self.card_spacing, player_y)

    def start_battle(self):
        if self.phase != "arrange" or self.battle_index >= len(self.player_cards):
            return
        
        self.phase = "battle"
        self.animating = True
        self.animation_step = 0
        self.battle_result = ""
        # 固定当前对战双方卡牌
        self.current_p_card = self.player_cards[self.battle_index]
        self.current_c_card = self.computer_cards[self.battle_index]
        self.play_sound("card_flip")

    def update_animation(self):
        if not self.animating:
            return

        self.animation_step += 1
        
        if self.animation_step > 100:  # 动画结束 - 延长以配合华丽特效
            self.animating = False
            self.resolve_battle()
            return

    def resolve_battle(self):
        if self.battle_index >= len(self.player_cards):
            return
        
        # 使用缓存的卡牌，确保显示稳定
        p_card = self.current_p_card
        c_card = self.current_c_card
        
        # 统一的胜负规则：King > Soldier > Slave > King；相同卡牌为平局
        def who_wins(a, b):
            if a == b:
                return "draw"
            beats = {"King": "Soldier", "Soldier": "Slave", "Slave": "King"}
            return "player" if beats[a] == b else ("computer" if beats[b] == a else "draw")
        
        outcome = who_wins(p_card.name, c_card.name)
        if outcome == "player":
            self.winner = "Player"
            self.battle_result = f"{p_card.name} beats {c_card.name}! Player Wins!"
        elif outcome == "computer":
            self.winner = "Computer"
            self.battle_result = f"{c_card.name} beats {p_card.name}! Computer Wins!"
        else:
            self.battle_result = f"{p_card.name} vs {c_card.name} - Draw! Continue..."
        
        # 保持 battle_index 不变，直到进入下一轮时再推进
        
        if self.winner:
            self.phase = "end"
            if self.winner == "Player":
                self.play_sound("victory")
            elif self.winner == "Computer":
                self.play_sound("defeat")
            else:
                self.play_sound("draw")
        elif (self.battle_index + 1) > len(self.player_cards) - 1:
            self.winner = "Draw"
            self.phase = "end"
            self.play_sound("draw")
        else:
            self.waiting_for_next = True
            self.wait_timer = 0

    def next_round(self):
        if not self.waiting_for_next:
            return
        
        # 移除已使用的卡牌
        # 移除首张（本轮已对战）
        if self.player_cards:
            self.player_cards.pop(0)
        if self.computer_cards:
            self.computer_cards.pop(0)
        
        # 重新排列剩余卡牌 - 使用与初始化时相同的布局计算
        panel_margin = 50
        card_width = CARD_SIZE[0]
        card_height = CARD_SIZE[1]
        panel_width = WIDTH - 2 * panel_margin
        panel_height = 200
        card_margin = 20
        available_width = panel_width - 2 * card_margin - card_width
        self.card_spacing = available_width // 4
        start_x = panel_margin + card_margin + (available_width - 4 * self.card_spacing) // 2
        
        computer_panel_y = 50
        computer_y = computer_panel_y + (panel_height - card_height) // 2
        player_panel_y = 300
        player_y = player_panel_y + (panel_height - card_height) // 2
        
        for i, card in enumerate(self.player_cards):
            card.set_position(start_x + i * self.card_spacing, player_y)
        for i, card in enumerate(self.computer_cards):
            card.set_position(start_x + i * self.card_spacing, computer_y)
        
        self.battle_index = 0
        self.current_p_card = None
        self.current_c_card = None
        self.phase = "arrange"
        self.waiting_for_next = False
        self.battle_result = ""

    def show_winner(self):
        # 配色：统一柔和渐变 + 玻璃拟态面板 + 干净留白
        if self.winner == "Player":
            winner_text = f"{self.deck_type} Wins!"
            winner_type = self.deck_type
            accent = COLORS['king_color'] if self.deck_type == "King" else COLORS['slave_color']
        elif self.winner == "Computer":
            opponent = "Slave" if self.deck_type == "King" else "King"
            winner_text = f"{opponent} Wins!"
            winner_type = opponent
            accent = COLORS['king_color'] if opponent == "King" else COLORS['slave_color']
        else:
            winner_text = "Draw!"
            winner_type = "Soldier"
            accent = COLORS['soldier_color']

        # 背景：竖向柔和渐变
        top_color = (245, 248, 255)
        bottom_color = (230, 235, 245)
        for y in range(HEIGHT):
            t = y / max(1, HEIGHT - 1)
            r = int(top_color[0] * (1 - t) + bottom_color[0] * t)
            g = int(top_color[1] * (1 - t) + bottom_color[1] * t)
            b = int(top_color[2] * (1 - t) + bottom_color[2] * t)
            pygame.draw.line(screen, (r, g, b), (0, y), (WIDTH, y))

        # 移除光束与环形装饰，保持干净背景

        # 玻璃面板
        panel_w, panel_h = 720, 520
        panel_rect = pygame.Rect((WIDTH - panel_w)//2, (HEIGHT - panel_h)//2 - 20, panel_w, panel_h)
        glass = pygame.Surface(panel_rect.size, pygame.SRCALPHA)
        glass.fill((255, 255, 255, 150))
        screen.blit(glass, panel_rect.topleft)
        pygame.draw.rect(screen, (255, 255, 255, 200), panel_rect, 2, border_radius=16)
        pygame.draw.rect(screen, (0, 0, 0, 30), panel_rect.inflate(12, 12), 2, border_radius=20)

        # 头像（仅人物，无额外杂纹理）
        winner_image = card_images[winner_type if winner_type in ("King", "Slave") else "Soldier"]
        face_h = 320
        face_w = int(face_h * CARD_SIZE[0] / CARD_SIZE[1])
        face = pygame.transform.smoothscale(winner_image, (face_w, face_h))
        face_rect = face.get_rect(center=(WIDTH//2, panel_rect.top + 180))

        # 仅显示头像，不添加环形光晕
        screen.blit(face, face_rect)

        # 主标题
        self.draw_text(winner_text, WIDTH//2 + 2, panel_rect.top + 330 + 2, (0, 0, 0), "large")
        self.draw_text(winner_text, WIDTH//2, panel_rect.top + 330, accent, "large")

        # 次标题
        sub = "Game Over"
        self.draw_text(sub, WIDTH//2, panel_rect.top + 370, COLORS['text_dark'], "medium")

        # 行为提示（胶囊按钮风格）
        btn_w, btn_h = 260, 44
        btn_x, btn_y = WIDTH//2 - btn_w//2, panel_rect.bottom - 80
        pygame.draw.rect(screen, (*accent, 220), (btn_x, btn_y, btn_w, btn_h), border_radius=22)
        pygame.draw.rect(screen, (255, 255, 255), (btn_x, btn_y, btn_w, btn_h), 2, border_radius=22)
        self.draw_text("Click to exit", WIDTH//2, btn_y + btn_h//2, (255, 255, 255), "small")

        pygame.display.flip()
        pygame.time.wait(3000)
        pygame.quit()
        sys.exit()

    def draw_game(self):
        screen.fill(COLORS['bg'])
        
        if self.phase == "cover":
            # 居中绘制封面
            if self.cover_image:
                rect = self.cover_image.get_rect(center=(WIDTH//2, HEIGHT//2))
                screen.blit(self.cover_image, rect.topleft)
            
            # 绘制标题 - 调整位置，不要太靠上
            title_y = 120  # 从80调整到120，给标题更多空间
            self.draw_text("King & Slave Card Game", WIDTH//2, title_y, (255, 255, 255), "large")
            
            # 添加英文副标题 - 与主标题对齐
            subtitle_y = title_y + 50  # 在标题下方50像素
            self.draw_text("A Strategic Card Battle Game", WIDTH//2, subtitle_y, (255, 255, 255), "small")
            
            # 绘制操作提示 - 调整位置
            self.draw_text("Click mouse or press any key to start", WIDTH//2, HEIGHT - 80, (255, 255, 255), "small")

        elif self.phase == "choose":
            # 绘制背景面板
            panel_rect = pygame.Rect(50, 120, WIDTH - 100, 280)
            pygame.draw.rect(screen, COLORS['panel_bg'], panel_rect)
            pygame.draw.rect(screen, COLORS['card_border'], panel_rect, 3)
            
            # 绘制标题 - 在面板内居中
            self.draw_text("King & Slave Card Game", WIDTH//2, 160, COLORS['text_dark'], "large")
            self.draw_text("Choose Your Deck:", WIDTH//2, 200, COLORS['text_dark'], "medium")
            
            # 绘制卡组选择按钮
            button_width, button_height = 180, 45
            button_y = 250
            
            # King 卡组按钮
            king_hover, self.king_button_rect = self.draw_button("King (Easy)", WIDTH//2 - 200, button_y, button_width, button_height, COLORS['king_color'])
            
            # Slave 卡组按钮 - 缩短文字
            slave_hover, self.slave_button_rect = self.draw_button("Slave (Hard)", WIDTH//2 + 20, button_y, button_width, button_height, COLORS['slave_color'])
            
            # 绘制说明 - 居中对齐到按钮中心
            self.draw_text("Press K for King", WIDTH//2 - 110, button_y + 60, COLORS['text_light'], "small")
            self.draw_text("Press S for Slave", WIDTH//2 + 110, button_y + 60, COLORS['text_light'], "small")
            
        elif self.phase == "arrange":
            # 绘制电脑卡牌区域背景
            computer_panel = pygame.Rect(50, 50, WIDTH - 100, 200)
            pygame.draw.rect(screen, COLORS['accent_bg'], computer_panel)
            pygame.draw.rect(screen, COLORS['card_border'], computer_panel, 2)
            
            # 绘制玩家卡牌区域背景
            player_panel = pygame.Rect(50, 300, WIDTH - 100, 200)
            pygame.draw.rect(screen, COLORS['accent_bg'], player_panel)
            pygame.draw.rect(screen, COLORS['card_border'], player_panel, 2)
            
            # 绘制电脑卡牌（显示为问号）
            for card in self.computer_cards:
                screen.blit(card_images["Unknown"], card.rect.topleft)
            
            # 绘制玩家卡牌
            for card in self.player_cards:
                card.draw(screen)
            
            # 绘制提示文字 - 在两个面板之间，避免重叠
            self.draw_text("Drag cards to reorder, Press Enter to start battle", WIDTH//2, 270, COLORS['text_dark'], "medium")
            self.draw_text(f"Current Deck: {self.deck_type}", WIDTH//2, 295, COLORS['text_light'], "small")
            
        elif self.phase == "battle":
            # 绘制华丽的翻牌动画
            if self.battle_index < len(self.player_cards):
                p_card = self.player_cards[self.battle_index]
                c_card = self.computer_cards[self.battle_index]
                
                center_x = WIDTH // 2
                center_y = HEIGHT // 2
                
                # 华丽的动画效果
                if self.animation_step < 20:
                    # 阶段1：显示问号卡牌，添加闪烁效果
                    alpha = 255 if (self.animation_step // 3) % 2 else 180
                    unknown_surface = card_images["Unknown"].copy()
                    unknown_surface.set_alpha(alpha)
                    screen.blit(unknown_surface, (center_x - 150, center_y - 90))
                    screen.blit(unknown_surface, (center_x + 30, center_y - 90))
                    
                    # 添加光晕效果
                    for i in range(3):
                        glow_size = 20 + i * 10
                        glow_surface = pygame.Surface((glow_size * 2, glow_size * 2), pygame.SRCALPHA)
                        pygame.draw.circle(glow_surface, (255, 255, 255, 50 - i * 15), (glow_size, glow_size), glow_size)
                        screen.blit(glow_surface, (center_x - 150 - glow_size + 60, center_y - 90 - glow_size + 90))
                        screen.blit(glow_surface, (center_x + 30 - glow_size + 60, center_y - 90 - glow_size + 90))
                        
                elif self.animation_step < 40:
                    # 阶段2：卡牌翻转效果 - 先缩小再放大
                    flip_progress = (self.animation_step - 20) / 20
                    if flip_progress < 0.5:
                        # 缩小阶段
                        scale = 1.0 - flip_progress * 1.4
                        rotation = flip_progress * 180
                    else:
                        # 放大阶段
                        scale = 0.3 + (flip_progress - 0.5) * 1.4
                        rotation = 180 - (flip_progress - 0.5) * 180
                    
                    new_width = int(CARD_SIZE[0] * scale)
                    new_height = int(CARD_SIZE[1] * scale)
                    
                    if new_width > 0 and new_height > 0:
                        # 创建旋转的卡牌
                        card_to_show = p_card.image if flip_progress > 0.5 else card_images["Unknown"]
                        scaled_card = pygame.transform.smoothscale(card_to_show, (new_width, new_height))
                        rotated_card = pygame.transform.rotate(scaled_card, rotation)
                        
                        p_x = center_x - 150 + (CARD_SIZE[0] - rotated_card.get_width()) // 2
                        p_y = center_y - 90 + (CARD_SIZE[1] - rotated_card.get_height()) // 2
                        screen.blit(rotated_card, (p_x, p_y))
                        
                        # 电脑卡牌
                        card_to_show = c_card.image if flip_progress > 0.5 else card_images["Unknown"]
                        scaled_card = pygame.transform.smoothscale(card_to_show, (new_width, new_height))
                        rotated_card = pygame.transform.rotate(scaled_card, rotation)
                        
                        c_x = center_x + 30 + (CARD_SIZE[0] - rotated_card.get_width()) // 2
                        c_y = center_y - 90 + (CARD_SIZE[1] - rotated_card.get_height()) // 2
                        screen.blit(rotated_card, (c_x, c_y))
                        
                        # 添加粒子效果
                        for i in range(5):
                            particle_x = center_x + (i - 2) * 30 + (self.animation_step % 10 - 5) * 2
                            particle_y = center_y + (self.animation_step % 15 - 7) * 3
                            pygame.draw.circle(screen, (255, 255, 255, 200), (int(particle_x), int(particle_y)), 3)
                            
                elif self.animation_step < 60:
                    # 阶段3：卡牌出现效果 - 带弹跳和光效
                    appear_progress = (self.animation_step - 40) / 20
                    bounce = abs(pygame.math.Vector2(0, 1).rotate(appear_progress * 360).y) * 20
                    
                    scale = 0.8 + appear_progress * 0.2 + bounce * 0.01
                    new_width = int(CARD_SIZE[0] * scale)
                    new_height = int(CARD_SIZE[1] * scale)
                    
                    if new_width > 0 and new_height > 0:
                        p_scaled = pygame.transform.smoothscale(p_card.image, (new_width, new_height))
                        c_scaled = pygame.transform.smoothscale(c_card.image, (new_width, new_height))
                        
                        p_x = center_x - 150 + (CARD_SIZE[0] - new_width) // 2
                        p_y = center_y - 90 + (CARD_SIZE[1] - new_height) // 2 - int(bounce)
                        c_x = center_x + 30 + (CARD_SIZE[0] - new_width) // 2
                        c_y = center_y - 90 + (CARD_SIZE[1] - new_height) // 2 - int(bounce)
                        
                        # 添加阴影效果
                        shadow_offset = 5
                        shadow_surface = pygame.Surface((new_width, new_height), pygame.SRCALPHA)
                        shadow_surface.fill((0, 0, 0, 100))
                        screen.blit(shadow_surface, (p_x + shadow_offset, p_y + shadow_offset))
                        screen.blit(shadow_surface, (c_x + shadow_offset, c_y + shadow_offset))
                        
                        screen.blit(p_scaled, (p_x, p_y))
                        screen.blit(c_scaled, (c_x, c_y))
                        
                        # 添加光效边框
                        pygame.draw.rect(screen, (255, 255, 255, 150), (p_x - 2, p_y - 2, new_width + 4, new_height + 4), 3)
                        pygame.draw.rect(screen, (255, 255, 255, 150), (c_x - 2, c_y - 2, new_width + 4, new_height + 4), 3)
                        
                else:
                    # 阶段4：最终显示 - 带震动效果
                    shake_x = (self.animation_step % 4 - 2) * 2
                    shake_y = ((self.animation_step + 1) % 3 - 1) * 2
                    
                    screen.blit(p_card.image, (center_x - 150 + shake_x, center_y - 90 + shake_y))
                    screen.blit(c_card.image, (center_x + 30 + shake_x, center_y - 90 + shake_y))
                    
                    # 添加最终光效
                    for i in range(8):
                        angle = i * 45
                        radius = 80 + (self.animation_step - 60) * 2
                        star_x = center_x + radius * pygame.math.Vector2(1, 0).rotate(angle).x
                        star_y = center_y + radius * pygame.math.Vector2(1, 0).rotate(angle).y
                        pygame.draw.circle(screen, (255, 255, 255, 100), (int(star_x), int(star_y)), 4)
                    
                    self.draw_text(f"{p_card.name} vs {c_card.name}", center_x, center_y + 100, COLORS['text_dark'], "medium")
            
            # 显示战斗结果
            if self.battle_result:
                self.draw_text(self.battle_result, WIDTH//2, HEIGHT - 100, COLORS['text_dark'], "medium")
                if self.waiting_for_next:
                    self.draw_text("Press Enter to continue next round", WIDTH//2, HEIGHT - 60, COLORS['text_light'], "small")
        
        elif self.phase == "end":
            self.show_winner()

# 主循环
game = Game()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif game.phase == "cover":
            if event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                game.phase = "choose"

        elif game.phase == "choose":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_k:
                    game.choose_deck("King")
                elif event.key == pygame.K_s:
                    game.choose_deck("Slave")
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # 检测鼠标点击按钮
                if game.king_button_rect and game.king_button_rect[0] <= event.pos[0] <= game.king_button_rect[0] + game.king_button_rect[2] and game.king_button_rect[1] <= event.pos[1] <= game.king_button_rect[1] + game.king_button_rect[3]:
                    game.choose_deck("King")
                elif game.slave_button_rect and game.slave_button_rect[0] <= event.pos[0] <= game.slave_button_rect[0] + game.slave_button_rect[2] and game.slave_button_rect[1] <= event.pos[1] <= game.slave_button_rect[1] + game.slave_button_rect[3]:
                    game.choose_deck("Slave")

        elif game.phase == "arrange":
            if event.type == pygame.MOUSEBUTTONDOWN:
                game.handle_drag(event)
            elif event.type == pygame.MOUSEMOTION:
                game.handle_motion(event)
            elif event.type == pygame.MOUSEBUTTONUP:
                game.handle_drop()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    game.start_battle()

        elif game.phase == "battle":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and game.waiting_for_next:
                    game.next_round()

    # 更新动画
    if game.phase == "battle":
        game.update_animation()

    # 绘制游戏
    game.draw_game()
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()