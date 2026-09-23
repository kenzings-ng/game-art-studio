#!/usr/bin/env python3
"""
Game Art Studio - Unreal Engine 5 Paper2D Flipbook Importer
Imports individual PNG frames, configures pixel filtering (Point/Nearest, No Mips),
creates UPaperSprite assets, and compiles them into a UPaperFlipbook asset.
"""

import argparse
import os
import sys

try:
    import unreal
except ImportError:
    unreal = None


def configure_pixel_texture(tex, tex_path):
    """
    Configures texture settings for crisp pixel art (Nearest filtering, No Mipmaps, Pixels2D LOD).
    """
    tex.set_editor_property('filter', unreal.TextureFilter.TF_NEAREST)
    tex.set_editor_property('mip_gen_settings', unreal.TextureMipGenSettings.TMGS_NO_MIPMAPS)

    # Resolve TextureGroup attribute across different Unreal Engine versions
    # In UE5 Python API, TextureGroup enum typically exposes TEXTUREGROUP_PIXELS2D or TEXTURE_GROUP_PIXELS2D
    lod_candidates = [
        'TEXTURE_GROUP_PIXELS2D',
        'TEXTUREGROUP_PIXELS2D',
        'TEXTURE_GROUP_PIXELS',
        'TEXTUREGROUP_PIXELS',
        'TEXTURE_GROUP_UI',
        'TEXTUREGROUP_UI',
        'PIXELS2D',
        'UI'
    ]
    set_lod = False
    for group_attr in lod_candidates:
        if hasattr(unreal.TextureGroup, group_attr):
            tex.set_editor_property('lod_group', getattr(unreal.TextureGroup, group_attr))
            set_lod = True
            break

    if not set_lod and hasattr(unreal, 'TextureGroup'):
        for attr in dir(unreal.TextureGroup):
            if 'PIXEL' in attr.upper():
                tex.set_editor_property('lod_group', getattr(unreal.TextureGroup, attr))
                set_lod = True
                break

    unreal.EditorAssetLibrary.save_asset(tex_path)


def import_texture_and_create_flipbook(png_frames_dir, ue_dest_path, flipbook_name, frames_per_second=12.0, pivot_mode="bottom_center"):
    """
    Imports individual PNG frames into Unreal Engine, configures pixel filtering,
    creates UPaperSprite assets from textures, and compiles them into a UPaperFlipbook.
    """
    if unreal is None:
        raise RuntimeError("Unreal Engine Python API ('unreal' module) is not available.")

    unreal.log(f"=== Game Art Studio: Importing Flipbook '{flipbook_name}' into {ue_dest_path} ===")

    asset_tools = unreal.AssetToolsHelpers.get_asset_tools()

    # 1. Gather all frames
    if not os.path.exists(png_frames_dir):
        unreal.log_error(f"Directory not found: {png_frames_dir}")
        return None

    frame_files = [os.path.join(png_frames_dir, f) for f in sorted(os.listdir(png_frames_dir)) if f.lower().endswith(".png")]
    if not frame_files:
        unreal.log_error(f"No PNG files found in {png_frames_dir}")
        return None

    textures_dest = f"{ue_dest_path}/textures"
    sprites_dest = f"{ue_dest_path}/sprites"

    tasks = []
    for f in frame_files:
        t = unreal.AssetImportTask()
        t.set_editor_property('filename', f)
        t.set_editor_property('destination_path', textures_dest)
        t.set_editor_property('destination_name', os.path.splitext(os.path.basename(f))[0])
        t.set_editor_property('replace_existing', True)
        t.set_editor_property('automated', True)
        t.set_editor_property('save', True)
        tasks.append(t)

    asset_tools.import_asset_tasks(tasks)

    # 2. Configure Pixel Filtering & collect loaded textures
    imported_textures = []
    for f in frame_files:
        base_name = os.path.splitext(os.path.basename(f))[0]
        tex_path = f"{textures_dest}/{base_name}"
        tex = unreal.EditorAssetLibrary.load_asset(tex_path)
        if tex:
            configure_pixel_texture(tex, tex_path)
            imported_textures.append((base_name, tex))
        else:
            unreal.log_warning(f"Could not load imported texture: {tex_path}")

    if not imported_textures:
        unreal.log_error(f"No textures were successfully loaded from {textures_dest}")
        return None

    # 3. Create UPaperSprite for each texture
    sprite_factory = unreal.PaperSpriteFactory()
    created_sprites = []

    # Determine pivot mode enum if available (avoid 'or' check so enum 0 isn't treated as falsy)
    pivot_enum_val = None
    if hasattr(unreal, 'SpritePivotMode'):
        if pivot_mode == "bottom_center":
            pivot_enum_val = getattr(unreal.SpritePivotMode, 'BOTTOM_CENTER', None)
            if pivot_enum_val is None:
                pivot_enum_val = getattr(unreal.SpritePivotMode, 'SPRITE_PIVOT_MODE_BOTTOM_CENTER', None)
        elif pivot_mode == "center":
            pivot_enum_val = getattr(unreal.SpritePivotMode, 'CENTER_CENTER', None)
            if pivot_enum_val is None:
                pivot_enum_val = getattr(unreal.SpritePivotMode, 'SPRITE_PIVOT_MODE_CENTER_CENTER', None)

    for base_name, tex in imported_textures:
        sprite_name = f"SP_{base_name}"
        sprite_full_path = f"{sprites_dest}/{sprite_name}"

        sprite = asset_tools.create_asset(sprite_name, sprites_dest, unreal.PaperSprite, sprite_factory)
        if sprite:
            sprite.set_editor_property('source_texture', tex)
            if pivot_enum_val is not None:
                sprite.set_editor_property('pivot_mode', pivot_enum_val)
            unreal.EditorAssetLibrary.save_asset(sprite_full_path)
            created_sprites.append(sprite)
        else:
            unreal.log_error(f"Failed to create UPaperSprite: {sprite_name}")

    if not created_sprites:
        unreal.log_error("No UPaperSprite assets were successfully created.")
        return None

    # 4. Create UPaperFlipbook and populate key frames
    flipbook_factory = unreal.PaperFlipbookFactory()
    flipbook_full_path = f"{ue_dest_path}/{flipbook_name}"

    fb = asset_tools.create_asset(flipbook_name, ue_dest_path, unreal.PaperFlipbook, flipbook_factory)
    if fb:
        key_frames = []
        for sprite in created_sprites:
            kf = unreal.PaperFlipbookKeyFrame()
            kf.set_editor_property('sprite', sprite)
            kf.set_editor_property('frame_run', 1)
            key_frames.append(kf)

        fb.set_editor_property('key_frames', key_frames)
        fb.set_editor_property('frames_per_second', float(frames_per_second))
        unreal.EditorAssetLibrary.save_asset(flipbook_full_path)
        unreal.log(f"Successfully created UPaperFlipbook at {flipbook_full_path} with {len(key_frames)} frames @ {frames_per_second} FPS")
        return fb

    return None


def main():
    parser = argparse.ArgumentParser(description="Unreal Engine 5 Paper2D Flipbook Importer")
    parser.add_argument("--frames_dir", required=True, help="Directory containing PNG frames")
    parser.add_argument("--dest_path", default="/Game/Art/Flipbooks", help="Unreal asset folder (e.g. /Game/Art/Flipbooks)")
    parser.add_argument("--name", "--flipbook_name", dest="flipbook_name", default=None, help="Name of the UPaperFlipbook asset")
    parser.add_argument("--fps", type=float, default=12.0, help="Frames per second (default: 12.0)")
    parser.add_argument("--pivot", choices=["bottom_center", "center"], default="bottom_center", help="Sprite pivot alignment")

    # Use parse_known_args to allow extra Unreal-specific flags without crashing
    args, _ = parser.parse_known_args()

    if unreal is None:
        print("Error: Unreal Engine Python API ('unreal' module) is not available in standard Python environment.", file=sys.stderr)
        print("Execute this script inside Unreal Editor or via UnrealEditor-Cmd with -ExecutePythonScript.", file=sys.stderr)
        sys.exit(1)

    name = args.flipbook_name
    if not name:
        name = os.path.basename(os.path.normpath(args.frames_dir)) or "FB_Animation"
        if not name.startswith("FB_"):
            name = f"FB_{name}"

    import_texture_and_create_flipbook(
        png_frames_dir=args.frames_dir,
        ue_dest_path=args.dest_path,
        flipbook_name=name,
        frames_per_second=args.fps,
        pivot_mode=args.pivot
    )


if __name__ == "__main__":
    main()
