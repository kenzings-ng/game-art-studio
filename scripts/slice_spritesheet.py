#!/usr/bin/env python3
"""
Game Art Studio - Spritesheet Slicer & Transparency Tool
Extracts animation frames from AI-generated spritesheets, removes solid backgrounds,
normalizes canvas bounds, and aligns bottom-center pivots.
"""

import os
import sys
import argparse
from PIL import Image
import numpy as np


def parse_color_key(color_key_str):
    """
    Parses a color_key string into:
    - 'auto': sample corners
    - 'none': do not remove background (preserve alpha)
    - (r, g, b): target RGB color tuple
    """
    if not color_key_str or color_key_str.lower() in ("auto", "sample"):
        return "auto"
    if color_key_str.lower() in ("none", "null", "false", "disabled"):
        return "none"

    named_colors = {
        "magenta": (255, 0, 255),
        "fuchsia": (255, 0, 255),
        "green": (0, 255, 0),
        "lime": (0, 255, 0),
        "black": (0, 0, 0),
        "white": (255, 255, 255),
        "cyan": (0, 255, 255)
    }
    key_lower = color_key_str.lower().strip()
    if key_lower in named_colors:
        return named_colors[key_lower]

    if key_lower.startswith("#"):
        hex_val = key_lower.lstrip("#")
        if len(hex_val) == 6:
            try:
                return tuple(int(hex_val[i:i+2], 16) for i in (0, 2, 4))
            except ValueError:
                pass

    return "auto"


def remove_background(img, color_key="auto", tolerance=30):
    """
    Replaces background color with full transparency.
    - If color_key is 'auto': samples from the 4 corners of the image.
    - If color_key is 'none': returns original image in RGBA without keying.
    - If color_key is an RGB tuple: removes that specific color within tolerance.
    """
    img = img.convert("RGBA")
    if color_key == "none":
        return img

    data = np.array(img)
    r, g, b, a = data[:, :, 0], data[:, :, 1], data[:, :, 2], data[:, :, 3]

    if color_key == "auto":
        corners = [
            data[0, 0, :3],
            data[0, -1, :3],
            data[-1, 0, :3],
            data[-1, -1, :3]
        ]
        bg_rgb = np.mean(corners, axis=0)
    else:
        bg_rgb = np.array(color_key[:3])

    diff = np.sqrt(
        (r.astype(float) - bg_rgb[0]) ** 2 +
        (g.astype(float) - bg_rgb[1]) ** 2 +
        (b.astype(float) - bg_rgb[2]) ** 2
    )

    mask = diff < tolerance
    data[mask, 3] = 0
    return Image.fromarray(data)


def slice_horizontal_strip(img, num_frames, output_dir, prefix="frame", anchor="bottom_center"):
    """
    Slices a horizontal strip into num_frames, trims excess padding, and standardizes canvas.
    Handles empty/blank frames safely without unintended cropping or clipping.
    """
    os.makedirs(output_dir, exist_ok=True)
    width, height = img.size
    frame_width = width // num_frames

    raw_frames = []
    max_w = 0
    max_h = 0

    for i in range(num_frames):
        box = (i * frame_width, 0, (i + 1) * frame_width, height)
        frame = img.crop(box)

        # Bounding box of non-transparent content
        bbox = frame.getbbox()
        if bbox:
            cropped = frame.crop(bbox)
            max_w = max(max_w, cropped.width)
            max_h = max(max_h, cropped.height)
            raw_frames.append(cropped)
        else:
            # Entirely transparent/empty frame. Store None to avoid size mismatch and clipping.
            raw_frames.append(None)

    # Fallback if every frame was empty
    if max_w == 0 or max_h == 0:
        max_w = max(1, frame_width)
        max_h = max(1, height)

    # Add a safety margin to canvas
    canvas_w = max_w + 8
    canvas_h = max_h + 8

    saved_paths = []
    for i, frame in enumerate(raw_frames):
        canvas = Image.new("RGBA", (canvas_w, canvas_h), (0, 0, 0, 0))

        if frame is not None:
            if anchor == "bottom_center":
                paste_x = (canvas_w - frame.width) // 2
                paste_y = canvas_h - frame.height - 4  # 4px padding from bottom
            elif anchor == "center":
                paste_x = (canvas_w - frame.width) // 2
                paste_y = (canvas_h - frame.height) // 2
            else:
                paste_x = 0
                paste_y = 0

            canvas.paste(frame, (paste_x, paste_y), frame)

        out_path = os.path.join(output_dir, f"{prefix}_{i:02d}.png")
        canvas.save(out_path, "PNG")
        saved_paths.append(out_path)

    print(f"Extracted {len(saved_paths)} frames to {output_dir} (Canvas: {canvas_w}x{canvas_h})")
    return saved_paths


def process_single_sheet(input_path, output_dir, frames, prefix, color_key, tolerance, anchor):
    parsed_key = parse_color_key(color_key)
    src_img = Image.open(input_path)
    transparent_img = remove_background(src_img, color_key=parsed_key, tolerance=tolerance)
    return slice_horizontal_strip(transparent_img, frames, output_dir, prefix=prefix, anchor=anchor)


def main():
    parser = argparse.ArgumentParser(description="Slice spritesheets with auto-transparency and anchor alignment")
    parser.add_argument("--input", "--input_sheet", dest="input", default=None, help="Path to input spritesheet image")
    parser.add_argument("--batch_dir", default=None, help="Process all spritesheets in this directory")
    parser.add_argument("--output_dir", required=True, help="Directory to save extracted frames")
    parser.add_argument("--frames", type=int, default=6, help="Number of horizontal animation frames")
    parser.add_argument("--prefix", default="frame", help="Prefix for output frame filenames")
    parser.add_argument("--color_key", default="auto", help="Background keying color: 'auto', 'none', '#FF00FF', 'magenta', etc.")
    parser.add_argument("--tolerance", type=int, default=35, help="Color tolerance for background keying")
    parser.add_argument("--anchor", choices=["bottom_center", "center", "none"], default="bottom_center")

    args = parser.parse_args()

    if not args.input and not args.batch_dir:
        print("Error: Either --input or --batch_dir must be specified.", file=sys.stderr)
        sys.exit(1)

    if args.batch_dir:
        if not os.path.exists(args.batch_dir):
            print(f"Error: Batch directory not found: {args.batch_dir}", file=sys.stderr)
            sys.exit(1)

        valid_exts = (".png", ".jpg", ".jpeg", ".webp")
        sheet_files = sorted([f for f in os.listdir(args.batch_dir) if f.lower().endswith(valid_exts)])
        if not sheet_files:
            print(f"No image files found in {args.batch_dir}", file=sys.stderr)
            sys.exit(1)

        total_extracted = 0
        for sheet_f in sheet_files:
            sheet_path = os.path.join(args.batch_dir, sheet_f)
            sheet_name = os.path.splitext(sheet_f)[0]
            sheet_out = os.path.join(args.output_dir, sheet_name)
            res = process_single_sheet(sheet_path, sheet_out, args.frames, args.prefix, args.color_key, args.tolerance, args.anchor)
            total_extracted += len(res)

        print(f"=== Batch Complete: Processed {len(sheet_files)} sheets ({total_extracted} total frames) ===")
    else:
        if not os.path.exists(args.input):
            print(f"Error: Input file not found: {args.input}", file=sys.stderr)
            sys.exit(1)

        process_single_sheet(args.input, args.output_dir, args.frames, args.prefix, args.color_key, args.tolerance, args.anchor)


if __name__ == "__main__":
    main()
