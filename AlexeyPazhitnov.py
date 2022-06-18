from settings import Settings, Block, BackGround
import sys
import pygame


class AlexeyPazhitnov:
    def __init__(self):
        '''初始化游戏资源'''
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("俄罗斯方块v1.0")
        self.back_ground = BackGround()
        self.block = Block()
        self.clock=pygame.time.Clock()
        self.game_continue=1


    def _game_condition(self):
        n=int(self.settings.col / 2)-1
        for i in range(1,3):
            for j in range(n,n+3):
                if self.back_ground.screen_piex[i][j]==0:
                    return
        self.game_continue=0

    def _check_events(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        if event.key == pygame.K_LEFT:
            self.block.moving_left = True
        elif event.key==pygame.K_a:
            self.block.moving_left=True
        elif event.key == pygame.K_RIGHT:
            self.block.moving_right = True
        elif event.key==pygame.K_d:
            self.block.moving_right=True
        elif event.key == pygame.K_UP :
            self.block.rotate(1,self.back_ground.screen_piex)
        elif event.key==pygame.K_w:
            self.block.rotate(1,self.back_ground.screen_piex)
        elif event.key == pygame.K_DOWN :
            self.block.rotate(3,self.back_ground.screen_piex)
        elif event.key == pygame.K_s :
            self.block.rotate(3,self.back_ground.screen_piex)
        elif event.key==pygame.K_SPACE:
            self.block.moving_down=True
        elif event.key==pygame.K_r:
            self.game_continue=0
        elif event.key == pygame.K_q:
            sys.exit()

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT :
            self.block.moving_right = False
        elif event.key == pygame.K_d:
            self.block.moving_right = False
        elif event.key == pygame.K_LEFT :
            self.block.moving_left = False
        elif event.key == pygame.K_a:
            self.block.moving_left = False
        elif event.key==pygame.K_SPACE:
            self.block.moving_down=False

    def _back_ground_updata(self):
        for i in range(len(self.block.block_piex_x)):
            if  self.back_ground.screen_piex[self.block.block_piex_x[i] + self.block.start_y + 1][
                self.block.block_piex_y[i] + self.block.start_x]:
                self.back_ground.updata(self.block.block_piex_x, self.block.block_piex_y, self.block.start_x,
                                        self.block.start_y, self.block.block_piex)
                self.block = Block()
                return 0
        return 1
    def _screen_updata(self,f):
        self.screen.fill(self.settings.bg_color)
        if f :
            self.block.block_draw(self.screen)
        self.back_ground.clean_line()
        self.back_ground.screen_draw(self.screen)
        self.back_ground.draw_score(self.screen)
        pygame.display.flip()

    def run_game(self):
        while self.game_continue:
            self.clock.tick(60)
            self.block.n=(self.block.n+1)%30#刷新率
            self._check_events()  # 键盘事件
            self.block.pos_updata(self.back_ground.screen_piex)  # block位置更新
            self._screen_updata(self._back_ground_updata())#背景显示 #数据更新
            self._game_condition()



if __name__ == '__main__':
    while(1):
        game = AlexeyPazhitnov()
        game.run_game()
