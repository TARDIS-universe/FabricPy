# Events

Register events with `@mod.event("name")`.

Supported event names:

- `player_join`
- `player_leave`
- `player_death`
- `player_respawn`
- `player_change_dimension`
- `player_chat`
- `player_offhand_change`
- `block_break`
- `player_tick`
- `player_use_item`
- `player_use_block`
- `player_attack_entity`
- `player_interact_entity`
- `entity_death`
- `server_start`
- `server_stop`
- `server_tick`

Keybind handlers are defined separately through `mod.keybind(...).on_press`, not through `@mod.event(...)`.

Example:

```python
@mod.event("player_join")
def on_join(ctx):
    ctx.player.send_message("Welcome")
```

Multiple common event examples:

```python
@mod.event("player_leave")
def on_leave(ctx):
    ctx.server.run_command("say A player left")


@mod.event("server_start")
def on_start(ctx):
    ctx.server.run_command("say Server started")


@mod.event("server_tick")
def on_server_tick(ctx):
    pass
```

Common context values:

- `ctx.player`
- `ctx.world`
- `ctx.pos`
- `ctx.state`
- `ctx.message`
- `ctx.server`

Event notes:

- `player_join`: player is available
- `player_leave`: player is available
- `player_death`: player is available
- `player_respawn`: player is available
- `player_change_dimension`: player is available after dimension transfer
- `player_chat`: player and `ctx.message` are available
- `player_offhand_change`: player, `ctx.hand`, `ctx.stack`, `ctx.player.get_offhand_item_id()`, and `ctx.player.get_offhand_count()` are available. It fires when the offhand item id or count changes.
- `block_break`: player, `ctx.world`, `ctx.pos`, and `ctx.state` are available
- `player_tick`: player is available every server tick
- `player_use_item`: player, `ctx.hand`, and `ctx.stack` are available
- `player_use_block`: player, `ctx.hand`, `ctx.stack`, `ctx.pos`, and `ctx.state` are available
- `player_attack_entity`: player and `ctx.entity` are available
- `player_interact_entity`: player, `ctx.entity`, `ctx.hand`, and `ctx.stack` are available
- `entity_death`: non-player `ctx.entity` is available
- `server_start`: `ctx.server` is available
- `server_stop`: `ctx.server` is available
- `server_tick`: `ctx.server` is available

Example chat event:

```python
@mod.event("player_chat")
def on_chat(ctx):
    if "pickle" in ctx.message:
        ctx.player.send_message("Pickle detected")
```

Example inventory and effects:

```python
@mod.event("player_join")
def on_join(ctx):
    ctx.player.add_effect("minecraft:speed", 15, 1)
    ctx.player.remove_item("minecraft:dirt", 8)
```

Example offhand change event:

```python
@mod.event("player_offhand_change")
def on_offhand(ctx):
    if ctx.stack.is_of("minecraft:shield"):
        ctx.player.send_action_bar("Shield equipped in offhand")
```

Example block break event:

```python
@mod.event("block_break")
def on_break(ctx):
    if not ctx.world.is_client():
        ctx.player.send_message("Block broken")
```

Example use-item event:

```python
@mod.event("player_use_item")
def on_item(ctx):
    if ctx.stack.is_of("minecraft:stick"):
        ctx.player.send_action_bar("Using a stick")
```

Example use-block event:

```python
@mod.event("player_use_block")
def on_block(ctx):
    if ctx.world.get_self_block_id() == "minecraft:chest":
        ctx.player.send_message("That is a chest")
```

Example player tick event:

```python
@mod.event("player_tick")
def on_tick(ctx):
    if ctx.player.get_health() < 6:
        ctx.player.send_action_bar("Low health")
```

Example block break event with drops logic:

```python
@mod.event("block_break")
def on_break(ctx):
    if ctx.world.get_self_block_id() == "minecraft:diamond_ore":
        ctx.player.add_experience(5)
```

Example entity interaction event:

```python
@mod.event("player_interact_entity")
def on_entity(ctx):
    ctx.player.send_message("Interacted with an entity")
```
