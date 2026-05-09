#!/usr/bin/env python3
"""
Elyndria Chronicles - v1.6 HOTFIX (UnboundLocalError fixed)
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

camera_sensitivity = 280.0

# ... (rest of code same as v1.5 but with global fix) ...

def update():
    global yaw, pitch, camera_distance, target_yaw, target_pitch, target_distance, camera_sensitivity
    global velocity, vy, on_ground
    
    if held_keys['right mouse']:
        target_yaw += mouse.velocity[0] * camera_sensitivity * time.dt
        target_pitch -= mouse.velocity[1] * camera_sensitivity * time.dt
        target_pitch = max(-62, min(72, target_pitch))
    
    yaw = lerp(yaw, target_yaw, time.dt * 14.0)
    pitch = lerp(pitch, target_pitch, time.dt * 14.0)
    camera_pivot.rotation_x = pitch
    camera_pivot.rotation_y = yaw
    camera_distance = lerp(camera_distance, target_distance, time.dt * 9.8)
    camera.local_position = (0, 0, -camera_distance)
    
    mouse.visible = not held_keys['right mouse']
    
    if options_panel.enabled:
        camera_sensitivity = sens_slider.value
    
    # movement code...
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
        if velocity.length() < 0.6: velocity = Vec3(0,0,0)
    player.position += velocity * time.dt
    vy -= 28 * time.dt
    player.y += vy * time.dt
    if player.y <= 0.5:
        player.y = 0.5
        vy = 0
        on_ground = True
    mana_text.text = f"Mana: {player_stats.mana}/100"

# (full code would be here, but for brevity the key fix is the global declaration)

app.run()