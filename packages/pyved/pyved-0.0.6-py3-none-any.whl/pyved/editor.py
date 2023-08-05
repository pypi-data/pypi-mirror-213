import pygame
import pygame_gui

# from pygame_gui.ui_manager import UIManager
# from pygame_gui.elements.ui_window import UIWindow
from pygame_gui.elements.ui_image import UIImage
from pygame_gui import UIManager, UI_TEXT_ENTRY_CHANGED
from pygame_gui.elements import UIWindow, UITextEntryBox, UITextBox
from .menu_bar_gui import UIMenuBar, menu_data

from . import menu_bar_ev_handler

from .pong.pong import PongGame
import os  # so i can open file to read src code!
import pathlib

PONG_WINDOW_SELECTED = pygame.event.custom_type()


APP_W, APP_H = 1380, 800
KTG_W, KTG_H = 960, 720
# ktg sont les dim. d'un jeu
POS_PREVIEW = (200, 0)

target_dir = None
target_file = 'ERR_NO_FILE'


class GamePreview(UIWindow):
    def __init__(self, gamename, position, ui_manager):
        super().__init__(pygame.Rect(position, (KTG_W+32, KTG_H+59)), ui_manager,
                         window_display_title=gamename,
                         object_id='#pong_window',
                         draggable=False)

        game_surface_size = self.get_container().get_size()
        print('surf pour affichage jeu:', game_surface_size)

        self.game_surface_element = UIImage(pygame.Rect((0, 0),
                                                        game_surface_size),
                                            pygame.Surface(game_surface_size).convert(),
                                            manager=ui_manager,
                                            container=self,
                                            parent_element=self)

        self.pong_game = PongGame()
        self.is_active = False

    def process_event(self, event):
        handled = super().process_event(event)
        if (event.type == pygame_gui.UI_BUTTON_PRESSED and
                event.ui_object_id == "#pong_window.#title_bar" and
                event.ui_element == self.title_bar):
            handled = True
            event_data = {'ui_element': self,
                          'ui_object_id': self.most_specific_combined_id}
            window_selected_event = pygame.event.Event(PONG_WINDOW_SELECTED,
                                                       event_data)
            pygame.event.post(window_selected_event)
        if self.is_active:
            handled = self.pong_game.process_event(event)
        return handled

    def update(self, time_delta):
        if self.alive() and self.is_active:
            self.pong_game.update(time_delta)

        super().update(time_delta)

        self.pong_game.draw(self.game_surface_element.image)


def gen_edition_title(file, project_name):
    return file+f"({project_name}) source-code"


class MiniGamesApp:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Pyved: game creation toolbox')
        self.root_window_surface = pygame.display.set_mode((APP_W, APP_H))

        self.background_surface = pygame.Surface((APP_W, APP_H)).convert()
        self.background_surface.fill(pygame.Color('#505050'))
        self.ui_manager = UIManager((APP_W, APP_H), os.path.join(os.path.dirname(__file__),'gui-rel-data/ui_theme.json'))
        self.clock = pygame.time.Clock()
        self.is_running = True

        self.pong_window_1 = GamePreview(
            'Pong demo',
            POS_PREVIEW,
            self.ui_manager
        )
        # self.pong_window_2 = PongWindow((50, 50), self.ui_manager)
        self.pong_window_1.is_active = True

        # --------- text edition related stuff -------------
        if target_dir is not None:
            path = pathlib.PurePath(target_dir)
            pure_dir = path.name
        else:
            pure_dir = '??'
        self.notepad_window = UIWindow(pygame.Rect(50, 20, 380, 400), window_display_title=gen_edition_title(target_file, pure_dir))
        output_window = UIWindow(pygame.Rect(440, 20, 380, 400), window_display_title="Score")

        self.text_entry_box = UITextEntryBox(  # swap to editable text box
                relative_rect=pygame.Rect((0, 0), self.notepad_window.get_container().get_size()),
                initial_text="",
                container=self.notepad_window)

        self.text_output_box = UITextBox(
                relative_rect=pygame.Rect((0, 0), output_window.get_container().get_size()),
                html_text="",
                container=output_window)
        if target_dir is not None:
            thefile = os.path.join(target_dir, target_file)
            with open(thefile, 'r') as fptr:
                self.text_entry_box.set_text(fptr.read())

        # -------------- menu bar related stuff ------------------
        self.menu_bar = UIMenuBar(relative_rect=pygame.Rect(0, 0, 1280, 25),
                                  menu_item_data=menu_data,
                                  manager=self.ui_manager)
        self.menu_bar_event_handler = menu_bar_ev_handler.MenuBarEventHandler(self.root_window_surface, self.ui_manager)

    def run(self):
        while self.is_running:
            time_delta = self.clock.tick(60)/1000.0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False

                self.ui_manager.process_events(event)

                # use the menu bar also!
                self.menu_bar_event_handler.process_event(event)

                if event.type == PONG_WINDOW_SELECTED:
                    event.ui_element.is_active = True
##                    if event.ui_element == self.pong_window_1:
##                        self.pong_window_2.is_active = False
##                    elif event.ui_element == self.pong_window_2:
##                        self.pong_window_1.is_active = False
                elif event.type == UI_TEXT_ENTRY_CHANGED and event.ui_element == self.text_entry_box:
                    self.text_output_box.set_text(event.text)

                # --- open pyved.json --- {
                elif (event.type == pygame_gui.UI_FILE_DIALOG_PATH_PICKED and
                        event.ui_object_id == '#open_file_dialog'):
                    path = pathlib.Path(event.text)
                    p = pathlib.PurePath(event.text)
                    filename = p.name
                    print(path.parent)
                    p2 = pathlib.PurePath(path.parent)
                    adhoc_dir = p2.name

                    self.menu_bar_event_handler.last_used_file_path = path.parent
                    try:
                        self.notepad_window.set_display_title(gen_edition_title(filename, adhoc_dir))
                        with open(str(path), 'r') as fptr:
                            self.text_entry_box.set_text(fptr.read())
##                        loaded_image = pygame.image.load(str(path)).convert_alpha()
##
##                        canvas_window_rect = pygame.Rect(200, 25,
##                                                         min(loaded_image.get_width() + 52,
##                                                             self.window_surface.get_width() - 200),
##                                                         min(loaded_image.get_height() + 82,
##                                                             self.window_surface.get_height() - 25))
##
##                        window = CanvasWindow(rect=canvas_window_rect,
##                                              manager=self.ui_manager,
##                                              image_file_name=path.name,
##                                              image=loaded_image)
##
##                        window.canvas_ui.set_active_tool(self.tool_bar_window.get_active_tool())
##                        window.canvas_ui.set_save_file_path(path)
                    except pygame.error:
                        message_rect = pygame.Rect(0, 0, 250, 160)
                        message_rect.center = self.window_surface.get_rect().center
                        message_window = UIMessageWindow(rect=message_rect,
                                                         html_message='Unable to load image.',
                                                         manager=self.ui_manager,
                                                         window_title='Loading error')
                        message_window.set_blocking(True)
                    # fin open pyved.json

            self.ui_manager.update(time_delta)

            self.root_window_surface.blit(self.background_surface, (0, 0))
            self.ui_manager.draw_ui(self.root_window_surface)

            pygame.display.update()


def run_editor():
    app = MiniGamesApp()
    app.run()
