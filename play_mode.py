from random import randint

from pico2d import *
import game_world
import game_framework
from boy import Boy
from bird import Bird, DISPLAY_HEIGHT
from grass import Grass

BIRD_COUNT = 10
boy = None


def handle_events():


    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
            return
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            boy.handle_event(event)


def init():
    global boy

    boy = Boy()
    game_world.add_oject(boy)

    min_bird_y = int(DISPLAY_HEIGHT / 2)
    max_bird_y = get_canvas_height() - min_bird_y
    for index in range(BIRD_COUNT):
        x = (index + 0.5) * get_canvas_width() / BIRD_COUNT
        y = randint(min_bird_y, max_bird_y)
        game_world.add_oject(Bird(x, y))

    grass = Grass()
    game_world.add_oject(grass, 0)


def pause():
    boy.pause()


def resume():
    pass


def finish():
    global boy
    game_world.clear()
    boy = None


def update():
    game_world.update()

def render():
    clear_canvas()
    game_world.render()
    update_canvas()
