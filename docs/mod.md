# Mod API

`mc.Mod(...)` is the root object for a mod definition.

Constructor arguments:

- `mod_id`: lowercase identifier used for registry names and asset/data paths
- `name`: display name shown in the mod list
- `version`: mod version string, default `1.0.0`
- `description`: short description
- `authors`: list of author names
- `minecraft_version`: target Minecraft version, default `1.20.1`
- `loader`: `fabric`, `forge`, `both`, or `all`
- `package`: Java package root, defaults to `com.generated.<mod_id>`
- `website`: optional homepage URL
- `license`: license string, default `MIT`

Main methods:

- `mod.register(cls)`: register a `mc.Block`, `mc.Item`, `mc.Entity`, or `mc.Mixin`
- `mod.event(name)`: register a mod event handler
- `mod.command(name, permission_level=0, aliases=None)`: register a slash command
- `mod.add_recipe(recipe_id, data)`: register raw recipe JSON
- `mod.shaped_recipe(recipe_id, result, pattern, key, count=1)`: register a shaped recipe
- `mod.shapeless_recipe(recipe_id, result, ingredients, count=1)`: register a shapeless recipe
- `mod.add_advancement(...)`: register an advancement from Python fields
- `mod.add_advancement_json(advancement_id, data)`: register raw advancement JSON
- `mod.item_advancement(...)`: register a simple inventory-based advancement
- `mod.add_sound(sound_id, sounds, subtitle="", replace=False)`: register a sound event for `sounds.json`
- `mod.creative_tab(tab_id, title, icon_item)`: create a custom creative tab builder
- `mod.keybind(keybind_id, title, key, category="", category_title="")`: define a client keybind
- `mod.add_dimension_type(type_id, data)`: register a dimension type JSON
- `mod.add_dimension(dimension_id, dimension_type, generator=None, data=None)`: register a dimension JSON
- `mod.add_structure(structure_id, nbt_path)`: copy an NBT structure template into the generated datapack
- `mod.compile(output_dir="./dist", clean=False)`: generate projects and build jars

Useful patterns:

- blocks that need persistent editable state should use `uses_block_data = True`
- global gameplay hooks such as `player_use_item`, `player_use_block`, `player_tick`, `player_attack_entity`, and `player_interact_entity` are registered through `mod.event(...)`
- runtime visual changes are currently done by swapping to another compiled block or variant block id, not by arbitrary live texture mutation
- advancements are emitted into `data/<modid>/advancements/...`
- creative tab titles are emitted into `assets/<modid>/lang/en_us.json`

Registration styles:

```python
mod.register(MyBlock)

@mod.register
class MyItem(mc.Item):
    item_id = "my_item"
```

The same registration API is used for entities:

```python
@mod.register
class MyEntity(mc.Entity):
    entity_id = "my_entity"
```

Example:

```python
import fabricpy as mc

mod = mc.Mod(
    mod_id="mymod",
    name="My Mod",
    version="1.0.0",
    description="Example mod",
    authors=["You"],
    minecraft_version="1.20.1",
    loader="both",
)
```

Full starter example:

```python
import fabricpy as mc

mod = mc.Mod(
    mod_id="examplemod",
    name="Example Mod",
    version="1.0.0",
    description="Example content pack",
    authors=["You"],
    minecraft_version="1.20.1",
    loader="both",
)


@mod.register
class ExampleItem(mc.Item):
    item_id = "example_item"
    display_name = "Example Item"
    texture = "tools/example_item"


@mod.register
class ExampleBlock(mc.Block):
    block_id = "example_block"
    display_name = "Example Block"
    texture = "machines/example_block"
    hardness = 2.0
    resistance = 4.0


@mod.event("player_join")
def on_join(ctx):
    ctx.player.send_message("Example Mod loaded")


mod.shapeless_recipe(
    "example_item",
    result="examplemod:example_item",
    ingredients=[{"item": "minecraft:iron_ingot"}],
)


if __name__ == "__main__":
    mod.compile()
```

Advancement example:

```python
mod.item_advancement(
    advancement_id="story/get_scanner",
    title="Field Kit",
    description="Obtain a hand scanner.",
    icon_item="playtime:hand_scanner",
    parent="playtime:story/root",
)
```

Creative tab example:

```python
tools_tab = mod.creative_tab(
    tab_id="tools",
    title="Playtime Tools",
    icon_item="playtime:hand_scanner",
)

tools_tab.item.add("playtime:hand_scanner")
tools_tab.item.add("minecraft:redstone")
```

Sound example:

```python
mod.add_sound(
    "machines/alarm",
    "machines/alarm",
    subtitle="Alarm sounding",
)
```

Keybind example:

```python
scanner_bind = mod.keybind(
    keybind_id="open_scanner",
    title="Open Scanner",
    key="R",
    category_title="Playtime Controls",
)

@scanner_bind.on_press
def on_open_scanner(ctx):
    ctx.player.send_action_bar("Scanner opened")
```

Dimension example:

```python
mod.add_dimension_type("pocket", {
    "ultrawarm": False,
    "natural": False,
    "coordinate_scale": 1.0,
    "has_skylight": False,
    "has_ceiling": True,
    "ambient_light": 0.0,
    "fixed_time": 18000,
    "bed_works": True,
    "respawn_anchor_works": False,
    "min_y": 0,
    "height": 256,
    "logical_height": 256,
    "infiniburn": "#minecraft:infiniburn_overworld",
    "effects": "minecraft:overworld",
})
```

Generated project layout:

- jars are copied to `dist/` by default
- generated projects live under `.fabricpy_build/`
- repo assets are sourced from `assets/<modid>/...`
- repo data files are sourced from `data/<modid>/...`
- dimension JSON goes under `data/<modid>/dimension_type` and `data/<modid>/dimension`
- structure NBT files go under `data/<modid>/structures`

Loader matrix:

- `1.20.1`: `fabric`, `forge`
- `1.21.1`: `fabric`, `forge`
- `both`: always means `fabric+forge`
- `all`: also resolves to `fabric+forge`
