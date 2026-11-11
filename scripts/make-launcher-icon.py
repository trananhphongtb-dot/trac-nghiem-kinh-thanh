#!/usr/bin/env python3
"""Build the real Android launcher icon for Bible Quiz.

Why this script exists (root cause, found 2026-11-09):
Android 8+ ignores the legacy mipmap-*/ic_launcher.png and uses the ADAPTIVE
icon instead: res/mipmap-anydpi-v26/ic_launcher.xml, whose foreground is
@mipmap/ic_launcher_foreground and whose background is
@color/ic_launcher_background. The old workflow only replaced ic_launcher.png,
so the shipped APK still showed Capacitor's default robot foreground (white
centre pixel) on a white background. This script replaces the FOREGROUND in
every density, sets the background to dark navy, and deletes the default
robot vector foreground.

Run after `npx cap add android` + `npx cap sync android`:
    python3 scripts/make-launcher-icon.py [android-res-dir]

Defaults: icon source = assets/icon.png (repo root),
res dir = android/app/src/main/res (repo root).
"""
import os
import sys

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ICON = os.path.join(ROOT, "assets", "icon.png")
RES = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
    ROOT, "android", "app", "src", "main", "res")

# (density, legacy icon px, adaptive foreground canvas px)
DENSITIES = [
    ("mdpi", 48, 108),
    ("hdpi", 72, 162),
    ("xhdpi", 96, 216),
    ("xxhdpi", 144, 324),
    ("xxxhdpi", 192, 432),
]
BG_COLOR = "#1a2340"  # deep navy, Bible Quiz theme
FG_FRACTION = 0.76    # icon size inside the 108dp adaptive canvas (safe zone)


def main():
    icon = Image.open(ICON).convert("RGBA")
    for density, legacy_px, fg_px in DENSITIES:
        d = os.path.join(RES, "mipmap-" + density)
        os.makedirs(d, exist_ok=True)
        # Legacy icon (used pre-Android 8): full icon, scaled.
        legacy = icon.resize((legacy_px, legacy_px), Image.LANCZOS)
        legacy.save(os.path.join(d, "ic_launcher.png"))
        legacy.save(os.path.join(d, "ic_launcher_round.png"))
        # Adaptive foreground: icon centred at 76% on a transparent canvas,
        # so the launcher mask never crops the gold rim.
        fg = Image.new("RGBA", (fg_px, fg_px), (0, 0, 0, 0))
        size = round(fg_px * FG_FRACTION)
        small = icon.resize((size, size), Image.LANCZOS)
        fg.paste(small, ((fg_px - size) // 2, (fg_px - size) // 2), small)
        fg.save(os.path.join(d, "ic_launcher_foreground.png"))
    # Adaptive background: solid dark navy (was #FFFFFF).
    values = os.path.join(RES, "values")
    os.makedirs(values, exist_ok=True)
    with open(os.path.join(values, "ic_launcher_background.xml"), "w") as f:
        f.write('<?xml version="1.0" encoding="utf-8"?>\n<resources>\n'
                '    <color name="ic_launcher_background">%s</color>\n</resources>\n'
                % BG_COLOR)
    # Delete Capacitor's default robot foreground vector + teal background
    # vector, so nothing default can resurface.
    for rel in ("drawable-v24/ic_launcher_foreground.xml",
                "drawable/ic_launcher_background.xml"):
        p = os.path.join(RES, rel)
        if os.path.exists(p):
            os.remove(p)
            print("removed", rel)
    print("launcher icon built from", ICON, "->", RES)


if __name__ == "__main__":
    main()
