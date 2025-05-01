from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from PIL import Image

def grass_texture(x, y):
    # Simple green color, you can make it fancier
    return (34, 139, 34, 255)

def create_block_texture(resolution=16, color_func=None):
    img = Image.new('RGBA', (resolution, resolution))
    pixels = img.load()
    for x in range(resolution):
        for y in range(resolution):
            if color_func:
                pixels[x, y] = color_func(x, y)
            else:
                pixels[x, y] = (255, 255, 255, 255)
    return Texture(img)

app = Ursina()

block_textures = {
    'grass': create_block_texture(color_func=grass_texture),
}

player = FirstPersonController()

# Example block
Entity(model='cube', texture=block_textures['grass'], position=(0,0,0))

app.run()
