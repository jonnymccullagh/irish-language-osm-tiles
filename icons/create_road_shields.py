#!/usr/bin/env python3
"""
Create road shield background rectangles for sprite sheet
"""

from PIL import Image, ImageDraw
import json

def create_road_shield(width, height, bg_color, border_color=None, border_width=2, corner_radius=4):
    """
    Create a rectangular road shield background with rounded corners

    Args:
        width: Width of rectangle
        height: Height of rectangle
        bg_color: Background color tuple (R, G, B, A)
        border_color: Optional border color tuple (R, G, B, A)
        border_width: Border width in pixels
        corner_radius: Radius of rounded corners

    Returns:
        PIL Image
    """
    img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Draw filled rounded rectangle
    draw.rounded_rectangle([0, 0, width-1, height-1], radius=corner_radius, fill=bg_color)

    # Draw border if specified
    if border_color:
        for i in range(border_width):
            draw.rounded_rectangle([i, i, width-1-i, height-1-i], radius=corner_radius, outline=border_color)

    return img

def add_road_shields_to_sprite(sprite_json_path, sprite_png_path, shields_config):
    """
    Add road shield backgrounds to existing sprite

    Args:
        sprite_json_path: Path to sprite.json
        sprite_png_path: Path to sprite.png
        shields_config: Dict of shield configs, e.g.:
            {
                'road_motorway': {
                    'width': 40,
                    'height': 24,
                    'bg_color': (0, 120, 168, 255),  # Blue
                    'border_color': (255, 255, 255, 255)  # White border
                }
            }
    """
    # Load existing sprite
    with open(sprite_json_path, 'r') as f:
        sprite_json = json.load(f)

    sprite_img = Image.open(sprite_png_path)

    # Find placement for new shields (append to right edge)
    max_x = max((data['x'] + data['width'] for data in sprite_json.values()), default=0)
    current_y = 0

    # Create new sprites for shields
    new_sprites = {}
    for shield_name, config in shields_config.items():
        width = config['width']
        height = config['height']
        bg_color = config['bg_color']
        border_color = config.get('border_color')
        border_width = config.get('border_width', 2)
        corner_radius = config.get('corner_radius', 4)

        shield_img = create_road_shield(width, height, bg_color, border_color, border_width, corner_radius)

        new_sprites[shield_name] = {
            'image': shield_img,
            'x': max_x,
            'y': current_y,
            'width': width,
            'height': height
        }

        current_y += height + 2  # Add small gap between shields

    # Calculate new sprite sheet size
    new_width = max(sprite_img.width, max_x + max(s['width'] for s in new_sprites.values()))
    new_height = max(sprite_img.height, current_y)

    # Create new sprite sheet
    new_sprite_img = Image.new('RGBA', (new_width, new_height), (0, 0, 0, 0))
    new_sprite_img.paste(sprite_img, (0, 0))

    # Add road shields to sprite
    for shield_name, sprite_data in new_sprites.items():
        new_sprite_img.paste(sprite_data['image'], (sprite_data['x'], sprite_data['y']))

        # Add to JSON
        sprite_json[shield_name] = {
            'x': sprite_data['x'],
            'y': sprite_data['y'],
            'width': sprite_data['width'],
            'height': sprite_data['height'],
            'pixelRatio': 1,
            'sdf': False
        }

    # Save updated sprite
    new_sprite_img.save(sprite_png_path)
    with open(sprite_json_path, 'w') as f:
        json.dump(sprite_json, f, indent=2)

    print(f"Added {len(new_sprites)} road shields to sprite")
    for name in new_sprites:
        print(f"  - {name}")

if __name__ == "__main__":
    # Define road shield styles
    shields = {
        'road_motorway': {
            'width': 27,
            'height': 16,
            'bg_color': (70, 93, 204, 255),       # Blue background #465dcc
            'border_color': (255, 255, 255, 255), # White border
            'border_width': 2,
            'corner_radius': 3
        },
        'road_primary': {
            'width': 27,
            'height': 16,
            'bg_color': (25, 164, 71, 255),       # Green background #19a447 (for A1, N-roads)
            'border_color': (255, 255, 255, 255), # White border
            'border_width': 2,
            'corner_radius': 3
        },
        'road_secondary': {
            'width': 27,
            'height': 16,
            'bg_color': (255, 193, 7, 255),       # Yellow/amber background (B roads)
            'border_color': (255, 255, 255, 255), # White border
            'border_width': 2,
            'corner_radius': 3
        },
        'road_tertiary': {
            'width': 27,
            'height': 16,
            'bg_color': (255, 255, 255, 255),     # White background (minor roads)
            'border_color': (0, 0, 0, 255),        # Black border
            'border_width': 1,
            'corner_radius': 3
        }
    }

    sprite_json = 'styles/sraid-v1/sprite.json'
    sprite_png = 'styles/sraid-v1/sprite.png'

    print(f"Adding road shields to: {sprite_png}")
    print(f"Shield configurations:")
    for name, config in shields.items():
        print(f"  {name}: RGB{config['bg_color'][:3]}")
    print()

    add_road_shields_to_sprite(sprite_json, sprite_png, shields)

    print(f"\nDone! Road shields added to sprite.")
    print(f"Don't forget to also update sprite@2x.json and sprite@2x.png")
