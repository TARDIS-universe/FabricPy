# Items

Create an item by subclassing `mc.Item` and registering it with the mod.

```python
@mod.register
class Pickle(mc.Item):
    item_id = "pickle"
    display_name = "Pickle"
    max_stack_size = 64
    max_damage = 0
    rarity = "epic"
    fireproof = False
    food_hunger = 4
    food_saturation = 6
    food_always_edible = True
    is_tool = False
    tool_type = ""
    tool_material = "iron"
```

Registry fields:

- `item_id`: required registry id
- `display_name`: optional in-game name
- `namespace`: set automatically from `mod_id`

Gameplay fields:

- `max_stack_size`
- `max_damage`
- `rarity`
- `fireproof`
- `food_hunger`
- `food_saturation`
- `food_always_edible`
- `is_tool`
- `tool_type`
- `tool_material`

Asset fields:

- `texture`: shortcut for a default generated item model `layer0`
- `emissive_texture`: optional overlay texture used for emissive parts
- `emissive_level`: emissive authoring value from `1` to `255`
- `textures`: full item model texture map override
- `model`: full item model JSON override

Asset path behavior:

- `texture = "food/pickle"` resolves to `assets/<modid>/textures/item/food/pickle.png`
- `emissive_texture = "food/pickle_glow"` resolves to `assets/<modid>/textures/item/food/pickle_glow.png`
- the generated default item model uses `layer0: "<modid>:item/food/pickle"`
- if `emissive_texture` is set, the generated default item model also adds `layer1`
- if you provide a manual `model`, you are responsible for writing the correct item texture id yourself

Emissive note:

- item emissive textures are currently emitted as an additional model layer
- that preserves the separate texture workflow and UV alignment
- true fullbright item rendering is still not guaranteed across every loader without a custom renderer

Hooks:

- `@mc.on_right_click`

Minimal item:

```python
@mod.register
class Gear(mc.Item):
    item_id = "gear"
    display_name = "Gear"
    texture = "parts/gear"
```

Food item:

```python
@mod.register
class Pickle(mc.Item):
    item_id = "pickle"
    display_name = "Pickle"
    texture = "food/pickle"
    food_hunger = 4
    food_saturation = 6
    food_always_edible = True
```

Single-stack tool item:

```python
@mod.register
class HandScanner(mc.Item):
    item_id = "hand_scanner"
    display_name = "Hand Scanner"
    texture = "tools/hand_scanner"
    max_stack_size = 1
    rarity = "rare"
```

Custom model item:

```python
@mod.register
class GrabPack(mc.Item):
    item_id = "grabpack_cannon"
    display_name = "Grabpack Cannon"
    max_stack_size = 1
    model = {
        "parent": "playtime:item/tool/grabpack"
    }
```

Item with right-click behavior:

```python
@mod.register
class TeleportAnchor(mc.Item):
    item_id = "teleport_anchor"
    display_name = "Teleport Anchor"
    texture = "tools/teleport_anchor"

    @mc.on_right_click
    def on_right_click(self, ctx):
        if not ctx.world.is_client():
            ctx.player.teleport(0, 80, 0)
            ctx.player.send_action_bar("Teleported")
```

Item appearance state example:

```python
@mod.register
class PaintGun(mc.Item):
    item_id = "paint_gun"
    display_name = "Paint Gun"
    texture = "tools/paint_gun"

    @mc.on_right_click
    def on_right_click(self, ctx):
        ctx.stack.texture_change("playtime:item/tools/paint_gun_red")
        ctx.stack.model_change("playtime:item/tools/paint_gun_red")
```

Example with assets:

```python
@mod.register
class Pickle(mc.Item):
    item_id = "pickle"
    texture = "food/pickle"
```

That `texture` value resolves to:

- `assets/<modid>/textures/item/food/pickle.png`

Equivalent generated model:

```json
{
  "parent": "minecraft:item/generated",
  "textures": {
    "layer0": "<modid>:item/food/pickle"
  }
}
```

Common mistake:

- writing a manual item model with `"<modid>:food/pickle"`
- item textures need the `item/` segment
- the correct value is `"<modid>:item/food/pickle"`
