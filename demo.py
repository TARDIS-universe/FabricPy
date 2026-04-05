import fabricpy as mc

mod = mc.Mod(
    mod_id="demo",
    name="Demo",
    version="1.0",
    description="Advanced demo mod for FabricPy",
    authors=["TheDJStudios"],
    minecraft_version="1.20.1",
    loader="all",
)


mod.item_advancement(
    advancement_id="story/get_pickle",
    title="Pickle Acquired",
    description="Obtain the demo pickle.",
    icon_item="demo:pickle",
    parent="minecraft:story/root",
)


demo_bind = mod.keybind(
    keybind_id="demo_ping",
    title="Demo Ping",
    key="R",
    category_title="Demo Controls",
)


@demo_bind.on_press
def on_demo_ping(ctx):
    dep.geckolib.software.bernie.geckolib.core.animation.RawAnimation.begin()
    ctx.player.send_action_bar("Demo keybind fired")


@mod.event("player_use_item")
def on_use_item(ctx):
    if ctx.stack.is_of("demo:pickle"):
        ctx.player.send_action_bar("Pickle demo item used")


@mod.command("demo_status")
def demo_status(ctx):
    ctx.source.send_message("Demo systems online")


@mod.register
class DemoBlock(mc.Block):
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
class DemoRelay(mc.Block):
    block_id = "relay"
    display_name = "Demo Relay"
    hardness = 2.0
    resistance = 4.0
    luminance = 6
    opaque = False
    collidable = True
    has_block_entity = True
    uses_block_data = True
    geo_model = "machines/demo_relay"
    geo_texture = "block"
    geo_animations = "machines/demo_relay"
    default_animation = "controller.idle"
    item_model = {
        "parent": "demo:block/block"
    }

    @mc.on_use
    def on_use(self, ctx):
        if not ctx.world.is_client():
            powered = ctx.block_entity.get_bool("powered")
            ctx.block_entity.set_bool("powered", not powered)
            if powered:
                ctx.block_entity.play_animation("controller.idle")
                ctx.player.send_action_bar("Relay idling")
            else:
                ctx.block_entity.play_animation_once("controller.pulse")
                ctx.player.send_action_bar("Relay pulsed")
            ctx.block_entity.sync()

    @mc.on_tick
    def on_tick(self, ctx):
        if ctx.block_entity.get_bool("powered"):
            if ctx.world.get_time() % 80 == 0:
                ctx.block_entity.play_animation_once("controller.pulse")


@mod.register
class DemoPickle(mc.Item):
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


demo_tab = mod.creative_tab(
    tab_id="demo_tab",
    title="Demo",
    icon_item="demo:pickle",
)
demo_tab.item.add("demo:block")
demo_tab.item.add("demo:relay")
demo_tab.item.add("demo:pickle")


if __name__ == "__main__":
    mod.compile()
