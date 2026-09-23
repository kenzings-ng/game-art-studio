# 🎨 Quy Chuẩn Chống "Mùi AI" & Thổi Hồn Thủ Công Vào Game Art (Anti-AI Craft Guide)

> **Mục tiêu**: Loại bỏ triệt để các dấu hiệu nhận biết của tranh do AI sinh ra (AI slop / AI tells) như: bóng gối mờ ảo (pillow shading), chi tiết rác vô nghĩa (ornate greeble), dải màu bẩn (dirty color bleed), tư thế ma-nơ-canh cứng đơ (stiff T-pose), và mang lại sự sống động, sắc nét, có hồn như được vẽ tay bởi các Art Director kỳ cựu của Capcom, SNK, hay Studio Ghibli.

---

## 1. Giải Phẫu 5 Dấu Hiệu "Mùi AI" (AI Tells) Trong 2D & Pixel Art

| Dấu Hiệu AI (AI Tell) | Bản Chất Lỗi Của AI | Cảm Giác Mang Lại | Cách Khắc Phục Thủ Công |
| :--- | :--- | :--- | :--- |
| **1. Pillow Shading (Đánh bóng hình gối)** | AI lấy trung bình màu và làm tối từ mép ngoài vào tâm mọi chi tiết, không có nguồn sáng vật lý. | Chủ thể phồng như gối ôm, mềm nhũn, trông như kẹo dẻo hoặc đất sét. | **Thiết lập nguồn sáng đơn góc $45^\circ$** (Key Light từ trên trái/phải), đổ bóng đổ cứng (Cast Shadow) dứt khoát. |
| **2. Micro-Color Bleed & Gradients (Dải màu bẩn)** | AI pha trộn hàng nghìn dải màu trung gian mờ mờ thay vì dùng bảng màu giới hạn (Indexed Palette). | Tranh bị mờ, đục ngục, bẩn màu, không đạt độ trong trẻo của game 2D. | **Quy tắc dải màu 3–4 bậc (3-4 Color Ramp)** và **Chuyển nhiệt độ màu (Hue Shifting)**. |
| **3. Ornate Greeble (Chi tiết rác ngẫu nhiên)** | Khi prompt "knight" hay "wizard", AI tự ý thêm hoa văn vàng uốn lượn, dây đai chằng chịt, viền rườm rà. | Mất tập trung, nhiễu hạt, không thể đọc được nhân vật từ khoảng cách camera game. | **Quy tắc tỉ lệ chi tiết 70 - 20 - 10**. Giữ 70% diện tích là mảng phẳng nghỉ mắt. |
| **4. Stiff Mannequin Poses (Tư thế ma-nơ-canh)** | AI luôn vẽ nhân vật đứng thẳng tưng, hai chân chịu lực đều 50/50, mắt nhìn vô hồn vào camera. | Cứng đơ như tượng sáp hoặc mô hình đồ chơi nhựa chưa bóc hộp. | **Line of Action (Đường cong chữ C/S)**, **Contrapposto (Trọng tâm lệch)**, và **Anticipation (Nén lực chuẩn bị ra đòn)**. |
| **5. Pixel Sins (Lỗi vỡ pixel)** | AI sinh "pixel giả": pixel không đều hạt (mixels), pixel đơn lẻ trôi nổi (orphan pixels), đường gấp khúc xấu xí (jaggies/doubles). | Trông như ảnh JPG chất lượng thấp bị giảm phân giải cẩu thả chứ không phải pixel art thật. | **Đường nét phân bậc toán học (1-2-3 staircases)**, **Contour viền ngoài đậm**, và **Selective Outlining (Selout)**. |

---

## 2. Bộ Quy Chuẩn 5 Trụ Cột Mỹ Thuật Thủ Công (Master Game Art Framework)

### Trụ Cột I: Tư Thế & Động Lực Học (Line of Action & Silhouette First)

1. **Đường Động Lực (Line of Action)**:
   - **Cấm tuyệt đối**: Cột sống thẳng đứng $90^\circ$.
   - **Bắt buộc**: Vẽ một đường cong chủ đạo (chữ **C** hoặc **S**) xuyên suốt từ đỉnh đầu qua sống lưng xuống chân trụ.
   - Thân người luôn có độ ngả: Chạy ngả về trước $15^\circ - 25^\circ$, gồng đòn ngả lùi nén lực, nhảy uốn cong lưng đón gió.
2. **Nguyên Tắc Trọng Tâm Lệch (Contrapposto & Weight Distribution)**:
   - 1 chân chịu $80\%$ trọng lượng cơ thể (chân trụ), 1 chân thả lỏng/co gối.
   - Trục vai và trục hông phải **nghiêng nghịch chiều nhau** (vai trái nhấc lên thì hông trái hạ xuống).
3. **Thử Nghiệm Bóng Đen (The Blackout Silhouette Test)**:
   - Nếu đổ toàn bộ nhân vật thành màu đen kịt `#000000`, người chơi có lập tức nhận ra class nhân vật, vũ khí và cảm xúc hành động không?
   - Luôn tạo **khoảng trống âm (Negative Space)** giữa hai cánh tay, giữa hai đùi và giữa thân mình với vũ khí. Đừng để tay ép sát sườn hay vũ khí dính liền vào áo giáp.

```
       ❌ DÁNG ĐỨNG AI (Cứng đơ)                  ✅ DÁNG ĐỨNG THỦ CÔNG (Sống động)
           [ O ] (Đầu thẳng)                          [ O ]  (Đầu nghiêng ngắm mục tiêu)
          /  |  \                                     /   \
         |   |   | (Tay ép sát, cột sống thẳng)      /  S  \ (Đường cong S-line mạnh mẽ)
         |   |   |                                  /       \
            / \                                    /  /|     \ (Chân trước tấn, chân sau đẩy)
           |   | (Chân chia lực 50/50)            *   |
```

---

### Trụ Cột II: Ánh Sáng & Quy Tắc Vàng Chuyển Nhiệt Độ Màu (Hue-Shifting)

Đây là bí mật số 1 phân biệt họa sĩ con người đẳng cấp với tranh AI:
> ⚠️ **LUẬT BẤT THÀNH VĂN**: Không bao giờ đổ bóng bằng cách thêm màu Đen/Xám, và không bao giờ tạo ánh sáng bằng cách thêm màu Trắng!

#### Cơ Chế Chuyển Màu Theo Nhiệt Độ (Warm / Cool Balance):
- **Nguồn sáng Nắng ấm (Warm Key Light - Vàng/Cam)**:
  - **Vùng sáng nhất (Highlight)**: Dịch quang phổ về phía Vàng Chanh / Kem Ấm (`Yellow/Cream`).
  - **Màu gốc (Midtone)**: Màu thực của chất liệu.
  - **Bóng đổ (Shadow)**: **Bắt buộc dịch quang phổ về phía Lạnh (Tím Indigo, Xanh Navy, hoặc Mận Chín)** vì bóng tối ngoài trời nhận ánh sáng tán xạ từ vòm trời xanh (Sky Ambient).
- **Nguồn sáng Lạnh (Cool Light - Ánh trăng / Phép thuật băng)**:
  - **Highlight**: Xanh Băng (`Cyan / Ice Blue`).
  - **Shadow**: Dịch sang Đỏ Mận / Tím Ấm (`Warm Plum / Deep Crimson`).

#### Bảng Kiểm Soát Bậc Màu (Color Ramp Budget):
Mỗi chất liệu chỉ được phép dùng **3 đến 4 sắc độ** dứt khoát:
1. `Tone 1 (Highlight)`: Ánh sáng gắt, chiếm 10% bề mặt đối diện đèn.
2. `Tone 2 (Midtone)`: Màu nhận diện chính, chiếm 50% bề mặt.
3. `Tone 3 (Core Shadow)`: Bóng chính có ranh giới rõ ràng, chiếm 35%.
4. `Tone 4 (Dark Accent / Bounce)`: Điểm nhấn rãnh sâu hoặc viền phản xạ, chiếm 5%.

---

### Trụ Cột III: Thanh Lọc Chi Tiết & Tỉ Lệ 70 - 20 - 10 (Resting Areas)

Để diệt trừ triệt để hội chứng "AI Greeble" (vẽ hoa văn rác tùm lum):

- **70% Vùng Nghỉ Mắt (Resting Areas / Broad Planes)**:
  - Tấm giáp ngực phẳng, tà áo choàng phẳng, ống quần trơn, da mặt mịn.
  - Cho mắt người chơi một khoảng lặng để cảm nhận khối hình học lớn.
- **20% Chi Tiết Chức Năng (Functional Secondary Shapes)**:
  - Khóa thắt lưng, nếp gấp khuỷu tay, bao da đựng kiếm, quấn cổ chân.
  - Chi tiết có mục đích thực tế trong chuyển động của nhân vật.
- **10% Điểm Nhấn Tiêu Điểm (Focal Accents)**:
  - Đốm sáng phản chiếu trong đồng tử, vết xước kim loại trên lưỡi gươm, viên ngọc phát sáng ở chuôi kiếm.

---

### Trụ Cột IV: Đường Viền & Kỹ Thuật Selout (Selective Outlining)

Trong game 2D chuyên nghiệp:
1. **Viền Bao Ngoài (External Contour)**:
   - Dùng màu tối sẫm (đen pha màu nền, ví dụ `#111827` hoặc `#1A0B2E`), độ dày 1px (pixel art) hoặc 2-3px (HD 2D).
   - Tách nhân vật hoàn toàn khỏi mọi bối cảnh bản đồ dù sáng hay tối.
2. **Đường Nét Nội Bộ (Internal Selective Outlining - Selout)**:
   - Giữa cơ bắp, múi giáp hay ngón tay: **Không dùng nét đen kịt**.
   - Dùng **phiên bản sẫm hơn của chính màu vật liệu đó** (ví dụ: viền giữa các ngón tay da người là màu Nâu Đỏ sẫm, không phải Đen). Điều này tạo cảm giác khối 3D tự nhiên, không bị cứng như tranh tô màu trẻ em.

---

## 3. Công Thức Soạn Prompt Tinh Gọn: "Chống Mùi AI"

### Từ Điển Cấm (Negative Blacklist):
> ❌ **CẤM DÙNG**: `masterpiece`, `hyperdetailed`, `ultra-realistic 8k`, `intricate filigree`, `unreal engine render`, `octane render`, `cinematic lighting`, `volumetric fog`, `diffuse bloom`, `ambient occlusion`, `trending on artstation`.
> *(Các từ này kích hoạt bộ lọc tạo hạt nhiễu, làm nhòe viền và sinh ra hoa văn rác của các mô hình AI).*

### Từ Điển Vàng Thủ Công (Positive Craft Keywords):
> ✅ **NÊN DÙNG**:
> - **Pixel Art**: `16-bit arcade sprite, Capcom CPS2 aesthetic, chunky pixel clusters, strict 4-tone color ramp, dynamic S-curve line of action, hue-shifted cool violet shadows, crisp 1px dark charcoal contour, no pillow shading, flat solid background #FF00FF`.
> - **HD 2D / Hand-Drawn**: `Clean stylized 2D game illustration, bold ink outlines, cell-shaded lighting, warm golden key light from top-left, rich saturated shadows, graphic shape design, expressive pose with contrapposto, Hollow Knight and Hades game art style, solid color background`.

---

## 4. Ví Dụ Mẫu Đối Chiếu: Dở vs Xuất Sắc

### Ví Dụ 1: Chiến Binh Pixel Đánh Kiếm

- ❌ **Prompt Kém (Đầy mùi AI)**:
  > `A fantasy knight warrior swinging a sword, masterpiece, 8k, hyper detailed armor with gold ornaments, dynamic lighting, octane render, unreal engine 5, beautiful background.`
  > *(Hậu quả: Giáp đầy rác vàng kim, mặt vô hồn, bóng viền mờ căm như đất sét, nền lem nhem).*

- ✅ **Prompt Chuẩn Studio (Sống động, Đậm chất nghệ nhân thủ công)**:
  > `16-bit arcade pixel art sprite of an athletic rogue knight mid-strike with an executioner sword. Action-first pose: body lunging forward at 20-degree angle, weight heavy on front bent knee, claymore swinging in a sharp motion arc. Clean Capcom CPS2 palette: burnished steel armor with crisp cel-shaded plane shifts, sunlight highlights from top-left shifting to deep indigo shadows. 70 percent clean resting metal plates, zero filigree, bold 1px charcoal outer contour, clear negative space between legs and blade, pure magenta background #FF00FF, no floor shadow.`

---

### Ví Dụ 2: Biểu Tượng Trang Bị (Item Icon)

- ❌ **Prompt Kém (Đầy mùi AI)**:
  > `Magic sword icon, ultra realistic glowing crystal sword, epic detailed, fantasy concept art, artstation.`

- ✅ **Prompt Chuẩn Studio**:
  > `Clean 32-bit RPG inventory icon of a runic frost broadsword, angled diagonally at 45 degrees. Chunky readable silhouette, clear geometric crossguard, deep cobalt steel blade with crisp cyan-white edge highlight. No blurry glow, hard-edged cel-shaded facets, limited 8-color palette, solid dark slate border, transparent background.`
