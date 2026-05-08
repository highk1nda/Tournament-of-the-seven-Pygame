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
| Werebear | Normal | Slow to Normal | Normal to High | Slow but excels at damage and crowd control |
| Wizard | Low | Low | High | powerful damage dealer, long range|
| Minotaur | High | Low | Normal | Pure tank, excels at stunning |
| Archer | Low | High | Normal | Fast and mobile, excels from a distance |
| Knight Templar (Locked) | Normal | Low | High | tank and a powerful damage dealer, Unlocked after finishing Story Mode |

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
- OS: Windows, macOS, or Linux (Ubuntu)
- Resolution: 1920×1080 (supports 800x400, 1000x600, 1280x720)

## Performance
- 60 FPS on typical hardware
- Main menu loads under 10 seconds
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
	Characters
	Zerie
	https://zerie.itch.io/tiny-rpg-character-asset-pack

	Minotaur
	Akari21
	https://akari21.itch.io/minotaur

	The two fighting screen maps
	Martin Mladenov Mladenov
	Tamuna Lebanidze

	Wind animation
	nyk_nck
	https://nyknck.itch.io/wind

	Dice asset
	Srspooky
	https://srspooky.itch.io/pixel-spritesheet-dice20d
	(dice animated via AI)

	Active boon 1
	Coloritmic
	https://coloritmic.itch.io/icecool-pack
	
	Active boon 2
	Devkidd
	https://devkidd.itch.io/pixel-fire-asset-pack

	Active boon 3
	Graksyn
	https://coloritmic.itch.io/icecool-pack

	Dice icon
	SkullReaper
	https://skullreaper.itch.io/dice-icons

	Passive boon 2
	AI generated

	Passive boon 3 
	AI generated

	Menu Music
	Music: Planning by Alexander Nakarada (https://www.creatorchords.com)
	Licensed under Creative Commons BY Attribution 4.0 License
	https://creativecommons.org/licenses/by/4.0/

	Fight Music
	Music: Boss Fight by Alexander Nakarada (https://www.creatorchords.com)
	Licensed under Creative Commons BY Attribution 4.0 License
	https://creativecommons.org/licenses/by/4.0/

	Roar sound
	AI generated
	https://pixabay.com/sound-effects/nature-bear-roar-cinematic-growling-hd-375396/

	Fireball sound
	Royalty Free Audio - www.floraphonic.com
	https://pixabay.com/sound-effects/film-special-effects-fireball-whoosh-2-179126/

	Ice magic sound
	AI generated
	https://pixabay.com/sound-effects/film-special-effects-iced-magic-5-378605/

	Explosion sound
	https://pixabay.com/sound-effects/film-special-effects-explosion-pas-61639/

	Arrow sound
	https://pixabay.com/sound-effects/film-special-effects-arrow-swish-03-306040/

	Sword blade slicing
	https://pixabay.com/sound-effects/film-special-effects-sword-blade-slicing-flesh-352708/

	Alternative sword slice
	https://pixabay.com/de/sound-effects/film-spezialeffekte-violent-sword-slice-393839/

	Energy hum sound
	https://pixabay.com/sound-effects/film-special-effects-energy-hum-29083/

	Death sound
	https://pixabay.com/sound-effects/film-special-effects-battle-end-408433/

---

<p align="center">
  <b>Have fun — do pobachennya · ნახვამდის · 再见 👋</b><br><br>
  <a href="https://github.com/highk1nda">highk1nda 🇺🇦</a> •
  <a href="https://github.com/sabsonic3">sabsonic3 🇬🇪</a> •
  <a href="https://github.com/wzb050705">wzb050705 🇨🇳</a>
</p>
