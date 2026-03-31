# Events

Register events with `@mod.event("name")`.

Supported event names:

- `player_join`
- `player_leave`
- `player_death`
- `player_respawn`
- `player_change_dimension`
- `player_chat`
- `block_break`
- `server_start`
- `server_stop`
- `server_tick`

Example:

```python
@mod.event("player_join")
def on_join(ctx):
    ctx.player.send_message("Welcome")
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
- `block_break`: player, `ctx.world`, `ctx.pos`, and `ctx.state` are available
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

Example block break event:

```python
@mod.event("block_break")
def on_break(ctx):
    if not ctx.world.is_client():
        ctx.player.send_message("Block broken")
```
