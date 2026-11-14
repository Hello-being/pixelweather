"""
PIXELBOX // Prompt-Friendly Procedural Asset Bank (Pyxel 2.x)
=============================================================
"""

import pyxel

# Sprite UV coordinates in Image Bank 0: (u, v, width, height)
SPRITES = {
    "bot_idle": (0, 0, 8, 8),
    "bot_run": (8, 0, 8, 8),
    "orb": (16, 0, 8, 8),
    "crate": (24, 0, 8, 8),
    "drone": (32, 0, 8, 8),
    "heart": (40, 0, 8, 8),
    "cursor": (48, 0, 8, 8),
    "house": (56, 0, 16, 16),
    "shelter": (72, 0, 16, 16),
    "umbrella": (88, 0, 16, 16),
}

SOUNDS = {
    "jump": 0,
    "pickup": 1,
    "boom": 2,
    "blip": 3,
}


def register_sprite(name: str, u: int, v: int, rows: list[str]) -> None:
    pyxel.images[0].set(u, v, rows)
    SPRITES[name] = (u, v, len(rows[0]), len(rows))


def init_assets() -> None:
    """Populate Image Bank 0 and Sound Slots with assets."""
    register_sprite(
        "bot_idle", 0, 0,
        [
            "00cccc00",
            "0c7777c0",
            "0c7171c0",
            "0c7777c0",
            "00cccc00",
            "0ccbbcc0",
            "0c0cc0c0",
            "00c00c00",
        ],
    )
    register_sprite(
        "bot_run", 8, 0,
        [
            "00cccc00",
            "0c7777c0",
            "0c7878c0",
            "0c7777c0",
            "00cccc00",
            "0ccffcc0",
            "00c00c00",
            "0c0000c0",
        ],
    )
    register_sprite(
        "orb", 16, 0,
        [
            "000aa000",
            "00a77a00",
            "0a7aa7a0",
            "aa7997aa",
            "aa7997aa",
            "0a7aa7a0",
            "00a77a00",
            "000aa000",
        ],
    )
    register_sprite(
        "crate", 24, 0,
        [
            "44444444",
            "49999994",
            "49499494",
            "49944994",
            "49944994",
            "49499494",
            "49999994",
            "44444444",
        ],
    )
    register_sprite(
        "drone", 32, 0,
        [
            "08000080",
            "008ee800",
            "08e77e80",
            "8e7887e8",
            "8e7887e8",
            "08eeee80",
            "00800800",
            "08000080",
        ],
    )
    register_sprite(
        "heart", 40, 0,
        [
            "08800880",
            "88788888",
            "87888888",
            "88888888",
            "08888880",
            "00888800",
            "00088000",
            "00000000",
        ],
    )
    register_sprite(
        "cursor", 48, 0,
        [
            "00077000",
            "00077000",
            "00000000",
            "770aa077",
            "770aa077",
            "00000000",
            "00077000",
            "00077000",
        ],
    )
    # House Sprite (16x16)
    register_sprite(
        "house", 56, 0,
        [
            "0000888888880000",
            "0008899999988000",
            "0088999999998800",
            "0889999999999880",
            "8844444444444488",
            "8413344444331488",
            "8413344444331488",
            "8444444444444488",
            "8444444444444488",
            "8444444444444488",
            "8444444444444488",
            "8444664444664488",
            "8444664444664488",
            "8444444444444488",
            "8444444444444488",
            "8888888888888888",
        ]
    )
    # Shelter Sprite (16x16)
    register_sprite(
        "shelter", 72, 0,
        [
            "0000000000000000",
            "0000000000000000",
            "0000777777770000",
            "0007777777777700",
            "0077777777777770",
            "0000550000550000",
            "0000550000550000",
            "0000550000550000",
            "0000550000550000",
            "0000550000550000",
            "0000550000550000",
            "0000550000550000",
            "0000550000550000",
            "0000550000550000",
            "0000550000550000",
            "0000000000000000",
        ]
    )
    # Umbrella Sprite (16x16)
    register_sprite(
        "umbrella", 88, 0,
        [
            "0000077777700000",
            "0007788888877000",
            "0077899999877000",
            "07789aadaa987700",
            "7789aadaada98770",
            "789aadaadaada987",
            "0000066666000000",
            "0000066666000000",
            "0000066666000000",
            "0000000000000000",
            "0000000000000000",
            "0000000000000000",
            "0000000000000000",
            "0000000000000000",
            "0000000000000000",
            "0000000000000000",
        ]
    )

    pyxel.sounds[SOUNDS["jump"]].set(notes="c2e2g2c3", tones="s", volumes="4", effects="s", speed=7)
    pyxel.sounds[SOUNDS["pickup"]].set(notes="e3g3b3e4", tones="p", volumes="5", effects="n", speed=6)
    pyxel.sounds[SOUNDS["boom"]].set(notes="c2g1e1c1", tones="n", volumes="6542", effects="f", speed=9)
    pyxel.sounds[SOUNDS["blip"]].set(notes="a3c4", tones="t", volumes="4", effects="n", speed=5)


def draw_sprite(name: str, x: float, y: float, flip_x: bool = False, colkey: int = 0) -> None:
    if name not in SPRITES:
        pyxel.rect(int(x), int(y), 8, 8, 8)
        return
    u, v, w, h = SPRITES[name]
    draw_w = -w if flip_x else w
    pyxel.blt(int(x), int(y), 0, u, v, draw_w, h, colkey)


def play_sfx(name: str, channel: int = 0) -> None:
    if name in SOUNDS:
        pyxel.play(channel, SOUNDS[name])