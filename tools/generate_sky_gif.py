#!/usr/bin/env python3
"""
Generate assets/main_menu_sky.gif — animated night sky background for the main menu.
Design source: Night Sky Background.html (claude.ai/design handoff)
Run once from the project root: python3 tools/generate_sky_gif.py
"""

import math
import sys
import numpy as np
from PIL import Image

# ── Output settings ──────────────────────────────────────────────────────────
W, H       = 480, 270       # rendered at quarter-res; pygame scales to 1920×1080
FRAMES     = 60             # 6-second loop at 10 fps
FRAME_MS   = 100            # ms per frame
OUT_PATH   = "assets/main_menu_sky.gif"

# ── Design constants (from 1920×1080 source, scaled to 480×270) ──────────────
SC         = W / 1920.0     # 0.25
CX, CY     = W // 2, H // 2
CLEAR_RX   = 460 * SC      # elliptical calm zone in center
CLEAR_RY   = 240 * SC
BG_COLOR   = np.array([2, 2, 9], dtype=np.uint8)

DRIFT_PX   = [0.025 * 6, 0.055 * 6, 0.1 * 6]   # px/frame at 10 fps (scaled from 60 fps)

STAR_COUNT = 260

# ── Seeded RNG — mulberry32(0xCAFEBABE), matches design JS exactly ───────────
def _make_rng(seed):
    state = [seed & 0xFFFFFFFF]
    def nxt():
        s = state[0]
        s = (s + 0x6D2B79F5) & 0xFFFFFFFF
        t = (s ^ (s >> 15)) & 0xFFFFFFFF
        t = (t * ((1 | s) & 0xFFFFFFFF)) & 0xFFFFFFFF
        t = (t ^ (t >> 7)) & 0xFFFFFFFF
        t = (t * ((61 | t) & 0xFFFFFFFF)) & 0xFFFFFFFF
        t = (t ^ (t >> 14)) & 0xFFFFFFFF
        state[0] = s
        return t / 4294967296.0
    return nxt

rng = _make_rng(0xCAFEBABE)

# ── Star generation ───────────────────────────────────────────────────────────
def _in_center(x, y):
    nx = (x - CX) / CLEAR_RX
    ny = (y - CY) / CLEAR_RY
    return nx * nx + ny * ny < 1

def make_stars():
    stars = []
    attempts = 0
    while len(stars) < STAR_COUNT and attempts < 30_000:
        attempts += 1
        x = rng() * W
        y = rng() * H
        if _in_center(x, y) and rng() > 0.15:
            continue

        # layer: 0=far, 1=mid, 2=near  (two rng calls if not layer 0)
        lr = rng()
        if lr < 0.45:
            layer = 0
        else:
            layer = 1 if rng() < 0.6 else 2

        r = rng()
        if layer == 0:
            t = 0 if r < 0.50 else (1 if r < 0.85 else 2)
        elif layer == 1:
            t = 0 if r < 0.25 else (1 if r < 0.60 else (2 if r < 0.88 else 3))
        else:
            t = 0 if r < 0.10 else (1 if r < 0.35 else (2 if r < 0.65 else 3))

        stars.append({
            "x": x, "y": y, "layer": layer, "type": t,
            "violet":     rng() < 0.62,
            "phase":      rng() * math.pi * 2,
            "speed":      0.35 + rng() * 1.1,
            "amp":        0.18 + rng() * 0.42,
            "base_alpha": 0.7  + rng() * 0.3,
        })
    return stars

STARS = make_stars()

# ── Drawing helpers ───────────────────────────────────────────────────────────
def _blend(arr, x1, y1, x2, y2, color, alpha):
    """Alpha-blend a rectangle onto arr (numpy uint8 H×W×3)."""
    x1, y1 = max(0, x1), max(0, y1)
    x2, y2 = min(W, x2), min(H, y2)
    if x1 >= x2 or y1 >= y2:
        return
    a = float(np.clip(alpha, 0, 1))
    c = np.array(color, dtype=np.float32)
    region = arr[y1:y2, x1:x2].astype(np.float32)
    arr[y1:y2, x1:x2] = np.clip(region + (c - region) * a, 0, 255).astype(np.uint8)

def _glow(arr, cx, cy, radius, color, max_alpha):
    """Radial gradient glow centred at (cx, cy)."""
    xi, yi = int(round(cx)), int(round(cy))
    r = int(math.ceil(radius))
    x1, x2 = max(0, xi - r), min(W, xi + r + 1)
    y1, y2 = max(0, yi - r), min(H, yi + r + 1)
    if x1 >= x2 or y1 >= y2:
        return
    yy, xx = np.mgrid[y1:y2, x1:x2]
    dist = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2)
    a3d = (np.clip(1.0 - dist / radius, 0, 1) * max_alpha).clip(0, 1)[:, :, np.newaxis]
    c = np.array(color, dtype=np.float32)
    region = arr[y1:y2, x1:x2].astype(np.float32)
    arr[y1:y2, x1:x2] = np.clip(region + (c - region) * a3d, 0, 255).astype(np.uint8)

def draw_star(arr, sx, sy, star_type, violet, alpha):
    px, py = int(round(sx)), int(round(sy))
    a = float(np.clip(alpha, 0, 1))
    WHITE  = (255, 255, 255)
    ARM    = (160, 110, 230) if violet else (200, 190, 255)

    if star_type == 0:
        _blend(arr, px - 1, py - 1, px + 2, py + 2, WHITE, a)
        return

    if star_type == 1:
        _glow(arr,  sx, sy, 3, ARM, a * 0.30)
        _blend(arr, px - 1, py - 1, px + 2, py + 2, WHITE, a)
        _blend(arr, px - 2, py,     px,     py + 1,  WHITE, a * 0.9)
        _blend(arr, px + 1, py,     px + 3, py + 1,  WHITE, a * 0.9)
        _blend(arr, px,     py - 2, px + 1, py,      WHITE, a * 0.9)
        _blend(arr, px,     py + 1, px + 1, py + 3,  WHITE, a * 0.9)
        _blend(arr, px - 3, py,     px - 2, py + 1,  ARM,   a * 0.55)
        _blend(arr, px + 2, py,     px + 3, py + 1,  ARM,   a * 0.55)
        _blend(arr, px,     py - 3, px + 1, py - 2,  ARM,   a * 0.55)
        _blend(arr, px,     py + 2, px + 1, py + 3,  ARM,   a * 0.55)
        return

    if star_type == 2:
        _glow(arr,  sx, sy, 5, ARM, a * 0.35)
        _blend(arr, px - 1, py - 1, px + 3, py + 3, WHITE, a)
        _blend(arr, px - 3, py,     px - 1, py + 1,  WHITE, a * 0.9)
        _blend(arr, px + 2, py,     px + 4, py + 1,  WHITE, a * 0.9)
        _blend(arr, px,     py - 3, px + 1, py - 1,  WHITE, a * 0.9)
        _blend(arr, px,     py + 2, px + 1, py + 4,  WHITE, a * 0.9)
        _blend(arr, px - 4, py,     px - 3, py + 1,  ARM,   a * 0.60)
        _blend(arr, px + 4, py,     px + 5, py + 1,  ARM,   a * 0.60)
        _blend(arr, px,     py - 4, px + 1, py - 3,  ARM,   a * 0.60)
        _blend(arr, px,     py + 4, px + 1, py + 5,  ARM,   a * 0.60)
        _blend(arr, px - 5, py,     px - 4, py + 1,  ARM,   a * 0.28)
        _blend(arr, px + 5, py,     px + 6, py + 1,  ARM,   a * 0.28)
        _blend(arr, px,     py - 5, px + 1, py - 4,  ARM,   a * 0.28)
        _blend(arr, px,     py + 5, px + 1, py + 6,  ARM,   a * 0.28)
        return

    # type 3 — large
    _glow(arr, sx, sy, 9, ARM, a * 0.45)
    _blend(arr, px - 2, py - 2, px + 3, py + 3, WHITE, a)
    _blend(arr, px - 4, py - 1, px - 2, py + 2,  WHITE, a * 0.92)
    _blend(arr, px + 2, py - 1, px + 5, py + 2,  WHITE, a * 0.92)
    _blend(arr, px - 1, py - 4, px + 2, py - 2,  WHITE, a * 0.92)
    _blend(arr, px - 1, py + 2, px + 2, py + 5,  WHITE, a * 0.92)
    _blend(arr, px - 6, py,     px - 4, py + 2,  ARM,   a * 0.65)
    _blend(arr, px + 4, py,     px + 6, py + 2,  ARM,   a * 0.65)
    _blend(arr, px,     py - 6, px + 2, py - 4,  ARM,   a * 0.65)
    _blend(arr, px,     py + 4, px + 2, py + 6,  ARM,   a * 0.65)
    _blend(arr, px - 8, py,     px - 6, py + 1,  ARM,   a * 0.30)
    _blend(arr, px + 7, py,     px + 9, py + 1,  ARM,   a * 0.30)
    _blend(arr, px,     py - 8, px + 1, py - 6,  ARM,   a * 0.30)
    _blend(arr, px,     py + 7, px + 1, py + 9,  ARM,   a * 0.30)

# ── Background (static; drawn once, composited each frame) ───────────────────
def make_background():
    arr = np.zeros((H, W, 3), dtype=np.uint8)
    arr[:] = BG_COLOR

    # Vertical gradient: darken top and bottom slightly
    yy = np.linspace(0, 1, H)
    grad = 1.0 - 0.3 * (1 - np.sin(np.pi * yy))   # brighter in the middle
    arr = (arr.astype(np.float32) * grad[:, np.newaxis, np.newaxis]).clip(0, 255).astype(np.uint8)

    # Corner vignettes — 4 radial gradients, one per corner
    yy_f, xx_f = np.mgrid[0:H, 0:W].astype(np.float32)
    # scale back to 1920×1080 space for correct radius
    xx_s = xx_f * (1920 / W)
    yy_s = yy_f * (1080 / H)
    radius = 1920 * 0.65
    for cx_c, cy_c in [(0, 0), (1920, 0), (0, 1080), (1920, 1080)]:
        dist = np.sqrt((xx_s - cx_c) ** 2 + (yy_s - cy_c) ** 2)
        t = np.clip(1.0 - dist / radius, 0, 1) ** 0.6
        dark = (t * 0.55)[:, :, np.newaxis]
        arr = np.clip(arr.astype(np.float32) * (1 - dark), 0, 255).astype(np.uint8)

    return arr

BG = make_background()

# ── Frame rendering ───────────────────────────────────────────────────────────
def render_frame(frame_idx):
    t = frame_idx * (FRAME_MS / 1000.0)   # seconds

    drift = [
        (DRIFT_PX[i] * frame_idx) % W
        for i in range(3)
    ]

    arr = BG.copy()

    for s in STARS:
        twinkle = math.sin(t * s["speed"] + s["phase"]) * 0.5 + 0.5
        alpha = s["base_alpha"] * ((1 - s["amp"]) + twinkle * s["amp"])
        if alpha < 0.03:
            continue

        dx = drift[s["layer"]]
        sx = (s["x"] + dx) % W

        draw_star(arr, sx, s["y"], s["type"], s["violet"], alpha)

        # seamless horizontal wrap ghost
        margin = 9
        if sx > W - margin:
            draw_star(arr, sx - W, s["y"], s["type"], s["violet"], alpha)
        if sx < margin:
            draw_star(arr, sx + W, s["y"], s["type"], s["violet"], alpha)

    return arr

# ── GIF export ────────────────────────────────────────────────────────────────
def main():
    print(f"Generating {FRAMES} frames at {W}×{H}…", flush=True)
    pil_frames = []
    for i in range(FRAMES):
        if i % 10 == 0:
            print(f"  frame {i}/{FRAMES}", flush=True)
        arr = render_frame(i)
        img = Image.fromarray(arr, "RGB")
        # Quantise to 256 colours with dithering for GIF
        img_p = img.quantize(colors=256, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.FLOYDSTEINBERG)
        pil_frames.append(img_p)

    print(f"Saving → {OUT_PATH}", flush=True)
    pil_frames[0].save(
        OUT_PATH,
        format="GIF",
        save_all=True,
        append_images=pil_frames[1:],
        loop=0,
        duration=FRAME_MS,
        optimize=False,
    )
    print("Done.")

if __name__ == "__main__":
    main()
