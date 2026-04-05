# Context API

Every block hook, item hook, event handler, keybind handler, and command callback receives a generated `ctx` surface.

You write Python against `ctx`. The compiler maps those calls to Fabric or Forge Java.

The important mental model is:

- `ctx` is not a generic Python object
- `ctx` is a compiler surface
- some values are available only in certain hooks/events

## Major Context Areas

- `ctx.player`
- `ctx.world`
- `ctx.stack`
- `ctx.block_entity`
- `ctx.entity`
- `ctx.server`
- `ctx.source`
- raw values such as `ctx.pos`, `ctx.state`, `ctx.hand`, `ctx.message`

## Player Helpers

- `ctx.player.send_message(text)`
- `ctx.player.send_action_bar(text)`
- `ctx.player.teleport(x, y, z)`
- `ctx.player.teleport_dimension(dimension_id, x, y, z)`
- `ctx.player.give_item(item_id, count)`
- `ctx.player.remove_item(item_id, count)`
- `ctx.player.get_health()`
- `ctx.player.set_health(value)`
- `ctx.player.heal(amount)`
- `ctx.player.damage(amount)`
- `ctx.player.add_effect(effect_id, seconds, amplifier)`
- `ctx.player.remove_effect(effect_id)`
- `ctx.player.clear_effects()`
- `ctx.player.get_hunger()`
- `ctx.player.set_hunger(value)`
- `ctx.player.get_saturation()`
- `ctx.player.set_saturation(value)`
- `ctx.player.add_experience(amount)`
- `ctx.player.kill()`
- `ctx.player.get_name()`
- `ctx.player.is_creative()`
- `ctx.player.is_sneaking()`
- `ctx.player.is_sprinting()`
- `ctx.player.set_on_fire(seconds)`
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

Example:

```python
@mod.event("player_join")
def on_join(ctx):
    ctx.player.give_item("minecraft:bread", 4)
    ctx.player.add_effect("minecraft:speed", 15, 0)
    ctx.player.send_message("Starter kit granted")
```

## World Helpers

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
- `ctx.world.get_time()`
- `ctx.world.is_day()`
- `ctx.world.is_raining()`
- `ctx.world.get_dimension()`
- `ctx.world.spawn_lightning()`
- `ctx.world.spawn_entity(entity_id, x, y, z)`
- `ctx.world.set_block_in_dimension(dimension_id, x, y, z, block_id)`
- `ctx.world.fill_in_dimension(dimension_id, x1, y1, z1, x2, y2, z2, block_id, mode)`
- `ctx.world.place_structure(dimension_id, structure_id, x, y, z)`
- `ctx.world.place_nbt(dimension_id, structure_id, x, y, z)`

## Stack Helpers

- `ctx.stack.get_item_id()`
- `ctx.stack.get_count()`
- `ctx.stack.decrement(count)`
- `ctx.stack.increment(count)`
- `ctx.stack.is_of(item_id)`
- `ctx.stack.get_texture()`
- `ctx.stack.texture_change(texture_id)`
- `ctx.stack.get_model()`
- `ctx.stack.model_change(model_id)`

## Block Entity Helpers

- `ctx.block_entity.mark_dirty()`
- `ctx.block_entity.get_string(key)`
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
- `ctx.block_entity.get_texture()`
- `ctx.block_entity.texture_change(texture_id)`
- `ctx.block_entity.get_model()`
- `ctx.block_entity.model_change(model_id)`
- `ctx.block_entity.get_animation()`
- `ctx.block_entity.play_animation(name)`
- `ctx.block_entity.play_animation_once(name)`
- `ctx.block_entity.stop_animation()`

Example:

```python
@mc.on_use
def on_use(self, ctx):
    count = ctx.block_entity.get_int("uses")
    ctx.block_entity.set_int("uses", count + 1)
    ctx.block_entity.set_bool("powered", True)
    ctx.block_entity.play_animation_once("controller.scan")
    ctx.block_entity.sync()
```

## Entity, Server, and Source Helpers

Entity:

- `ctx.entity.get_pos_x()`
- `ctx.entity.get_pos_y()`
- `ctx.entity.get_pos_z()`
- `ctx.entity.teleport(x, y, z)`
- `ctx.entity.discard()`
- `ctx.entity.set_on_fire(seconds)`
- `ctx.entity.damage(amount)`

Server:

- `ctx.server.run_command(command)`
- `ctx.server.reload_data()`

Command source:

- `ctx.source.send_message(text)`
- `ctx.source.get_player()`
- `ctx.source.get_pos()`
- `ctx.source.run_command(command)`

## Availability Rules

Typical patterns:

- block hooks: `ctx.world`, `ctx.pos`, `ctx.state`, sometimes `ctx.hand`, `ctx.stack`, `ctx.player`, `ctx.block_entity`
- item right-click hooks: `ctx.player`, `ctx.world`, `ctx.hand`, `ctx.stack`
- player events: `ctx.player`
- chat events: `ctx.player`, `ctx.message`
- block-break events: `ctx.player`, `ctx.world`, `ctx.pos`, `ctx.state`
- entity events: `ctx.entity`
- server lifecycle events: `ctx.server`
- commands: `ctx.source`
- keybinds: `ctx.client`, `ctx.keybind`, and often `ctx.player`

## Advanced Interop Note

For advanced cases, `ctx` values are also emitted as real Java objects in generated source. That means advanced direct calls can be expressed when you know the loader-side API names.

See [interop.md](./interop.md) for the dependency side of that system.
