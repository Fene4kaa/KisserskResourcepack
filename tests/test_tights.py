"""Client-facing stocking resources must remain usable in the combined pack."""
import json
from pathlib import Path
import unittest
import zipfile


ROOT = Path(__file__).resolve().parents[1]
STYLES = (
    "white", "black", "pink", "red", "blue", "purple", "green", "yellow", "orange", "cyan",
    "magenta", "lime", "gray", "light_gray", "brown", "light_blue", "navy", "beige", "peach",
    "lavender", "mint", "burgundy", "gold", "silver", "black_white_stripes", "pink_white_stripes",
    "blue_white_stripes", "red_white_stripes", "purple_black_stripes", "mint_pink_stripes",
    "green_white_stripes", "yellow_white_stripes", "orange_white_stripes", "cyan_white_stripes",
    "lavender_white_stripes", "navy_white_stripes", "red_black_stripes", "blue_black_stripes",
    "pink_black_stripes", "yellow_black_stripes", "cyan_purple_stripes", "orange_purple_stripes",
    "sunset_gradient", "ocean_gradient", "galaxy_gradient", "berry_gradient",
    "rainbow", "pastel_rainbow",
)
PATTERNS = (
    "sentry", "dune", "coast", "wild", "ward", "eye", "vex", "tide", "snout", "rib", "spire",
    "wayfinder", "shaper", "silence", "raiser", "host", "flow", "bolt",
)


def resource_path(identifier, directory, extension):
    namespace, path = identifier.split(":", 1)
    return f"assets/{namespace}/{directory}/{path}{extension}"


class StockingPackTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.archive = zipfile.ZipFile(ROOT / "KisserskPack.zip")

    @classmethod
    def tearDownClass(cls):
        cls.archive.close()

    def json(self, name):
        return json.loads(self.archive.read(name))

    def test_all_stocking_styles_have_equipment_and_inventory_textures(self):
        for style in STYLES:
            with self.subTest(style=style):
                equipment = self.json(f"assets/meowtights/equipment/stockings/{style}.json")["layers"]
                self.assertIn("humanoid_leggings", equipment)
                self.assertNotIn("humanoid", equipment, "Boot armor must not render stockings")
                for layer in equipment["humanoid_leggings"]:
                    self.assertIn(resource_path(layer["texture"], "textures/entity/equipment/humanoid_leggings", ".png"),
                                  self.archive.namelist())
                item = self.json(f"assets/meowtights/items/stockings/{style}.json")["model"]
                self.assertEqual("minecraft:model", item["type"])
                model = self.json(resource_path(item["model"], "models", ".json"))
                self.assertEqual("minecraft:item/generated", model["parent"])
                self.assertIn(resource_path(model["textures"]["layer0"], "textures", ".png"), self.archive.namelist())

    def test_standard_trim_patterns_resolve_without_replacing_normal_trims(self):
        atlas = self.json("assets/minecraft/atlases/armor_trims.json")
        sprites = {source["sprite"]: source for source in atlas["sources"]}
        for pattern in PATTERNS:
            sprite = f"minecraft:trims/entity/humanoid_leggings/{pattern}_meowtights_hidden"
            self.assertIn(sprite, sprites)
            self.assertIn(resource_path(sprites[sprite]["resource"], "textures", ".png"), self.archive.namelist())
        self.assertTrue(all(sprite.endswith("_meowtights_hidden") for sprite in sprites),
                        "The combined pack must not hide ordinary armor trims")

    def test_invisible_armor_has_no_player_armor_layers(self):
        equipment = self.json("assets/meowtights/equipment/invisible_armor.json")["layers"]
        self.assertNotIn("humanoid", equipment)
        self.assertNotIn("humanoid_leggings", equipment)
        for layer_type, layers in equipment.items():
            for layer in layers:
                self.assertIn(resource_path(layer["texture"], f"textures/entity/equipment/{layer_type}", ".png"),
                              self.archive.namelist())


if __name__ == "__main__":
    unittest.main()
