import unreal
import os
import sys

def import_texture_and_create_flipbook(png_frames_dir, ue_dest_path, flipbook_name, frames_per_second=12.0):
    """
    Imports individual PNG frames into Unreal Engine, configures pixel filtering,
    creates PaperSprites, and compiles them into a UPaperFlipbook.
    """
    unreal.log(f"=== Game Art Studio: Importing Flipbook '{flipbook_name}' into {ue_dest_path} ===")
    
    asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
    
    # 1. Gather all frames
    frame_files = [os.path.join(png_frames_dir, f) for f in sorted(os.listdir(png_frames_dir)) if f.endswith(".png")]
    if not frame_files:
        unreal.log_error(f"No PNG files found in {png_frames_dir}")
        return None
        
    tasks = []
    for f in frame_files:
        t = unreal.AssetImportTask()
        t.set_editor_property('filename', f)
        t.set_editor_property('destination_path', f"{ue_dest_path}/textures")
        t.set_editor_property('destination_name', os.path.splitext(os.path.basename(f))[0])
        t.set_editor_property('replace_existing', True)
        t.set_editor_property('automated', True)
        t.set_editor_property('save', True)
        tasks.append(t)
        
    asset_tools.import_asset_tasks(tasks)
    
    # 2. Configure Pixel Filtering (TF_NEAREST, TMGS_NO_MIPMAPS, TEXTUREGROUP_Pixels)
    imported_textures = []
    for f in frame_files:
        base_name = os.path.splitext(os.path.basename(f))[0]
        tex_path = f"{ue_dest_path}/textures/{base_name}"
        tex = unreal.EditorAssetLibrary.load_asset(tex_path)
        if tex:
            tex.set_editor_property('filter', unreal.TextureFilter.TF_NEAREST)
            tex.set_editor_property('mip_gen_settings', unreal.TextureMipGenSettings.TMGS_NO_MIPMAPS)
            for group_attr in ['TEXTUREGROUP_PIXELS', 'TEXTURE_GROUP_PIXELS', 'TEXTURE_GROUP_UI']:
                if hasattr(unreal.TextureGroup, group_attr):
                    tex.set_editor_property('lod_group', getattr(unreal.TextureGroup, group_attr))
                    break
            unreal.EditorAssetLibrary.save_asset(tex_path)
            imported_textures.append(tex)
            
    # 3. Create PaperFlipbook
    flipbook_factory = unreal.PaperFlipbookFactory()
    flipbook_full_path = f"{ue_dest_path}/{flipbook_name}"
    
    fb = asset_tools.create_asset(flipbook_name, ue_dest_path, unreal.PaperFlipbook, flipbook_factory)
    if fb:
        fb.set_editor_property('frames_per_second', float(frames_per_second))
        unreal.EditorAssetLibrary.save_asset(flipbook_full_path)
        unreal.log(f"Successfully created UPaperFlipbook at {flipbook_full_path} @ {frames_per_second} FPS")
        return fb
        
    return None
