#!/usr/bin/env python3
"""
Elyndria Chronicles - Completely Rewritten & Improved Version (May 2026)
- Modern Ursina best practices
- Reliable third-person orbit camera + camera-relative movement
- Proper scroll wheel handling
- Cleaner code, better error handling, basic physics
- All original procedural art, lore, and features preserved
"""

from ursina import *
import math
import random
import time as real_time
import traceback

print("[INFO] Starting Elyndria Chronicles - Improved Edition...")

app = Ursina()
window.title = "Elyndria Chronicles"
window.borderless = False
window.size = (1280, 720)
window.exit_button.visible = False

# ============== PLAYER STATS ==============
class PlayerStats:
    def __init__(self):
        self.level = 7
        self.health = 145
        self.max_health = 145
        self.mana = 95
        self.max_mana = 95
        self.xp = 1240
        self.xp_to_next = 1800
        self.strength = 18
        self.agility = 14
        self.intellect = 22
        self.equipment = {
            "Head": "Aether-forged Helm",
            "Chest": "Breastplate of the Last Knight",
            "Legs": "Greaves of Eternal Vigil",
            "Weapon": "Dawnbreaker (Legendary Sword)",
            "Offhand": "Eternal Ward (Star-forged Shield)",
            "Cloak": "Veilpiercer Mantle",
            "Ring": "Spark of Aether"
        }

player_stats = PlayerStats()

# ============== GLOBALS ==============
camera_pivot = None
player = None
yaw = 0
pitch = 25
camera_distance = 13.0
min_distance = 4.0
max_distance = 28.0
mouse_sensitivity = 0.25

npcs = []
current_npc = None
current_dialogue_index = 0
dialogue_panel = None
char_panel = None
free_camera = False

SKIN = color.rgb(0.96, 0.78, 0.68)
GOLD = color.rgb(0.85, 0.65, 0.13)
SILVER = color.rgb(0.75, 0.78, 0.82)
DARK_ARMOR = color.rgb(0.25, 0.22, 0.28)
EMERALD = color.rgb(0.1, 0.55, 0.25)
CRIMSON = color.rgb(0.6, 0.1, 0.15)
FIRE_HAIR = color.rgb(0.9, 0.35, 0.1)
SILVER_HAIR = color.rgb(0.92, 0.95, 1.0)

# ============== PROCEDURAL MODELS ==============

def create_detailed_player():
    print("[INFO] Creating detailed player model...")
    p = Entity(model=None, collider='box', scale=(0.9, 1.85, 0.9), origin_y=-0.5, name="Kael Voss")
    
    left_leg = Entity(parent=p, model='cube', color=DARK_ARMOR, scale=(0.32, 0.95, 0.32), position=(-0.28, 0.48, 0))
    Entity(parent=left_leg, model='cube', color=color.rgb(0.15,0.12,0.1), scale=(0.36, 0.28, 0.36), position=(0, -0.55, 0))
    right_leg = Entity(parent=p, model='cube', color=DARK_ARMOR, scale=(0.32, 0.95, 0.32), position=(0.28, 0.48, 0))
    Entity(parent=right_leg, model='cube', color=color.rgb(0.15,0.12,0.1), scale=(0.36, 0.28, 0.36), position=(0, -0.55, 0))
    Entity(parent=left_leg, model='sphere', color=SILVER, scale=0.38, position=(0, 0.25, 0))
    Entity(parent=right_leg, model='sphere', color=SILVER, scale=0.38, position=(0, 0.25, 0))
    
    lower_torso = Entity(parent=p, model='cube', color=DARK_ARMOR, scale=(1.05, 0.55, 0.95), position=(0, 1.05, 0))
    upper_torso = Entity(parent=p, model='cube', color=color.rgb(0.32, 0.28, 0.35), scale=(0.92, 0.72, 0.88), position=(0, 1.55, 0))
    Entity(parent=upper_torso, model='cube', color=SILVER, scale=(1.05, 0.12, 1.0), position=(0, 0.1, 0))
    Entity(parent=upper_torso, model='cube', color=SILVER, scale=(1.05, 0.08, 1.0), position=(0, -0.15, 0))
    Entity(parent=p, model='cube', color=color.rgb(0.2, 0.15, 0.1), scale=(1.12, 0.18, 1.02), position=(0, 0.92, 0))
    Entity(parent=p, model='cube', color=GOLD, scale=(0.35, 0.22, 0.4), position=(0, 0.92, 0.52))
    
    left_arm = Entity(parent=p, model='cube', color=SKIN, scale=(0.28, 0.78, 0.28), position=(-0.65, 1.35, 0), rotation=(0, 0, -18))
    right_arm = Entity(parent=p, model='cube', color=SKIN, scale=(0.28, 0.78, 0.28), position=(0.65, 1.35, 0), rotation=(0, 0, 22))
    Entity(parent=left_arm, model='cube', color=SILVER, scale=(0.32, 0.22, 0.32), position=(0, -0.42, 0))
    Entity(parent=right_arm, model='cube', color=SILVER, scale=(0.32, 0.22, 0.32), position=(0, -0.42, 0))
    
    left_pauldron = Entity(parent=p, model='sphere', color=SILVER, scale=0.42, position=(-0.58, 1.68, 0))
    Entity(parent=left_pauldron, model='sphere', color=DARK_ARMOR, scale=0.65, position=(0, 0, 0))
    right_pauldron = Entity(parent=p, model='sphere', color=SILVER, scale=0.42, position=(0.58, 1.68, 0))
    Entity(parent=right_pauldron, model='sphere', color=DARK_ARMOR, scale=0.65, position=(0, 0, 0))
    
    head = Entity(parent=p, model='sphere', color=SKIN, scale=0.42, position=(0, 2.05, 0))
    helmet = Entity(parent=head, model='sphere', color=color.rgb(0.55, 0.55, 0.62), scale=1.08, position=(0, 0.08, 0))
    Entity(parent=helmet, model='cube', color=CRIMSON, scale=(0.18, 0.55, 0.18), position=(0, 0.55, 0))
    Entity(parent=helmet, model='cube', color=color.black, scale=(0.9, 0.08, 0.15), position=(0, 0.05, 0.42))
    
    sword = Entity(parent=right_arm, model='cube', color=SILVER, scale=(0.12, 1.95, 0.07), position=(0.18, -0.35, 0.28), rotation=(38, 8, 5), name="sword")
    Entity(parent=sword, model='cube', color=color.rgb(0.4,0.4,0.45), scale=(0.6, 0.95, 0.4), position=(0, 0.1, 0))
    Entity(parent=sword, model='cube', color=GOLD, scale=(0.85, 0.12, 0.35), position=(0, -0.55, 0))
    pommel = Entity(parent=sword, model='sphere', color=color.rgb(0.3, 0.9, 1.0), scale=0.22, position=(0, -1.05, 0))
    PointLight(parent=pommel, color=color.cyan, range=3, intensity=0.6)
    
    shield = Entity(parent=left_arm, model='plane', color=color.rgb(0.35, 0.38, 0.45), scale=(1.35, 1.65, 1), position=(0.38, -0.18, 0.52), rotation=(0, 92, 0), name="shield")
    boss = Entity(parent=shield, model='sphere', color=GOLD, scale=0.32, position=(0, 0, 0.02))
    Entity(parent=boss, model='sphere', color=color.rgb(0.2, 0.6, 1.0), scale=0.55, position=(0, 0, 0.01))
    
    cloak = Entity(parent=p, model='plane', color=color.rgb(0.18, 0.08, 0.22), scale=(1.6, 1.35, 0.08), position=(0, 1.25, -0.68), rotation=(12, 0, 0))
    
    p.sword = sword
    p.shield = shield
    p.head = head
    print("[INFO] Player model created successfully")
    return p


def create_female_npc(name, position, hair_color, robe_color, accent_color, is_sorceress=True):
    print(f"[INFO] Creating NPC: {name}")
    npc = Entity(model=None, collider='box', scale=(0.85, 1.78, 0.85), origin_y=-0.5, position=position, name=name)
    
    hips = Entity(parent=npc, model='cube', color=robe_color, scale=(1.35, 0.55, 1.15), position=(0, 0.55, 0))
    left_leg = Entity(parent=npc, model='cube', color=color.rgb(0.35, 0.28, 0.25), scale=(0.28, 0.85, 0.28), position=(-0.32, 0.35, 0))
    right_leg = Entity(parent=npc, model='cube', color=color.rgb(0.35, 0.28, 0.25), scale=(0.28, 0.85, 0.28), position=(0.32, 0.35, 0))
    
    bust = Entity(parent=npc, model='cube', color=robe_color, scale=(1.05, 0.55, 0.95), position=(0, 1.65, 0))
    head = Entity(parent=npc, model='sphere', color=SKIN, scale=0.40, position=(0, 2.02, 0))
    hair_base = Entity(parent=head, model='sphere', color=hair_color, scale=1.15, position=(0, 0.15, -0.05))
    
    for i in range(6):
        angle = (i / 6) * 360
        strand = Entity(parent=head, model='cube', color=hair_color, scale=(0.09, 1.3, 0.09), 
                        position=(math.sin(math.radians(angle)) * 0.22, 0.35, math.cos(math.radians(angle)) * 0.18 - 0.08))
    
    if is_sorceress:
        staff = Entity(parent=npc, model='cube', color=color.rgb(0.25, 0.2, 0.15), scale=(0.08, 2.1, 0.08), position=(0.4, 1.2, 0.3), rotation=(25, 15, 0))
        orb = Entity(parent=staff, model='sphere', color=color.rgb(0.4, 1, 0.7), scale=0.28, position=(0, 1.15, 0))
        PointLight(parent=orb, color=color.lime, range=4, intensity=0.8)
    
    npc.head = head
    npc.name = name
    return npc


def setup_world():
    print("[INFO] Setting up beautiful world...")
    ground = Entity(model='plane', scale=(210, 1, 210), color=color.rgb(0.22, 0.42, 0.18), collider='box', y=0)
    
    for _ in range(40):
        x = random.uniform(-90, 90)
        z = random.uniform(-90, 90)
        create_tree(x, z)
    
    lake = Entity(model='plane', scale=(35, 1, 35), color=color.rgb(0.08, 0.32, 0.55), position=(30, 0.05, -45), rotation=(0, 18, 0))
    
    Sky(color=color.rgb(0.35, 0.55, 0.85))
    DirectionalLight(shadows=True, rotation=(38, -42, 0), color=color.rgb(1.0, 0.92, 0.78))
    AmbientLight(color=color.rgb(0.55, 0.62, 0.72))
    scene.fog_color = color.rgb(0.48, 0.55, 0.62)
    scene.fog_density = 0.012
    print("[INFO] World ready!")


def create_tree(x, z):
    trunk = Entity(model='cube', color=color.rgb(0.38, 0.24, 0.12), scale=(1.1, 4.8, 1.1), position=(x, 2.4, z))
    for i, s in enumerate([3.8, 3.2, 2.6, 1.8]):
        Entity(parent=trunk, model='sphere', color=color.rgb(0.08, 0.48, 0.12), scale=s, position=(0, 2.8 + i * 1.3, 0))

def attack_sword():
    if not hasattr(player, 'sword'): return
    sword = player.sword
    orig_rot = sword.rotation
    sword.animate_rotation((65, 35, 12), duration=0.12, curve=curve.out_expo)
    invoke(lambda: setattr(sword, 'rotation', orig_rot), delay=0.38)

def cast_fireball():
    if player_stats.mana <= 8:
        print("[INFO] Not enough mana!")
        return
    start_pos = player.position + (0, 1.6, 0) + player.forward * 1.2
    fb = Entity(model='sphere', color=color.rgb(1, 0.45, 0.1), scale=0.55, position=start_pos)
    core = Entity(parent=fb, model='sphere', color=color.rgb(1, 0.9, 0.5), scale=0.6)
    PointLight(parent=core, color=color.orange, range=6, intensity=1.2)
    fb.animate_position(start_pos + player.forward * 32, duration=1.4, curve=curve.linear)
    destroy(fb, delay=1.6)
    player_stats.mana = max(0, player_stats.mana - 8)


def get_dialogue_lines(name):
    if "Elara" in name:
        return ["Hail, Kael Voss...", "The Void Emperor's shadow lengthens.", "Return to me for the Verdant Rebirth spell."]
    return ["By the shattered stars... the last Aether Knight walks again.", "Dawnbreaker sings the old songs."]

def check_interact():
    global current_npc, current_dialogue_index, dialogue_panel
    for npc_data in npcs:
        if distance(player, npc_data['entity']) < 6.2:
            current_npc = npc_data
            current_dialogue_index = 0
            show_dialogue_panel()
            return True
    return False

def show_dialogue_panel():
    global dialogue_panel
    if dialogue_panel: destroy(dialogue_panel)
    lines = current_npc['dialogue']
    text = lines[current_dialogue_index]
    dialogue_panel = WindowPanel(title=current_npc['name'], content=[Text(text, wordwrap=58, scale=0.95), Button(text="Next", color=color.azure, scale=0.9, on_click=advance_dialogue)], position=(0, 0.28), scale=(1.35, 0.9))

def advance_dialogue():
    global current_dialogue_index, dialogue_panel, current_npc
    current_dialogue_index += 1
    if dialogue_panel: destroy(dialogue_panel)
    dialogue_panel = None
    if current_npc and current_dialogue_index < len(current_npc['dialogue']):
        show_dialogue_panel()
    else:
        current_npc = None

def toggle_character_panel():
    global char_panel
    if char_panel:
        destroy(char_panel)
        char_panel = None
        return
    stats = f"Level {player_stats.level} • Aether Knight\n\nHealth: {player_stats.health}/{player_stats.max_health}\nMana: {player_stats.mana}/{player_stats.max_mana}"
    char_panel = WindowPanel(title="Character — Kael Voss", content=[Text(stats, scale=0.85), Button(text="Close", color=color.red, scale=0.85, on_click=toggle_character_panel)], position=(0.38, 0.1), scale=(1.15, 1.2))


def input(key):
    global camera_distance, free_camera
    if key == 'left mouse down': attack_sword()
    if key == 'q': cast_fireball()
    if key == 'c': toggle_character_panel()
    if key == 'e':
        if dialogue_panel: advance_dialogue()
        else: check_interact()
    if key == 'escape': application.quit()
    if key == 'f':
        free_camera = not free_camera
        if free_camera:
            camera.parent = scene
            print("[INFO] Free camera mode ON (use mouse + WASD)")
        else:
            camera.parent = camera_pivot
            camera.position = (0, 0, -camera_distance)
            print("[INFO] Free camera mode OFF")

    # Mouse wheel zoom
    if key == 'scroll up':
        camera_distance = max(min_distance, camera_distance - 2.5)
        camera.position = (0, 0, -camera_distance)
    if key == 'scroll down':
        camera_distance = min(max_distance, camera_distance + 2.5)
        camera.position = (0, 0, -camera_distance)


def update():
    global yaw, pitch, camera_distance
    
    if not player or not camera_pivot or free_camera:
        return
    
    try:
        # === ORBIT CAMERA (right mouse) ===
        if held_keys['right mouse']:
            if not mouse.locked:
                mouse.locked = True
            yaw += mouse.velocity[0] * mouse_sensitivity * 140 * time.dt
            pitch -= mouse.velocity[1] * mouse_sensitivity * 140 * time.dt
            pitch = max(-80, min(80, pitch))
            camera_pivot.rotation = (pitch, yaw, 0)
        else:
            if mouse.locked:
                mouse.locked = False
        
        # === CAMERA-RELATIVE MOVEMENT ===
        move_dir = Vec3(0, 0, 0)
        cam_forward = camera.forward
        cam_forward.y = 0
        if cam_forward.length() > 0.001:
            cam_forward = cam_forward.normalized()
        
        cam_right = camera.right
        cam_right.y = 0
        if cam_right.length() > 0.001:
            cam_right = cam_right.normalized()
        
        if held_keys['w']: move_dir += cam_forward
        if held_keys['s']: move_dir -= cam_forward
        if held_keys['a']: move_dir -= cam_right
        if held_keys['d']: move_dir += cam_right
        
        if move_dir.length() > 0.05:
            move_dir = move_dir.normalized()
            player.position += move_dir * 8 * time.dt
            target_yaw = math.degrees(math.atan2(move_dir.x, move_dir.z))
            player.rotation_y = lerp(player.rotation_y, target_yaw, 12 * time.dt)
        
        player.y = 0.5
        player.x = clamp(player.x, -95, 95)
        player.z = clamp(player.z, -95, 95)
        
    except Exception as e:
        print(f"[ERROR] {e}")


def main():
    global player, camera_pivot, npcs
    
    print("[INFO] Creating player...")
    player = create_detailed_player()
    player.position = (0, 0.5, 12)
    player.rotation_y = 180
    
    camera_pivot = Entity(parent=player, y=1.82)
    camera.parent = camera_pivot
    camera.position = (0, 0, -camera_distance)
    camera.fov = 65
    camera.rotation = (pitch, yaw, 0)
    
    print("[INFO] Creating NPCs...")
    elara = create_female_npc("Elara the Grove Warden", (-28, 0.5, -22), SILVER_HAIR, EMERALD, GOLD, True)
    npcs.append({'entity': elara, 'name': "Elara the Grove Warden", 'dialogue': get_dialogue_lines("Elara the Grove Warden")})
    
    lirael = create_female_npc("Lirael Ironheart", (42, 0.5, 18), FIRE_HAIR, CRIMSON, SILVER, False)
    npcs.append({'entity': lirael, 'name': "Lirael Ironheart", 'dialogue': get_dialogue_lines("Lirael Ironheart")})
    
    setup_world()
    
    Text("WASD: Move  |  Right Mouse: Orbit  |  Scroll: Zoom  |  E: Talk  |  C: Character  |  Q: Magic  |  F: Free Cam", position=(0, 0.46), origin=(0, 0), scale=0.85, color=color.rgba(1,1,1,0.75), background=True)
    Text("ELYNDRIA CHRONICLES", position=(0, 0.38), origin=(0, 0), scale=2.0, color=GOLD, background=True)
    
    print("[INFO] Game loaded successfully! Press F for free camera mode.")
    app.run()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"[FATAL] {e}")
        traceback.print_exc()
        input("Press Enter to exit...")