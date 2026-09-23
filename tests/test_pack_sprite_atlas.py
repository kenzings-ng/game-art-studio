import os
import sys
import json
import tempfile
import unittest
from PIL import Image

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "scripts")))

from pack_sprite_atlas import pack_frames, next_power_of_two


class TestPackSpriteAtlas(unittest.TestCase):
    def test_next_power_of_two(self):
        self.assertEqual(next_power_of_two(1), 1)
        self.assertEqual(next_power_of_two(3), 4)
        self.assertEqual(next_power_of_two(4), 4)
        self.assertEqual(next_power_of_two(50), 64)
        self.assertEqual(next_power_of_two(100), 128)

    def test_pack_frames(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create 4 test frames
            for i in range(4):
                im = Image.new("RGBA", (32, 32), (i * 40, 100, 200, 255))
                im.save(os.path.join(tmpdir, f"frame_{i:02d}.png"))

            atlas_img, atlas_json = pack_frames(tmpdir, padding=2, power_of_two=True)

            self.assertIsNotNone(atlas_img)
            self.assertEqual(len(atlas_json["frames"]), 4)

            # Check power of two dimensions
            w, h = atlas_img.size
            self.assertEqual(w, next_power_of_two(w))
            self.assertEqual(h, next_power_of_two(h))

            # Verify frame keys and metadata
            self.assertIn("frame_00.png", atlas_json["frames"])
            f0 = atlas_json["frames"]["frame_00.png"]
            self.assertEqual(f0["frame"]["w"], 32)
            self.assertEqual(f0["frame"]["h"], 32)
            self.assertEqual(atlas_json["meta"]["format"], "RGBA8888")


if __name__ == "__main__":
    unittest.main()
