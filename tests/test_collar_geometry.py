"""Check the shipped collar against a neutral vanilla player, in player pixels."""
from itertools import product
import json
import math
from pathlib import Path
import unittest
import zipfile


PACK = Path(__file__).resolve().parents[1] / "KisserskPack.zip"


def corners(low, high):
    return [tuple(high[i] if bit else low[i] for i, bit in enumerate(bits))
            for bits in product((0, 1), repeat=3)]


def rotate(point, origin, axis, angle):
    result = [point[i] - origin[i] for i in range(3)]
    a, b = {"x": (1, 2), "y": (2, 0), "z": (0, 1)}[axis]
    cosine, sine = math.cos(math.radians(angle)), math.sin(math.radians(angle))
    result[a], result[b] = (result[a] * cosine - result[b] * sine,
                            result[a] * sine + result[b] * cosine)
    return tuple(result[i] + origin[i] for i in range(3))


def player_vertices(element, display):
    vertices = corners(element["from"], element["to"])
    rotation = element.get("rotation")
    if rotation:
        vertices = [rotate(p, rotation["origin"], rotation["axis"], rotation["angle"])
                    for p in vertices]
    # CustomHeadLayer: +4 pixels, scale 0.625; its Y half-turn cancels head.rotation.y.
    result = []
    for vertex in vertices:
        point = tuple((vertex[i] - 8) * display["scale"][i] for i in range(3))
        for axis, angle in zip("xyz", display.get("rotation", [0, 0, 0])):
            point = rotate(point, (0, 0, 0), axis, angle)
        point = tuple((point[i] + display["translation"][i]) * 0.625 for i in range(3))
        point = rotate(point, (0, 0, 0), "y", 180)
        result.append((point[0], point[1] + 4, point[2]))
    return result


def subtract(a, b):
    return tuple(x - y for x, y in zip(a, b))


def cross(a, b):
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2],
            a[0] * b[1] - a[1] * b[0])


def intersects(vertices, low, high):
    """Separating-axis test: rotated cuboid versus axis-aligned player part."""
    other = corners(low, high)
    edges = [subtract(vertices[i], vertices[0]) for i in (4, 2, 1)]
    basis = [(1, 0, 0), (0, 1, 0), (0, 0, 1)]
    axes = basis + [cross(edges[i], edges[(i + 1) % 3]) for i in range(3)]
    axes += [cross(edge, axis) for edge in edges for axis in basis]
    for axis in axes:
        magnitude = math.sqrt(sum(x * x for x in axis))
        if magnitude < 1e-9:
            continue
        axis = tuple(x / magnitude for x in axis)
        left = [sum(x * y for x, y in zip(point, axis)) for point in vertices]
        right = [sum(x * y for x, y in zip(point, axis)) for point in other]
        if min(max(left), max(right)) - max(min(left), min(right)) <= 1e-6:
            return False
    return True


class CollarFitTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with zipfile.ZipFile(PACK) as pack:
            model = json.loads(pack.read("assets/meowdoggie/models/item/collar.json"))
        cls.elements = [(e.get("name", str(i)), player_vertices(e, model["display"]["head"]))
                        for i, e in enumerate(model["elements"])]
        cls.leather = [geometry for element, geometry in zip(model["elements"], cls.elements)
                       if element["faces"]["north"]["texture"] == "#leather"]

    def test_no_head_penetration(self):
        collisions = [name for name, vertices in self.elements
                      if intersects(vertices, (-4, 0, -4), (4, 8, 4))]
        self.assertEqual([], collisions, "Collar or fittings penetrate the head")

    def test_no_shoulder_or_torso_penetration(self):
        # Together these are the torso and both classic arms in their neutral pose.
        collisions = [name for name, vertices in self.elements
                      if intersects(vertices, (-8, -12, -2), (8, 0, 2))]
        self.assertEqual([], collisions, "Collar is buried in the shoulders or torso")

    def test_lateral_sections_rest_on_shoulders(self):
        # Only geometry directly over a shoulder must stay within 1/8 pixel of it.
        supported = []
        for name, vertices in self.leather:
            # Test the footprint by extending the shoulder volume vertically.
            for low_x, high_x in ((-8, -4), (4, 8)):
                if intersects(vertices, (low_x, -100, -2), (high_x, 100, 2)):
                    supported.append((name, min(p[1] for p in vertices)))
        self.assertTrue(supported, "The collar no longer reaches the shoulders")
        for name, bottom in supported:
            with self.subTest(element=name):
                self.assertGreaterEqual(bottom, -1e-6)
                self.assertLessEqual(bottom, 0.125, "Side section floats above the shoulder")


if __name__ == "__main__":
    unittest.main()
