# Entities

Create a normal entity by subclassing `mc.Entity` and registering it with the mod.

```python
@mod.register
class PocketSentinel(mc.Entity):
    entity_id = "pocket_sentinel"
    display_name = "Pocket Sentinel"
    width = 0.8
    height = 2.1
    tracking_range = 10
    update_rate = 3
    spawn_group = "misc"
    fireproof = False
    summonable = True
    max_health = 30.0
    movement_speed = 0.3
    attack_damage = 4.0
    follow_range = 24.0
    knockback_resistance = 0.2

    @mc.on_tick
    def on_tick(self, ctx):
        if ctx.entity.get_pos_y() < 0:
            ctx.entity.discard()
```

Registry fields:

- `entity_id`: required registry id
- `display_name`: optional in-game name
- `namespace`: set automatically from `mod_id`

Size and networking fields:

- `width`: entity hitbox width
- `height`: entity hitbox height
- `tracking_range`: how far away clients keep tracking the entity
- `update_rate`: network update interval
- `spawn_group`: one of `misc`, `creature`, `monster`, `ambient`, `water_creature`, `water_ambient`, `underground_water_creature`, `axolotls`
- `fireproof`: register the entity as fire-immune when the loader supports it
- `summonable`: Python-side metadata for intent; the current generators do not yet change registration based on this flag

Attribute fields:

- `max_health`
- `movement_speed`
- `attack_damage`
- `follow_range`
- `knockback_resistance`

Current generated Java shape:

- Fabric generates a `PathAwareEntity`
- Forge generates a `PathfinderMob`
- a basic attribute builder is generated from the fields above
- no default AI goals are generated yet

Hooks:

- `@mc.on_tick`

`@mc.on_tick` on an entity maps to the Java entity `tick()` method. In that hook:

- `ctx.entity` is the current entity
- `ctx.world` is the owning world/level
- `ctx.pos` is the current block position

Useful context helpers:

- `ctx.entity.get_pos_x()`
- `ctx.entity.get_pos_y()`
- `ctx.entity.get_pos_z()`
- `ctx.entity.teleport(x, y, z)`
- `ctx.entity.discard()`
- `ctx.entity.set_on_fire(seconds)`
- `ctx.entity.damage(amount)`
- `ctx.world.spawn_entity(entity_id, x, y, z)`

Spawn example:

```python
@mod.event("player_join")
def on_join(ctx):
    if not ctx.world.is_client():
        ctx.world.spawn_entity("mymod:pocket_sentinel", 0, 80, 0)
```

Notes:

- `ctx.world.spawn_entity(...)` uses Minecraft's summon command under the hood
- entity rendering is not exposed as a Python API yet
- the generated entities are usable for server logic and registration, but custom client rendering is still a manual Java-side concern if you need something other than the default loader behavior
