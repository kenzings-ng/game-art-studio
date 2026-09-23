#!/usr/bin/env python3
"""
Game Art Studio - Item Icon & Rarity Frame Generator
Slices item icon grids (weapons, armor, potions, tomes) and applies standardized 5-tier
colored borders (Common, Uncommon, Rare, Epic, Legendary) for inventory and quickbars.
"""

import os
import sys
import argparse
from PIL import Image, ImageDraw

# 5-Tier Rarity Color Palette
RARITY_COLORS = {
    "common": (156, 163, 175, 255),       # Gray #9CA3AF
    "uncommon": (34, 197, 94, 255),       # Green #22C55E
    "rare": (59, 130, 246, 255),          # Blue #3B82F6
    "epic": (168, 85, 247, 255),          # Purple #A855F7
    "legendary": (245, 158, 11, 255),     # Gold #F59E0B
}

def apply_rarity_border(icon_img, rarity="common", border_width=2):
    """
    Applies a clean 16-bit style colored frame around an icon.
    """
    icon_img = icon_img.convert("RGBA")
    w, h = icon_img.size
    color = RARITY_COLORS.get(rarity.lower(), RARITY_COLORS["common"])

    draw = ImageDraw.Draw(icon_img)
    for b in range(border_width):
        draw.rectangle([b, b, w - 1 - b, h - 1 - b], outline=color)

    return icon_img

def slice_icon_grid(grid_image_path, output_dir, rows=4, cols=4, icon_size=(64, 64), default_rarity="common"):
    os.makedirs(output_dir, exist_ok=True)
    img = Image.open(grid_image_path).convert("RGBA")

    cell_w = img.width // cols
    cell_h = img.height // rows

    saved = []
    idx = 0
    for r in range(rows):
        for c in range(cols):
            box = (c * cell_w, r * cell_h, (c + 1) * cell_w, (r + 1) * cell_h)
            cell = img.crop(box)
            if icon_size:
                cell = cell.resize(icon_size, Image.NEAREST)
            cell = apply_rarity_border(cell, rarity=default_rarity)
            out_file = os.path.join(output_dir, f"icon_{idx:03d}.png")
            cell.save(out_file, "PNG")
            saved.append(out_file)
            idx += 1

    print(f"Generated {len(saved)} icons at {output_dir} ({cols}x{rows} grid, rarity: {default_rarity})")
    return saved

def parse_grid_dimensions(grid_str):
    """Parses '4x4', '4X4', or '4' into (rows, cols)."""
    if not grid_str:
        return None, None
    s = grid_str.lower().strip()
    if 'x' in s:
        parts = s.split('x')
        try:
            return int(parts[0]), int(parts[1])
        except ValueError:
            pass
    elif s.isdigit():
        val = int(s)
        return val, val
    return None, None

def main():
    parser = argparse.ArgumentParser(description="Slice and frame item icons with 5-tier rarity colors")
    parser.add_argument("--input", "--input_sheet", dest="input", required=True, help="Input icon grid image")
    parser.add_argument("--output_dir", required=True, help="Output folder")
    parser.add_argument("--grid", default=None, help="Grid format like '4x4' or '4' (sets both rows and cols)")
    parser.add_argument("--rows", type=int, default=None, help="Grid rows (default: 4 or parsed from --grid)")
    parser.add_argument("--cols", type=int, default=None, help="Grid columns (default: 4 or parsed from --grid)")
    parser.add_argument("--rarity", choices=["common", "uncommon", "rare", "epic", "legendary"], default="common")

    args = parser.parse_args()

    # Resolve grid dimensions
    grid_rows, grid_cols = parse_grid_dimensions(args.grid)
    final_rows = args.rows if args.rows is not None else (grid_rows if grid_rows is not None else 4)
    final_cols = args.cols if args.cols is not None else (grid_cols if grid_cols is not None else 4)

    if not os.path.exists(args.input):
        print(f"Error: Input file not found: {args.input}", file=sys.stderr)
        sys.exit(1)

    slice_icon_grid(args.input, args.output_dir, rows=final_rows, cols=final_cols, default_rarity=args.rarity)

if __name__ == "__main__":
    main()
