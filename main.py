#!/usr/bin/env python3
"""
Elyndria Chronicles - Final Stable Version
Simple, reliable, works out of the box with current Ursina
"""

from ursina import *
import math
import random

app = Ursina()
window.title = "Elyndria Chronicles"
window.size = (1280, 720)

# Simple player stats
class PlayerStats:
    def __init__(self):
        self.mana = 95

player_stats = PlayerStats()

# Create simple but nice looking player
def create_player():
    player = Entity(model=None, collider='box', scale=(0.9, 1.8, 0.9), y=0.5)
    
    # Body
    Entity(parent=player, model='cube', color=color.rgb(0.25, 0.22, 0.28), scale=(0.9, 1.2, 0.7), y=1.0)
    Entity(parent=player, model='cube', color=color.rgb(0.96, 0.78, 0.68), scale=(0.5, 0.5, 0.5), y=1.8)  # head
    
    # Sword
    sword = Entity(parent=player, model='cube', color=color.rgb(0.75, 0.78, 0.82), scale=(0.1, 1.5, 0.1), 
                   position=(0.5, 1.2, 0.3), rotation=(30, 0, 0))
    
    player.sword = sword
    return player

player = create_player()
player.position = (0, 0.5, 0)

# Simple camera setup - very reliable
camera_pivot = Entity(parent=player, y=1.8)
camera.parent = camera_pivot
camera.position = (0, 0, -12)
camera.fov = 65

# Basic world
ground = Entity(model='plane', scale=200, color=color.rgb(0.2, 0.4, 0.2), collider='box', y=0)
Sky(color=color.rgb(0.4, 0.6, 0.9))

# Simple tree
def make_tree(x, z):
    Entity(model='cube', color=color.brown, scale=(1, 4, 1), position=(x, 2, z))
    Entity(model='sphere', color=color.green, scale=3, position=(x, 5, z))

for i in range(20):
    make_tree(random.uniform(-80, 80), random.uniform(-80, 80))

# UI
Text("WASD: Move  |  Right Mouse: Orbit  |  Scroll: Zoom  |  Left Click: Attack  |  Q: Fireball", 
     position=(0, 0.45), origin=(0,0), scale=0.8, color=color.white, background=True)

# Input
def input(key):
    if key == 'left mouse down':
        # Simple sword swing animation
        if hasattr(player, 'sword'):
            player.sword.animate_rotation((80, 0, 0), duration=0.15, curve=curve.out_expo)
            invoke(lambda: setattr(player.sword, 'rotation', (30, 0, 0)), delay=0.3)
    
    if key == 'q':
        if player_stats.mana > 10:
            player_stats.mana -= 10
            fireball = Entity(model='sphere', color=color.orange, scale=0.6, 
                             position=player.position + (0, 1.5, 0) + player.forward * 1.5)
            fireball.animate_position(player.position + player.forward * 40, duration=1.2)
            destroy(fireball, delay=1.5)
            print(f"[INFO] Fireball cast! Mana left: {player_stats.mana}")

    # Mouse wheel zoom (reliable way)
    global camera_distance
    if key == 'scroll up':
        camera_distance = max(4, camera_distance - 2)
        camera.position = (0, 0, -camera_distance)
    if key == 'scroll down':
        camera_distance = min(25, camera_distance + 2)
        camera.position = (0, 0, -camera_distance)

# Update - simple and reliable
yaw = 0
pitch = 20
camera_distance = 12

def update():
    global yaw, pitch, camera_distance
    
    # Right mouse orbit
    if held_keys['right mouse']:
        yaw += mouse.velocity[0] * 0.3 * 100 * time.dt
        pitch -= mouse.velocity[1] * 0.3 * 100 * time.dt
        pitch = max(-70, min(70, pitch))
        camera_pivot.rotation = (pitch, yaw, 0)
    
    # Movement (camera relative)
    move = Vec3(0)
    if held_keys['w']: move += camera.forward
    if held_keys['s']: move -= camera.forward
    if held_keys['a']: move -= camera.right
    if held_keys['d']: move += camera.right
    
    move.y = 0
    if move.length() > 0.01:
        move = move.normalized()
        player.position += move * 10 * time.dt
        player.rotation_y = math.degrees(math.atan2(move.x, move.z))

app.run()