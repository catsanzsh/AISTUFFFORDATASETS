
from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import random

app = Ursina()

# Set target FPS to 60 (Ursina will attempt to maintain this)
application.target_frame_rate = 60

# Define a simple block
class Block(Entity):
    def __init__(self, position=(0, 0, 0), color=color.white):
        super().__init__(
            model='cube',
            color=color,
            collider='box',
            position=position,
            scale=(1, 1, 1)
        )

# Create a dictionary to store blocks in the world
world_blocks = {}

# Function to generate a very small world similar to Cave Game (16x16 base, minimal height)
def generate_world(size=8, base_height=8):
    for x in range(-size, size):
        for z in range(-size, size):
            # Very simple height variation for early Cave Game feel
            height = base_height + random.randint(-1, 1)
            for y in range(height):
                block_pos = (x, y, z)
                # Top layer is grass-like, rest is stone-like (Cave Game simplicity)
                if y == height - 1:
                    world_blocks[block_pos] = Block(position=block_pos, color=color.green)
                else:
                    world_blocks[block_pos] = Block(position=block_pos, color=color.gray)

# Generate the initial tiny world (emulating Cave Game's small test area)
generate_world()

# Player - position it above the ground, minimal movement features
player = FirstPersonController(position=(0, 10, 0))
player.speed = 3  # Slower movement like early prototypes
player.jump_height = 0  # No jumping in earliest Cave Game
player.gravity = 0.5

# No skybox or complex sky (Cave Game had a plain background)
Sky(color=color.gray)  # Simple gray background

# Minimal lighting (Cave Game had almost no shading in first version)
# No DirectionalLight to keep it ultra-simple; rely on default ambient light

# Variable to store the currently selected block type for placement
selected_block_color = color.gray  # Default to stone-like

# Function to place a block
def place_block():
    hit_info = raycast(camera.world_position, camera.forward, distance=3)
    if hit_info.hit:
        new_pos = hit_info.world_point + hit_info.normal
        new_pos = (round(new_pos.x), round(new_pos.y), round(new_pos.z))
        if new_pos not in world_blocks:
            world_blocks[new_pos] = Block(position=new_pos, color=selected_block_color)

# Function to destroy a block
def destroy_block():
    hit_info = raycast(camera.world_position, camera.forward, distance=3)
    if hit_info.hit and isinstance(hit_info.entity, Block):
        block_pos = hit_info.entity.position
        block_pos = (round(block_pos.x), round(block_pos.y), round(block_pos.z))
        if block_pos in world_blocks:
            destroy(world_blocks[block_pos])
            del world_blocks[block_pos]

# Input handling for block placement, destruction, and exit
def input(key):
    if key == 'escape':
        application.quit()
    elif key == 'left mouse down':
        place_block()
    elif key == 'right mouse down':
        destroy_block()
    # Switch block types with number keys (minimal selection for Cave Game)
    elif key == '1':
        global selected_block_color
        selected_block_color = color.gray  # Stone-like
    elif key == '2':
        selected_block_color = color.green  # Grass-like

# Lock mouse for first-person control (Cave Game hid cursor)
mouse.locked = True
player.mouse_sensitivity = Vec2(20, 20)  # Lower sensitivity for retro feel

app.run()
