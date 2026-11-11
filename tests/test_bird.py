import sys
import types
import unittest
from unittest.mock import patch


canvas = types.ModuleType('pico2d')
canvas.width = 1600
canvas.get_canvas_width = lambda: canvas.width
canvas.load_image = lambda _path: object()

import game_framework

with patch.dict(sys.modules, {'pico2d': canvas}):
    import bird


class BirdMovementTests(unittest.TestCase):
    def setUp(self):
        canvas.width = 1600
        game_framework.frame_time = 0.02

    def test_keeps_moving_left_after_bouncing_off_right_wall(self):
        right_bound = canvas.width - bird.FRAME_WIDTH / 2
        sprite = bird.Bird(right_bound - 0.1, 480)

        sprite.update()
        self.assertEqual(sprite.direction, -1)
        position_after_bounce = sprite.x

        sprite.update()

        self.assertEqual(sprite.direction, -1)
        self.assertLess(sprite.x, position_after_bounce)

    def test_moves_at_80_kmh_in_game_coordinates(self):
        sprite = bird.Bird(800, 480)
        game_framework.frame_time = 0.1

        sprite.update()

        self.assertAlmostEqual(
            sprite.x,
            800 + bird.SPEED_PPS * game_framework.frame_time,
        )

    def test_reverses_at_both_walls(self):
        left_bound = bird.FRAME_WIDTH / 2
        right_bound = canvas.width - left_bound
        sprite = bird.Bird(100, 480)
        directions_seen = {sprite.direction}

        for _ in range(220):
            sprite.update()
            directions_seen.add(sprite.direction)
            self.assertGreaterEqual(sprite.x, left_bound)
            self.assertLessEqual(sprite.x, right_bound)

        self.assertEqual(directions_seen, {-1, 1})


if __name__ == '__main__':
    unittest.main()
