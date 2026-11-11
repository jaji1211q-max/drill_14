import game_framework
from pico2d import get_canvas_width, load_image


PIXELS_PER_METER = 10.0 / 0.3
SPEED_KMPH = 80.0
SPEED_MPS = SPEED_KMPH * 1000.0 / 3600.0
SPEED_PPS = SPEED_MPS * PIXELS_PER_METER

FRAME_WIDTH = 183
FRAME_HEIGHT = 168
FRAME_RATE = 12.0
FRAME_ROWS_Y = (338, 170, 1)
FRAME_COUNT = 14


class Bird:
    def __init__(self, x, y):
        self.image = load_image('bird_animation.png')
        self.x, self.y = x, y
        self.direction = 1
        self.frame = 0.0

    def update(self):
        self.frame = (self.frame + FRAME_RATE * game_framework.frame_time) % FRAME_COUNT

        left_bound = FRAME_WIDTH / 2
        right_bound = get_canvas_width() - left_bound
        travel_distance = self.x - left_bound + (
            self.direction * SPEED_PPS * game_framework.frame_time
        )
        travel_span = right_bound - left_bound
        if travel_span <= 0:
            self.x = get_canvas_width() / 2
            return

        travel = travel_distance % (2 * travel_span)
        if travel < travel_span:
            self.x = left_bound + travel
            self.direction = 1
        else:
            self.x = right_bound - (travel - travel_span)
            self.direction = -1

    def draw(self):
        frame_index = int(self.frame)
        row = frame_index // 5
        column = frame_index % 5
        flip = '' if self.direction == 1 else 'h'
        self.image.clip_composite_draw(
            column * FRAME_WIDTH,
            FRAME_ROWS_Y[row],
            FRAME_WIDTH,
            FRAME_HEIGHT,
            0,
            flip,
            self.x,
            self.y,
            FRAME_WIDTH,
            FRAME_HEIGHT,
        )
