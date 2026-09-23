#!/usr/bin/env python3
"""
Game Art Studio - Godot 4 SpriteFrames & AnimatedSprite2D Importer
Generates native Godot 4 .tres (SpriteFrames) and optional .tscn (AnimatedSprite2D) scene
from a sequence of sliced PNG animation frames without requiring Godot Editor binary.
"""

import argparse
import os
import sys
import uuid


def generate_godot_uid():
    """Generates a random Godot-compatible UID string."""
    return f"uid://{uuid.uuid4().hex[:12]}"


def create_godot_sprite_frames(
    frames_dir,
    output_tres_path,
    godot_res_dir="res://art",
    anim_name="default",
    fps=12.0,
    loop=True,
    generate_scene=False
):
    """
    Creates a native Godot 4 SpriteFrames (.tres) text resource.
    Optionally creates a ready-to-use AnimatedSprite2D (.tscn) scene file.
    """
    if not os.path.exists(frames_dir):
        print(f"Error: Frames directory not found: {frames_dir}", file=sys.stderr)
        return False

    png_files = sorted([f for f in os.listdir(frames_dir) if f.lower().endswith(".png")])
    if not png_files:
        print(f"Error: No PNG frames found in {frames_dir}", file=sys.stderr)
        return False

    godot_res_dir = godot_res_dir.rstrip("/")
    load_steps = len(png_files) + 1
    tres_uid = generate_godot_uid()

    # Build ExtResource entries
    ext_resources = []
    frame_blocks = []

    for idx, fname in enumerate(png_files, start=1):
        ext_id = f"{idx}_{os.path.splitext(fname)[0]}"
        res_path = f"{godot_res_dir}/{fname}"
        ext_uid = generate_godot_uid()
        ext_resources.append(f'[ext_resource type="Texture2D" uid="{ext_uid}" path="{res_path}" id="{ext_id}"]')

        frame_blocks.append(f'\t{{\n\t\t"duration": 1.0,\n\t\t"texture": ExtResource("{ext_id}")\n\t}}')

    formatted_frames = ",\n".join(frame_blocks)

    tres_content = f"""[gd_resource type="SpriteFrames" load_steps={load_steps} format=3 uid="{tres_uid}"]

{chr(10).join(ext_resources)}

[resource]
animations = [{{
\t"frames": [
{formatted_frames}
\t],
\t"loop": {"true" if loop else "false"},
\t"name": &"{anim_name}",
\t"speed": {float(fps)}
}}]
"""

    os.makedirs(os.path.dirname(os.path.abspath(output_tres_path)), exist_ok=True)
    with open(output_tres_path, "w", encoding="utf-8") as f:
        f.write(tres_content)

    print(f"Successfully generated Godot 4 SpriteFrames: {output_tres_path} ({len(png_files)} frames @ {fps} FPS)")

    # Optionally generate .tscn AnimatedSprite2D
    if generate_scene:
        scene_path = os.path.splitext(output_tres_path)[0] + ".tscn"
        tres_filename = os.path.basename(output_tres_path)
        scene_res_path = f"{godot_res_dir}/{tres_filename}"
        node_name = os.path.splitext(os.path.basename(output_tres_path))[0]
        scene_uid = generate_godot_uid()

        tscn_content = f"""[gd_scene load_steps=2 format=3 uid="{scene_uid}"]

[ext_resource type="SpriteFrames" uid="{tres_uid}" path="{scene_res_path}" id="1_frames"]

[node name="{node_name}" type="AnimatedSprite2D"]
sprite_frames = ExtResource("1_frames")
animation = &"{anim_name}"
autoplay = "{anim_name}"
"""
        with open(scene_path, "w", encoding="utf-8") as f:
            f.write(tscn_content)

        print(f"Successfully generated Godot 4 AnimatedSprite2D scene: {scene_path}")

    return True


def main():
    parser = argparse.ArgumentParser(description="Generate native Godot 4 SpriteFrames (.tres) from PNG animation frames")
    parser.add_argument("--frames_dir", required=True, help="Directory containing sliced PNG frames")
    parser.add_argument("--output_tres", default=None, help="Output path for .tres file (default: <frames_dir>/<anim_name>.tres)")
    parser.add_argument("--godot_res_dir", default="res://art", help="Godot internal res:// path prefix (default: res://art)")
    parser.add_argument("--anim_name", default="default", help="Animation name in SpriteFrames (default: default)")
    parser.add_argument("--fps", type=float, default=12.0, help="Playback speed in frames per second (default: 12.0)")
    parser.add_argument("--no_loop", action="store_true", help="Disable animation looping")
    parser.add_argument("--generate_scene", action="store_true", help="Also generate an AnimatedSprite2D .tscn scene file")

    args = parser.parse_args()

    output_tres = args.output_tres
    if not output_tres:
        output_tres = os.path.join(args.frames_dir, f"{args.anim_name}.tres")

    success = create_godot_sprite_frames(
        frames_dir=args.frames_dir,
        output_tres_path=output_tres,
        godot_res_dir=args.godot_res_dir,
        anim_name=args.anim_name,
        fps=args.fps,
        loop=not args.no_loop,
        generate_scene=args.generate_scene
    )

    if not success:
        sys.exit(1)


if __name__ == "__main__":
    main()
