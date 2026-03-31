# Context API

Generated handlers and commands use a lightweight `ctx` surface. In Python you write against `ctx`, and the compiler maps that to the matching Fabric or Forge Java calls.

Player helpers:

- `ctx.player`
- `ctx.player.send_message(text)`
- `ctx.player.send_action_bar(text)`
- `ctx.player.teleport(x, y, z)`
- `ctx.player.give_item(item_id, count)`
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
- `ctx.player.get_pos_x()`
- `ctx.player.get_pos_y()`
- `ctx.player.get_pos_z()`

World helpers:

- `ctx.world`
- `ctx.world.is_client()`
- `ctx.world.play_sound(sound_id, volume, pitch)`
- `ctx.world.explode(x, y, z, power)`
- `ctx.world.set_block(x, y, z, block_id)`
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

Raw context values that can appear depending on the hook or event:

- `ctx.pos`
- `ctx.state`
- `ctx.hand`
- `ctx.stack`
- `ctx.message`
- `ctx.server`

Notes:

- availability depends on the specific hook or event
- `ctx.message` is primarily for chat events
- `ctx.server` is primarily for server lifecycle and tick events
