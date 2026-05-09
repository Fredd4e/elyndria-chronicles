# Elyndria Chronicles

**A breathtaking third-person 3D RPG built entirely in Python with the Ursina engine.**

Inspired by World of Warcraft's iconic camera and movement system, this game features a stunning open world, deeply detailed characters, rich lore, magic, sword & shield combat, and heartfelt interactions with two captivating female NPCs.

## 🌟 Features

- **WoW-Style Orbit Camera & Movement**: Hold Right Mouse Button to freely orbit the camera around your character. Mouse wheel to zoom. WASD movement is directional — you walk *toward the camera's facing direction* with smooth turning. Jump with Space.
- **Detailed Player Character**: Fully modeled knight "Kael Voss" with layered armor, flowing cloak, glowing Dawnbreaker sword, and Eternal Ward shield. Every piece hand-crafted from primitives for maximum detail.
- **Two Voluptuous Female NPCs**:
  - **Elara the Grove Warden** — Elegant elven sorceress with silver flowing hair, emerald robes that accentuate her curvaceous figure, and a radiant staff.
  - **Lirael Ironheart** — Fierce amazonian shieldmaiden with fiery red hair, ornate battle armor hugging her powerful yet feminine form, and a massive battle axe.
- **Immersive Lore & Dialogue**: Press **E** when near an NPC to hear beautiful, multi-page stories about the world, the Void Emperor, ancient prophecies, and personal tales. Fully voiced in text with rich flavor.
- **Character Equipment Panel**: Press **C** to open a detailed character sheet showing stats (Health, Mana, XP, Strength, Agility, Intellect), level, and all equipped gear slots (Head, Chest, Weapon, Offhand, etc.).
- **Magic & Combat**: Left-click to swing your legendary sword with visual slash effects. Press **Q** to unleash Aether magic fireballs that streak across the battlefield.
- **Vast Beautiful World**: Expansive 200x200 meadow with dense forests of detailed trees, sparkling lakes, ancient ruins, glowing flora, dynamic lighting, fog, and a majestic sky. Every detail crafted for immersion.
- **Beautiful Graphics**: Custom lighting (sun + ambient), atmospheric fog, smooth animations, particle-like effects for spells, and carefully chosen color palettes for a magical fantasy feel.

## 🚀 Easy Launcher (Recommended for Updates)

After the **first clone**, you never have to open a terminal again!

1. Double-click **`launcher.bat`** (included in the repo)
2. It will automatically:
   - `git pull` the latest version
   - Install/update `requirements.txt`
   - Launch the game

Perfect for staying up to date with new features, bug fixes, or content additions.

## 📜 The Lore of Elyndria

Long ago, the twin goddesses **Aethera** (light) and **Nyxara** (shadow) wove the world of **Elyndria** from pure cosmic threads. For millennia, harmony reigned. Then the **Void Emperor** — an ancient horror from beyond the stars — shattered the **Great Veil**, flooding the land with corrupting darkness.

You are **Kael Voss**, the last living **Aether Knight**, awakened from a 300-year magical slumber by a prophetic vision. You carry **Dawnbreaker**, the star-forged sword, and **Eternal Ward**, the shield that once sealed the Veil. With the **Spark of Aether** burning in your veins, you must gather the shattered relics, rally the last guardians, and restore the Veil before Elyndria is consumed forever.

The two women who will stand by your side:

- **Elara Voss** (your distant blood-kin and Grove Warden): Guardian of the last pure forests. Her magic can mend the land itself.
- **Lirael Ironheart** (legendary Shieldmaiden): Once led the charge against the first Void incursion. Her axe and shield have tasted more voidspawn blood than any mortal.

Together, you will face horrors, uncover ancient truths, and perhaps... find more than just victory in the coming storm.

## 🎮 Controls

| Key / Mouse          | Action                          |
|----------------------|---------------------------------|
| **W A S D**          | Move (directional, camera-relative) |
| **Right Mouse Hold** | Orbit camera around character   |
| **Mouse Wheel**      | Zoom in/out                     |
| **Space**            | Jump (demo)                     |
| **Left Mouse Click** | Sword attack (slash effect)     |
| **Q**                | Cast Aether Fireball            |
| **E**                | Interact with nearby NPC        |
| **C**                | Open / Close Character Panel    |
| **Esc**              | Quit game                       |

## 🛠️ How to Run (First Time)

1. Clone the repo: `git clone https://github.com/Fredd4e/elyndria-chronicles.git`
2. `cd elyndria-chronicles`
3. Double-click `launcher.bat` (it handles everything)

Or manually:
```bash
pip install -r requirements.txt
python main.py
```

## 🛠️ Technical Notes

- Built with **Ursina (Panda3D backend)** for pure Python 3D.
- All models are **procedurally detailed** using layered primitives (cylinders, spheres, planes, cones) — no external assets required.
- Fully self-contained single-file game (main.py + launcher.bat).
- Smooth 60+ FPS on modest hardware.
- Extensible: Easy to add quests, enemies, more spells, inventory, etc.

This project was created with love for classic MMORPG aesthetics and storytelling. Enjoy your adventure in Elyndria!

*May the light of Aethera guide your blade.*

---

**Created for the love of beautiful worlds and unforgettable characters.** 

If you enjoy it, star the repo and share your screenshots of the NPCs or epic moments!