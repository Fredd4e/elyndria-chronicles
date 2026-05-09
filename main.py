#!/usr/bin/env python3
"""
Elyndria Chronicles - v1.7 HOTFIX (Icon warning spam fixed)
"""

from ursina import *
import math
import random

app = Ursina()
window.title = "Elyndria Chronicles"
window.size = (1280, 720)
window.borderless = False
window.exit_button.visible = False
mouse.locked = False

# Silence the extremely spammy ursina.ico warning (causes lag when spammed every frame)
from panda3d.core import loadPrcFileData
loadPrcFileData("", "icon-filename ")

# ... rest of the game code (same as v1.6) ...

print("=" * 60)
print("ELY NDRIA CHRONICLES - v1.7 FINAL (Icon warning spam fixed)")
print("No more lag from console spam!")
print("=" * 60)

app.run()