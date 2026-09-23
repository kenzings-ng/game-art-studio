import os
import sys
import tempfile
import unittest
from PIL import Image

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "scripts")))

from import_godot_flipbooks import generate_godot_uid, create_godot_sprite_frames


class TestImportGodotFlipbooks(unittest.TestCase):
    def test_generate_godot_uid(self):
        uid = generate_godot_uid()
        self.assertTrue(uid.startswith("uid://"))
        self.assertTrue(len(uid) > 10)

    def test_create_godot_sprite_frames(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            for i in range(3):
                im = Image.new("RGBA", (32, 32), (i * 50, 100, 100, 255))
                im.save(os.path.join(tmpdir, f"frame_{i:02d}.png"))

            tres_path = os.path.join(tmpdir, "output.tres")
            success = create_godot_sprite_frames(
                frames_dir=tmpdir,
                output_tres_path=tres_path,
                godot_res_dir="res://test_art",
                anim_name="walk",
                fps=15.0,
                loop=True,
                generate_scene=True
            )

            self.assertTrue(success)
            self.assertTrue(os.path.exists(tres_path))

            with open(tres_path, "r", encoding="utf-8") as f:
                content = f.read()

            self.assertIn('[gd_resource type="SpriteFrames"', content)
            self.assertIn('path="res://test_art/frame_00.png"', content)
            self.assertIn('path="res://test_art/frame_01.png"', content)
            self.assertIn('path="res://test_art/frame_02.png"', content)
            self.assertIn('"name": &"walk"', content)
            self.assertIn('"speed": 15.0', content)
            self.assertIn('"loop": true', content)

            tscn_path = os.path.join(tmpdir, "output.tscn")
            self.assertTrue(os.path.exists(tscn_path))
            with open(tscn_path, "r", encoding="utf-8") as f:
                tscn_content = f.read()

            self.assertIn('[node name="output" type="AnimatedSprite2D"]', tscn_content)
            self.assertIn('autoplay = "walk"', tscn_content)


if __name__ == "__main__":
    unittest.main()
