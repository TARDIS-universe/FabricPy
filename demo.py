import fabricpy as mc

mod = mc.Mod(
    mod_id="demo",
    name="Demo",
    version="1.0",
    description="This is a demo for all loaders on 1.20.1",
    authors=["TheDJStudios"],
    minecraft_version="1.20.1",
    loader="all",
)

@mod.register
class block(mc.Block):
    block_id = "block"
    display_name = "Demo Block"
    hardness = 2.0
    resistance = 4.0
    luminance = 8
    slipperiness = 0.6
    material = "stone"
    sound_group = "stone"
    requires_tool = False
    opaque = True
    collidable = True
    texture = "block/block"
    blockstate = {
        "variants": {
            "": {"model": "demo:block/block"}
        }
    }
    model = {
        "parent": "minecraft:block/cube_all",
        "textures": {
            "all": "demo:block/block"
        }
    }
    item_model = {
        "parent": "demo:block/block"
    }
@mod.register
class pickle(mc.Item):
    item_id = "pickle"
    display_name = "Pickle"
    max_stack_size = 8
    max_damage = 0
    rarity = "epic"
    food_hunger = 4
    food_saturation = 6
    food_always_edible = True
    is_tool = False
    texture = "food/pickle"

if __name__ == "__main__":
    mod.compile()