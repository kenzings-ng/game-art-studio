import os
import sys
import tempfile
import unittest

from PIL import Image

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "scripts")))

from generate_item_icon_sheet import RARITY_COLORS, apply_rarity_border, parse_grid_dimensions, slice_icon_grid


class TestGenerateItemIconSheet(unittest.TestCase):
    def test_parse_grid_dimensions(self):
        self.assertEqual(parse_grid_dimensions("4x4"), (4, 4))
        self.assertEqual(parse_grid_dimensions("3x5"), (3, 5))
        self.assertEqual(parse_grid_dimensions("4X4"), (4, 4))
        self.assertEqual(parse_grid_dimensions("4"), (4, 4))
        self.assertEqual(parse_grid_dimensions("5"), (5, 5))
        self.assertEqual(parse_grid_dimensions(""), (None, None))
        self.assertEqual(parse_grid_dimensions(None), (None, None))
        self.assertEqual(parse_grid_dimensions("invalid"), (None, None))

    def test_apply_rarity_border(self):
        img = Image.new("RGBA", (32, 32), (0, 0, 0, 255))
        bordered = apply_rarity_border(img, rarity="rare", border_width=2)
        expected_color = RARITY_COLORS["rare"]

        self.assertEqual(bordered.getpixel((0, 0)), expected_color)
        self.assertEqual(bordered.getpixel((1, 1)), expected_color)
        self.assertEqual(bordered.getpixel((31, 31)), expected_color)
        self.assertEqual(bordered.getpixel((16, 16)), (0, 0, 0, 255))

    def test_slice_icon_grid(self):
        img = Image.new("RGBA", (128, 128), (100, 100, 100, 255))
        with tempfile.TemporaryDirectory() as tmpdir:
            input_path = os.path.join(tmpdir, "icons.png")
            out_dir = os.path.join(tmpdir, "output")
            img.save(input_path)

            saved = slice_icon_grid(input_path, out_dir, rows=2, cols=2, icon_size=(48, 48), default_rarity="epic")
            self.assertEqual(len(saved), 4)
            for p in saved:
                self.assertTrue(os.path.exists(p))
                with Image.open(p) as icon:
                    self.assertEqual(icon.size, (48, 48))


if __name__ == "__main__":
    unittest.main()
