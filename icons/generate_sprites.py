#!/usr/bin/env python3
"""
Generate sprite.json and sprite.png from SVG files
"""

import os
import json
from pathlib import Path
from PIL import Image
import cairosvg
import io
import math

def svg_to_png(svg_path, size=22):
    """Convert SVG to PNG at specified size"""
    png_data = cairosvg.svg2png(url=str(svg_path), output_width=size, output_height=size)
    return Image.open(io.BytesIO(png_data)).convert('RGBA')

def generate_sprite(svg_dir, output_prefix, icon_size=22):
    """
    Generate sprite sheet and JSON from SVG files

    Args:
        svg_dir: Directory containing SVG files
        output_prefix: Output file prefix (e.g., 'sprite' creates sprite.png and sprite.json)
        icon_size: Size to render each icon (default 22x22)
    """
    svg_dir = Path(svg_dir)
    svg_files = sorted(svg_dir.glob('*.svg'))

    if not svg_files:
        print(f"No SVG files found in {svg_dir}")
        return

    print(f"Found {len(svg_files)} SVG files")

    # Convert all SVGs to PNGs
    icons = {}
    for svg_file in svg_files:
        icon_name = svg_file.stem  # filename without extension
        try:
            img = svg_to_png(svg_file, icon_size)
            icons[icon_name] = img
            print(f"Converted: {icon_name}")
        except Exception as e:
            print(f"Error converting {icon_name}: {e}")

    if not icons:
        print("No icons were successfully converted")
        return

    # Calculate sprite sheet dimensions
    num_icons = len(icons)
    # Try to make roughly square sprite sheet
    cols = math.ceil(math.sqrt(num_icons))
    rows = math.ceil(num_icons / cols)

    sprite_width = cols * icon_size
    sprite_height = rows * icon_size

    print(f"\nCreating sprite sheet: {sprite_width}x{sprite_height} ({cols} cols x {rows} rows)")

    # Create sprite sheet
    sprite_img = Image.new('RGBA', (sprite_width, sprite_height), (0, 0, 0, 0))
    sprite_json = {}

    # Place icons on sprite sheet
    for idx, (icon_name, img) in enumerate(sorted(icons.items())):
        col = idx % cols
        row = idx // cols
        x = col * icon_size
        y = row * icon_size

        sprite_img.paste(img, (x, y))

        # Add to JSON
        sprite_json[icon_name] = {
            "x": x,
            "y": y,
            "width": icon_size,
            "height": icon_size,
            "pixelRatio": 1,
            "sdf": False
        }

    # Save sprite sheet
    sprite_png_path = f"{output_prefix}.png"
    sprite_img.save(sprite_png_path)
    print(f"\nSaved sprite sheet: {sprite_png_path}")

    # Save JSON
    sprite_json_path = f"{output_prefix}.json"
    with open(sprite_json_path, 'w') as f:
        json.dump(sprite_json, f, indent=2)
    print(f"Saved sprite JSON: {sprite_json_path}")

    print(f"\nGenerated {len(icons)} icons in sprite sheet")

if __name__ == "__main__":
    import sys

    # Default parameters
    svg_directory = "svgs"
    output_prefix = "sprites"
    icon_size = 22

    # Check if SVG directory exists
    if not os.path.exists(svg_directory):
        print(f"Error: SVG directory '{svg_directory}' not found")
        print("\nUsage: python3 generate_sprites.py [svg_dir] [output_prefix] [icon_size]")
        print(f"Example: python3 generate_sprites.py all_maki_icons/svgs sprite 22")
        sys.exit(1)

    # Allow command line arguments
    if len(sys.argv) > 1:
        svg_directory = sys.argv[1]
    if len(sys.argv) > 2:
        output_prefix = sys.argv[2]
    if len(sys.argv) > 3:
        icon_size = int(sys.argv[3])

    print(f"SVG directory: {svg_directory}")
    print(f"Output prefix: {output_prefix}")
    print(f"Icon size: {icon_size}x{icon_size}\n")

    generate_sprite(svg_directory, output_prefix, icon_size)
