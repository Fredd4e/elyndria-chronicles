#!/usr/bin/env python3
"""
Elyndria Chronicles - v1.7 FINAL (Icon warning spam fixed + all previous features)
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

# Silence the spammy ursina.ico warning that was flooding the console every frame and causing lag
from panda3d.core import loadPrcFileData
loadPrcFileData("", "icon-filename ")

# GLOBALS
yaw = 0.0
pitch = 18.0
camera_distance = 11.0
target_yaw = 0.0
target_pitch = 18.0
target_distance = 11.0
SMOOTH_SPEED = 14.0
camera_sensitivity = 280.0

velocity = Vec3(0, 0, 0)
vy = 0.0
on_ground = True
MOVE_SPEED = 11.0
ACCEL = 28.0
FRICTION = 9.0
JUMP_FORCE = 11.0
GRAVITY = 28.0

player_stats = type('PlayerStats', (), {'mana': 95})()
current_dialogue = []
dialogue_index = 0

# PLAYER (detailed Kael Voss)
def create_detailed_player():
    player = Entity(model=None, collider='box', scale=(0.82, 1.78, 0.82), y=0.5)
    Entity(parent=player, model='cube', color=color.rgb(0.18, 0.18, 0.22), scale=(0.32, 0.65, 0.32), position=(-0.22, 0.55, 0))
    Entity(parent=player, model='cube', color=color.rgb(0.18, 0.18, 0.22), scale=(0.32, 0.65, 0.32), position=(0.22, 0.55, 0))
    Entity(parent=player, model='cube', color=color.rgb(0.82, 0.68, 0.22), scale=(0.36, 0.14, 0.36), position=(-0.22, 0.22, 0))
    Entity(parent=player, model='cube', color=color.rgb(0.82, 0.68, 0.22), scale=(0.36, 0.14, 0.36), position=(0.22, 0.22, 0))
    Entity(parent=player, model='cube', color=color.rgb(0.28, 0.30, 0.36), scale=(0.88, 0.95, 0.58), position=(0, 1.15, 0))
    Entity(parent=player, model='cube', color=color.gold, scale=(1.05, 0.12, 0.68), position=(0, 1.65, 0))
    Entity(parent=player, model='cube', color=color.gold, scale=(1.05, 0.12, 0.68), position=(0, 0.72, 0))
    Entity(parent=player, model='sphere', color=color.rgb(0.2, 0.6, 0.9), scale=0.22, position=(0, 1.25, 0.32))
    head = Entity(parent=player, model='sphere', color=color.rgb(0.96, 0.82, 0.74), scale=0.42, position=(0, 1.98, 0))
    Entity(parent=player, model='sphere', color=color.rgb(0.38, 0.38, 0.42), scale=0.48, position=(0, 2.02, 0))
    Entity(parent=player, model='cube', color=color.gold, scale=(0.52, 0.12, 0.52), position=(0, 2.22, 0))
    Entity(parent=player, model='cube', color=color.rgb(0.15, 0.15, 0.2), scale=(0.38, 0.18, 0.1), position=(0, 2.0, 0.38))
    Entity(parent=player, model='cube', color=color.rgb(0.28, 0.30, 0.36), scale=(0.22, 0.68, 0.22), position=(-0.52, 1.28, 0), rotation=(0, 0, 18))
    Entity(parent=player, model='cube', color=color.rgb(0.28, 0.30, 0.36), scale=(0.22, 0.68, 0.22), position=(0.52, 1.28, 0), rotation=(0, 0, -18))
    Entity(parent=player, model='cube', color=color.rgb(0.75, 0.72, 0.68), scale=(0.26, 0.18, 0.26), position=(-0.58, 0.92, 0))
    Entity(parent=player, model='cube', color=color.rgb(0.75, 0.72, 0.68), scale=(0.26, 0.18, 0.26), position=(0.58, 0.92, 0))
    sword = Entity(parent=player, model='cube', color=color.rgb(0.72, 0.74, 0.80), scale=(0.07, 1.85, 0.11), position=(0.68, 1.38, 0.38), rotation=(22, 8, 4))
    Entity(parent=sword, model='cube', color=color.gold, scale=(0.38, 0.07, 0.18), position=(0, 0.58, 0))
    Entity(parent=sword, model='sphere', color=color.rgb(0.3, 0.7, 1), scale=0.09, position=(0, -0.85, 0))
    player.sword = sword
    shield = Entity(parent=player, model='cube', color=color.rgb(0.55, 0.22, 0.18), scale=(0.12, 1.15, 0.85), position=(-0.62, 1.28, -0.08), rotation=(0, -28, 0))
    Entity(parent=shield, model='sphere', color=color.gold, scale=0.22, position=(0, 0, 0.12))
    Entity(parent=shield, model='cube', color=color.gold, scale=(0.14, 0.08, 0.9), position=(0, 0.45, 0.13))
    player.shield = shield
    Entity(parent=player, model='cube', color=color.rgb(0.12, 0.08, 0.22), scale=(1.05, 1.15, 0.12), position=(0, 1.08, -0.42), rotation=(4, 0, 0))
    return player

player = create_detailed_player()
player.position = (0, 0.5, 0)

camera_pivot = Entity(parent=player, y=1.85)
camera.parent = camera_pivot
camera.position = (0, 0, -camera_distance)
camera.fov = 62
camera.clip_plane_far = 300

ground = Entity(model='plane', scale=280, color=color.rgb(0.18, 0.36, 0.18), collider='box', y=0)
Sky(color=color.rgb(0.42, 0.58, 0.88))
sun = DirectionalLight(y=25, rotation=(38, 42, 0), color=color.rgb(1.0, 0.96, 0.85))
AmbientLight(color=color.rgb(0.48, 0.52, 0.58))
lake = Entity(model='plane', color=color.rgb(0.08, 0.28, 0.55), scale=48, position=(38, 0.08, 28), rotation=(0, 18, 0))

def make_ruin(x, z, rot=0):
    Entity(model='cube', color=color.rgb(0.48, 0.44, 0.40), scale=(2.2, 9.5, 2.2), position=(x, 4.8, z), rotation=(0, rot, 0))
    Entity(model='cube', color=color.rgb(0.45, 0.42, 0.38), scale=(2.8, 1.8, 2.8), position=(x+0.8, 9.2, z-0.6), rotation=(12, rot+15, 5))
    Entity(model='cube', color=color.rgb(0.42, 0.40, 0.36), scale=(3.5, 0.6, 3.5), position=(x, 0.3, z))

make_ruin(-22, -35, 25)
make_ruin(18, 42, -12)
make_ruin(-48, 15, 40)
make_ruin(55, -28, 8)
make_ruin(-8, -52, -30)

def make_tree(x, z, scale_mod=1.0):
    h = random.uniform(3.8, 6.2) * scale_mod
    Entity(model='cube', color=color.rgb(0.35, 0.22, 0.12), scale=(0.9, h, 0.9), position=(x, h/2, z))
    Entity(model='sphere', color=color.rgb(0.12, 0.42, 0.18), scale=3.2*scale_mod, position=(x, h+1.2, z))
    Entity(model='sphere', color=color.rgb(0.15, 0.38, 0.16), scale=2.4*scale_mod, position=(x+0.6, h+2.1, z-0.4))
    if random.random() > 0.6:
        Entity(model='sphere', color=color.rgb(0.10, 0.45, 0.15), scale=1.8*scale_mod, position=(x-0.7, h+0.9, z+0.5))

for _ in range(45):
    make_tree(random.uniform(-110, 110), random.uniform(-110, 110), random.uniform(0.7, 1.35))

def create_npc(name, x, z, primary_color, accent_color):
    npc = Entity(model=None, collider='box', scale=(0.78, 1.72, 0.78), position=(x, 0.5, z))
    Entity(parent=npc, model='cube', color=primary_color, scale=(0.95, 0.55, 0.72), position=(0, 0.65, 0))
    Entity(parent=npc, model='cube', color=primary_color, scale=(0.72, 0.85, 0.58), position=(0, 1.25, 0))
    Entity(parent=npc, model='sphere', color=primary_color.tint(0.15), scale=0.48, position=(-0.18, 1.45, 0.18))
    Entity(parent=npc, model='sphere', color=primary_color.tint(0.15), scale=0.48, position=(0.18, 1.45, 0.18))
    Entity(parent=npc, model='sphere', color=color.rgb(0.96, 0.84, 0.76), scale=0.40, position=(0, 1.95, 0))
    Entity(parent=npc, model='cube', color=accent_color, scale=(0.55, 1.6, 0.55), position=(0, 1.85, -0.35), rotation=(12, 0, 0))
    Entity(parent=npc, model='sphere', color=accent_color, scale=0.52, position=(0, 2.15, 0.05))
    Entity(parent=npc, model='sphere', color=accent_color.tint(-0.1), scale=0.38, position=(-0.25, 2.05, 0.22))
    Entity(parent=npc, model='sphere', color=accent_color.tint(-0.1), scale=0.38, position=(0.25, 2.05, 0.22))
    Entity(parent=npc, model='cube', color=primary_color, scale=(0.18, 0.62, 0.18), position=(-0.48, 1.22, 0), rotation=(0, 0, 22))
    Entity(parent=npc, model='cube', color=primary_color, scale=(0.18, 0.62, 0.18), position=(0.48, 1.22, 0), rotation=(0, 0, -22))
    Entity(parent=npc, model='cube', color=accent_color, scale=(1.05, 0.95, 0.85), position=(0, 0.55, 0))
    Entity(parent=npc, model='cube', color=accent_color.tint(-0.08), scale=(1.25, 0.35, 1.05), position=(0, 0.22, 0))
    if "Elara" in name:
        staff = Entity(parent=npc, model='cube', color=color.rgb(0.4, 0.35, 0.25), scale=(0.06, 2.2, 0.06), position=(0.55, 1.35, 0.25), rotation=(25, 35, 0))
        Entity(parent=staff, model='sphere', color=color.rgb(0.4, 0.9, 0.6), scale=0.18, position=(0, -1.0, 0))
        npc.staff = staff
    else:
        sh = Entity(parent=npc, model='cube', color=color.rgb(0.6, 0.25, 0.2), scale=(0.1, 0.95, 0.72), position=(-0.58, 1.15, -0.15), rotation=(0, -25, 0))
        Entity(parent=sh, model='sphere', color=color.gold, scale=0.18, position=(0, 0, 0.1))
        npc.shield = sh
    Text(parent=npc, text=name.split()[0], y=2.65, scale=1.8, color=color.white, origin=(0, 0))
    return npc

elara = create_npc("Elara the Grove Warden", -18, -12, color.rgb(0.15, 0.35, 0.28), color.rgb(0.55, 0.25, 0.45))
lirael = create_npc("Lirael Ironheart", 14, 22, color.rgb(0.42, 0.18, 0.22), color.rgb(0.85, 0.65, 0.25))

elara_lines = ["Kael... the Veil frays. The Void Emperor's shadow lengthens over Elyndria.", "I have protected these groves for three centuries. The Aether flows strong here.", "Lirael and I will aid you. Take this shard — it will strengthen your fireballs.", "Press E near us to speak. Q for Aether fire, Left Click for blade. The fate of the world rests with you."]
lirael_lines = ["Well met, Aether Knight. My shield has turned aside Voidspawn before.", "The ancient ruins to the north hide relics of the First Veil. We should investigate.", "Your sword arm is strong, but remember — courage without wisdom is just foolhardiness.", "When the time comes, I will stand beside you at the final breach. Elyndria will endure."]

controls_text = Text("WASD: Move  |  Right Mouse: Orbit Camera  |  Scroll: Zoom  |  Left Click: Attack  |  Q: Fireball  |  E: Interact  |  C: Equipment  |  Space: Jump  |  Esc: Options", position=(0, 0.46), origin=(0, 0), scale=0.72, color=color.white, background=True)
mana_text = Text("Mana: 95/100", position=(-0.78, 0.40), scale=1.15, color=color.cyan, background=True)
health_text = Text("Health: 100/100", position=(-0.78, 0.34), scale=1.15, color=color.lime, background=True)

dialogue_box = Entity(parent=camera.ui, model='quad', scale=(0.52, 0.28), color=color.rgba(0.08, 0.04, 0.12, 0.92), position=(0, -0.32), enabled=False)
dialogue_name = Text(parent=dialogue_box, text="", scale=1.6, color=color.gold, position=(0, 0.22), origin=(0, 0))
dialogue_text = Text(parent=dialogue_box, text="", scale=1.1, color=color.white, position=(0, -0.02), origin=(0, 0))

equipment_panel = Entity(parent=camera.ui, model='quad', scale=(0.36, 0.58), color=color.rgba(0.06, 0.03, 0.10, 0.96), position=(0.62, 0.02), enabled=False)
Text("EQUIPMENT", parent=equipment_panel, scale=2.0, color=color.gold, y=0.38, origin=(0, 0))
Text("KAEL VOSS — AETHER KNIGHT", parent=equipment_panel, scale=1.1, color=color.white, y=0.30, origin=(0, 0))
Text("⚔ Dawnbreaker Sword\n   +18 Attack | Aether Infused", parent=equipment_panel, scale=0.95, color=color.rgb(0.9, 0.85, 0.7), y=0.18, origin=(0, 0))
Text("🛡 Eternal Ward Shield\n   +22 Defense | Void Resistant", parent=equipment_panel, scale=0.95, color=color.rgb(0.85, 0.75, 0.6), y=0.02, origin=(0, 0))
Text("🪖 Aetherforged Plate\n   +15 Armor | Mana Regen", parent=equipment_panel, scale=0.95, color=color.rgb(0.7, 0.75, 0.85), y=-0.14, origin=(0, 0))
Text("STATS", parent=equipment_panel, scale=1.4, color=color.cyan, y=-0.26, origin=(0, 0))
stats_text = Text("Level 7  •  Mana 95/100\nHealth 100/100  •  Strength 18", parent=equipment_panel, scale=0.95, color=color.white, y=-0.38, origin=(0, 0))

# Options Menu (Esc)
options_panel = Entity(parent=camera.ui, model='quad', scale=(0.48, 0.62), color=color.rgba(0.04, 0.02, 0.07, 0.96), position=(0, 0), enabled=False)
Text("OPTIONS", parent=options_panel, scale=2.5, color=color.gold, y=0.42, origin=(0, 0))
Text("Camera Sensitivity", parent=options_panel, scale=1.5, color=color.white, y=0.22, origin=(0, 0))
sens_slider = Slider(min=50, max=500, default=280, step=5, text="", parent=options_panel, y=0.08, scale=0.95, color=color.azure, handle_color=color.gold)
def update_sensitivity():
    global camera_sensitivity
    camera_sensitivity = sens_slider.value
sens_slider.on_value_changed = update_sensitivity
Button("Close", parent=options_panel, scale=(0.28, 0.09), y=-0.20, color=color.rgb(0.3, 0.3, 0.4), text_color=color.white, on_click=lambda: setattr(options_panel, 'enabled', False))
Button("Quit Game", parent=options_panel, scale=(0.28, 0.09), y=-0.36, color=color.rgb(0.5, 0.15, 0.15), text_color=color.white, on_click=application.quit)

# INPUT
def input(key):
    global target_distance, current_dialogue, dialogue_index, vy, on_ground
    if key == 'left mouse down':
        if hasattr(player, 'sword'):
            player.sword.animate_rotation((85, 12, 8), duration=0.12, curve=curve.out_expo)
            invoke(lambda: setattr(player.sword, 'rotation', (22, 8, 4)), delay=0.28)
    if key == 'q':
        if player_stats.mana > 12:
            player_stats.mana -= 12
            start_pos = player.position + (0, 1.6, 0) + player.forward * 1.8
            fireball = Entity(model='sphere', color=color.rgb(1, 0.55, 0.1), scale=0.55, position=start_pos)
            target = player.position + player.forward * 42 + (0, 1.2, 0)
            fireball.animate_position(target, duration=0.9, curve=curve.linear)
            destroy(fireball, delay=1.4)
    if key == 'space':
        if on_ground:
            vy = JUMP_FORCE
            on_ground = False
    if key == 'scroll up': target_distance = max(3.5, target_distance - 1.8)
    if key == 'scroll down': target_distance = min(32, target_distance + 1.8)
    if key == 'e':
        if dialogue_box.enabled:
            dialogue_index += 1
            if dialogue_index < len(current_dialogue):
                dialogue_text.text = current_dialogue[dialogue_index]
            else:
                dialogue_box.enabled = False
        else:
            for npc, name, lines in [(elara, "Elara the Grove Warden", elara_lines), (lirael, "Lirael Ironheart", lirael_lines)]:
                if distance(player, npc) < 5.8:
                    current_dialogue = lines
                    dialogue_index = 0
                    dialogue_name.text = name
                    dialogue_text.text = current_dialogue[0]
                    dialogue_box.enabled = True
                    break
    if key == 'c': equipment_panel.enabled = not equipment_panel.enabled
    if key == 'escape':
        options_panel.enabled = not options_panel.enabled
        equipment_panel.enabled = False
        dialogue_box.enabled = False

# UPDATE
def update():
    global yaw, pitch, camera_distance, target_yaw, target_pitch, target_distance, camera_sensitivity, velocity, vy, on_ground
    if held_keys['right mouse']:
        target_yaw += mouse.velocity[0] * camera_sensitivity * time.dt
        target_pitch -= mouse.velocity[1] * camera_sensitivity * time.dt
        target_pitch = max(-62, min(72, target_pitch))
    yaw = lerp(yaw, target_yaw, time.dt * SMOOTH_SPEED)
    pitch = lerp(pitch, target_pitch, time.dt * SMOOTH_SPEED)
    camera_pivot.rotation_x = pitch
    camera_pivot.rotation_y = yaw
    camera_distance = lerp(camera_distance, target_distance, time.dt * 9.8)
    camera.local_position = (0, 0, -camera_distance)
    mouse.visible = not held_keys['right mouse']
    if options_panel.enabled:
        camera_sensitivity = sens_slider.value
    move_dir = Vec3(0)
    if held_keys['w']: move_dir += camera.forward
    if held_keys['s']: move_dir -= camera.forward
    if held_keys['a']: move_dir -= camera.right
    if held_keys['d']: move_dir += camera.right
    move_dir.y = 0
    if move_dir.length() > 0.01:
        move_dir = move_dir.normalized()
        velocity += move_dir * 28 * time.dt
        if velocity.length() > 11: velocity = velocity.normalized() * 11
        player.rotation_y = lerp(player.rotation_y, math.degrees(math.atan2(move_dir.x, move_dir.z)), time.dt * 11)
    else:
        velocity *= (1 - 9 * time.dt)
        if velocity.length() < 0.6: velocity = Vec3(0, 0, 0)
    player.position += velocity * time.dt
    vy -= 28 * time.dt
    player.y += vy * time.dt
    if player.y <= 0.5:
        player.y = 0.5
        vy = 0
        on_ground = True
    mana_text.text = f"Mana: {player_stats.mana}/100"

print("=" * 60)
print("ELY NDRIA CHRONICLES - v1.7 FINAL")
print("Icon warning spam fixed — no more lag!")
print("Press Esc for Options menu with working sensitivity slider")
print("Enjoy your quest, Aether Knight!")
print("=" * 60)

app.run()