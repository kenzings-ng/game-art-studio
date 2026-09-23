#!/usr/bin/env python3
"""
Game Art Studio - Flipbook GIF Assembler
Takes a directory of sequentially numbered PNG frames and creates an animated GIF
with custom frame rate, loop count, and optional upscale/palette quantization.
"""

import os
import sys
import glob
import argparse
from PIL import Image

def assemble_gif(frames_dir, output_gif, fps=12.0, loop=0, scale=1):
    frame_files = sorted(glob.glob(os.path.join(frames_dir, "*.png")))
    if not frame_files:
        print(f"Error: No PNG frames found in {frames_dir}", file=sys.stderr)
        return False
        
    images = []
    duration_ms = int(1000.0 / max(1.0, fps))
    
    for f in frame_files:
        img = Image.open(f).convert("RGBA")
        if scale > 1:
            img = img.resize((img.width * scale, img.height * scale), Image.NEAREST)
        images.append(img)
        
    # Convert RGBA to palette mode with transparency support
    palette_images = []
    for img in images:
        alpha = img.split()[3]
        p_img = img.convert("RGB").convert("P", palette=Image.ADAPTIVE, colors=255)
        # Set mask for transparent pixels
        mask = Image.eval(alpha, lambda a: 255 if a < 128 else 0)
        p_img.paste(255, mask)
        p_img.info["transparency"] = 255
        palette_images.append(p_img)
        
    os.makedirs(os.path.dirname(os.path.abspath(output_gif)), exist_ok=True)
    palette_images[0].save(
        output_gif,
        save_all=True,
        append_images=palette_images[1:],
        duration=duration_ms,
        loop=loop,
        disposal=2
    )
    
    print(f"Successfully generated GIF: {output_gif} ({len(palette_images)} frames @ {fps} FPS, {duration_ms}ms/frame)")
    return True

def main():
    parser = argparse.ArgumentParser(description="Assemble sequential PNG frames into animated GIF")
    parser.add_argument("--frames_dir", required=True, help="Directory containing input PNG frames")
    parser.add_argument("--output_gif", required=True, help="Destination GIF path")
    parser.add_argument("--fps", type=float, default=12.0, help="Frames per second (default 12.0)")
    parser.add_argument("--loop", type=int, default=0, help="0 for infinite loop, N for N loops")
    parser.add_argument("--scale", type=int, default=1, help="Integer upscale factor (e.g. 2 for 2x nearest-neighbor)")
    
    args = parser.parse_args()
    assemble_gif(args.frames_dir, args.output_gif, fps=args.fps, loop=args.loop, scale=args.scale)

if __name__ == "__main__":
    main()
