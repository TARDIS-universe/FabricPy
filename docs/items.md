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
- `textures`: full item model texture map override
- `model`: full item model JSON override

Hooks:

- `@mc.on_right_click`

Example with assets:

```python
@mod.register
class Pickle(mc.Item):
    item_id = "pickle"
    texture = "food/pickle"
```

That `texture` value resolves to:

- `assets/<modid>/textures/item/food/pickle.png`
