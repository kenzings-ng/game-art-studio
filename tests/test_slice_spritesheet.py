import os
import sys
import tempfile
import unittest

import numpy as np
from PIL import Image

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "scripts")))

from slice_spritesheet import parse_color_key, remove_background, slice_horizontal_strip


class TestSliceSpritesheet(unittest.TestCase):
    def test_parse_color_key(self):
        self.assertEqual(parse_color_key("auto"), "auto")
        self.assertEqual(parse_color_key("sample"), "auto")
        self.assertEqual(parse_color_key("none"), "none")
        self.assertEqual(parse_color_key("null"), "none")
        self.assertEqual(parse_color_key("magenta"), (255, 0, 255))
        self.assertEqual(parse_color_key("green"), (0, 255, 0))
        self.assertEqual(parse_color_key("black"), (0, 0, 0))
        self.assertEqual(parse_color_key("white"), (255, 255, 255))
        self.assertEqual(parse_color_key("#FF00FF"), (255, 0, 255))
        self.assertEqual(parse_color_key("#00FF00"), (0, 255, 0))
        self.assertEqual(parse_color_key("#123456"), (18, 52, 86))
        self.assertEqual(parse_color_key("invalid_value"), "auto")

    def test_remove_background(self):
        img = Image.new("RGBA", (50, 50), (255, 0, 255, 255))
        for x in range(20, 30):
            for y in range(20, 30):
                img.putpixel((x, y), (0, 255, 0, 255))

        res_auto = remove_background(img, color_key="auto", tolerance=10)
        self.assertEqual(res_auto.getpixel((0, 0))[3], 0)
        self.assertEqual(res_auto.getpixel((25, 25)), (0, 255, 0, 255))

        res_keyed = remove_background(img, color_key=(255, 0, 255), tolerance=10)
        self.assertEqual(res_keyed.getpixel((0, 0))[3], 0)
        self.assertEqual(res_keyed.getpixel((25, 25)), (0, 255, 0, 255))

        res_none = remove_background(img, color_key="none")
        self.assertEqual(res_none.getpixel((0, 0))[3], 255)

    def test_slice_horizontal_strip_with_empty_frame(self):
        strip = Image.new("RGBA", (300, 100), (0, 0, 0, 0))

        # Frame 0: 30x30 red box
        for x in range(35, 65):
            for y in range(60, 90):
                strip.putpixel((x, y), (255, 0, 0, 255))

        # Frame 1: empty/transparent

        # Frame 2: 20x20 blue box
        for x in range(240, 260):
            for y in range(70, 90):
                strip.putpixel((x, y), (0, 0, 255, 255))

        with tempfile.TemporaryDirectory() as tmpdir:
            paths = slice_horizontal_strip(strip, num_frames=3, output_dir=tmpdir, prefix="test", anchor="bottom_center")
            self.assertEqual(len(paths), 3)

            sizes = []
            for p in paths:
                self.assertTrue(os.path.exists(p))
                with Image.open(p) as frame_im:
                    sizes.append(frame_im.size)

            self.assertEqual(sizes[0], sizes[1])
            self.assertEqual(sizes[1], sizes[2])
            self.assertEqual(sizes[0], (38, 38))

            with Image.open(paths[1]) as empty_frame:
                alpha = np.array(empty_frame)[:, :, 3]
                self.assertEqual(np.max(alpha), 0)

    def test_slice_horizontal_strip_all_empty(self):
        strip = Image.new("RGBA", (200, 50), (0, 0, 0, 0))
        with tempfile.TemporaryDirectory() as tmpdir:
            paths = slice_horizontal_strip(strip, num_frames=2, output_dir=tmpdir)
            self.assertEqual(len(paths), 2)
            with Image.open(paths[0]) as im:
                self.assertTrue(im.width > 0 and im.height > 0)


if __name__ == "__main__":
    unittest.main()
