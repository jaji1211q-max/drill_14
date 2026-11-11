import importlib
import sys
import types
import unittest
from unittest.mock import patch


canvas = types.ModuleType('pico2d')
canvas.width = 1600
canvas.height = 600
canvas.get_canvas_width = lambda: canvas.width
canvas.get_canvas_height = lambda: canvas.height
canvas.load_image = lambda _path: object()

import game_framework

with patch.dict(sys.modules, {'pico2d': canvas}):
    import bird


class BirdMovementTests(unittest.TestCase):
    def setUp(self):
        canvas.width = 1600
        game_framework.frame_time = 0.02

    def test_keeps_moving_left_after_bouncing_off_right_wall(self):
        right_bound = canvas.width - bird.DISPLAY_WIDTH / 2
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

    def test_uses_80_kmh_and_12_animation_frames_per_second(self):
        self.assertEqual(bird.SPEED_KMPH, 80.0)
        self.assertEqual(bird.FRAME_RATE, 12.0)
        self.assertAlmostEqual(
            bird.SPEED_PPS,
            80.0 * 1000.0 / 3600.0 * bird.PIXELS_PER_METER,
        )

    def test_reverses_at_both_walls(self):
        left_bound = bird.DISPLAY_WIDTH / 2
        right_bound = canvas.width - left_bound
        sprite = bird.Bird(100, 480)
        directions_seen = {sprite.direction}

        for _ in range(220):
            sprite.update()
            directions_seen.add(sprite.direction)
            self.assertGreaterEqual(sprite.x, left_bound)
            self.assertLessEqual(sprite.x, right_bound)

        self.assertEqual(directions_seen, {-1, 1})

    def test_draws_bird_at_half_sprite_sheet_size(self):
        sprite = bird.Bird(800, 480)
        draw_calls = []
        sprite.image = types.SimpleNamespace(
            clip_composite_draw=lambda *args: draw_calls.append(args)
        )

        sprite.draw()

        self.assertEqual(
            draw_calls[0][-2:],
            (bird.DISPLAY_WIDTH, bird.DISPLAY_HEIGHT),
        )

    def test_play_mode_spawns_ten_birds_at_random_heights(self):
        import game_world

        boy_module = types.ModuleType('boy')
        boy_module.Boy = lambda: object()
        grass_module = types.ModuleType('grass')
        grass_module.Grass = lambda: object()

        with patch.dict(
            sys.modules,
            {
                'pico2d': canvas,
                'bird': bird,
                'boy': boy_module,
                'game_world': game_world,
                'grass': grass_module,
            },
        ):
            play_mode = importlib.import_module('play_mode')

        game_world.clear()
        try:
            with patch.object(
                play_mode, 'randint', side_effect=range(100, 110)
            ) as random_y:
                play_mode.init()

            birds = [
                obj
                for layer in game_world.world
                for obj in layer
                if isinstance(obj, bird.Bird)
            ]
            self.assertEqual(len(birds), 10)
            self.assertEqual([obj.y for obj in birds], list(range(100, 110)))
            random_y.assert_any_call(
                int(bird.DISPLAY_HEIGHT / 2),
                canvas.height - int(bird.DISPLAY_HEIGHT / 2),
            )
            self.assertEqual(random_y.call_count, 10)
        finally:
            game_world.clear()
            play_mode.boy = None


if __name__ == '__main__':
    unittest.main()
