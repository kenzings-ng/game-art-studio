#!/usr/bin/env python3
"""
Game Art Studio - Automated Asset QA & Anti-AI Verification Tool
Verifies:
1. Palette discipline (Flags unquantized AI color bleed / excessive micro-colors)
2. Directional motion padding (Flags edge-touching clipping)
3. Animation frame pacing consistency (Flags sudden bbox size jumps)
4. 2.5D Isometric Diamond grid boundary compliance (128x64 seam detection)
"""

import os
import sys
import argparse
from PIL import Image
import numpy as np


PRESET_COLOR_BUDGETS = {
    "stardew": 16,
    "pico8": 16,
    "cps2": 32,
    "gba": 48,
    "hd": 256,
}


def analyze_palette(image):
    """Returns the set of unique RGB colors in non-transparent pixels."""
    im = image.convert("RGBA")
    data = np.array(im)
    alpha = data[:, :, 3]
    visible_mask = alpha > 10  # ignore near-zero alpha
    visible_pixels = data[visible_mask][:, :3]
    if len(visible_pixels) == 0:
        return set()
    # Unique colors
    unique_colors = np.unique(visible_pixels, axis=0)
    return set(tuple(c) for c in unique_colors)


def check_clipping(image, margin=1):
    """
    Checks if non-transparent pixels touch or come within `margin` px of canvas bounds.
    Returns (is_clipped, edges_touched).
    """
    im = image.convert("RGBA")
    bbox = im.getbbox()
    if bbox is None:
        return False, []

    w, h = im.size
    left, top, right, bottom = bbox
    touched = []

    if left <= margin:
        touched.append("left")
    if top <= margin:
        touched.append("top")
    if right >= w - margin:
        touched.append("right")
    if bottom >= h - margin:
        touched.append("bottom")

    return len(touched) > 0, touched


def validate_animation_frames(frames_dir, max_colors=16, margin=1, max_jump_ratio=0.55):
    """
    Validates a sequence of PNG frames in a directory.
    Reports warnings and errors.
    """
    if not os.path.exists(frames_dir):
        print(f"Error: Directory not found: {frames_dir}", file=sys.stderr)
        return False, ["Directory not found"]

    files = sorted([f for f in os.listdir(frames_dir) if f.lower().endswith(".png")])
    if not files:
        print(f"Error: No PNG frames found in {frames_dir}", file=sys.stderr)
        return False, ["No PNG files found"]

    all_colors = set()
    warnings = []
    frame_bboxes = []
    frame_sizes = []

    for idx, fname in enumerate(files):
        fpath = os.path.join(frames_dir, fname)
        with Image.open(fpath) as im:
            frame_sizes.append(im.size)
            colors = analyze_palette(im)
            all_colors.update(colors)

            # Check clipping
            is_clipped, edges = check_clipping(im, margin=margin)
            if is_clipped:
                warnings.append(
                    f"Frame {fname}: Motion padding warning! Non-transparent pixels touch {','.join(edges)} edge(s)."
                )

            bbox = im.getbbox()
            frame_bboxes.append(bbox)

    # 1. Check canvas size consistency
    first_size = frame_sizes[0]
    for idx, sz in enumerate(frame_sizes):
        if sz != first_size:
            warnings.append(
                f"Frame {files[idx]}: Canvas dimension mismatch! Expected {first_size}, found {sz}."
            )

    # 2. Check palette budget
    if max_colors is not None and len(all_colors) > max_colors:
        warnings.append(
            f"Palette Budget Exceeded: Asset uses {len(all_colors)} unique colors (budget: {max_colors}). "
            f"Contains unquantized AI micro-gradients."
        )

    # 3. Check frame-to-frame size stability (jitter/glitch detection)
    for i in range(len(frame_bboxes) - 1):
        b1 = frame_bboxes[i]
        b2 = frame_bboxes[i + 1]
        if b1 and b2:
            w1 = b1[2] - b1[0]
            h1 = b1[3] - b1[1]
            w2 = b2[2] - b2[0]
            h2 = b2[3] - b2[1]

            area1 = max(w1 * h1, 1)
            area2 = max(w2 * h2, 1)
            ratio = abs(area1 - area2) / max(area1, area2)

            if ratio > max_jump_ratio:
                warnings.append(
                    f"Frame Jitter: Large bbox jump between {files[i]} and {files[i+1]} "
                    f"({area1}px vs {area2}px, delta: {ratio:.1%})."
                )

    passed = len(warnings) == 0
    return passed, warnings


def validate_isometric_tile(tile_path, base_width=128, base_height=64, tolerance=0.04):
    """
    Validates that a 2.5D Isometric Diamond tile strictly conforms to the 2:1 dimetric ratio.
    Checks for out-of-bounds pixel leakage that causes seam overlapping on tilemaps.
    Diamond equation: |x - center_x| / (W / 2) + |y - center_y| / (H / 2) <= 1.0
    """
    if not os.path.exists(tile_path):
        return False, [f"File not found: {tile_path}"]

    warnings = []
    with Image.open(tile_path) as im:
        im = im.convert("RGBA")
        w, h = im.size

        if w != base_width or h != base_height:
            warnings.append(f"Dimensions mismatch: Expected {base_width}x{base_height}, got {w}x{h}.")

        data = np.array(im)
        alpha = data[:, :, 3]

        center_x = (w - 1) / 2.0
        center_y = (h - 1) / 2.0
        radius_x = w / 2.0
        radius_y = h / 2.0

        # Calculate normalized diamond distance for each pixel
        y_indices, x_indices = np.indices((h, w))
        dist = (np.abs(x_indices - center_x) / radius_x) + (np.abs(y_indices - center_y) / radius_y)

        # Detect pixels with visible alpha outside the diamond boundary
        leaking_pixels = (dist > (1.0 + tolerance)) & (alpha > 20)
        num_leaking = np.sum(leaking_pixels)

        if num_leaking > 0:
            warnings.append(
                f"Isometric Seam Defect: Found {num_leaking} non-transparent pixels leaking outside the "
                f"2:1 diamond boundary ({base_width}x{base_height}). Will cause tile seams!"
            )

    passed = len(warnings) == 0
    return passed, warnings


def main():
    parser = argparse.ArgumentParser(description="Automated Game Asset Quality Assurance & Anti-AI Verification")
    parser.add_argument("--frames_dir", default=None, help="Directory of sliced animation frames to inspect")
    parser.add_argument("--tile", default=None, help="Path to an isometric diamond tile to inspect")
    parser.add_argument("--preset", choices=list(PRESET_COLOR_BUDGETS.keys()), default=None,
                        help="Asset preset to enforce (stardew, pico8, cps2, gba, hd)")
    parser.add_argument("--max_colors", type=int, default=None, help="Explicit maximum allowed unique colors")
    parser.add_argument("--tile_width", type=int, default=128, help="Expected isometric tile width (default: 128)")
    parser.add_argument("--tile_height", type=int, default=64, help="Expected isometric tile height (default: 64)")
    parser.add_argument("--strict", action="store_true", help="Exit with code 1 if any warning is reported")

    args = parser.parse_args()

    if not args.frames_dir and not args.tile:
        parser.print_help()
        sys.exit(1)

    max_colors = args.max_colors
    if max_colors is None and args.preset:
        max_colors = PRESET_COLOR_BUDGETS.get(args.preset)

    total_warnings = []

    if args.frames_dir:
        print(f"=== Inspecting Animation Frames: {args.frames_dir} ===")
        passed, warnings = validate_animation_frames(args.frames_dir, max_colors=max_colors)
        if passed:
            print("✅ All animation frame checks passed! (Zero clipping, consistent canvas, strict palette).")
        else:
            for w in warnings:
                print(f"⚠️  {w}")
            total_warnings.extend(warnings)

    if args.tile:
        print(f"\n=== Inspecting Isometric Tile: {args.tile} ===")
        passed, warnings = validate_isometric_tile(
            args.tile, base_width=args.tile_width, base_height=args.tile_height
        )
        if passed:
            print("✅ Isometric diamond boundary check passed! (No leaking seam pixels).")
        else:
            for w in warnings:
                print(f"⚠️  {w}")
            total_warnings.extend(warnings)

    if total_warnings and args.strict:
        print(f"\n❌ QA Validation Failed ({len(total_warnings)} warnings in strict mode).", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
