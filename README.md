# 🎨 Game Art Studio

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Engine: Unreal Engine 5](https://img.shields.io/badge/Unreal%20Engine-5.8%20%7C%20Paper2D%20%7C%20PaperZD-blue.svg)](https://unrealengine.com)
[![Architecture: Meowa AI](https://img.shields.io/badge/Architecture-Meowa%20Open--Source-orange.svg)](https://github.com/Meowa-AI/meowa-skills)

> **Game Art Studio** is an end-to-end Game Art & Asset Production Studio powered by the open-source **Meowa AI** architecture. It provides production-ready pipelines for 2D pixel & HD game assets, 8-directional character spritesheets, action-first animations, 2.5D isometric diamond ($128 \times 64$) tilesets, dual-grid autotiling atlases, 5-tier RPG item icons, interactive browser previewers, and direct Unreal Engine 5 Paper2D / PaperZD flipbook generation.

---

## ✨ Key Features

1. **Meowa Asset Contract & Action-First Posing**:
   - Zero-delay animation startup: Action poses begin with weapons drawn / mid-stride to prevent initial loop lag.
   - **Directional Motion Padding**: Dynamic boundary buffers on 4 edges (`top`, `down`, `left`, `right`) to prevent sprite clipping during attacks and dashes.
2. **2.5D Isometric Map Engine ($128 \times 64$)**:
   - Dimetric 2:1 projection ($-45^\circ$ Pitch, $45^\circ$ Yaw).
   - Base diamond calculation with neighbor offsets `(+64, +32)` and `(-64, +32)`.
   - Hex-Isometric grids with seamless $64\text{px}$ edges.
   - Dual-Grid Autotiling Atlas ($4 \times 4$ Wang/Blob tilesets).
   - In-browser interactive map preview server (`map-preview-server.py`).
3. **5-Tier Rarity Item Icon Matrix**:
   - Automated RPG item framing ($64 \times 64$ / $48 \times 48$):
     - **Common** (`#9CA3AF`)
     - **Uncommon** (`#22C55E`)
     - **Rare** (`#3B82F6`)
     - **Epic** (`#A855F7`)
     - **Legendary** (`#F59E0B`)
4. **Unreal Engine 5 Paper2D / PaperZD Importer**:
   - Automated sprite slicing, bottom-center pivot anchoring, and `UPaperZDAnimSequence` / `UPaperFlipbook` generation.

---

## 📁 Repository Structure

```text
game-art-studio/
├── SKILL.md                          # Main Skill specification for AI Coding Assistants
├── assets/
│   └── map-tile-layout-demo.html     # Interactive in-browser tileset layout previewer
├── scripts/
│   ├── slice_spritesheet.py          # Slices spritesheets & sets bottom-center pivots
│   ├── assemble_flipbook_gif.py      # Assembles sliced frames into animated GIF previews
│   ├── build-map-preview.py          # Compiles isometric and parallax map layouts
│   ├── map-preview-server.py         # Standalone HTTP server for live map previews
│   ├── map-tile-layout.js            # Geometric calculations for 2.5D isometric & hex grids
│   ├── generate_item_icon_sheet.py   # Batches item icons with 5-tier rarity borders
│   └── import_ue_flipbooks.py        # Python automation script for Unreal Engine 5 Editor
└── references/
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

### 1. Slice Spritesheet with Bottom-Center Pivot
```bash
python3 scripts/slice_spritesheet.py \
    --input <path_to_spritesheet.png> \
    --output_dir <output_frames_folder> \
    --frames 8 \
    --color_key auto \
    --anchor bottom_center
```

### 2. Assemble Animated GIF Preview
```bash
python3 scripts/assemble_flipbook_gif.py \
    --frames_dir <output_frames_folder> \
    --output_gif <preview.gif> \
    --fps 12.0
```

### 3. Launch In-Browser Isometric Map Previewer
```bash
python3 scripts/map-preview-server.py \
    --mode isometric \
    --image <tile_1.png> \
    --image <tile_2.png> \
    --columns 8 \
    --rows 6 \
    --lifetime 900
```
Then open `http://localhost:8080` in your web browser.

### 4. Batch Frame Item Icons with 5-Tier Rarity
```bash
python3 scripts/generate_item_icon_sheet.py \
    --input_sheet <icons_raw.png> \
    --output_dir <output_dir> \
    --grid 4x4 \
    --rarity rare
```

### 5. Import Directly into Unreal Engine 5
```bash
/path/to/UnrealEditor-Cmd \
    <YourProject>/<YourProject>.uproject \
    -ExecutePythonScript=scripts/import_ue_flipbooks.py \
    -nullrhi -nosound -unattended
```

---

## 📜 License

Licensed under the [MIT License](LICENSE).  
Architecture patterns inherited from [Meowa AI](https://github.com/Meowa-AI/meowa-skills).
