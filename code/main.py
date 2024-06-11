import pygame

class Game:
    def __init__(self):
        pygame.init()
        pygame.font.init()

        self.size = (1600, 960)
        self.screen = pygame.display.set_mode(self.size)
        self.background = pygame.Surface(self.size)
        self.clock = pygame.time.Clock()

        pygame.display.set_caption("A zelda like game")

    
    def run_homescreen(self):
        from home_screen import Home_screen
        HOME_SCREEN = Home_screen()

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        running = False
                        self.run_gameplay()
                    if event.key == pygame.K_c:
                        # go to character creation
                        ...
                    if event.key == pygame.K_e:
                        running = False
                        self.run_combat_environment()

            self.screen.fill("black")
            HOME_SCREEN.draw(self.screen, self.size)

            pygame.display.update()
            self.clock.tick(60)


    def run_gameplay(self):
        from world import World

        WORLD = World()

        # font for FPS
        font = pygame.font.SysFont("arial", 25)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()

            self.screen.fill("#48acac")
            WORLD.draw_map()

            fps_text = font.render(f"FPS: {self.clock.get_fps()}", False, "black")
            self.screen.blit(fps_text, (0,0))

            WORLD.player.actions(pygame.sprite.Group())

            pygame.display.update()
            self.clock.tick(60)



    def run_combat_environment(self):
        from helpers.test.test_combat_environment import Combat_Environment
        from helpers.sprites.enemies import Enemie
        from player import Player

        enemies_sprites = pygame.sprite.Group()
        Enemie(name="zombie_l_01", pos=(1000, 300), groups=enemies_sprites)
        
        obstacles_sprites = pygame.sprite.Group()
        PLAYER = Player(pos=(1000, 500), obstacle_sprites=obstacles_sprites)

        COMBAT_ENVIRONMENT = Combat_Environment(PLAYER, enemies_sprites)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()

            self.screen.fill("white")
            COMBAT_ENVIRONMENT.draw(self.screen, self.background)

            PLAYER.actions(enemies_sprites)

            pygame.display.update()
            self.clock.tick(60)



if __name__ == "__main__":
    game = Game()
    game.run_homescreen()