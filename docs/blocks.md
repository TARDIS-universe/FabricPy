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

`has_block_entity` controls generated block-entity support:

- set it to `True` when the block needs persistent ticking behavior
- `@mc.on_tick` on a block will also force block-entity generation even if you forget to set `has_block_entity`
- generated block entities are used for ticking logic, not for Python-defined custom fields or inventory schemas

Asset fields:

- `texture`: shortcut for a default `cube_all` model texture
- `textures`: full block model texture map override
- `model`: full block model JSON override
- `blockstate`: full blockstate JSON override
- `item_model`: full inventory item model JSON override for the block item

Asset path behavior:

- `texture = "decor/lamp"` resolves to `assets/<modid>/textures/block/decor/lamp.png`
- the generated default block model uses that as `<modid>:block/decor/lamp`
- the generated default block item model points back to the block model
- if you provide a manual `model`, you are responsible for the texture ids inside it

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
- works across Fabric, Quilt, Forge, and NeoForge
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
