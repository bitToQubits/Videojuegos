# -*- coding: utf-8 -*-
from turtle import up
import pygame

import keybinds
import rendering.neon as neon
import config
import util.profiling as profiling
import util.fonts as fonts
from sound_manager.SoundManager import SoundManager
import rendering.levelbuilder3d as levelbuilder3d
import gameplay.highscores as highscores
import util.utility_functions as utils
import json,os

TARGET_FPS = config.Display.fps if not config.Debug.fps_test else -1
down = False
up = False
left = False
right = False
class GameLoop:
    def __init__(self):
        self.running = True
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.get_surface()
        self.current_mode = MainMenuMode(self)
        self.current_mode.on_mode_start()
        
    def set_mode(self, next_mode):
        if self.current_mode != next_mode:
            self.current_mode.on_mode_end()
        self.current_mode = next_mode
        self.current_mode.on_mode_start

    def start(self):

        dt = 0
        while self.running:
            joysticks = []
            for i in range(pygame.joystick.get_count()):
                joysticks.append(pygame.joystick.Joystick(i))

            for joystick in joysticks:
                joystick.init()

            with open(os.path.join(os.getcwd(), "ps4_keys.json"), "r+") as file:
                button_keys = json.load(file)

            analog_keys = {0:0, 1:0,2:0,3:0,4:-1, 5:-1}
            events = []
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    print("INFO: quitting game")
                    self.running = False
                    return
                else:
                    # collect all the events so we can pass them into the current game mode.
                    events.append(e)
                
                #Botones presionados
                if e.type == pygame.JOYBUTTONDOWN:
                    if e.button == button_keys['left_arrow']:
                        left = True
                    if e.button == button_keys['right_arrow']:
                        right = True
                    if e.button == button_keys['up_arrow']:
                        up = True
                    if e.button == button_keys['down_arrow']:
                        down = True

                #Botones que se dejan de presionar
                if e.type == pygame.JOYBUTTONUP:
                    if e.button == button_keys['left_arrow']:
                        left = False
                    if e.button == button_keys['right_arrow']:
                        right = False
                    if e.button == button_keys['down_arrow']:
                        down = False
                    if e.button == button_keys['up_arrow']:
                        up = False

                if e.type == pygame.JOYAXISMOTION:
                    analog_keys[e.axis] = e.value
                    #Horizontal analogico
                    if abs(analog_keys[0]) > .4:
                        if analog_keys[0] < -.7:
                            left = True
                        else:
                            left = False

                        if analog_keys[0] > .7:
                            right = True
                        else:
                            right = False
                    #Vertical analogico
                    if abs(analog_keys[1]) > .4:
                        if analog_keys[1] < -.7:
                            up = True
                        else:
                            up = False

                        if analog_keys[1] > -.7:
                            down = True
                        else:
                            down = False



                # global keybinds
                if e.type == pygame.KEYDOWN:
                    if e.key in keybinds.TOGGLE_NEON:
                        config.Debug.use_neon = not config.Debug.use_neon
                        print("INFO: toggling neon to: {}".format(config.Debug.use_neon))
                    if e.key in keybinds.TOGGLE_PROFILER:
                        profiling.get_instance().toggle()
            cur_mode = self.current_mode

            cur_mode.update(dt, events)
            cur_mode.draw_to_screen(self.screen)

            pygame.display.flip()

            if config.Debug.fps_test:
                pygame.display.set_caption(f"{config.Display.title} {int(self.clock.get_fps())} FPS")

            dt = self.clock.tick(TARGET_FPS) / 1000.0


class GameMode:

    def __init__(self, loop: GameLoop):
        self.loop: GameLoop = loop

    def on_mode_start(self):
        """Called when mode becomes active"""
        pass

    def on_mode_end(self):
        """Called when mode becomes inactive"""
        pass

    def update(self, dt, events):
        pass

    def draw_to_screen(self, screen):
        pass


class MainMenuMode(GameMode):

    def __init__(self, loop: GameLoop):
        super().__init__(loop)
        self.selected_option_idx = 0
        self.options = [
            ("start", lambda: self.start_pressed()),
            ("help", lambda: self.help_pressed()),
            ("settings", lambda: self.settings_pressed()),
            ("credits", lambda: self.credits_pressed()),
            ("exit", lambda: self.exit_pressed())
        ]

        self.title_font = fonts.get_font(config.FontSize.title)
        self.option_font = fonts.get_font(config.FontSize.option)

        import gameplay.levels as levels
        import rendering.threedee as threedee
        import rendering.neon as neon
        self.bg_level = levels.InfiniteGeneratingLevel(10)
        self.bg_camera = threedee.Camera3D()
        self.bg_renderer = neon.NeonRenderer()

    def on_mode_start(self):
        SoundManager.play_song("menu_theme", fadein_ms=0)

    def start_pressed(self):
        import gameplay.gamestuff  # shh don't tell pylint about this
        self.loop.set_mode(gameplay.gamestuff.GameplayMode(self.loop))

    def help_pressed(self):
        import menus.help_menu as help_menu
        self.loop.set_mode(help_menu.HelpMenuMode(self.loop, self))

    def settings_pressed(self):
        import menus.settings_menu as settings_menu
        self.loop.set_mode(settings_menu.SettingsMenuMode(self.loop))

    def credits_pressed(self):
        import menus.credits_menu as credits_menu
        self.loop.set_mode(credits_menu.CreditsMenuMode(self.loop, self))

    def exit_pressed(self):
        self.loop.running = False

    def update(self, dt, events):
        for e in events:
            if e.type == pygame.KEYDOWN:
                if e.key in keybinds.MENU_UP:
                    SoundManager.play("blip")
                    self.selected_option_idx = (self.selected_option_idx - 1) % len(self.options)
                elif e.key in keybinds.MENU_DOWN:
                    SoundManager.play("blip")
                    self.selected_option_idx = (self.selected_option_idx + 1) % len(self.options)
                elif e.key in keybinds.MENU_ACCEPT:
                    SoundManager.play("accept")
                    self.options[self.selected_option_idx][1]()  # activate the option's lambda
                    return
                elif e.key in keybinds.MENU_CANCEL:
                    SoundManager.play("blip2")
                    self.exit_pressed()
                    return

        self._update_bg(dt)

    def draw_to_screen(self, screen: pygame.Surface):
        screen.fill((0, 0, 0))

        self._draw_bg(screen)

        screen_size = screen.get_size()
        title_surface = self.title_font.render('TEMPEST RUN', True, neon.WHITE)

        title_size = title_surface.get_size()
        title_y = screen_size[1] // 3 - title_size[1] // 2
        screen.blit(title_surface, dest=(screen_size[0] // 2 - title_size[0] // 2,
                                         title_y))

        option_y = max(screen_size[1] // 2, title_y + title_size[1])
        for i in range(len(self.options)):
            option_text = self.options[i][0]
            is_selected = i == self.selected_option_idx
            color = neon.WHITE if not is_selected else neon.RED

            option_surface = self.option_font.render(option_text.upper(), True, color)
            option_size = option_surface.get_size()
            screen.blit(option_surface, dest=(screen_size[0] // 2 - option_size[0] // 2, option_y))
            option_y += option_size[1]

    def _update_bg(self, dt):
        rot_speed = 10    # degrees per sec
        move_speed = 5  # units per sec
        self.bg_camera.position.z += dt * move_speed
        self.bg_camera.position.y = -1
        self.bg_level.set_rotation(self.bg_level.get_rotation(self.bg_camera.position.z) + rot_speed * dt)

    def _draw_bg(self, screen):
        import rendering.levelbuilder3d as levelbuilder3d
        import rendering.neon as neon
        cur_z = self.bg_camera.position.z
        cell_len = 20

        all_3d_lines = []
        for i in range(-1, 20):
            all_3d_lines.extend(levelbuilder3d.build_section((i + cur_z // cell_len) * cell_len, cell_len, self.bg_level))

        lines_to_draw = self.bg_camera.project_to_surface(screen, all_3d_lines, depth_shading=(0, 100))
        self.bg_renderer.draw_lines(screen, neon.NeonLine.convert_line2ds_to_neon_lines(lines_to_draw))


def create_or_recreate_window():
    size = config.Display.width, config.Display.height

    pygame.display.set_mode(size)
    pygame.display.set_caption(config.Display.title)
    pygame.display.set_icon(pygame.image.load(utils.resource_path("pygame-summer-team-jam-main/assets/icon/icon.png")))


def _main():
    config.load_configs_from_disk()

    # create config.json on game start if it's been deleted
    if not config.get_config_path().exists():
        config.save_configs_to_disk()

    pygame.init()
    SoundManager.init()
    levelbuilder3d.load_player_art()
    create_or_recreate_window()
    highscores.load_score()

    loop = GameLoop()
    loop.start()


if __name__ == "__main__":
    _main()
