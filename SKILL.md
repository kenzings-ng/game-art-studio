---
name: game-art-studio
description: End-to-end AI Game Art & Asset Studio powered by local Nano Banana (Imagen 3 / Gemini Image) and open-source Meowa AI architecture. Creates 2D pixel & HD game assets, 8-directional character spritesheets, action-first animations, 2:1 isometric & hex tilesets, dual-grid autotiling atlases, parallax side-scrollers, 5-tier UI item icons, interactive browser map previewer, and direct Unreal Engine Paper2D/PaperZD flipbook generation — 100% free with zero credits or subscriptions.
---

# Game Art Studio (Meowa Open-Source Architecture + Local Nano Banana Engine)

Game Art Studio là studio sản xuất tài nguyên đồ họa game toàn diện, kết hợp giữa:
1. **Lõi sinh ảnh Nano Banana nội bộ** (`generate_image` — tương đương `gemini-3.1-flash-image` / `gemini-3-pro-image` mà chính Meowa AI sử dụng làm backend).
2. **Kiến trúc mã nguồn mở chuẩn mực của Meowa AI** (`Meowa-AI/meowa-skills`): Quy chuẩn hợp đồng tài nguyên (Asset Contract), kỹ thuật Action-First Pose, ma trận căn lề đệm động (Directional Motion Padding), hệ tọa độ Isometric Diamond $128 \times 64$, Hex-Isometric, Dual-Grid Autotiling $4 \times 4$, và máy chủ xem trước bản đồ trên trình duyệt.
3. **Pipeline xuất xưởng Game Engine tự động**: Tách nền Chroma-key/Alpha, ghim tâm chân (Bottom-Center Pivot), tạo GIF preview động, và import trực tiếp vào **Unreal Engine 5 Paper2D / PaperZD** hoặc **Godot 4**.

Toàn bộ quy trình chạy **cục bộ 100%, vĩnh viễn không tốn credit, không cần API key trả phí**.

---

## 1. Hợp Đồng Tài Nguyên & Triết Lý Prompt (Meowa Asset Contract)

### A. Thiết Lập Hợp Đồng Tài Nguyên (Asset Contract First)
Trước khi ra lệnh vẽ, luôn xác định rõ các ràng buộc:
- **Loại tài nguyên runtime**: Sprite nhân vật, quái vật, đạo cụ (prop), ô gạch địa hình (tile), UI/Icon, hay lớp bản đồ (map layer).
- **Quy chuẩn hiển thị**: Pixel Art hay HD Art.
- **Kích thước & Bố cục**: Kích thước ô (cell size), số lượng frame, tỷ lệ khung hình (aspect ratio: 1:1, 4:3, 16:9), kênh trong suốt (transparency).
- **Cấu trúc bàn giao**: Sprite sheet tuyến tính, bộ 8 hướng (8-direction set), hay atlas địa hình (terrain atlas).

### B. Triết Lý Prompt Tự Nhiên (Natural Language Prompting)
> ⚠️ **Quy tắc Meowa**: Tuyệt đối **không** dùng từ khóa rườm rà kiểu Stable Diffusion cũ (như *"masterpiece, 8k, trending on artstation, unreal engine render, photorealistic"*).
> 
> Hãy mô tả bằng ngôn ngữ tự nhiên, ngắn gọn và trực tiếp vào chủ thể, hành động, góc nhìn và chất liệu:
> - Tốt: `16-bit pixel art, Vanguard warrior in dark steel plate armor, heavy claymore raised above shoulder ready to strike, facing right, pure magenta background #FF00FF, no floor shadow.`
> - Tránh: `masterpiece, ultra realistic 8k, beautiful anime warrior, dynamic lighting, octane render, highly detailed.`

---

## 2. Quy Trình Character & Animation (Meowa Action-First Pipeline)

### A. Kỹ Thuật Tư Thế Mở Đầu Hành Động (Action-First Pose)
Trong diễn hoạt game, khung hình đầu tiên của animation chính là nguồn gốc chuyển động. Nếu bắt đầu từ tư thế đứng im (Neutral Idle) để làm hoạt ảnh Chém kiếm hay Chạy, mô hình sẽ lãng phí 2-3 frame đầu chỉ để "vung kiếm lên" hoặc "nhấc chân", khiến animation bị delay và giật vòng lặp (loop glitch).

- **Hoạt ảnh Đánh (Attack)**: Tư thế đầu tiên phải là nhân vật đã rút vũ khí, giương kiếm hoặc gồng đòn sẵn sàng chém.
- **Hoạt ảnh Chạy / Đi (Run / Walk)**: Tư thế đầu tiên phải là hai chân đã bước dạng rộng, một chân trước một chân sau (`legs separated, one in front and one behind`).
- **Hoạt ảnh Nhảy (Jump)**: Bắt đầu từ tư thế chùng gối hoặc chân vừa rời mặt đất.
- **Kích thước tối ưu**: Giữ kích thước nhân vật pixel ở mức $\le 128 \times 128$ pixel. Canvas nhân vật pixel không bao giờ vượt quá $256 \times 256$ để đảm bảo độ sắc nét điểm ảnh.

### B. Ma Trận Đệm Chuyển Động (Directional Motion Padding)
Chuyển động cần khoảng trống trong suốt để di chuyển mà không bị cắt cụt rìa ảnh. Phân bổ đệm độc lập 4 phía (`top`, `down`, `left`, `right`):
- **Chém kiếm sang phải**: Thêm đệm phía trước (`padding_right: 20-30px`), đệm trên (`padding_top: 10px`).
- **Nhảy cao**: Thêm đệm trên đỉnh đầu (`padding_top: 30-40px`), đệm dưới (`padding_down: 8px`).
- **Lướt lùi / Né đòn (Back-dash)**: Thêm đệm phía sau lưng (`padding_left: 25px`).

### C. Công Cụ Xử Lý Animation Đi Kèm:
1. **Cắt Frame & Ghim Pivot Chân (`scripts/slice_spritesheet.py`)**:
   ```bash
   python3 /home/kenzings/.gemini/config/skills/game-art-studio/scripts/slice_spritesheet.py \
       --input <path_to_spritesheet.png> \
       --output_dir <output_frames_folder> \
       --frames 8 \
       --color_key auto \
       --anchor bottom_center
   ```
2. **Ghép Animated GIF Preview (`scripts/assemble_flipbook_gif.py`)**:
   ```bash
   python3 /home/kenzings/.gemini/config/skills/game-art-studio/scripts/assemble_flipbook_gif.py \
       --frames_dir <output_frames_folder> \
       --output_gif <preview.gif> \
       --fps 12.0
   ```
3. **Import Tự Động vào Unreal Engine 5 Paper2D (`scripts/import_ue_flipbooks.py`)**:
   ```bash
   /mnt/Data/Engine/Binaries/Linux/UnrealEditor-Cmd \
       ProjectAscendant/ProjectAscendant.uproject \
       -ExecutePythonScript=/home/kenzings/.gemini/config/skills/game-art-studio/scripts/import_ue_flipbooks.py \
       -nullrhi -nosound -unattended
   ```

---

## 3. Quy Trình Level Tilesets & Hệ Tọa Độ Bản Đồ (Meowa Map Engine)

Được kế thừa nguyên bản từ bộ tính toán tọa độ và script bản đồ của Meowa AI:

### A. 2.5D Isometric Diamond Grid ($128 \times 64$)
- **Hình chiếu Dimetric 2:1**: Góc nhìn camera $-45^\circ$ Pitch, $45^\circ$ Yaw.
- **Kích thước cơ sở (Base Diamond)**: $128 \times 64$ pixels.
- **Độ dịch tâm các ô lân cận (Neighbor Offsets)**:
  - Trục X: `(+64, +32)`
  - Trục Y: `(-64, +32)`
- **Khoảng cách tâm cùng hàng**: $128$ px.
- **Khoảng cách tâm cùng cột**: $64$ px.
- **Tetraploid Tile ($2 \times 2$)**: Phủ 4 ô cơ sở, kích thước logic $256 \times 128$ px. Neo tại tâm của vùng $2 \times 2$.

### B. Hex-Isometric Grid (Bản Đồ Lục Giác)
- **Cạnh lục giác $64$px**: Khoảng cách tâm cùng hàng là $127$ px (`2 * 64 - 1`) để ghép khít không để lại khe hở pixel.
- **Dịch dòng tiếp theo**: Dịch ngang $64$ px và dịch dọc $64$ px. Các vector chéo xuống là `(+64, +64)` và `(-63, +64)`.

### C. Dual-Grid Autotiling Atlas ($4 \times 4$)
- Atlas chuẩn 16 ô gạch chuyển tiếp (Wang / Blob Tileset) để tự động hóa địa hình nối giữa Cỏ - Nước, Đất - Đá, Dung nham - Tro tàn mà không bị lộ đường viền.

### D. Máy Chủ Xem Trước Bản Đồ Trực Quan Trên Trình Duyệt (`map-preview-server.py`)
Khởi động máy chủ xem trước độc lập để kiểm tra độ khít ô gạch, độ sâu z-order và hiệu ứng cuộn parallax ngay trên trình duyệt:
```bash
python3 /home/kenzings/.gemini/config/skills/game-art-studio/scripts/map-preview-server.py \
    --mode isometric \
    --image <tile_1.png> \
    --image <tile_2.png> \
    --columns 8 \
    --rows 6 \
    --lifetime 900
```
- Hỗ trợ các chế độ: `isometric`, `hex`, `hd-isometric`, `dual-grid`, và `side-scrolling` (cuộn mượt 3 lớp parallax: background, midground, foreground).
- File giao diện: [`assets/map-tile-layout-demo.html`](file:///home/kenzings/.gemini/config/skills/game-art-studio/assets/map-tile-layout-demo.html) kết hợp thư viện toán học [`scripts/map-tile-layout.js`](file:///home/kenzings/.gemini/config/skills/game-art-studio/scripts/map-tile-layout.js).

---

## 4. Quy Trình Game UI & Item Icons (5-Tier Rarity Matrix)

Hỗ trợ sản xuất icon trang bị $64 \times 64$ hoặc $48 \times 48$ với khung viền 5 cấp độ hiếm chuẩn RPG:

| Cấp Độ (Rarity) | Mã Màu Viền (Hex) | Hiệu Ứng Nền (Background Glow) |
| :--- | :---: | :--- |
| **Common** | `#9CA3AF` (Xám) | Nền đá phiến mờ, không hạt |
| **Uncommon** | `#22C55E` (Xanh Lục) | Ánh sáng ngọc bích viền kim loại |
| **Rare** | `#3B82F6` (Xanh Lam) | Viền thép rèn khắc chữ rune lam |
| **Epic** | `#A855F7` (Tím Huyền Bí) | Viền vàng cổ khắc ấn phù tím, khói ma thuật |
| **Legendary** | `#F59E0B` (Hoàng Kim) | Hào quang rực lửa vàng kim, hạt tro phát sáng |

Chạy đóng khung hàng loạt:
```bash
python3 /home/kenzings/.gemini/config/skills/game-art-studio/scripts/generate_item_icon_sheet.py \
    --input_sheet <icons_raw.png> \
    --output_dir <output_dir> \
    --grid 4x4 \
    --rarity rare
```

---

## 5. Thư Viện Tài Liệu Tham Khảo Chuyên Sâu (Meowa References)

Được tích hợp đầy đủ trong thư mục `references/`:
- [`pixel-and-hd-assets.md`](file:///home/kenzings/.gemini/config/skills/game-art-studio/references/pixel-and-hd-assets.md): Hướng dẫn chi tiết tạo sprite, nhân vật 8 hướng, tách nền và chuẩn hóa điểm ảnh.
- [`animation-and-video.md`](file:///home/kenzings/.gemini/config/skills/game-art-studio/references/animation-and-video.md): Hướng dẫn thiết lập tư thế đầu, đệm chuyển động, pacing 8/12/16 frame, keyframe posing.
- [`maps-tiles-and-textures.md`](file:///home/kenzings/.gemini/config/skills/game-art-studio/references/maps-tiles-and-textures.md): Toàn bộ toán học hình học Isometric, Hex-grid, Dual-grid và Parallax side-scroller.
- [`ui-and-image-editing.md`](file:///home/kenzings/.gemini/config/skills/game-art-studio/references/ui-and-image-editing.md): Phân tách UI sheet và tạo biến thể trang bị nâng cấp.
- [`web_parameter_contract.json`](file:///home/kenzings/.gemini/config/skills/game-art-studio/references/web_parameter_contract.json): Bản đặc tả tham số của Meowa AI (chứng minh backend dùng Nano Banana `gemini-3.1-flash-image`).
