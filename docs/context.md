# Context API

Generated handlers and commands use a lightweight `ctx` surface. In Python you write against `ctx`, and the compiler maps that to the matching Fabric or Forge Java calls.

Player helpers:

- `ctx.player`
- `ctx.player.send_message(text)`
- `ctx.player.send_action_bar(text)`
- `ctx.player.teleport(x, y, z)`
- `ctx.player.give_item(item_id, count)`
- `ctx.player.remove_item(item_id, count)`
- `ctx.player.get_health()`
- `ctx.player.set_health(value)`
- `ctx.player.is_creative()`
- `ctx.player.is_sneaking()`
- `ctx.player.is_sprinting()`
- `ctx.player.get_name()`
- `ctx.player.set_on_fire(seconds)`
- `ctx.player.heal(amount)`
- `ctx.player.damage(amount)`
- `ctx.player.add_effect(effect, seconds, amplifier)`
- `ctx.player.remove_effect(effect)`
- `ctx.player.clear_effects()`
- `ctx.player.get_hunger()`
- `ctx.player.set_hunger(value)`
- `ctx.player.get_saturation()`
- `ctx.player.set_saturation(value)`
- `ctx.player.add_experience(amount)`
- `ctx.player.kill()`
- `ctx.player.teleport_dimension(dimension_id, x, y, z)`
- `ctx.player.get_pos_x()`
- `ctx.player.get_pos_y()`
- `ctx.player.get_pos_z()`
- `ctx.player.get_main_hand_item_id()`
- `ctx.player.get_main_hand_count()`
- `ctx.player.get_offhand_item_id()`
- `ctx.player.get_offhand_count()`
- `ctx.player.consume_main_hand_item(count)`
- `ctx.player.set_main_hand_item(item_id, count)`
- `ctx.player.has_item(item_id)`
- `ctx.player.count_item(item_id)`
- `ctx.player.add_cooldown(item_id, ticks)`

Player example:

```python
def reward_player(ctx):
    ctx.player.give_item("minecraft:emerald", 3)
    ctx.player.add_effect("minecraft:speed", 10, 1)
    ctx.player.add_experience(5)
```

World helpers:

- `ctx.world`
- `ctx.world.is_client()`
- `ctx.world.play_sound(sound_id, volume, pitch)`
- `ctx.world.explode(x, y, z, power)`
- `ctx.world.set_block(x, y, z, block_id)`
- `ctx.world.set_block_self(block_id)`
- `ctx.world.break_block(x, y, z, drop)`
- `ctx.world.break_self(drop)`
- `ctx.world.get_block_id(x, y, z)`
- `ctx.world.get_self_block_id()`
- `ctx.world.is_air(x, y, z)`
- `ctx.world.is_self_air()`
- `ctx.world.set_block_in_dimension(dimension_id, x, y, z, block_id)`
- `ctx.world.fill_in_dimension(dimension_id, x1, y1, z1, x2, y2, z2, block_id, mode)`
- `ctx.world.place_structure(dimension_id, structure_id, x, y, z)`
- `ctx.world.place_nbt(dimension_id, structure_id, x, y, z)`
- `ctx.world.spawn_entity(entity_id, x, y, z)`
- `ctx.world.get_time()`
- `ctx.world.is_day()`
- `ctx.world.is_raining()`
- `ctx.world.get_dimension()`
- `ctx.world.spawn_lightning()`
- `ctx.client`
- `ctx.keybind`

World example:

```python
def do_world_action(ctx):
    ctx.world.set_block(0, 64, 0, "minecraft:gold_block")
    ctx.world.play_sound("minecraft:block.note_block.pling", 1.0, 1.0)
```

Command source helpers:

- `ctx.source`
- `ctx.source.send_message(text)`
- `ctx.source.get_player()`
- `ctx.source.get_pos()`
- `ctx.source.run_command(command)`

Server helpers:

- `ctx.server`
- `ctx.server.run_command(command)`
- `ctx.server.reload_data()`

Raw context values that can appear depending on the hook or event:

- `ctx.pos`
- `ctx.state`
- `ctx.hand`
- `ctx.stack`
- `ctx.stack.get_item_id()`
- `ctx.stack.get_count()`
- `ctx.stack.get_texture()`
- `ctx.stack.texture_change(texture_id)`
- `ctx.stack.get_model()`
- `ctx.stack.model_change(model_id)`
- `ctx.stack.decrement(count)`
- `ctx.stack.increment(count)`
- `ctx.stack.is_of(item_id)`
- `ctx.message`
- `ctx.entity`
- `ctx.block_entity`
- `ctx.server`

Stack example:

```python
def handle_stack(ctx):
    if ctx.stack.is_of("minecraft:red_dye"):
        ctx.stack.decrement(1)
        ctx.stack.texture_change("playtime:item/tools/painter_red")
        ctx.stack.model_change("playtime:item/tools/painter_red")
```

Entity helpers:

- `ctx.entity`
- `ctx.entity.get_pos_x()`
- `ctx.entity.get_pos_y()`
- `ctx.entity.get_pos_z()`
- `ctx.entity.teleport(x, y, z)`
- `ctx.entity.discard()`
- `ctx.entity.set_on_fire(seconds)`
- `ctx.entity.damage(amount)`

Block entity helpers:

- `ctx.block_entity`
- `ctx.block_entity.mark_dirty()`
- `ctx.block_entity.get_string(key)`
- `ctx.block_entity.get_texture()`
- `ctx.block_entity.texture_change(texture_id)`
- `ctx.block_entity.get_model()`
- `ctx.block_entity.model_change(model_id)`
- `ctx.block_entity.set_string(key, value)`
- `ctx.block_entity.get_int(key)`
- `ctx.block_entity.set_int(key, value)`
- `ctx.block_entity.get_bool(key)`
- `ctx.block_entity.set_bool(key, value)`
- `ctx.block_entity.get_double(key)`
- `ctx.block_entity.set_double(key, value)`
- `ctx.block_entity.has(key)`
- `ctx.block_entity.remove(key)`
- `ctx.block_entity.sync()`

Block entity example:

```python
def update_panel(ctx):
    uses = ctx.block_entity.get_int("uses")
    ctx.block_entity.set_int("uses", uses + 1)
    ctx.block_entity.set_string("mode", "armed")
    ctx.block_entity.texture_change("playtime:block/panel_armed")
    ctx.block_entity.model_change("playtime:block/panel_armed")
    ctx.block_entity.sync()
```

Notes:

- availability depends on the specific hook or event
- `ctx.message` is primarily for chat events
- `ctx.server` is primarily for server lifecycle and tick events
- item ids should be full ids like `"minecraft:stone"` or `"mymod:pickle"`
- entity ids should be full ids like `"minecraft:pig"` or `"mymod:pocket_sentinel"`
- effect ids should be strings like `"minecraft:speed"` or `"speed"`
- dimension ids should be full ids like `"minecraft:overworld"` or `"mymod:pocket"`
- cross-dimension block and structure helpers use Minecraft commands under the hood
- `ctx.entity` and `ctx.block_entity` are also exposed as the raw generated Java-backed objects, so advanced calls can be emitted if you use the loader method names directly
- `ctx.stack.texture_change(...)` and `ctx.stack.model_change(...)` store appearance override keys on the item stack data
- `ctx.block_entity.texture_change(...)` and `ctx.block_entity.model_change(...)` store appearance override keys in persistent block data
- those appearance helpers are state storage helpers, not full generic hot-reload renderer mutation across all block and item models

Example block-data workflow:

```python
@mod.register
class Scanner(mc.Block):
    block_id = "scanner"
    uses_block_data = True

    @mc.on_use
    def on_use(self, ctx):
        if ctx.stack.is_of("minecraft:red_dye"):
            ctx.block_entity.set_string("color", "red")
            ctx.block_entity.set_int("uses", ctx.block_entity.get_int("uses") + 1)
            ctx.block_entity.sync()
            ctx.player.consume_main_hand_item(1)
```

That pattern is good for persistent logic and state. For actual visual changes, swap to another compiled block or variant block id rather than expecting arbitrary runtime texture mutation.

Example appearance data workflow:

```python
@mod.register
class Scanner(mc.Block):
    block_id = "scanner"
    uses_block_data = True

    @mc.on_use
    def on_use(self, ctx):
        if ctx.stack.is_of("minecraft:red_dye"):
            ctx.block_entity.texture_change("playtime:block/scanner_red")
            ctx.block_entity.model_change("playtime:block/scanner_red")
            ctx.block_entity.sync()
```

Cross-dimension example:

```python
@mod.event("player_join")
def on_join(ctx):
    ctx.world.set_block_in_dimension("minecraft:overworld", 0, 64, 0, "minecraft:stone")
    ctx.player.teleport_dimension("minecraft:overworld", 0, 80, 0)
```
