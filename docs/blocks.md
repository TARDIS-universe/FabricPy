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
- `opaque`
- `collidable`

Asset fields:

- `texture`: shortcut for a default `cube_all` model texture
- `textures`: full block model texture map override
- `model`: full block model JSON override
- `blockstate`: full blockstate JSON override
- `item_model`: full inventory item model JSON override for the block item

Hooks:

- `@mc.on_use`
- `@mc.on_place`
- `@mc.on_break`
- `@mc.on_tick`

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
