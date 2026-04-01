# Blocks

Create a block by subclassing `mc.Block` and registering it with the mod.

```python
@mod.register
class CoolBlock(mc.Block):
    block_id = "cool_block"
    display_name = "Cool Block"
    hardness = 2.0
    resistance = 6.0
    luminance = 0
    slipperiness = 0.6
    material = "stone"
    sound_group = "stone"
    requires_tool = False
    drops_self = True
    has_block_entity = False
    opaque = True
    collidable = True
```

Registry fields:

- `block_id`: required registry id
- `display_name`: optional in-game name
- `namespace`: set automatically from `mod_id`

Behavior and properties:

- `hardness`
- `resistance`
- `luminance`
- `slipperiness`
- `material`
- `sound_group`
- `requires_tool`
- `drops_self`
- `has_block_entity`
- `uses_block_data`
- `opaque`
- `collidable`
- `variable_rotation`
- `rotation_mode`
- `model_collision`

`has_block_entity` controls generated block-entity support:

- set it to `True` when the block needs persistent ticking behavior
- `@mc.on_tick` on a block will also force block-entity generation even if you forget to set `has_block_entity`
- generated block entities are used for ticking logic, not for Python-defined custom fields or inventory schemas

`uses_block_data` enables a generated persistent block-data store even if the block does not tick:

- use it when you want `ctx.block_entity.get_*` and `ctx.block_entity.set_*` helpers in block hooks
- the compiler will generate a backing block entity automatically
- data is persisted with the block entity NBT
- call `ctx.block_entity.sync()` after changing values when the change should be pushed back through the world update path

Important runtime-appearance limit:

- persistent block data can store things like `"color"`, `"mode"`, `"owner"`, or counters
- Minecraft does not support arbitrary cross-loader hot-swapping of a block's texture/model/emissive assets from raw data alone
- today, the reliable way to change visuals at runtime is to swap the block to another compiled block or variant block id
- so a dye-style workflow is practical as: inspect held item, update block data, and/or replace the block with another registered block that has the desired model and textures

Asset fields:

- `texture`: shortcut for a default `cube_all` model texture
- `emissive_texture`: optional overlay texture used for emissive parts
- `emissive_level`: emissive authoring value from `1` to `255`
- `textures`: full block model texture map override
- `emissive_textures`: full emissive overlay texture map override
- `model`: full block model JSON override
- `emissive_model`: full emissive overlay block model JSON override
- `wall_model`: optional model id/path override used when `rotation_mode = "wall"`
- `floor_model`: optional model id/path override used when `rotation_mode = "floor"`
- `blockstate`: full blockstate JSON override
- `item_model`: full inventory item model JSON override for the block item

Minimal cube block:

```python
@mod.register
class SteelBlock(mc.Block):
    block_id = "steel_block"
    display_name = "Steel Block"
    texture = "storage/steel_block"
```

Interactive block:

```python
@mod.register
class AlarmPanel(mc.Block):
    block_id = "alarm_panel"
    display_name = "Alarm Panel"
    texture = "machines/alarm_panel"
    hardness = 3.0
    resistance = 5.0
    opaque = False

    @mc.on_use
    def on_use(self, ctx):
        if not ctx.world.is_client():
            ctx.player.send_message("Panel used")
            ctx.world.play_sound("playtime:machines/alarm", 1.0, 1.0)
```

Block with persistent data:

```python
@mod.register
class DyeablePanel(mc.Block):
    block_id = "dyeable_panel"
    display_name = "Dyeable Panel"
    texture = "machines/panel_gray"
    uses_block_data = True

    @mc.on_use
    def on_use(self, ctx):
        if ctx.stack.is_of("minecraft:red_dye"):
            ctx.block_entity.set_string("color", "red")
            ctx.block_entity.texture_change("playtime:block/machines/panel_red")
            ctx.block_entity.model_change("playtime:block/dyeable_panel_red")
            ctx.block_entity.sync()
            ctx.stack.decrement(1)
```

Wall-rotated model block:

```python
@mod.register
class HandScanner(mc.Block):
    block_id = "hand_scanner"
    display_name = "Hand Scanner"
    opaque = False
    variable_rotation = True
    rotation_mode = "wall"
    model_collision = True
    model = {
        "parent": "playtime:block/hand_scanner"
    }
    item_model = {
        "parent": "playtime:block/hand_scanner"
    }
```

Floor-rotated model block:

```python
@mod.register
class FloorButton(mc.Block):
    block_id = "floor_button"
    display_name = "Floor Button"
    opaque = False
    variable_rotation = True
    rotation_mode = "floor"
    model = {
        "parent": "playtime:block/floor_button"
    }
```

Emissive block example:

```python
@mod.register
class ReactorLamp(mc.Block):
    block_id = "reactor_lamp"
    display_name = "Reactor Lamp"
    texture = "machines/reactor_lamp"
    emissive_texture = "machines/reactor_lamp_em"
    emissive_level = 191
    opaque = False
```

Rotation and model-shape fields:

- `variable_rotation = True` tells `fabricpy` to generate a horizontal `facing` blockstate automatically
- the compiler assumes your authored model faces north
- `rotation_mode = "wall"` means the model is treated as an upright wall-style model and only gets Y rotation
- `rotation_mode = "floor"` means the model is treated as a floor-placed model and gets the compiler's floor rotation handling before the horizontal facing rotation
- `wall_model` and `floor_model` are optional model id overrides if you want different source model files for the two handling modes
- `model_collision = True` makes generated collision shape follow the model cuboids instead of using the default full cube
- generated outline/selection shape also follows the derived model cuboids when available

Important rotation rule:

- author the model facing north in Blockbench
- `variable_rotation` is only telling the compiler how to rotate that north-facing model in blockstates and generated shapes
- you do not need to pre-rotate the model JSON for east, south, or west variants yourself

Current model-shape limits:

- shape generation only reads plain Blockbench-style `elements` cuboids from the block model JSON
- per-element rotation, cullface tricks, and other advanced model features are not converted into collision math
- if the model has no readable `elements`, `fabricpy` falls back to normal block shapes even if `model_collision = True`

Asset path behavior:

- `texture = "decor/lamp"` resolves to `assets/<modid>/textures/block/decor/lamp.png`
- the generated default block model uses that as `<modid>:block/decor/lamp`
- the generated default block item model points back to the block model
- if you provide a manual `model`, you are responsible for the texture ids inside it

Emissive behavior:

- `emissive_texture` is a second texture aligned to the same UV layout as the base texture
- the usual authoring pattern is to keep only the glowing pixels in the emissive texture and leave the rest transparent
- `emissive_level` is a Python-side value from `1` to `255`
- `fabricpy` maps that value to Minecraft block light `1` to `15`
- on Forge the generated block properties also enable emissive rendering hints for the block
- `fabricpy` generates an extra overlay block model and appends it into the blockstate automatically

Default emissive generation:

- base block model: `assets/<modid>/models/block/<block_id>.json`
- emissive overlay model: `assets/<modid>/models/block/<block_id>__emissive.json`
- blockstate gets an extra overlay model entry for each generated or Python-defined variant/apply entry

Example:

```python
@mod.register
class HandScanner(mc.Block):
    block_id = "hand_scanner"
    texture = "playtime/red_right"
    emissive_texture = "playtime/red_right_emissive"
    emissive_level = 220
    variable_rotation = True
    rotation_mode = "wall"
    model_collision = True
```

That expects:

- base texture:
  `assets/<modid>/textures/block/playtime/red_right.png`
- emissive overlay:
  `assets/<modid>/textures/block/playtime/red_right_emissive.png`

Hooks:

- `@mc.on_use`
- `@mc.on_place`
- `@mc.on_break`
- `@mc.on_tick`

Hook behavior:

- `@mc.on_use`: right click interaction
- `@mc.on_place`: after placement
- `@mc.on_break`: when broken by a player
- `@mc.on_tick`: block-entity tick hook

Block entity example:

```python
@mod.register
class ReactorCore(mc.Block):
    block_id = "reactor_core"
    display_name = "Reactor Core"
    has_block_entity = True
    texture = "machines/reactor_core"

    @mc.on_tick
    def on_tick(self, ctx):
        if not ctx.world.is_client():
            ctx.block_entity.mark_dirty()
```

In a block tick hook:

- `ctx.block_entity` is the generated block entity instance
- `ctx.world` is the block's world
- `ctx.pos` is the block position
- `ctx.state` is the current block state

Current block-entity scope:

- generated automatically per block
- works across Fabric and Forge
- intended for ticking logic and access to the backing block entity object
- custom inventories, menus, sync payloads, and serializers are not yet first-class Python APIs

Example with assets:

```python
@mod.register
class Lamp(mc.Block):
    block_id = "lamp"
    display_name = "Lamp"
    luminance = 15
    texture = "decor/lamp"
```

That `texture` value resolves to:

- `assets/<modid>/textures/block/decor/lamp.png`

If you provide `model`, `blockstate`, or `item_model` manually, those values are emitted as JSON. Repo files under `assets/<modid>/blockstates` and `assets/<modid>/models` override generated defaults.

Rotation examples:

```python
@mod.register
class WallScanner(mc.Block):
    block_id = "wall_scanner"
    texture = "machines/wall_scanner"
    variable_rotation = True
    rotation_mode = "wall"
```

That expects the model front to face north in Blockbench. `fabricpy` generates `facing=north/east/south/west` blockstate variants automatically.

```python
@mod.register
class FloorPad(mc.Block):
    block_id = "floor_pad"
    model = {
        "parent": "minecraft:block/block",
        "textures": {"particle": "mymod:block/machines/floor_pad"},
        "elements": [...]
    }
    variable_rotation = True
    rotation_mode = "floor"
    model_collision = True
```

In that case:

- the model is still authored facing north
- the compiler applies floor-style rotation handling for blockstate variants
- the collision and outline shapes are derived from the model cuboids when possible

Particle note:

- if your block uses a manual model JSON, add a `particle` texture entry
- example:

```json
{
  "parent": "minecraft:block/cube_all",
  "textures": {
    "all": "mymod:block/decor/lamp",
    "particle": "mymod:block/decor/lamp"
  }
}
```

- missing `particle` is the most common reason a block looks correct in-world but breaks with missing-texture particles
