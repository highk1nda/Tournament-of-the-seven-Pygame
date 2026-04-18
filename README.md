# Mythological 2D Fighting Game

A simple 2D fighting game made with Python and pygame. You choose a fighter, fight in arenas, and try to win without getting knocked out right away.


<p align="center">
  <img src="assets/gameplay.gif" alt="Howdy? Yet another easter egg">
</p>

---

## Game Modes

**Story Mode** : Fight CPU enemies in two arenas. If you win, you unlock the Knight Templar.
**Singleplayer** :  Choose an opponent and fight the CPU.
**Multiplayer** : Play 1v1 with a friend on the same keyboard.

All modes are best of three. A round ends when someone’s health hits zero (death) or the 90-second timer ends.


---

## Characters

| Character | Health | Speed | Damage | Notes |
|-----------|--------|-------|--------|-------|
| Knight | Normal | Normal | Normal | Good at everything |
| Werebear | Normal | Slow to Normal | Normal to High | Gets stronger below 40% HP |
| Wizard | Low | Low | High | Slowly regens HP up to 60% |
| Minotaur | High | Low | Normal | Pure tank |
| Archer | Low | High | Normal | Fast and mobile |
| Knight Templar (Locked) | Normal | Low | High | Unlocked after finishing Story Mode |

---

## Boon System

Before each fight, both players pick THREE active and THREE passive boon.

* **Active boons** :  you use them yourself, and they have a cooldown bar at the bottom.
* **Passive boons** : activate automatically when something happens, for instance - losing a round.

---

## Controls

| Action | Player 1 | Player 2 |
|--------|----------|----------|
| Move | `A` / `D` | `←` / `→` |
| Jump | `W` | `↑` |
| Block (crouch) | `S` | `↓` |
| Attacks | R, F, V | >, ?, SHIFT |

---

## How to launch?

**Requirements:** Python 3.x and pygame.

```bash
pip install pygame
python main.py
```
## System Requirements

- **OS:** Windows, macOS, or Linux (Ubuntu)
- **Resolution:** 1920×1080 by default (more supported resolutions are comming)
- **Performance:** 60+ FPS on typical hardware
- **Load time:** Should load main menu in under 10 seconds
---

## Project Structure

```
/
├── assets/
│   ├── Tiny RPG Character Asset Pack/
│   │   ├── Characters(100x100)/
│   │   ├── Arrow(Projectile)/
│   │   ├── Magic(Projectile)/
│   │   └── Aseprite file/
│   ├── sfx/
│   ├── forest.jpg
│   └── gameplay.gif
├── src/modules/
│   ├── Screens/
│   │   ├── FightScreen.py
│   │   ├── Help.py
│   │   └── MainMenu.py
│   ├── UI/
│   │   ├── Button.py
│   │   └── constants.py
│   ├── fighter/
│   │   ├── Fighter.py
│   │   └── render.py
│   ├── sfx/
│   │   └── sound_loader.py
│   └── systems/
│       └── Draw.py
├── tests/
│   └── test.py
├── main.py
└── README.md
```
---

## Team

| Name | GitHub |
|------|--------|
| Saba Sturua | sabsonic3 |
| Zibo Wang | wzb050705 |
| Anton Satsuk | highk1nda |

---

## Asset Credits

Character sprites: [Tiny RPG Character Asset Pack](https://www.example.com)
Minotaur sprite: [Introducing One Dollar Monsters #1: The Minotaur!](https://akari21.itch.io/minotaur)
Wind animation: [Wind - Pixel Art](https://nyknck.itch.io/wind)

---

<p align="center">
  <b>Have fun — do pobachennya · ნახვამდის · 再见 👋</b><br><br>
  <a href="https://github.com/highk1nda">highk1nda 🇺🇦</a> •
  <a href="https://github.com/sabsonic3">sabsonic3 🇬🇪</a> •
  <a href="https://github.com/wzb050705">wzb050705 🇨🇳</a>
</p>
