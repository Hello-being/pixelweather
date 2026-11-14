"""
PIXEL WEATHER STATION // Main Game Application
==============================================
"""

import math
import random
import pyxel

from assets import draw_sprite, init_assets, play_sfx
from engine import Camera, FloatingTextManager, ParticleSystem

SCREEN_W = 160
SCREEN_H = 120
FLOOR_Y = 100


class PixelWeatherStation:
    def __init__(self) -> None:
        pyxel.init(SCREEN_W, SCREEN_H, title="Pixel Weather Station", fps=30)
        init_assets()
        pyxel.mouse(False)
        self.reset()
        pyxel.run(self.update, self.draw)

    def reset(self) -> None:
        self.camera = Camera()
        self.particles = ParticleSystem()
        self.popups = FloatingTextManager()

        self.state = "TITLE"  # TITLE, PLAYING, WIN, LOSE
        self.game_timer = 0.0
        self.max_game_time = 90.0  # 90 seconds to win

        self.mood = 50.0  # 0 to 100, starts at 50

        self.player_x = 72.0
        self.player_y = FLOOR_Y - 16
        self.player_speed = 2.5

        self.umbrella_active = False
        self.umbrella_timer = 0
        self.umbrella_cooldown = 0

        self.weather_types = ["Sunny", "Rain", "Wind", "Lightning"]
        self.current_weather = "Sunny"
        self.weather_timer = 0
        self.weather_duration = random.randint(150, 240)

    def update(self) -> None:
        if pyxel.btnp(pyxel.KEY_ESCAPE):
            pyxel.quit()
        if pyxel.btnp(pyxel.KEY_R):
            self.reset()

        if self.state == "TITLE":
            if pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.KEY_RETURN):
                self.reset()
                self.state = "PLAYING"
                play_sfx("blip")

        elif self.state == "PLAYING":
            self.game_timer += 1 / 30.0
            if self.game_timer >= self.max_game_time:
                self.state = "WIN"
                play_sfx("pickup")
                return

            self._update_weather()
            self._update_player()
            self._update_environmental_effects()

            if self.mood <= 0.0 or self.mood >= 100.0:
                self.state = "LOSE"
                play_sfx("boom")

            self.particles.update(gravity=0.08)
            self.popups.update()
            self.camera.update()

        elif self.state in ["WIN", "LOSE"]:
            if pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.KEY_R):
                self.reset()
                self.state = "PLAYING"

    def _update_weather(self) -> None:
        self.weather_timer += 1
        if self.weather_timer >= self.weather_duration:
            self.weather_timer = 0
            self.weather_duration = random.randint(150, 240)
            self.current_weather = random.choice(self.weather_types)

            if self.current_weather == "Lightning":
                self.camera.flash(frames=8, color=7)
                self.camera.shake(frames=10, intensity=3.0)
                play_sfx("boom")
                for _ in range(20):
                    self.particles.burst(random.randint(10, SCREEN_W - 10), random.randint(10, 40), count=2, colors=[7, 9, 10], speed=2.5, life=15)

    def _update_player(self) -> None:
        dx = 0.0
        if pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.KEY_A) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT):
            dx -= 1.0
        if pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.KEY_D) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT):
            dx += 1.0

        self.player_x += dx * self.player_speed
        self.player_x = max(8.0, min(float(SCREEN_W - 24), self.player_x))

        if self.umbrella_cooldown > 0:
            self.umbrella_cooldown -= 1

        if pyxel.btnp(pyxel.KEY_SPACE) and self.umbrella_cooldown == 0 and not self.umbrella_active:
            self.umbrella_active = True
            self.umbrella_timer = 90
            play_sfx("jump")

        if self.umbrella_active:
            self.umbrella_timer -= 1
            if self.umbrella_timer <= 0:
                self.umbrella_active = False
                self.umbrella_cooldown = 150

    def _update_environmental_effects(self) -> None:
        w = self.current_weather

        if w == "Sunny":
            self.mood = min(100.0, self.mood + 0.05)
            if random.random() < 0.08:
                self.popups.spawn("+MOOD", self.player_x, self.player_y - 8, color=11)

        elif w == "Rain":
            if random.random() < 0.6:
                rx = random.randint(0, SCREEN_W)
                self.particles.burst(rx, 0, count=1, colors=[12, 13], speed=3.0, life=35)

            if not self.umbrella_active:
                self.mood = max(0.0, self.mood - 0.08)
                if random.random() < 0.08:
                    self.popups.spawn("-MOOD", SCREEN_W // 2 - 12, FLOOR_Y - 24, color=8)

        elif w == "Wind":
            if random.random() < 0.5:
                wx = 0 if random.random() < 0.5 else SCREEN_W
                wy = random.randint(20, FLOOR_Y - 10)
                vx = 2.0 if wx == 0 else -2.0
                self.particles.burst(wx, wy, count=1, colors=[6, 7], speed=abs(vx), life=20)

            shelter_covers_town = 24 <= self.player_x <= 120
            if not shelter_covers_town:
                self.mood = max(0.0, self.mood - 0.1)
                if random.random() < 0.08:
                    self.popups.spawn("-MOOD", self.player_x, self.player_y - 8, color=8)

        elif w == "Lightning":
            if random.random() < 0.03:
                self.mood = max(0.0, self.mood - 8.0)
                self.camera.flash(frames=6, color=7)
                self.popups.spawn("-8 MOOD!", SCREEN_W // 2 - 16, FLOOR_Y - 24, color=8)

    def draw(self) -> None:
        if self.camera.flash_frames > 0:
            pyxel.cls(self.camera.flash_color)
            return

        bg_color = 1
        if self.current_weather == "Sunny":
            bg_color = 6
        elif self.current_weather == "Rain":
            bg_color = 13
        elif self.current_weather == "Wind":
            bg_color = 5
        elif self.current_weather == "Lightning":
            bg_color = 1

        pyxel.cls(bg_color)
        cam_x, cam_y = self.camera.get_offset()

        if self.state == "TITLE":
            pyxel.text(18, 10, "PIXEL WEATHER STATION", 7)
            pyxel.text(20, 22, "Survive 90s & Balance Mood!", 10)
            pyxel.text(10, 38, "MOVE: Arrow Keys / A & D", 13)
            pyxel.text(10, 48, "UMBRELLA: SPACE (Blocks Rain)", 13)
            pyxel.text(10, 58, "WIND: Cover houses with shelter", 13)
            pyxel.text(10, 68, "SUN: +Mood | LIGHTNING: Flash", 13)
            pyxel.text(10, 78, "GOAL: Keep Mood meter 1 to 99", 11)
            pyxel.text(22, 102, "- PRESS SPACE TO START -", 9)

        else:
            if self.current_weather == "Sunny":
                pyxel.circ(135, 22, 10, 10)

            for hx in range(16, 128, 32):
                draw_sprite("house", hx - cam_x, FLOOR_Y - 16 - cam_y)

            draw_sprite("shelter", self.player_x - cam_x, self.player_y - cam_y)

            if self.umbrella_active:
                draw_sprite("umbrella", self.player_x - cam_x, self.player_y - 10 - cam_y)

            self.particles.draw(cam_x, cam_y)
            self.popups.draw(cam_x, cam_y)

            pyxel.rect(0, 0, SCREEN_W, 14, 0)
            
            time_remaining = max(0, int(self.max_game_time - self.game_timer))
            pyxel.text(4, 4, f"W: {self.current_weather.upper()}", 7)
            pyxel.text(68, 4, f"T: {time_remaining}s", 10)

            pyxel.text(102, 4, "MOOD", 13)
            pyxel.rect(130, 4, 26, 6, 0)
            fill_w = int((self.mood / 100.0) * 24)
            bar_col = 11 if self.mood > 30 else 8
            pyxel.rect(131, 5, fill_w, 4, bar_col)

            if self.state == "WIN":
                pyxel.rect(20, 35, 120, 50, 0)
                pyxel.rectb(20, 35, 120, 50, 11)
                pyxel.text(54, 48, "YOU WIN!", 11)
                pyxel.text(32, 60, "Town survived 90s!", 7)
                pyxel.text(30, 72, "PRESS SPACE TO RESTART", 9)

            elif self.state == "LOSE":
                pyxel.rect(20, 35, 120, 50, 0)
                pyxel.rectb(20, 35, 120, 50, 8)
                pyxel.text(48, 48, "GAME OVER", 8)
                pyxel.text(36, 60, "Mood hit limit!", 7)
                pyxel.text(30, 72, "PRESS SPACE TO RESTART", 9)


if __name__ == "__main__":
    PixelWeatherStation()