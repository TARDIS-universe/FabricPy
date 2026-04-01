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

World helpers:

- `ctx.world`
- `ctx.world.is_client()`
- `ctx.world.play_sound(sound_id, volume, pitch)`
- `ctx.world.explode(x, y, z, power)`
- `ctx.world.set_block(x, y, z, block_id)`
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
- `ctx.message`
- `ctx.entity`
- `ctx.block_entity`
- `ctx.server`

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
