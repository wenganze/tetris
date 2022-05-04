import pygame
import random
import os

#利用list儲存RGB顏色參數
colors = [
    (0, 0, 0),
    (120, 37, 179),
    (100, 179, 179),
    (80, 34, 22),
    (80, 134, 22),
    (180, 34, 22),
    (180, 34, 122),
    (100, 100, 100)
]

#建立落下物件的屬性與動作
class Figure:
    x = 0
    y = 0

    #用list表示不同的樣式與旋轉
    figures = [
        [[1, 5, 9, 13], [4, 5, 6, 7]],
        [[4, 5, 9, 10], [2, 6, 5, 9]],
        [[6, 7, 9, 10], [1, 5, 6, 10]],
        [[1, 2, 5, 9], [0, 4, 5, 6], [1, 5, 9, 8], [4, 5, 6, 10]],
        [[1, 2, 6, 10], [5, 6, 7, 9], [2, 6, 10, 11], [3, 5, 6, 7]],
        [[1, 4, 5, 6], [1, 4, 5, 9], [4, 5, 6, 9], [1, 5, 6, 9]],
        [[1, 2, 5, 6]],
    ]

    #物件的初始化函數
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.type = random.randint(0, len(self.figures) - 1)
        self.color = random.randint(1, len(colors) - 2)
        self.rotation = 0

    #回傳物件樣式
    def image(self):
        return self.figures[self.type][self.rotation]

    #旋轉
    def rotate(self):
        self.rotation = (self.rotation + 1) % len(self.figures[self.type])

#建立遊戲介面
class Tetris:
    level = 2
    score = 0
    state = "start"
    field = []
    height = 0
    width = 0
    x = 100
    y = 60
    zoom = 20
    figure = None

    #介面初始化
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.field = []
        self.score = 0
        self.state = "start"
        for i in range(height):
            new_line = []
            for j in range(width):
                new_line.append(0)
            self.field.append(new_line)

    #產生新物件
    def new_figure(self):
        self.figure = Figure(3, 0)

    #判斷物件是否超過遊戲邊界
    def intersects(self):
        intersection = False
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.image():
                    if i + self.figure.y > self.height - 1 or \
                            j + self.figure.x > self.width - 1 or \
                            j + self.figure.x < 0 or \
                            self.field[i + self.figure.y][j + self.figure.x] > 0:
                        intersection = True
        return intersection

    #消去已經填滿的排數
    def break_lines(self):
        lines = 0
        for i in range(1, self.height):
            zeros = 0
            for j in range(self.width):
                if self.field[i][j] == 0:
                    zeros += 1
            if zeros == 0:
                lines += 1
                for i1 in range(i, 1, -1):
                    for j in range(self.width):
                        self.field[i1][j] = self.field[i1 - 1][j]
        self.score += lines ** 2    #依消去排數^2進行加分

    #直接將物件移動到底面邊界
    def go_space(self):
        while not self.intersects():
            self.figure.y += 1
        self.figure.y -= 1
        self.freeze()

    #讓物件在長按向下鍵時下降一段距離直到放開
    def go_down(self):
        self.figure.y += 1
        if self.intersects():
            self.figure.y -= 1
            self.freeze()

    #將以不可移動的物件固定
    def freeze(self):
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.image():
                    self.field[i + self.figure.y][j + self.figure.x] = self.figure.color
        self.break_lines()
        self.new_figure()
        if self.intersects():
            self.state = "gameover"

    #讓物件左右移動
    def go_side(self, dx):
        old_x = self.figure.x
        self.figure.x += dx
        if self.intersects():
            self.figure.x = old_x

    #旋轉物件
    def rotate(self):
        old_rotation = self.figure.rotation
        self.figure.rotate()
        if self.intersects():
            self.figure.rotation = old_rotation
    
    #當分數達到五的倍數時，在最底部增加分數/5排灰色空一格新排提升難度
    def harder(self,height):
        for i in range(self.height-height):
            for j in range(self.width):
                self.field[i][j] = self.field[i+height][j]
        num = random.randrange(self.width)  #在一排中隨機空一格
        for i in range(1,height+1):
            for j in range(self.width):
                if j == num:
                    color = 0
                else:
                    color = 7
                self.field[self.height-i][j] = color

#引入微軟黑正體用來輸出中文
font_name = os.path.join("font.ttf")

#建立函數方便產生字
def draw_text(surf , text , size , x , y , color):
    font_example = pygame.font.Font(font_name , size)   #設定自型與大小
    text_surface = font_example.render(text , True , color) #設定內容與顏色
    text_rect = text_surface.get_rect() 
    text_rect.centerx = x   #設定x座標
    text_rect.top = y       #設定y座標
    surf.blit(text_surface, text_rect)  #加入內容

#建立遊戲初始介面
def draw_init():
    #建立所需顯現的內容
    draw_text(screen , 'TETRIS' , 64 , WIDTH/2 , HEIGHT/4 , WHITE)
    draw_text(screen , '←→控制方向 ↑變換樣式 ↓快速下降 空白鍵直接到底' , 15 , WIDTH/2 , HEIGHT/2 , WHITE)
    draw_text(screen , '按任意鍵開始', 20 , WIDTH/2 , HEIGHT*3/4 , WHITE)
    pygame.display.update() #刷新頁面
    #在偵測到有按住的鍵盤放開時，結束初始頁面的狀態
    waiting = True
    while waiting:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return True
            elif event.type == pygame.KEYUP:
                waiting = False
                return False

#建立gameover畫面
def game_over():
    screen.fill((0,0,0))    #將畫面填成黑色
    #在畫面上標示所需的內容
    draw_text(screen,'GAME OVER' , 64 ,WIDTH/2 , HEIGHT/4 , WHITE)
    draw_text(screen,f'最高分數:{best_score}', 30 , WIDTH/2 , HEIGHT /2 , WHITE)
    draw_text(screen, '按任意鍵繼續', 20 ,WIDTH / 2, HEIGHT * 3 / 4 , WHITE)
    pygame.display.update() #刷新頁面
    waiting = True
    #在偵測到有按住的鍵盤放開時，結束gameover的狀態
    while waiting:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return True
            elif event.type == pygame.KEYUP:
                waiting = False
                return False

#初始化pygame
pygame.init()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)

WIDTH = 400
HEIGHT = 500
size = ( WIDTH, HEIGHT)
screen = pygame.display.set_mode(size) #設定視窗大小

#叫出視窗並將視窗標題改成Tetris
pygame.display.set_caption("Tetris")    

done = False
clock = pygame.time.Clock()
fps = 25
game = Tetris(20, 10)
counter = 0
best_score = 0
hard_index = False

point = 0
point1 = 5

show_init = True
pressing_down = False

#迴圈讓遊戲可以持續進行
while not done:
    #叫出初始畫面
    if show_init:
        draw_init()
        show_init = False
    
    #當畫面上沒有物件時，建立新物件
    if game.figure is None:
        game.new_figure()
    
    #計數
    counter += 1
    
    if counter > 100000:
        counter = 0
    
    #取得在遊戲中的得分
    if game.score > point:
        point = game.score
        hard_index = True
    
    #讓物體下落
    if counter % (fps // game.level // 2) == 0 or pressing_down:
        if game.state == "start":
            game.go_down()
    
    #判斷分數是否超過每五分
    if game.state != 'gameover':
        if game.score >= point1 and hard_index == True:
            game.harder(game.score//5)
            hard_index = False
            while(point1 <= game.score):
                point1 += 5
    
    #紀錄最佳分數
    if game.state == 'gameover':
        if game.score > best_score:
            best_score = game.score
    
    #偵測遊戲中發生的事件
    for event in pygame.event.get():
        #關閉時結束迴圈
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if game.state != "gameover":
                if event.key == pygame.K_UP:  #按↑旋轉物件
                    game.rotate()
                if event.key == pygame.K_DOWN:#按↓讓物件下降一段距離
                    pressing_down = True
                if event.key == pygame.K_LEFT:#按←讓物體左移
                    game.go_side(-1)
                if event.key == pygame.K_RIGHT:#按→讓物體右移
                    game.go_side(1)
                if event.key == pygame.K_SPACE:#按空白鍵讓物體到底
                    game.go_space()
        #偵測什麼時候放開鍵盤
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                pressing_down = False

    #將畫面填白
    screen.fill(WHITE)

    #顯現邊界
    for i in range(game.height):
        for j in range(game.width):
            pygame.draw.rect(screen, GRAY, [game.x + game.zoom * j, game.y + game.zoom * i, game.zoom, game.zoom], 1)
            if game.field[i][j] > 0:
                pygame.draw.rect(screen, colors[game.field[i][j]],
                                 [game.x + game.zoom * j + 1, game.y + game.zoom * i + 1, game.zoom - 2, game.zoom - 1])

    #顯現可移動與不可移動的物件
    if game.figure is not None:
        for i in range(4):
            for j in range(4):
                p = i * 4 + j
                if p in game.figure.image():
                    pygame.draw.rect(screen, colors[game.figure.color],
                                     [game.x + game.zoom * (j + game.figure.x) + 1,
                                      game.y + game.zoom * (i + game.figure.y) + 1,
                                      game.zoom - 2, game.zoom - 2])

    #顯示目前分數
    draw_text(screen , f'分數:{point}' , 20 , WIDTH/15 , 0 ,(0 , 0 , 0))
    
    #當遊戲狀態為gameover時
    if game.state == "gameover":
        #產生gameover畫面並停頓
        game_over()
        #刷新遊戲畫面並重置部分數值
        game.__init__(20, 10)
        hard_index = True
        point = 0
        point1 = 5
    
    #刷新整個頁面
    pygame.display.flip()
    clock.tick(fps)

#跳出迴圈後關閉遊戲
pygame.quit()
