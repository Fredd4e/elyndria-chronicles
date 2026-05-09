#!/usr/bin/env python3
"""
Elyndria Chronicles - A beautiful third-person RPG in Ursina/Python
WoW-style orbit camera + directional movement
Detailed characters, lore-rich NPCs, magic, sword & shield, character panel
All models procedurally built for maximum detail without external assets
"""

from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController  # kept for reference, not used
import math
import random
import time as pytime

# ============== CONFIG & GLOBALS ==============
app = Ursina()
window.title = "Elyndria Chronicles"
window.borderless = False
window.size = (1280, 720)
window.color = color.rgb(0.05, 0.05, 0.1)

# Player stats
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

# Camera & movement globals
camera_pivot = None
player = None
yaw = 0
pitch = 25
camera_distance = 13.0
min_distance = 4.0
max_distance = 28.0
mouse_sensitivity = 0.25

# NPCs & dialogue
npcs = []
current_npc = None
current_dialogue_index = 0
dialogue_panel = None
prompt_text = None
char_panel = None

# Colors
SKIN = color.rgb(0.96, 0.78, 0.68)
GOLD = color.rgb(0.85, 0.65, 0.13)
SILVER = color.rgb(0.75, 0.78, 0.82)
DARK_ARMOR = color.rgb(0.25, 0.22, 0.28)
EMERALD = color.rgb(0.1, 0.55, 0.25)
CRIMSON = color.rgb(0.6, 0.1, 0.15)
FIRE_HAIR = color.rgb(0.9, 0.35, 0.1)
SILVER_HAIR = color.rgb(0.92, 0.95, 1.0)

# ============== DETAILED CHARACTER BUILDERS ==============

def create_detailed_player():
    """Kael Voss - Detailed Aether Knight with sword, shield, layered armor"""
    p = Entity(model=None, collider='box', scale=(0.9, 1.85, 0.9), origin_y=-0.5, name="Kael Voss")
    
    # === LEGS & BOOTS ===
    # Left leg
    left_leg = Entity(parent=p, model='cylinder', color=DARK_ARMOR, scale=(0.32, 0.95, 0.32), position=(-0.28, 0.48, 0))
    Entity(parent=left_leg, model='cylinder', color=color.rgb(0.15,0.12,0.1), scale=(1.15, 0.28, 1.15), position=(0, -0.55, 0))  # boot
    # Right leg
    right_leg = Entity(parent=p, model='cylinder', color=DARK_ARMOR, scale=(0.32, 0.95, 0.32), position=(0.28, 0.48, 0))
    Entity(parent=right_leg, model='cylinder', color=color.rgb(0.15,0.12,0.1), scale=(1.15, 0.28, 1.15), position=(0, -0.55, 0))
    
    # Knee guards
    Entity(parent=left_leg, model='sphere', color=SILVER, scale=0.38, position=(0, 0.25, 0))
    Entity(parent=right_leg, model='sphere', color=SILVER, scale=0.38, position=(0, 0.25, 0))
    
    # === TORSO (layered armor for detail) ===
    # Lower torso / hips
    lower_torso = Entity(parent=p, model='cylinder', color=DARK_ARMOR, scale=(1.05, 0.55, 0.95), position=(0, 1.05, 0))
    # Upper torso / chest (slightly tapered)
    upper_torso = Entity(parent=p, model='cylinder', color=color.rgb(0.32, 0.28, 0.35), scale=(0.92, 0.72, 0.88), position=(0, 1.55, 0))
    # Breastplate ridges
    Entity(parent=upper_torso, model='cylinder', color=SILVER, scale=(1.05, 0.12, 1.0), position=(0, 0.1, 0))
    Entity(parent=upper_torso, model='cylinder', color=SILVER, scale=(1.05, 0.08, 1.0), position=(0, -0.15, 0))
    
    # Belt with gold buckle
    Entity(parent=p, model='cylinder', color=color.rgb(0.2, 0.15, 0.1), scale=(1.12, 0.18, 1.02), position=(0, 0.92, 0))
    Entity(parent=p, model='cube', color=GOLD, scale=(0.35, 0.22, 0.4), position=(0, 0.92, 0.52))
    
    # === ARMS ===
    # Left arm (shield side)
    left_arm = Entity(parent=p, model='cylinder', color=SKIN, scale=(0.28, 0.78, 0.28), position=(-0.65, 1.35, 0), rotation=(0, 0, -18))
    Entity(parent=left_arm, model='cylinder', color=SILVER, scale=(1.25, 0.22, 1.25), position=(0, -0.42, 0))  # gauntlet
    # Right arm (sword side)
    right_arm = Entity(parent=p, model='cylinder', color=SKIN, scale=(0.28, 0.78, 0.28), position=(0.65, 1.35, 0), rotation=(0, 0, 22))
    Entity(parent=right_arm, model='cylinder', color=SILVER, scale=(1.25, 0.22, 1.25), position=(0, -0.42, 0))
    
    # Shoulder pauldrons (detailed)
    left_pauldron = Entity(parent=p, model='sphere', color=SILVER, scale=0.42, position=(-0.58, 1.68, 0))
    Entity(parent=left_pauldron, model='sphere', color=DARK_ARMOR, scale=0.65, position=(0, 0, 0))  # inner
    right_pauldron = Entity(parent=p, model='sphere', color=SILVER, scale=0.42, position=(0.58, 1.68, 0))
    Entity(parent=right_pauldron, model='sphere', color=DARK_ARMOR, scale=0.65, position=(0, 0, 0))
    
    # === HEAD & HELMET ===
    head = Entity(parent=p, model='sphere', color=SKIN, scale=0.42, position=(0, 2.05, 0))
    # Helmet (full coverage with crest)
    helmet = Entity(parent=head, model='sphere', color=color.rgb(0.55, 0.55, 0.62), scale=1.08, position=(0, 0.08, 0))
    # Helmet crest / plume
    Entity(parent=helmet, model='cone', color=CRIMSON, scale=(0.22, 0.65, 0.22), position=(0, 0.55, 0), rotation=(180, 0, 0))
    # Visor slit
    Entity(parent=helmet, model='cube', color=color.black, scale=(0.9, 0.08, 0.15), position=(0, 0.05, 0.42))
    
    # === WEAPON: DAWNBREAKER SWORD (highly detailed) ===
    sword = Entity(parent=right_arm, model='cube', color=SILVER, scale=(0.12, 1.95, 0.07), position=(0.18, -0.35, 0.28), rotation=(38, 8, 5), name="sword")
    # Sword fuller (groove)
    Entity(parent=sword, model='cube', color=color.rgb(0.4,0.4,0.45), scale=(0.6, 0.95, 0.4), position=(0, 0.1, 0))
    # Crossguard (ornate)
    Entity(parent=sword, model='cube', color=GOLD, scale=(0.85, 0.12, 0.35), position=(0, -0.55, 0))
    Entity(parent=sword, model='cube', color=GOLD, scale=(0.25, 0.08, 0.6), position=(0, -0.55, 0))
    # Grip
    Entity(parent=sword, model='cylinder', color=color.rgb(0.25,0.18,0.1), scale=(0.7, 0.35, 0.7), position=(0, -0.82, 0))
    # Pommel (glowing gem)
    pommel = Entity(parent=sword, model='sphere', color=color.rgb(0.3, 0.9, 1.0), scale=0.22, position=(0, -1.05, 0))
    PointLight(parent=pommel, color=color.cyan, range=3, intensity=0.6)
    
    # === SHIELD: ETERNAL WARD (highly detailed) ===
    shield = Entity(parent=left_arm, model='plane', color=color.rgb(0.35, 0.38, 0.45), scale=(1.35, 1.65, 1), position=(0.38, -0.18, 0.52), rotation=(0, 92, 0), name="shield")
    # Shield boss (central emblem)
    boss = Entity(parent=shield, model='sphere', color=GOLD, scale=0.32, position=(0, 0, 0.02))
    Entity(parent=boss, model='sphere', color=color.rgb(0.2, 0.6, 1.0), scale=0.55, position=(0, 0, 0.01))
    # Decorative rim
    Entity(parent=shield, model='torus', color=SILVER, scale=(0.72, 0.72, 0.72), position=(0, 0, 0.015), rotation=(90, 0, 0))
    # Inner engravings (cross)
    Entity(parent=shield, model='cube', color=SILVER, scale=(0.08, 1.1, 0.03), position=(0, 0, 0.025))
    Entity(parent=shield, model='cube', color=SILVER, scale=(0.08, 0.08, 1.0), position=(0, 0, 0.025), rotation=(0, 0, 90))
    
    # === CLOAK (flowing, dramatic) ===
    cloak = Entity(parent=p, model='plane', color=color.rgb(0.18, 0.08, 0.22), scale=(1.6, 1.35, 0.08), position=(0, 1.25, -0.68), rotation=(12, 0, 0))
    # Inner lining
    Entity(parent=cloak, model='plane', color=color.rgb(0.35, 0.15, 0.4), scale=(0.92, 0.85, 0.9), position=(0, -0.1, -0.01))
    # Clasps
    Entity(parent=p, model='sphere', color=GOLD, scale=0.18, position=(-0.45, 1.55, -0.55))
    Entity(parent=p, model='sphere', color=GOLD, scale=0.18, position=(0.45, 1.55, -0.55))
    
    # Store references for animation
    p.sword = sword
    p.shield = shield
    p.head = head
    
    return p


def create_female_npc(name, position, hair_color, robe_color, accent_color, is_sorceress=True):
    """Detailed voluptuous female NPC with flowing hair, curves, and unique outfit"""
    npc = Entity(model=None, collider='box', scale=(0.85, 1.78, 0.85), origin_y=-0.5, position=position, name=name)
    
    # === LEGS (curvy hips start here) ===
    # Wide hips for voluptuous silhouette
    hips = Entity(parent=npc, model='cylinder', color=robe_color, scale=(1.35, 0.55, 1.15), position=(0, 0.55, 0))
    # Legs (slender)
    left_leg = Entity(parent=npc, model='cylinder', color=color.rgb(0.35, 0.28, 0.25), scale=(0.28, 0.85, 0.28), position=(-0.32, 0.35, 0))
    right_leg = Entity(parent=npc, model='cylinder', color=color.rgb(0.35, 0.28, 0.25), scale=(0.28, 0.85, 0.28), position=(0.32, 0.35, 0))
    # Elegant boots / shoes
    Entity(parent=left_leg, model='cylinder', color=accent_color, scale=(1.2, 0.32, 1.2), position=(0, -0.52, 0))
    Entity(parent=right_leg, model='cylinder', color=accent_color, scale=(1.2, 0.32, 1.2), position=(0, -0.52, 0))
    
    # === TORSO (voluptuous: narrow waist + full bust + wide hips) ===
    # Lower torso / skirt top (wide for curves)
    lower = Entity(parent=npc, model='cylinder', color=robe_color, scale=(1.28, 0.48, 1.18), position=(0, 1.0, 0))
    # Waist (cinched, very narrow for hourglass)
    waist = Entity(parent=npc, model='cylinder', color=color.rgb(0.15, 0.12, 0.18), scale=(0.72, 0.35, 0.68), position=(0, 1.32, 0))
    # Upper torso / bust (full, voluptuous)
    bust = Entity(parent=npc, model='cylinder', color=robe_color, scale=(1.05, 0.55, 0.95), position=(0, 1.65, 0))
    # Bust accent / cleavage suggestion (tasteful clothing fold)
    Entity(parent=bust, model='sphere', color=color.rgb(0.12, 0.1, 0.15), scale=(0.85, 0.35, 0.6), position=(0, 0.05, 0.32))
    
    # Decorative belt / sash (accentuates waist)
    Entity(parent=npc, model='cylinder', color=accent_color, scale=(1.35, 0.15, 1.25), position=(0, 1.18, 0))
    Entity(parent=npc, model='cube', color=GOLD, scale=(0.25, 0.18, 0.5), position=(0, 1.18, 0.65))
    
    # === ARMS (graceful) ===
    left_arm = Entity(parent=npc, model='cylinder', color=SKIN, scale=(0.24, 0.72, 0.24), position=(-0.58, 1.38, 0), rotation=(0, 0, -22))
    right_arm = Entity(parent=npc, model='cylinder', color=SKIN, scale=(0.24, 0.72, 0.24), position=(0.58, 1.38, 0), rotation=(0, 0, 22))
    # Elegant long gloves / sleeves
    Entity(parent=left_arm, model='cylinder', color=robe_color, scale=(1.15, 0.55, 1.15), position=(0, -0.25, 0))
    Entity(parent=right_arm, model='cylinder', color=robe_color, scale=(1.15, 0.55, 1.15), position=(0, -0.25, 0))
    
    # === HEAD & VOLUPTUOUS HAIR (flowing, detailed) ===
    head = Entity(parent=npc, model='sphere', color=SKIN, scale=0.40, position=(0, 2.02, 0))
    
    # Long flowing hair base (voluminous)
    hair_base = Entity(parent=head, model='sphere', color=hair_color, scale=1.15, position=(0, 0.15, -0.05))
    
    # Multiple flowing hair strands for volume and movement feel (6-8 strands)
    for i in range(8):
        angle = (i / 8) * 360 + random.uniform(-8, 8)
        strand = Entity(parent=head, model='cylinder', color=hair_color, 
                        scale=(0.09, 1.45, 0.09), 
                        position=(math.sin(math.radians(angle)) * 0.22, 0.35, math.cos(math.radians(angle)) * 0.18 - 0.08),
                        rotation=(random.uniform(-25, 25), angle + random.uniform(-15, 15), random.uniform(-8, 8)))
        # Add slight wave to some strands
        if i % 2 == 0:
            Entity(parent=strand, model='sphere', color=hair_color, scale=0.7, position=(0, 0.6, 0))
    
    # Hair accessories / circlet
    Entity(parent=head, model='torus', color=GOLD, scale=(0.52, 0.52, 0.52), position=(0, 0.28, 0), rotation=(90, 0, 0))
    # Gem on circlet
    Entity(parent=head, model='sphere', color=color.rgb(0.2, 1, 0.6), scale=0.12, position=(0, 0.42, 0.38))
    
    # === OUTFIT DETAILS (sorceress vs warrior) ===
    if is_sorceress:
        # Elara - Sorceress staff (glowing orb)
        staff = Entity(parent=right_arm, model='cylinder', color=color.rgb(0.25, 0.2, 0.15), scale=(0.08, 2.1, 0.08), position=(0.22, -0.15, 0.35), rotation=(25, 15, 0))
        orb = Entity(parent=staff, model='sphere', color=color.rgb(0.4, 1, 0.7), scale=0.28, position=(0, 1.15, 0))
        PointLight(parent=orb, color=color.lime, range=4, intensity=0.8)
        # Flowing robe hem details
        for j in range(3):
            Entity(parent=hips, model='plane', color=accent_color, scale=(1.6, 0.6, 0.6), 
                   position=(0, -0.35 - j*0.25, 0.45 + j*0.1), rotation=(15 + j*8, 0, 0))
    else:
        # Lirael - Warrior battle axe + shield accents
        axe_handle = Entity(parent=right_arm, model='cylinder', color=color.rgb(0.2, 0.15, 0.1), scale=(0.1, 1.6, 0.1), position=(0.25, -0.1, 0.32), rotation=(35, 10, 0))
        axe_head = Entity(parent=axe_handle, model='cube', color=SILVER, scale=(0.9, 0.55, 0.15), position=(0, 0.95, 0))
        Entity(parent=axe_head, model='cube', color=GOLD, scale=(0.35, 0.08, 0.25), position=(0, 0, 0))  # axe edge
        # Battle skirt plates (accentuate curves)
        for j in range(4):
            plate = Entity(parent=hips, model='plane', color=SILVER, scale=(0.55, 0.7, 0.08), 
                           position=(random.uniform(-0.6, 0.6), -0.2, 0.55), rotation=(random.uniform(20, 40), random.uniform(-15, 15), 0))
    
    # Necklace / amulet (emphasizes bust)
    Entity(parent=npc, model='torus', color=GOLD, scale=(0.25, 0.25, 0.25), position=(0, 1.55, 0.48), rotation=(90, 0, 0))
    Entity(parent=npc, model='sphere', color=color.rgb(1, 0.85, 0.3), scale=0.11, position=(0, 1.55, 0.5))
    
    # Store for interaction
    npc.head = head
    npc.name = name
    return npc


# ============== WORLD BUILDING ==============

def create_tree(x, z):
    """Detailed low-poly tree with layered foliage"""
    trunk = Entity(model='cylinder', color=color.rgb(0.38, 0.24, 0.12), scale=(1.1, 4.8, 1.1), position=(x, 2.4, z))
    # Layered foliage (3-4 spheres for volume)
    colors = [color.rgb(0.08, 0.48, 0.12), color.rgb(0.12, 0.55, 0.18), color.rgb(0.06, 0.42, 0.1)]
    for i, s in enumerate([3.8, 3.2, 2.6, 1.8]):
        f = Entity(parent=trunk, model='sphere', color=colors[i % 3], scale=s, position=(0, 2.8 + i * 1.3, 0))
        if random.random() > 0.75:
            Entity(parent=f, model='sphere', color=color.red, scale=0.25, position=(random.uniform(-0.8, 0.8), random.uniform(-0.5, 0.5), random.uniform(-0.8, 0.8)))


def setup_world():
    global prompt_text
    
    # Vast ground plane (beautiful meadow green)
    ground = Entity(model='plane', scale=(210, 1, 210), color=color.rgb(0.22, 0.42, 0.18), collider='box', y=0)
    # Subtle ground variation (darker patches)
    for _ in range(25):
        patch = Entity(model='plane', scale=random.uniform(8, 18), color=color.rgb(0.18, 0.35, 0.15), 
                       position=(random.uniform(-95, 95), 0.02, random.uniform(-95, 95)), rotation=(0, random.uniform(0, 360), 0))
    
    # Sparkling lake
    lake = Entity(model='plane', scale=(38, 1, 38), color=color.rgb(0.08, 0.32, 0.55), position=(35, 0.05, -48), rotation=(0, 18, 0))
    # Lake ripples (animated planes)
    for i in range(5):
        ripple = Entity(parent=lake, model='plane', color=color.rgba(0.4, 0.7, 1, 0.25), scale=0.9 - i*0.12, position=(0, 0.01 + i*0.005, 0))
    
    # Dense forest (60 trees)
    for _ in range(60):
        x = random.uniform(-92, 92)
        z = random.uniform(-92, 92)
        if 20 < x < 55 and -65 < z < -30:  # avoid lake
            continue
        create_tree(x, z)
    
    # Scattered rocks & boulders
    for _ in range(35):
        x = random.uniform(-85, 85)
        z = random.uniform(-85, 85)
        s = random.uniform(1.2, 3.5)
        rock = Entity(model='sphere', color=color.rgb(0.45, 0.42, 0.38), scale=s, position=(x, s*0.4, z), 
                      rotation=(random.uniform(0, 40), random.uniform(0, 360), random.uniform(0, 40)))
    
    # Ancient ruins (8 pillars + broken walls)
    ruin_positions = [(-55, -55), (58, 62), (-48, 48), (65, -40), (-30, 70), (22, -68), (-68, 22), (40, 35)]
    for rx, rz in ruin_positions:
        for h in range(5):
            pillar = Entity(model='cylinder', color=color.rgb(0.48, 0.42, 0.35), scale=(2.8, 2.8, 2.8), position=(rx, h*2.4 + 1.4, rz))
        # Broken top
        Entity(model='cube', color=color.rgb(0.4, 0.35, 0.3), scale=(4.2, 0.6, 4.2), position=(rx, 12.2, rz), rotation=(random.uniform(-8, 8), random.uniform(0, 360), random.uniform(-5, 5)))
        # Rubble
        for _ in range(3):
            Entity(model='cube', color=color.rgb(0.35, 0.3, 0.25), scale=random.uniform(0.8, 1.6), 
                   position=(rx + random.uniform(-3, 3), 0.6, rz + random.uniform(-3, 3)))
    
    # Glowing flora (magic crystals / flowers)
    for _ in range(28):
        x = random.uniform(-75, 75)
        z = random.uniform(-75, 75)
        if 22 < x < 52 and -62 < z < -35:
            continue
        glow = Entity(model='sphere', color=color.random_color(), scale=random.uniform(0.25, 0.45), position=(x, 0.75, z))
        PointLight(parent=glow, color=glow.color, range=2.5, intensity=0.4)
    
    # Sky & atmosphere
    Sky(color=color.rgb(0.35, 0.55, 0.85))
    
    # Lighting (beautiful golden hour feel)
    sun = DirectionalLight(shadows=True, rotation=(38, -42, 0), color=color.rgb(1.0, 0.92, 0.78))
    sun.shadow_map_size = 2048
    AmbientLight(color=color.rgb(0.55, 0.62, 0.72))
    
    # Atmospheric fog
    scene.fog_color = color.rgb(0.48, 0.55, 0.62)
    scene.fog_density = 0.012
    
    # Interaction prompt (hidden until near NPC)
    prompt_text = Text(text="Press  [E]  to speak", position=(0, -0.42), origin=(0, 0), 
                       scale=1.8, color=color.yellow, enabled=False, background=True)


# ============== CAMERA & MOVEMENT SYSTEM (WoW Style) ==============

def update_camera_and_movement():
    global yaw, pitch, camera_distance
    
    if not player or not camera_pivot:
        return
    
    # === ORBIT CAMERA (Right Mouse Hold) ===
    if held_keys['right mouse']:
        yaw += mouse.velocity[0] * mouse_sensitivity * 120 * time.dt
        pitch -= mouse.velocity[1] * mouse_sensitivity * 120 * time.dt
        pitch = max(-82, min(82, pitch))
        camera_pivot.rotation = (pitch, yaw, 0)
    
    # === ZOOM (Mouse Wheel) ===
    if mouse.wheel_up:
        camera_distance = max(min_distance, camera_distance - 2.5)
        camera.position = (0, 0, -camera_distance)
    if mouse.wheel_down:
        camera_distance = min(max_distance, camera_distance + 2.5)
        camera.position = (0, 0, -camera_distance)
    
    # === DIRECTIONAL MOVEMENT (camera-relative, like WoW) ===
    move_dir = Vec3(0, 0, 0)
    
    # Get camera forward/right on XZ plane
    cam_forward = camera.forward
    cam_forward.y = 0
    if cam_forward.length() > 0.001:
        cam_forward = cam_forward.normalized()
    else:
        cam_forward = Vec3(0, 0, 1)
    
    cam_right = camera.right
    cam_right.y = 0
    if cam_right.length() > 0.001:
        cam_right = cam_right.normalized()
    
    if held_keys['w']:
        move_dir += cam_forward
    if held_keys['s']:
        move_dir -= cam_forward
    if held_keys['a']:
        move_dir -= cam_right
    if held_keys['d']:
        move_dir += cam_right
    
    if move_dir.length() > 0.05:
        move_dir = move_dir.normalized()
        player.position += move_dir * 7.5 * time.dt
        
        # Smooth turn toward movement direction (WoW feel)
        target_yaw = math.degrees(math.atan2(move_dir.x, move_dir.z))
        player.rotation_y = lerp(player.rotation_y, target_yaw, 9 * time.dt)
        
        # Subtle walk bob on head
        if hasattr(player, 'head'):
            player.head.y = 2.05 + math.sin(pytime.time() * 8) * 0.015
    
    # Keep player in world bounds
    player.x = clamp(player.x, -96, 96)
    player.z = clamp(player.z, -96, 96)
    player.y = 0.5  # lock to ground (flat world)
    
    # Update prompt visibility
    global prompt_text
    if prompt_text:
        near_any = False
        for npc_data in npcs:
            if distance(player, npc_data['entity']) < 6.5:
                near_any = True
                break
        prompt_text.enabled = near_any and dialogue_panel is None


# ============== COMBAT & MAGIC ==============

def attack_sword():
    if not hasattr(player, 'sword'):
        return
    sword = player.sword
    orig_rot = sword.rotation
    
    # Swing animation
    sword.animate_rotation((65, 35, 12), duration=0.12, curve=curve.out_expo)
    
    # Spawn slash effect
    slash_pos = player.position + player.forward * 2.8 + Vec3(0, 1.35, 0)
    slash = Entity(model='plane', color=color.white, scale=(3.2, 1.8, 1), 
                   position=slash_pos, rotation=player.rotation + (random.uniform(-8, 8), 90, random.uniform(-12, 12)), alpha=0.75)
    slash.animate_scale((0.05, 1.8, 1), duration=0.28, curve=curve.out_quad)
    destroy(slash, delay=0.32)
    
    # Return sword
    invoke(lambda: setattr(sword, 'rotation', orig_rot), delay=0.38)
    
    # Optional: screen flash on hit (simple)
    if random.random() > 0.6:
        flash = Entity(model='quad', color=color.rgba(1, 0.9, 0.7, 0.15), scale=2, position=(0, 0), parent=camera.ui)
        destroy(flash, delay=0.08)


def cast_fireball():
    """Beautiful Aether fireball"""
    start_pos = player.position + Vec3(0, 1.6, 0) + player.forward * 1.2
    fb = Entity(model='sphere', color=color.rgb(1, 0.45, 0.1), scale=0.55, position=start_pos)
    
    # Core glow
    core = Entity(parent=fb, model='sphere', color=color.rgb(1, 0.9, 0.5), scale=0.6, position=(0, 0, 0))
    PointLight(parent=core, color=color.orange, range=6, intensity=1.2)
    
    # Fly forward
    target_pos = start_pos + player.forward * 32
    fb.animate_position(target_pos, duration=1.4, curve=curve.linear)
    
    # Trail particles (simple)
    for i in range(4):
        invoke(lambda pos=start_pos + player.forward * (i * 3): 
               Entity(model='sphere', color=color.rgb(1, 0.6, 0.2), scale=0.2, position=pos, alpha=0.6), 
               delay=i * 0.08)
    
    destroy(fb, delay=1.6)
    
    # Mana cost visual
    if player_stats.mana > 8:
        player_stats.mana = max(0, player_stats.mana - 8)


# ============== DIALOGUE SYSTEM ==============

def get_dialogue_lines(name):
    if "Elara" in name:
        return [
            "Hail, Kael Voss... I knew the Spark would call you home. I am Elara, last Grove Warden of the Whispering Glades. The ancient oaks have sung your name for three centuries.",
            "The Void Emperor's shadow lengthens. Every night the trees bleed black sap and the stars dim. Only the blood of an Aether Knight can mend the Great Veil.",
            "Dawnbreaker was not forged by mortal hands — it was quenched in the tears of Aethera herself. Its light burns voidspawn from within. Wield it, and the land will remember its true shape.",
            "Lirael waits at the Watcher's Spire. Her shield has turned aside more darkness than any living soul. Together you will claim the first Veil Shard from the Sunspire ruins.",
            "When the time comes, return to me. I will teach you the Verdant Rebirth — a spell to heal the wounded earth itself. Go now, hero. The groves watch over you."
        ]
    else:  # Lirael
        return [
            "By the shattered stars... the last Aether Knight walks again. I am Lirael Ironheart, once Captain of the Silver Shields. I have waited three hundred years for this moment.",
            "I watched my sisters fall at the Battle of Broken Stars. My axe drank deep that day, but even I could not stop the Emperor's first incursion. Your arrival changes everything.",
            "Dawnbreaker sings the old songs. I can hear it from here. The shield on your arm — Eternal Ward — once sealed the original Veil. Its power sleeps, but it will awaken for you.",
            "The path to the Sunspire is drenched in void-taint. Stay close to the light of your blade. When we stand together before the Emperor's gate, even he will tremble.",
            "After this is over... perhaps we can speak of quieter things. The wind in the high pines. The taste of fresh bread. Things worth fighting for. Now go — I will guard your back."
        ]


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
    global dialogue_panel, current_dialogue_index, current_npc
    if dialogue_panel:
        destroy(dialogue_panel)
    
    lines = current_npc['dialogue']
    text = lines[current_dialogue_index]
    
    next_text = "Next →" if current_dialogue_index < len(lines) - 1 else "Farewell"
    
    dialogue_panel = WindowPanel(
        title=current_npc['name'],
        content=[
            Text(text, wordwrap=58, scale=0.95, color=color.white),
            Button(text=next_text, color=color.azure, scale=0.9, on_click=advance_dialogue)
        ],
        position=(0, 0.28),
        scale=(1.35, 0.9)
    )


def advance_dialogue():
    global current_dialogue_index, dialogue_panel, current_npc
    current_dialogue_index += 1
    if dialogue_panel:
        destroy(dialogue_panel)
        dialogue_panel = None
    
    if current_npc and current_dialogue_index < len(current_npc['dialogue']):
        show_dialogue_panel()
    else:
        current_npc = None
        current_dialogue_index = 0


# ============== CHARACTER PANEL ==============

def toggle_character_panel():
    global char_panel
    if char_panel:
        destroy(char_panel)
        char_panel = None
        return
    
    stats = f"""Level {player_stats.level}   •   Aether Knight

Health:  {player_stats.health} / {player_stats.max_health}
Mana:    {player_stats.mana} / {player_stats.max_mana}
XP:      {player_stats.xp} / {player_stats.xp_to_next}

Strength:   {player_stats.strength}     Agility:  {player_stats.agility}
Intellect:  {player_stats.intellect}"""

    gear_lines = "\n".join([f"{slot:8}: {item}" for slot, item in player_stats.equipment.items()])
    
    char_panel = WindowPanel(
        title="Character — Kael Voss",
        content=[
            Text(stats, scale=0.85, color=color.white),
            Text("\nEQUIPMENT", scale=1.0, color=GOLD),
            Text(gear_lines, scale=0.78, color=color.light_gray),
            Button(text="Close", color=color.red, scale=0.85, on_click=toggle_character_panel)
        ],
        position=(0.38, 0.1),
        scale=(1.15, 1.65)
    )


# ============== INPUT HANDLER ==============

def input(key):
    global dialogue_panel
    
    if key == 'left mouse down':
        attack_sword()
    
    if key == 'q':
        cast_fireball()
    
    if key == 'c':
        toggle_character_panel()
    
    if key == 'e':
        if dialogue_panel:
            advance_dialogue()
        else:
            check_interact()
    
    if key == 'escape':
        application.quit()
    
    # Quick stat display (debug, optional)
    if key == 'h':
        print(f"Health: {player_stats.health} | Mana: {player_stats.mana}")


# ============== MAIN SETUP ==============

def main():
    global player, camera_pivot, npcs, prompt_text
    
    # === PLAYER ===
    player = create_detailed_player()
    player.position = (0, 0.5, 12)
    player.rotation_y = 180
    
    # === CAMERA PIVOT (WoW style) ===
    camera_pivot = Entity(parent=player, y=1.82, rotation=(pitch, yaw, 0))
    camera.parent = camera_pivot
    camera.position = (0, 0, -camera_distance)
    camera.fov = 68
    camera.clip_plane_near = 0.1
    camera.clip_plane_far = 300
    
    # === NPCs ===
    # Elara - Sorceress (left side, near forest)
    elara = create_female_npc(
        "Elara the Grove Warden", 
        position=(-28, 0.5, -22), 
        hair_color=SILVER_HAIR, 
        robe_color=EMERALD, 
        accent_color=GOLD, 
        is_sorceress=True
    )
    npcs.append({
        'entity': elara,
        'name': "Elara the Grove Warden",
        'dialogue': get_dialogue_lines("Elara the Grove Warden")
    })
    
    # Lirael - Warrior (right side, near ruins)
    lirael = create_female_npc(
        "Lirael Ironheart", 
        position=(42, 0.5, 18), 
        hair_color=FIRE_HAIR, 
        robe_color=CRIMSON, 
        accent_color=SILVER, 
        is_sorceress=False
    )
    npcs.append({
        'entity': lirael,
        'name': "Lirael Ironheart",
        'dialogue': get_dialogue_lines("Lirael Ironheart")
    })
    
    # === WORLD ===
    setup_world()
    
    # === UI OVERLAY (instructions) ===
    instructions = Text(
        "WASD: Move  |  Right Mouse: Orbit Camera  |  Wheel: Zoom  |  E: Talk  |  C: Character  |  Q: Magic  |  Left Click: Attack",
        position=(0, 0.46), origin=(0, 0), scale=0.9, color=color.rgba(1,1,1,0.7), background=True
    )
    
    # Title banner
    title = Text("ELYNDRIA CHRONICLES", position=(0, 0.38), origin=(0, 0), scale=2.2, color=GOLD, background=True)
    
    # === UPDATE LOOP ===
    def game_update():
        update_camera_and_movement()
        
        # Gentle idle animations for NPCs
        for npc_data in npcs:
            npc = npc_data['entity']
            if hasattr(npc, 'head'):
                npc.head.rotation_y = math.sin(pytime.time() * 0.6) * 4  # subtle head turn
            # Gentle breathing on torso
            if hasattr(npc, 'children') and len(npc.children) > 2:
                torso = npc.children[2]  # rough index for bust/upper
                if torso:
                    torso.scale_y = 1.0 + math.sin(pytime.time() * 1.8) * 0.012
    
    app.update = game_update   # override update
    
    # Start message
    invoke(lambda: print("Elyndria Chronicles loaded successfully. Explore, talk to the NPCs, enjoy the world!"), delay=1.5)
    
    # Run
    app.run()


if __name__ == "__main__":
    main()