---
name: game-art-studio
description: End-to-end AI Game Art & Asset Studio powered by local Nano Banana (Imagen 3 / Gemini Image) and open-source Meowa AI architecture. Creates 2D pixel & HD game assets, 8-directional character spritesheets, action-first animations, 2:1 isometric & hex tilesets, dual-grid autotiling atlases, parallax side-scrollers, 5-tier UI item icons, interactive browser map previewer, direct Unreal Engine Paper2D/PaperZD flipbook generation, and Anti-AI Handcrafted Art Styling — 100% free with zero credits or subscriptions.
---

# Game Art Studio (Meowa Open-Source Architecture + Local Nano Banana Engine)

Game Art Studio là studio sản xuất tài nguyên đồ họa game toàn diện, kết hợp giữa:
1. **Lõi sinh ảnh Nano Banana nội bộ** (`generate_image` — tương đương `gemini-3.1-flash-image` / `gemini-3-pro-image` mà chính Meowa AI sử dụng làm backend).
2. **Kiến trúc mã nguồn mở chuẩn mực của Meowa AI** (`Meowa-AI/meowa-skills`): Quy chuẩn hợp đồng tài nguyên (Asset Contract), kỹ thuật Action-First Pose, ma trận căn lề đệm động (Directional Motion Padding), hệ tọa độ Isometric Diamond $128 \times 64$, Hex-Isometric, Dual-Grid Autotiling $4 \times 4$, và máy chủ xem trước bản đồ trên trình duyệt.
3. **Giao Thức Khởi Tạo Hợp Đồng & Chống "Mùi AI" (Asset Contract & Anti-AI Engine)**: Tuyệt đối không sinh ảnh bừa bãi khi chưa chốt hợp đồng phong cách. Tự động liên kết các Preset kinh điển (Stardew Valley 16x16, Capcom CPS2, Hades, Hollow Knight) và áp dụng bộ luật thủ công (Hue-shifting, Line of Action, Không bóng gối).
4. **Pipeline xuất xưởng Game Engine tự động**: Tách nền Chroma-key/Alpha, ghim tâm chân (Bottom-Center Pivot), tạo GIF preview động, và import trực tiếp vào **Unreal Engine 5 Paper2D / PaperZD** hoặc **Godot 4**.

Toàn bộ quy trình chạy **cục bộ 100%, vĩnh viễn không tốn credit, không cần API key trả phí**.

---

## 1. Giao Thức Khởi Tạo Hợp Đồng Bắt Buộc (Mandatory Asset Contract)

> 🛑 **QUY TẮC CỐT LÕI: KHÔNG ĐƯỢC TỰ Ý SINH ẢNH KHI THIẾU RÀNG BUỘC**
> Nếu người dùng yêu cầu vẽ một tài nguyên game mà **chưa chỉ định phong cách hoặc thông số kỹ thuật rõ ràng**, AI Agent **CẤM** đoán mò rồi sinh ảnh ngay lập tức. Làm vậy sẽ khiến kết quả bị lệch hoàn toàn so với mong đợi (như vẽ đại kiếm 128x128 khi người dùng thực chất cần icon 16x16 kiểu Stardew Valley), bắt người dùng phải prompt đi prompt lại rất nhiều lần tốn thời gian.

### A. Quy Trình Khóa Hợp Đồng 2 Nhánh (Two-Branch Contract Resolution):

1. **Nhánh 1: Người dùng đã nêu tên Game cụ thể (e.g. "Stardew Valley", "Capcom", "Hollow Knight")**:
   - **TỰ ĐỘNG ÁP DỤNG PRESET CHUẨN** trong [`references/asset-contract-presets.md`](file:///mnt/Data/Projects/game-art-studio/references/asset-contract-presets.md):
     - **Stardew Valley / Terraria**: Lưới siêu thô $16 \times 16$ native, ngân sách màu 8-16 màu, viền neon đảo ngược nếu là vũ khí thiên hà.
     - **Capcom CPS2 / NeoGeo**: Lưới $64 \times 64$ / $128 \times 128$, viền đen than 1px, chuyển nhiệt độ màu gắt (Hue-shifting).
     - **Hollow Knight / Cuphead**: 2D HD cọ mực vẽ tay, nét cọ biến thiên, màu bệt phẳng.
     - **Hades / Dead Cells**: 2D Chiaroscuro tương phản cực độ, viền sáng ven (Rim light).
   - Tóm tắt nhanh hợp đồng rồi tiến hành sinh ảnh đúng chuẩn.

2. **Nhánh 2: Yêu cầu chung chung (e.g. "vẽ cho tôi cây kiếm", "vẽ nhân vật chiến binh")**:
   - Dùng công cụ `ask_question` (hoặc đưa ra bảng tùy chọn nhanh) để người dùng chọn:
     - **Phong cách đồ họa**: 16x16 Pixel thô (Stardew/Celeste) | 16-bit/32-bit Arcade (SNES/Capcom) | 2D Vẽ tay Stylized HD (Hades/Hollow Knight).
     - **Mục đích sử dụng**: Icon túi đồ (góc $45^\circ$) | Sprite nhân vật ngang (Side-scroller) | Sprite góc nhìn trên xuống (Top-down) | Gạch địa hình (Tileset).
     - **Bảng màu & Chất liệu**: Kim loại phản quang | Tinh thể ma thuật phát sáng | Đồ da/vải mộc.

---

## 2. Bí Quyết Vẽ Art Sống Động, Không Giống AI (Anti-AI Craft Rules)

Chi tiết chuyên sâu xem tại [`references/anti-ai-craft-guide.md`](file:///mnt/Data/Projects/game-art-studio/references/anti-ai-craft-guide.md):

1. **Đường Động Lực (Line of Action) & Dáng Đứng Bất Đối Xứng (Contrapposto)**:
   - Cấm vẽ cột sống thẳng đứng $90^\circ$. Bắt buộc uốn cong hình chữ **C** hoặc chữ **S**.
   - Trọng tâm lệch: 1 chân chịu $80\%$ sức nặng (chân trụ), 1 chân co/thả lỏng. Trục vai nghiêng ngược chiều trục hông.
   - **Thử nghiệm bóng đen (The Blackout Test)**: Nhân vật khi tô đen kịt `#000000` vẫn phải đọc rõ hình thái, vũ khí và cảm xúc từ xa. Luôn để khoảng trống âm (Negative Space) giữa hai tay, chân và thân mình.
2. **Quy Tắc Vàng Chuyển Nhiệt Độ Màu (Hue-Shifting)**:
   - **Cấm**: Đổ bóng bằng cách pha đen/xám, nâng sáng bằng cách pha trắng (làm tranh bị đục, bẩn và tái).
   - **Bắt buộc**: Đèn ấm (Ánh nắng/Lửa) thì Highlight ngả Vàng Chanh $\rightarrow$ Shadow **dịch sang Tím Indigo/Xanh Navy** (do phản chiếu vòm trời). Đèn lạnh (Ánh trăng/Phép) thì Shadow **dịch sang Đỏ Mận/Tím Ấm**.
3. **Nguồn Sáng Đơn Rõ Ràng (Key Light at $45^\circ$) — Diệt Trừ Pillow Shading**:
   - Khóa chặt nguồn sáng chính từ góc trên-trái ($10$ giờ) hoặc trên-phải ($2$ giờ).
   - Đổ bóng đổ cứng (Cast shadow) dưới cằm, vạt áo, lưỡi kiếm. Ranh giới sáng - tối sắc nét, tuyệt đối không làm mờ dần từ mép vào tâm.
4. **Quy Tắc Tỉ Lệ Chi Tiết 70 - 20 - 10 (Resting Areas)**:
   - **70% Vùng nghỉ mắt**: Mảng giáp phẳng, vạt áo trơn, cơ bắp liền khối để tạo cảm giác đồ họa vững chãi.
   - **20% Chi tiết chức năng**: Dây thắt lưng, khóa cài, nẹp ủng.
   - **10% Điểm nhấn tiêu điểm**: Ánh sáng phản quang trong đồng tử, vết rạn trên chuôi gươm.
   - *Bỏ hoàn toàn các hoa văn vàng kim vô nghĩa mà AI hay tự vẽ.*

---

## 3. Quy Trình Character & Animation (Meowa Action-First Pipeline)

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
       --input_sheet <path_to_spritesheet.png> \
       --output_dir <output_frames_folder> \
       --frames 8 \
       --color_key auto \
       --tolerance 35 \
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
       -ExecutePythonScript="scripts/import_ue_flipbooks.py --frames_dir <output_frames_folder> --dest_path /Game/Art/Flipbooks --name FB_Hero_Attack --fps 12.0" \
       -nullrhi -nosound -unattended
   ```

---

## 4. Quy Trình Level Tilesets & Hệ Tọa Độ Bản Đồ (Meowa Map Engine)

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

## 5. Quy Trình Game UI & Item Icons (5-Tier Rarity Matrix)

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

## 6. Thư Viện Tài Liệu Tham Khảo Chuyên Sâu (Meowa References)

Được tích hợp đầy đủ trong thư mục `references/`:
- [`asset-contract-presets.md`](file:///home/kenzings/.gemini/config/skills/game-art-studio/references/asset-contract-presets.md): **Bộ hợp đồng tài nguyên định sẵn cho các game kinh điển (Stardew Valley 16x16, Capcom CPS2, Hollow Knight, Hades, Pokémon GBA).**
- [`anti-ai-craft-guide.md`](file:///home/kenzings/.gemini/config/skills/game-art-studio/references/anti-ai-craft-guide.md): Bộ quy chuẩn mỹ thuật thủ công, diệt trừ "mùi AI", nguyên tắc hue-shifting, đường động lực và từ điển prompt chuẩn studio.
- [`pixel-and-hd-assets.md`](file:///home/kenzings/.gemini/config/skills/game-art-studio/references/pixel-and-hd-assets.md): Hướng dẫn chi tiết tạo sprite, nhân vật 8 hướng, tách nền và chuẩn hóa điểm ảnh.
- [`animation-and-video.md`](file:///home/kenzings/.gemini/config/skills/game-art-studio/references/animation-and-video.md): Hướng dẫn thiết lập tư thế đầu, đệm chuyển động, pacing 8/12/16 frame, keyframe posing.
- [`maps-tiles-and-textures.md`](file:///home/kenzings/.gemini/config/skills/game-art-studio/references/maps-tiles-and-textures.md): Toàn bộ toán học hình học Isometric, Hex-grid, Dual-grid và Parallax side-scroller.
- [`ui-and-image-editing.md`](file:///home/kenzings/.gemini/config/skills/game-art-studio/references/ui-and-image-editing.md): Phân tách UI sheet và tạo biến thể trang bị nâng cấp.
- [`web_parameter_contract.json`](file:///home/kenzings/.gemini/config/skills/game-art-studio/references/web_parameter_contract.json): Bản đặc tả tham số của Meowa AI (chứng minh backend dùng Nano Banana `gemini-3.1-flash-image`).
