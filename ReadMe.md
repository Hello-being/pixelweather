# Pixel Weather Station

A one-screen weather survival game built with [Pyxel](https://github.com/kitao/pyxel). Keep a small town's mood meter between 0 and 100 for 90 seconds while the weather changes around you.

**Demo video:** (https://drive.google.com/file/d/1rWpQyJJD1XOVh8_Gn84pyZT684jGcG4F/view?usp=sharing)

## Screenshots

![Title screen](screenshots/title.png)
![Gameplay](screenshots/gameplay.png)
![Win or lose screen](screenshots/end.png)

## Overview

The town sits along the bottom of the screen. Every 5 to 8 seconds the weather changes at random between four types:

- **Sunny:** Slowly raises mood.
- **Rain:** Lowers mood unless your umbrella is up.
- **Wind:** Lowers mood unless your shelter is covering the houses.
- **Lightning:** Causes a sudden mood drop and a white screen flash.

**Win:** Survive 90 seconds with the mood meter never reaching 0 or 100.
**Lose:** The mood meter hits 0 or 100.

## Controls

| Key | Action |
| :--- | :--- |
| Left / Right arrows or A / D | Move the shelter |
| SPACE | Raise the umbrella for 3 seconds (5-second cooldown). On the title or end screens, starts or restarts the game |
| R | Restart |
| ESC | Quit |

## How to Run

Requires **Python 3.10 or newer**.

```bash
pip install -r requirements.txt
python main.py
```

On Windows, use `py` in place of `python` if needed.

## Project Structure

```text
pixel_weather_station/
├── main.py            # Game states, weather, mood logic, drawing
├── engine.py          # Particles, floating text, camera shake and flash
├── assets.py          # Pixel sprites and sound effects
├── requirements.txt   # Pyxel dependency
└── README.md
```

## Built With

- Python 3
- Pyxel 2.x (standard library only otherwise)

## PromptCraft

[Replace this section with your own notes. Judges look for specific prompts, what the AI got right, and what you changed by hand.]

**Starting prompt:** [Paste the main prompt you used to generate the first version.]

**Iterations:**
1. [Prompt you used to fix or change something, and what happened.]
2. [Next prompt, such as adding particles, fixing the umbrella cooldown, or adjusting balance.]
3. [Next prompt.]

**What worked:** [For example, asking for the full file in one piece made it easier to paste back in.]

**What didn't work:** [For example, the first output was cut off partway through, so I had to ask again for the complete file.]

**What I changed by hand:** [For example, tuned the mood rates so the game lasts longer, or changed the weather timing.]

**Creative choices:** [Explain why you picked this idea and how you pushed it beyond the starter code.]