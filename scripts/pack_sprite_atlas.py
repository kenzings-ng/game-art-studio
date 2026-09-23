#!/usr/bin/env python3
"""
Game Art Studio - TexturePacker Sprite Atlas & JSON Exporter
Packs individual sprite frames into a unified texture atlas PNG and standard
TexturePacker JSON format for direct use in Godot, Unity, PixiJS, Phaser, and Defold.
"""

import os
import sys
import json
import math
import argparse
from PIL import Image


def next_power_of_two(val):
    """Returns the smallest power of 2 >= val."""
    if val <= 0:
        return 1
    return 2 ** math.ceil(math.log2(val))


def pack_frames(frames_dir, padding=2, power_of_two=True):
    """
    Packs all PNG images in frames_dir using a shelf-packing algorithm.
    Returns (atlas_image, texture_packer_dict).
    """
    if not os.path.exists(frames_dir):
        raise FileNotFoundError(f"Directory not found: {frames_dir}")

    files = sorted([f for f in os.listdir(frames_dir) if f.lower().endswith(".png")])
    if not files:
        raise ValueError(f"No PNG files found in {frames_dir}")

    sprites = []
    for f in files:
        im = Image.open(os.path.join(frames_dir, f)).convert("RGBA")
        sprites.append({"name": f, "image": im, "w": im.width, "h": im.height})

    # Sort sprites by height descending for efficient packing
    sprites.sort(key=lambda s: s["h"], reverse=True)

    # Estimate required width
    total_area = sum((s["w"] + padding) * (s["h"] + padding) for s in sprites)
    target_width = max(int(math.sqrt(total_area) * 1.2), max(s["w"] for s in sprites) + padding)
    if power_of_two:
        target_width = next_power_of_two(target_width)

    # Shelf packing
    current_x = padding
    current_y = padding
    shelf_height = 0
    max_x = 0
    max_y = 0

    placements = []

    for s in sprites:
        w, h = s["w"], s["h"]
        if current_x + w + padding > target_width:
            # Move to next shelf
            current_x = padding
            current_y += shelf_height + padding
            shelf_height = 0

        placements.append({
            "name": s["name"],
            "image": s["image"],
            "x": current_x,
            "y": current_y,
            "w": w,
            "h": h
        })

        shelf_height = max(shelf_height, h)
        current_x += w + padding
        max_x = max(max_x, current_x)
        max_y = max(max_y, current_y + shelf_height + padding)

    atlas_w = max_x
    atlas_h = max_y

    if power_of_two:
        atlas_w = next_power_of_two(atlas_w)
        atlas_h = next_power_of_two(atlas_h)

    # Assemble Atlas Image
    atlas_img = Image.new("RGBA", (atlas_w, atlas_h), (0, 0, 0, 0))
    frames_dict = {}

    for p in placements:
        atlas_img.paste(p["image"], (p["x"], p["y"]), p["image"])
        frames_dict[p["name"]] = {
            "frame": {"x": p["x"], "y": p["y"], "w": p["w"], "h": p["h"]},
            "rotated": False,
            "trimmed": False,
            "spriteSourceSize": {"x": 0, "y": 0, "w": p["w"], "h": p["h"]},
            "sourceSize": {"w": p["w"], "h": p["h"]}
        }

    atlas_json = {
        "frames": frames_dict,
        "meta": {
            "app": "Game Art Studio TexturePacker Exporter",
            "version": "1.0",
            "image": "atlas.png",
            "format": "RGBA8888",
            "size": {"w": atlas_w, "h": atlas_h},
            "scale": "1"
        }
    }

    return atlas_img, atlas_json


def main():
    parser = argparse.ArgumentParser(description="Pack sprite frames into TexturePacker Atlas PNG + JSON")
    parser.add_argument("--frames_dir", required=True, help="Directory containing PNG sprite frames")
    parser.add_argument("--output_atlas", default=None, help="Output atlas PNG path (default: <frames_dir>/atlas.png)")
    parser.add_argument("--output_json", default=None, help="Output JSON path (default: <frames_dir>/atlas.json)")
    parser.add_argument("--padding", type=int, default=2, help="Padding in pixels between sprites (default: 2)")
    parser.add_argument("--no_pot", action="store_true", help="Disable padding canvas to nearest power of two")

    args = parser.parse_args()

    out_atlas = args.output_atlas or os.path.join(args.frames_dir, "atlas.png")
    out_json = args.output_json or os.path.join(args.frames_dir, "atlas.json")

    atlas_img, atlas_data = pack_frames(
        args.frames_dir, padding=args.padding, power_of_two=not args.no_pot
    )

    atlas_data["meta"]["image"] = os.path.basename(out_atlas)

    os.makedirs(os.path.dirname(os.path.abspath(out_atlas)), exist_ok=True)
    atlas_img.save(out_atlas, "PNG")

    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(atlas_data, f, indent=2)

    print(f"✅ Successfully packed {len(atlas_data['frames'])} sprites into Atlas:")
    print(f"   Atlas Image: {out_atlas} ({atlas_img.width}x{atlas_img.height})")
    print(f"   TexturePacker JSON: {out_json}")


if __name__ == "__main__":
    main()
