import copy
import pygame
import random


class Settings:
    def __init__(self):
        self.screen_width = 300
        self.screen_height = 600
        self.bg_color = (230, 230, 230)
        self.size = 4  # 4*4单个方块
        self.row = 20
        self.col = 10
        self.squre_long = int(self.screen_width / self.col)
        self.text_color=(30,30,30)
        self.font=pygame.font.SysFont(None,48)
        self.block_chose = [
            [0,
             ],

            [[0, 0, 0, 0],
             [1, 1, 1, 1, ],
             [0, 0, 0, 0],
             [0, 0, 0, 0],
             ],
            [[0, 0, 0, 0],
             [0, 2, 0, 0],
             [0, 2, 2, 2],
             [0, 0, 0, 0],
             ],
            [[0, 0, 0, 0],
             [0, 0, 3, 0],
             [3, 3, 3, 0],
             [0, 0, 0, 0],
             ],
            [[0, 0, 0, 0],
             [0, 4, 4, 0],
             [0, 4, 4, 0],
             [0, 0, 0, 0],
             ],
            [[0, 0, 0, 0],
             [0, 0, 5, 5],
             [0, 5, 5, 0],
             [0, 0, 0, 0],
             ],
            [[0, 0, 0, 0],
             [0, 0, 6, 0],
             [0, 6, 6, 6],
             [0, 0, 0, 0],
             ],
            [[0, 0, 0, 0],
             [0, 7, 7, 0],
             [0, 0, 7, 7],
             [0, 0, 0, 0],
             ],
        ]
        self.color_chose = [0, (0, 180, 255), (0, 30, 255), (255, 200, 0), (250, 255, 0), (80, 255, 0), (155, 0, 255),
                            (255, 0, 0)]


class Block(Settings):
    def __init__(self):
        Settings.__init__(self)
        self.start_x = int((self.col - self.size) / 2)
        self.start_y = 0
        chose = random.randint(1, 7)
        self.block_piex = self.block_chose[chose]
        self.color = self.color_chose[chose]
        self.pos = 0
        self.block_piex_x,self.block_piex_y=self.search_block_piex()
        self.moving_right=False
        self.moving_left=False
        self.moving_down=False
        self.n=0

    def check_lr_edge(self):
        '''边界检测'''
        if self.start_x + min(self.block_piex_y) < 0:
            self.start_x = -min(self.block_piex_y)
        if self.start_x + max(self.block_piex_y) > self.col - 1:
            self.start_x = self.col - 1 - max(self.block_piex_y)

    def pos_updata(self,array):

        if self.n==0 :#刷新率控制
            if self.moving_right and self.start_x+max(self.block_piex_y)<self.col-1 and self.mov_left_or_right_check(array,1) :#右边不能有方块
                self.start_x+=1
                self.start_y-=1
            elif self.moving_left and self.start_x+min(self.block_piex_y)>0 and self.mov_left_or_right_check(array,-1):
                self.start_x-=1
                self.start_y-=1
            self.start_y += 1
        if self.moving_down and self.mov_left_or_right_check(array, 0, 1):
            self.start_y += 1


    def block_draw(self, screen):
        for i, j in zip(self.block_piex_x,self.block_piex_y):
            a = (j + self.start_x) * self.squre_long
            b = (i + self.start_y) * self.squre_long
            self.pos = a, b, self.squre_long, self.squre_long
            pygame.draw.rect(screen, self.color, self.pos, 0)

    def rotate(self, n,array):
        sour = copy.deepcopy(self.block_piex)
        re = copy.deepcopy(self.block_piex)
        for total in range(n):
            for j in range(self.size):
                for i in range(self.size):
                    re[j][i] = self.block_piex[self.size - 1 - i][j]
            self.block_piex = copy.deepcopy(re)
        self.block_piex_x, self.block_piex_y = self.search_block_piex()

        self.check_lr_edge()
        for i,j in zip(self.block_piex_x,self.block_piex_y):
            if array[self.start_y+i][self.start_x+j]:
                self.block_piex=sour
                break
        self.block_piex_x, self.block_piex_y = self.search_block_piex()



    def mov_left_or_right_check(self,array,n,f=0):
        '''周围色块检测，n=-1左；n=1右；f=1，n=0时下'''
        re = 1
        m=0
        if f:
            m=1
        for i,j in zip(self.block_piex_x,self.block_piex_y):
            if array[i+ self.start_y+m][j + self.start_x+n]:
                re = 0
                break
        return re



    def search_block_piex(self):
        '''寻找存储block的坐标，返回为列表'''
        x = []
        y = []
        for i in range(self.size):
            for j in range(self.size):
                if self.block_piex[i][j]:
                    x.append(i)
                    y.append(j)
        return x, y


class BackGround(Settings):
    def __init__(self):
        Settings.__init__(self)
        self.pos = 0
        self.screen_piex = [[0 for i in range(self.col)] for j in range(self.row)]
        self.screen_piex.append([1 for i in range(self.col)])
        self.score=0

    def updata(self, x, y, dx, dy, array):
        for i, j in zip(x, y):
            self.screen_piex[i + dy][j + dx] = array[i][j]

    def screen_draw(self, screen):
        for i in range(self.row):
            y = i * self.squre_long
            for j in range(self.col):
                x = j * self.squre_long
                self.pos = x, y, self.squre_long, self.squre_long
                if self.screen_piex[i][j]:
                    pygame.draw.rect(screen, self.color_chose[self.screen_piex[i][j]], self.pos, 0)

    def clean_line(self):
        '''消除行'''
        n=0
        for i in range(self.row - 1, -1, -1):
            k = 0
            for j in range(self.col):
                if self.screen_piex[i][j]:
                    k += 1
            if k == self.col:
                n+=1
                a = [0 for i in range(self.col)]
                self.screen_piex.pop(i)
                self.screen_piex.insert(0, a)
                i += 1
        self.score+=n*2

    def draw_score(self,screen):
        '''分数计算'''
        self.screen_rect = screen.get_rect()

        score_str=str(self.score)
        self.score_image=self.font.render(score_str,True,self.text_color,self.bg_color)


        self.score_rect = self.score_image.get_rect()
        self.score_rect.right=self.screen_rect.right-20
        self.score_rect.top=20
        screen.blit(self.score_image,self.score_rect)
