# 🎨 Game Art Studio

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Engine: Unreal Engine 5](https://img.shields.io/badge/Unreal%20Engine-5.8%20%7C%20Paper2D%20%7C%20PaperZD-blue.svg)](https://unrealengine.com)
[![Engine: Godot 4](https://img.shields.io/badge/Godot-4.x%20%7C%20SpriteFrames-478cbf.svg)](https://godotengine.org)
[![Architecture: Meowa AI](https://img.shields.io/badge/Architecture-Meowa%20Open--Source-orange.svg)](https://github.com/Meowa-AI/meowa-skills)
[![CI: Test & Lint](https://github.com/kenzings-ng/game-art-studio/actions/workflows/ci.yml/badge.svg)](https://github.com/kenzings-ng/game-art-studio/actions)

> **Game Art Studio** is an end-to-end Game Art & Asset Production Studio powered by the open-source **Meowa AI** architecture. It provides production-ready pipelines for 2D pixel & HD game assets, 8-directional character spritesheets, action-first animations, 2.5D isometric diamond ($128 \times 64$) tilesets, dual-grid autotiling atlases, 5-tier RPG item icons, interactive browser previewers, direct Unreal Engine 5 & Godot 4 flipbook generation, automated asset QA verification, and an **Anti-AI Handcrafted Art Styling Engine** that eliminates synthetic "AI slop".

---

## ✨ Key Features

1. **Mandatory Asset Contract Protocol**:
   - Zero-guesswork design: Locks down art style, pixel grid resolution, view angle, and shading rules before generation.
   - Built-in presets for **Stardew Valley 16×16**, **Capcom CPS2 32-bit**, **Hollow Knight 2D**, **Hades Chiaroscuro**, and **Pokémon GBA**.
2. **Anti-AI Handcrafted Art Directives**:
   - **Line of Action & Dynamic Silhouettes**: Dynamic C/S-curve spine, contrapposto weight distribution, and high-readability blackout silhouette test.
   - **Hue-Shifting Color Theory**: Warm golden highlights shifting into cool indigo/violet shadows—never muddy gray/black shadows.
   - **70-20-10 Shape Hierarchy**: 70% clean resting surfaces, 20% functional shapes, 10% micro-accents. Strictly bans random ornamental AI filigree (greeble).
   - **No Pillow Shading**: Single directional key light at $45^\circ$ with crisp cel-shaded plane shifts and hard cast shadows.
3. **Automated Quality Assurance (QA Verification Loop)**:
   - `qa_asset_validator.py`: Automated checks for color palette budgets (catches unquantized AI color bleed), directional motion padding clipping, animation frame jitter, and 2.5D isometric diamond seam leaks.
4. **Multi-Engine Game Export Pipelines**:
   - **Unreal Engine 5 Paper2D / PaperZD**: Automatic texture import, nearest filtering, bottom-center pivot anchoring, and `UPaperFlipbook` compilation with full keyframes.
   - **Godot 4**: Generates native `.tres` `SpriteFrames` resources and `.tscn` `AnimatedSprite2D` scenes.
   - **Universal TexturePacker Atlas**: Packs frames into an optimized sprite atlas PNG + standard JSON hash format for Unity, Godot, PixiJS, Phaser, Defold.
5. **Batch Processing**:
   - Batch-slice multiple spritesheets and icon grids across entire directories in a single command.

---

## 📁 Repository Structure

```text
game-art-studio/
├── .github/workflows/
│   └── ci.yml                        # GitHub Actions CI for multi-version pytest & lint
├── SKILL.md                          # Main Skill specification for AI Coding Assistants
├── pyproject.toml                    # Standard Python project metadata & tool configurations
├── requirements.txt                  # Python dependencies (Pillow, numpy, pytest)
├── assets/
│   └── map-tile-layout-demo.html     # Interactive in-browser tileset layout previewer
├── scripts/
│   ├── slice_spritesheet.py          # Slices spritesheets (single & batch), handles empty frames
│   ├── assemble_flipbook_gif.py      # Assembles sliced frames into animated GIF previews
│   ├── pack_sprite_atlas.py          # Packs frames into TexturePacker Atlas PNG + JSON
│   ├── import_ue_flipbooks.py        # Python automation script for Unreal Engine 5 Editor (Paper2D)
│   ├── import_godot_flipbooks.py     # Generates native Godot 4 SpriteFrames (.tres) & .tscn scenes
│   ├── qa_asset_validator.py         # Automated QA: palette budget, clipping, jitter, isometric seams
│   ├── generate_item_icon_sheet.py   # Batches item icons with 5-tier rarity borders & grid layouts
│   ├── build-map-preview.py          # Compiles isometric and parallax map layouts
│   ├── map-preview-server.py         # Standalone HTTP server for live map previews
│   └── map-tile-layout.js            # Geometric calculations for 2.5D isometric & hex grids
├── tests/
│   ├── test_slice_spritesheet.py     # Unit tests for slicer & empty frame edge cases
│   ├── test_generate_item_icon_sheet.py # Unit tests for icon grid parsing & borders
│   ├── test_import_godot_flipbooks.py# Unit tests for Godot 4 SpriteFrames generator
│   ├── test_pack_sprite_atlas.py     # Unit tests for TexturePacker atlas packing
│   └── test_qa_asset_validator.py    # Unit tests for QA color & isometric diamond checks
└── references/
    ├── asset-contract-presets.md     # Presets for Stardew Valley, Capcom CPS2, Hades, Hollow Knight
    ├── anti-ai-craft-guide.md        # Comprehensive Anti-AI Craft & Dynamic Art Directives
    ├── pixel-and-hd-assets.md        # Guidelines for 8-directional character sprites
    ├── animation-and-video.md        # Pacing, keyframing, and motion padding rules
    ├── maps-tiles-and-textures.md    # Math for isometric, hex, and dual-grid tiling
    ├── ui-and-image-editing.md       # Modular UI & equipment layering
    ├── game-design.md                # GDD asset alignment contracts
    ├── audio.md                      # Audio stem sync guidelines
    └── web_parameter_contract.json   # Parameter specifications
```

---

## 🚀 Usage & Quick Start

### 1. Slice Spritesheet with Bottom-Center Pivot (Single or Batch)
```bash
# Single spritesheet
python3 scripts/slice_spritesheet.py \
    --input_sheet <path_to_spritesheet.png> \
    --output_dir <output_frames_folder> \
    --frames 8 \
    --color_key auto \
    --tolerance 35 \
    --anchor bottom_center

# Batch mode: slice an entire directory of spritesheets
python3 scripts/slice_spritesheet.py \
    --batch_dir <folder_with_spritesheets> \
    --output_dir <output_root_folder> \
    --frames 8
```

### 2. Verify Asset Quality with Automated QA
```bash
# Verify animation frames against Stardew 16-color budget & motion padding
python3 scripts/qa_asset_validator.py \
    --frames_dir <output_frames_folder> \
    --preset stardew \
    --strict

# Verify 2.5D Isometric Diamond tile (128x64) for seam leaks
python3 scripts/qa_asset_validator.py \
    --tile <tile_128x64.png> \
    --strict
```

### 3. Assemble Animated GIF Preview
```bash
python3 scripts/assemble_flipbook_gif.py \
    --frames_dir <output_frames_folder> \
    --output_gif <preview.gif> \
    --fps 12.0
```

### 4. Pack into Universal TexturePacker Atlas (PNG + JSON)
```bash
python3 scripts/pack_sprite_atlas.py \
    --frames_dir <output_frames_folder> \
    --output_atlas <output_folder>/atlas.png \
    --output_json <output_folder>/atlas.json
```

### 5. Import Directly into Unreal Engine 5 (Paper2D)
```bash
/path/to/UnrealEditor-Cmd \
    <YourProject>/<YourProject>.uproject \
    -ExecutePythonScript="scripts/import_ue_flipbooks.py --frames_dir <output_frames_folder> --dest_path /Game/Art/Flipbooks --name FB_Hero_Attack --fps 12.0 --pivot bottom_center" \
    -nullrhi -nosound -unattended
```

### 6. Import Directly into Godot 4 (SpriteFrames & AnimatedSprite2D)
```bash
python3 scripts/import_godot_flipbooks.py \
    --frames_dir <output_frames_folder> \
    --output_tres <output_frames_folder>/hero_run.tres \
    --godot_res_dir res://art/characters \
    --anim_name run \
    --fps 12.0 \
    --generate_scene
```

### 7. Batch Frame Item Icons with 5-Tier Rarity
```bash
python3 scripts/generate_item_icon_sheet.py \
    --input_sheet <icons_raw.png> \
    --output_dir <output_dir> \
    --grid 4x4 \
    --rarity rare
```

### 8. Run Unit Tests
```bash
python3 -m unittest discover -s tests -p "test_*.py" -v
```

---

## 📜 License

Licensed under the [MIT License](LICENSE).  
Architecture patterns inherited from [Meowa AI](https://github.com/Meowa-AI/meowa-skills).
