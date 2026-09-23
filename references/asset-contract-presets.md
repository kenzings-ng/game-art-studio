# 📋 Bộ Hợp Đồng Tài Nguyên Định Sẵn (Asset Contract Presets)

> Tài liệu này chuẩn hóa các ràng buộc kỹ thuật & mỹ thuật cho các phong cách game phổ biến nhất. Khi người dùng yêu cầu vẽ theo phong cách một tựa game cụ thể, AI Agent bắt buộc áp dụng trực tiếp hợp đồng tương ứng mà không được suy đoán lung tung.

---

## 1. Preset: Stardew Valley / Terraria (16×16 Micro-Pixel Style)

* **Hệ quy chiếu lưới pixel**:
  * **Kích thước bản vẽ gốc**: Chuẩn xác $16 \times 16$ pixel (tối đa $24 \times 24$ cho vũ khí lớn).
  * **Kích thước xuất xưởng**: Phóng to Nearest Neighbor 4x thành $64 \times 64$ pixel để nhập vào game.
  * **Kích thước hạt pixel**: Siêu thô (Chunky Micro-pixel), mỗi điểm màu là một ô vuông rõ rệt.
* **Ngân sách bảng màu (Color Budget)**:
  * Giới hạn nghiêm ngặt từ 8 đến 16 màu cho toàn bộ vật thể.
  * Không dùng dải chuyển màu mịn. Mỗi bậc sáng/tối là một bước nhảy màu dứt khoát.
* **Quy chuẩn vũ khí & Đồ vật (Items)**:
  * Góc nghiêng cố định $45^\circ$ chạy chéo từ góc dưới-trái lên góc trên-phải.
  * Chiếm trọn không gian $16 \times 16$ để dễ nhận diện trong thanh Quickbar 12 ô của Stardew.
* **Đặc thù dòng vũ khí Thiên Hà (Galaxy Equipment)**:
  * **Chất liệu**: Tinh thể thiên hà nguyên khối (Monolithic Cosmic Crystal), không tách chuôi kim loại vàng.
  * **Đổ sáng phát quang ngược (Inverted Neon Glow)**: Viền ngoài cùng của kiếm là màu hồng tím neon rực sáng nhất (`#F193FF`), lòng kiếm màu tím sẫm (`#5D269B`), chuôi kiếm và lõi bóng đổ là tím than vũ trụ / xanh navy (`#310074`, `#000053`).
* **Prompt Mẫu Chuẩn Stardew Valley**:
  ```text
  Authentic 16x16 pixel art item icon of the Tempered Galaxy Sword from Stardew Valley, displayed at 45-degree diagonal. Strict minimal 16x16 chunky pixel grid, exactly like Stardew Valley inventory sprite. Monolithic pure cosmic crystal blade, glowing neon pink-violet outer edges (#F193FF), deep cosmic purple core, dark navy hilt (#000053), no gold or metal crossguard, flat solid background #000000, perfectly pixelated with zero anti-aliasing.
  ```

---

## 2. Preset: Capcom CPS2 / NeoGeo (16-bit / 32-bit Arcade Fighting)

* **Hệ quy chiếu lưới pixel**:
  * **Kích thước bản vẽ gốc**: $64 \times 64$ đến $128 \times 128$ pixel.
* **Ngân sách bảng màu**:
  * 16 màu đến 32 màu (theo bảng màu chuẩn Capcom CPS2 / Street Fighter Zero / Darkstalkers).
  * 3–4 bậc sắc độ cho mỗi chất liệu (Highlight, Midtone, Core Shadow, Dark Accent).
* **Đặc trưng mỹ thuật**:
  * Viền bao ngoài (Outer Contour) màu đen than sẫm dày 1px dứt khoát.
  * Chuyển nhiệt độ màu (Hue Shifting) cực gắt: Da sáng vàng ấm chuyển sang bóng tím mận; Giáp thép bạc chuyển sang bóng chàm/navy.
  * Khối cơ bắp và mảng giáp phân diện hình học rõ ràng (Hard Cel-Shading).

---

## 3. Preset: Hollow Knight / Cuphead (Stylized Hand-Drawn 2D Ink)

* **Hệ quy chiếu**:
  * Đồ họa 2D HD vector hoặc cọ mực vẽ tay (Hand-inked lineart).
* **Đặc trưng mỹ thuật**:
  * Đường nét mực đen dày mỏng biến thiên linh hoạt (Dynamic variable ink line weight).
  * Tô màu bệt phẳng (Flat cel fills) hoặc dải chuyển nhẹ nhàng theo phong cách truyện tranh hoạt họa cổ điển.
  * Bảng màu u tối, huyền bí (Hollow Knight: xanh chàm, xám than, trắng ngà) hoặc bảng màu phim hoạt hình thập niên 1930 (Cuphead).

---

## 4. Preset: Hades (Supergiant High-Contrast Chiaroscuro)

* **Hệ quy chiếu**:
  * Đồ họa 2D minh họa bán thực tế cách điệu (Stylized Comic / Chiaroscuro).
* **Đặc trưng mỹ thuật**:
  * Tương phản ánh sáng cực độ: Đèn chính chói lòa và bóng tối đen kịt đồ họa (lấy cảm hứng từ nét vẽ Mike Mignola).
  * Đèn viền ven (Rim Light) màu nóng rực rỡ (đỏ cam magma, xanh ngọc thần thánh) bao quanh khối nhân vật.
  * Dáng đứng mang tính điêu khắc Hy Lạp cổ điển với trọng tâm lệch (Contrapposto) dũng mãnh.

---

## 5. Preset: Pokémon Gen 3 GBA (Game Boy Advance $32 \times 32$ / $64 \times 64$)

* **Hệ quy chiếu**:
  * Nhân vật Overworld: $16 \times 32$ pixel.
  * Sprite Chiến đấu (Battle Sprite): $64 \times 64$ pixel.
* **Đặc trưng mỹ thuật**:
  * Màu sắc trong trẻo, bão hòa vừa phải, thân thiện với màn hình không đèn nền của GBA gốc.
  * Kỹ thuật viền màu chọn lọc (Selective Outlining): Viền bên trong dùng màu tối hơn của mảng màu tiếp giáp, viền ngoài cùng dùng màu nâu sẫm hoặc xám đen.
  * Góc nhìn phối cảnh nghiêng $45^\circ$ nhìn từ trên xuống (Top-down oblique).
