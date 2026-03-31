import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import fabricpy as mc

mod = mc.Mod(
    mod_id="test",
    name="Test Mod",
    version="1.0.0",
    description="A mod to test fabricpy",
    authors=["TheDJStudios"],
    minecraft_version="1.20.1",
    loader="both",          # Generates both Fabric AND Forge .jar files
    package="com.tdjs.testmod",
)

@mod.event("player_join")
def on_join(ctx):
    ctx.player.send_message("You are running a Development build Of a demo for FabricPy")

class pickle(mc.Item):
    item_id = "pickle"
    display_name = "Pickle"
    max_stack_size = 64
    rarity = "epic"
    food_hunger = 4
    food_saturation = 6
    food_always_edible = True
    texture = "food/pickle"
    model = {
        "parent": "minecraft:item/generated",
        "textures": {
            "layer0": "test:item/food/pickle"
        }
    }

class block(mc.Block):
    block_id = "block"
    display_name = "Block"
    hardness = 2.0
    resistance = 2.0
    luminance = 10
    slipperiness = 0.5
    sound_group = "stone"
    requires_tool = False
    drops_self = True
    opaque = True
    collidable = True
    texture = "test/block"
    blockstate = {
        "variants": {
            "": {"model": "test:block/block"}
        }
    }
    model = {
        "parent": "minecraft:block/cube_all",
        "textures": {
            "all": "test:block/test/block"
        }
    }
    item_model = {
        "parent": "test:block/block"
    }

@mod.command("test", permission_level=0)
def test(ctx):
    player = ctx.source.get_player()
    ctx.source.send_message(f"{player}")

mod.register(pickle)
mod.register(block)
mod.shapeless_recipe(
    "pickle",
    result="test:pickle",
    ingredients=[
        {"item": "minecraft:slime_ball"}
    ],
)


if __name__ == "__main__":
    mod.compile(output_dir="dist", clean=True)
