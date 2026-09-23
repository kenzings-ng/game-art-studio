#!/usr/bin/env python3
"""
Game Art Studio - Spritesheet Slicer & Transparency Tool
Extracts animation frames from AI-generated spritesheets, removes solid backgrounds,
normalizes canvas bounds, and aligns bottom-center pivots.
"""

import os
import sys
import argparse
from PIL import Image, ImageOps
import numpy as np

def remove_background(img, bg_color=None, tolerance=30):
    """
    Replaces background color with full transparency.
    If bg_color is None, samples from the 4 corners of the image.
    """
    img = img.convert("RGBA")
    data = np.array(img)
    
    r, g, b, a = data[:, :, 0], data[:, :, 1], data[:, :, 2], data[:, :, 3]
    
    if bg_color is None:
        # Sample corners
        corners = [
            data[0, 0, :3],
            data[0, -1, :3],
            data[-1, 0, :3],
            data[-1, -1, :3]
        ]
        # Average corner color
        bg_rgb = np.mean(corners, axis=0)
    else:
        bg_rgb = np.array(bg_color[:3])
        
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
            raw_frames.append(frame)
            
    # Add a safety margin to canvas
    canvas_w = max_w + 8
    canvas_h = max_h + 8
    
    saved_paths = []
    for i, frame in enumerate(raw_frames):
        canvas = Image.new("RGBA", (canvas_w, canvas_h), (0, 0, 0, 0))
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

def main():
    parser = argparse.ArgumentParser(description="Slice spritesheets with auto-transparency and anchor alignment")
    parser.add_argument("--input", required=True, help="Path to input spritesheet image")
    parser.add_argument("--output_dir", required=True, help="Directory to save extracted frames")
    parser.add_argument("--frames", type=int, default=6, help="Number of horizontal animation frames")
    parser.add_argument("--prefix", default="frame", help="Prefix for output frame filenames")
    parser.add_argument("--tolerance", type=int, default=35, help="Color tolerance for background keying")
    parser.add_argument("--anchor", choices=["bottom_center", "center", "none"], default="bottom_center")
    
    args = parser.parse_args()
    
    if not os.path.exists(args.input):
        print(f"Error: Input file not found: {args.input}", file=sys.stderr)
        sys.exit(1)
        
    src_img = Image.open(args.input)
    transparent_img = remove_background(src_img, tolerance=args.tolerance)
    slice_horizontal_strip(transparent_img, args.frames, args.output_dir, prefix=args.prefix, anchor=args.anchor)

if __name__ == "__main__":
    main()
