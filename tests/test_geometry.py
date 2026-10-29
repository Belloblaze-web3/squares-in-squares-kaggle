import unittest, math
from squares_in_squares.geometry import Square, overlaps, inside, validate_layout
from squares_in_squares.layouts import rectangular_layout

class GeometryTests(unittest.TestCase):
    def test_separate(self): self.assertFalse(overlaps(Square(.5,.5), Square(1.5,.5)))
    def test_overlap(self): self.assertTrue(overlaps(Square(.5,.5), Square(.75,.5)))
    def test_touching_allowed(self): self.assertFalse(overlaps(Square(.5,.5), Square(1.5,.5)))
    def test_rotated_boundary(self): self.assertTrue(inside(Square(1,1,math.pi/4), 2))
    def test_layouts_valid(self):
        for n in range(1,101):
            sq,L=rectangular_layout(n); self.assertEqual(validate_layout(sq,L),[])

if __name__ == '__main__': unittest.main()
