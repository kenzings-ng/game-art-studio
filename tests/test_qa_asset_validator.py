import os
import sys
import tempfile
import unittest

from PIL import Image

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "scripts")))

from qa_asset_validator import (
    analyze_palette,
    check_clipping,
    validate_animation_frames,
    validate_isometric_tile,
)


class TestQAAssetValidator(unittest.TestCase):
    def test_analyze_palette(self):
        im = Image.new("RGBA", (10, 10), (0, 0, 0, 0))
        im.putpixel((1, 1), (255, 0, 0, 255))
        im.putpixel((2, 2), (0, 255, 0, 255))
        im.putpixel((3, 3), (0, 0, 255, 255))

        palette = analyze_palette(im)
        self.assertEqual(len(palette), 3)
        self.assertIn((255, 0, 0), palette)
        self.assertIn((0, 255, 0), palette)
        self.assertIn((0, 0, 255), palette)

    def test_check_clipping(self):
        # 20x20 image with pixel at border (0, 10) -> left clipped
        clipped_im = Image.new("RGBA", (20, 20), (0, 0, 0, 0))
        clipped_im.putpixel((0, 10), (255, 255, 255, 255))
        is_clipped, edges = check_clipping(clipped_im, margin=1)
        self.assertTrue(is_clipped)
        self.assertIn("left", edges)

        # 20x20 image with content safely padded in center
        safe_im = Image.new("RGBA", (20, 20), (0, 0, 0, 0))
        safe_im.putpixel((10, 10), (255, 255, 255, 255))
        is_clipped, edges = check_clipping(safe_im, margin=1)
        self.assertFalse(is_clipped)
        self.assertEqual(len(edges), 0)

    def test_validate_animation_frames(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create 2 valid frames with 2 colors and proper padding
            for i in range(2):
                frame = Image.new("RGBA", (32, 32), (0, 0, 0, 0))
                frame.putpixel((16, 16), (255, 0, 0, 255))
                frame.putpixel((16, 17), (0, 255, 0, 255))
                frame.save(os.path.join(tmpdir, f"frame_{i:02d}.png"))

            passed, warnings = validate_animation_frames(tmpdir, max_colors=16)
            self.assertTrue(passed)
            self.assertEqual(len(warnings), 0)

            # Palette budget test: pass max_colors=1 when 2 colors are used
            passed_strict, warnings_strict = validate_animation_frames(tmpdir, max_colors=1)
            self.assertFalse(passed_strict)
            self.assertTrue(any("Palette Budget Exceeded" in w for w in warnings_strict))

    def test_validate_isometric_tile(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            # 1. Perfectly conformant 128x64 diamond
            tile = Image.new("RGBA", (128, 64), (0, 0, 0, 0))
            center_x, center_y = 63.5, 31.5
            for y in range(64):
                for x in range(128):
                    if (abs(x - center_x) / 64.0) + (abs(y - center_y) / 32.0) <= 0.95:
                        tile.putpixel((x, y), (100, 200, 100, 255))

            tile_path = os.path.join(tmpdir, "good_tile.png")
            tile.save(tile_path)
            passed, warnings = validate_isometric_tile(tile_path)
            self.assertTrue(passed)
            self.assertEqual(len(warnings), 0)

            # 2. Defective tile with pixels leaking in the corners
            tile.putpixel((0, 0), (255, 0, 0, 255))  # Corner outside diamond
            bad_tile_path = os.path.join(tmpdir, "bad_tile.png")
            tile.save(bad_tile_path)
            passed, warnings = validate_isometric_tile(bad_tile_path)
            self.assertFalse(passed)
            self.assertTrue(any("Isometric Seam Defect" in w for w in warnings))


if __name__ == "__main__":
    unittest.main()
