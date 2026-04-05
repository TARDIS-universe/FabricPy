# Programmed Animations

`fabricpy` supports programmed animated blocks through GeckoLib-backed block entity rendering.

Use this when you need:

- element movement
- stretching or scaling
- bone rotation
- switching between named animations from Python

This is the correct route for real animated model parts. Static block JSON alone cannot do that.

## Python Fields

Animated blocks use these `mc.Block` fields:

- `geo_model`
- `geo_texture`
- `geo_animations`
- `default_animation`

## Minimal Example

```python
@mod.register
class AnimatedPanel(mc.Block):
    block_id = "animated_panel"
    display_name = "Animated Panel"
    has_block_entity = True
    opaque = False

    geo_model = "machines/animated_panel"
    geo_texture = "machines/animated_panel"
    geo_animations = "machines/animated_panel"
    default_animation = "idle"

    @mc.on_use
    def on_use(self, ctx):
        ctx.block_entity.play_animation("open")
```

## Resource Layout

For this Python setup:

```python
geo_model = "machines/animated_panel"
geo_texture = "machines/animated_panel"
geo_animations = "machines/animated_panel"
```

the expected files are:

- `assets/<modid>/geo/machines/animated_panel.geo.json`
- `assets/<modid>/textures/block/machines/animated_panel.png`
- `assets/<modid>/animations/machines/animated_panel.animation.json`

## Animation Control

Available on `ctx.block_entity` for animated blocks:

- `ctx.block_entity.get_animation()`
- `ctx.block_entity.play_animation(name)`
- `ctx.block_entity.play_animation_once(name)`
- `ctx.block_entity.stop_animation()`

Examples:

```python
@mc.on_use
def on_use(self, ctx):
    ctx.block_entity.play_animation("open")
```

```python
@mc.on_use
def on_use(self, ctx):
    ctx.block_entity.play_animation_once("press")
```

```python
@mc.on_break
def on_break(self, ctx):
    ctx.block_entity.stop_animation()
```

## Stateful Example

```python
@mod.register
class ReactorDoor(mc.Block):
    block_id = "reactor_door"
    display_name = "Reactor Door"
    has_block_entity = True
    uses_block_data = True
    opaque = False

    geo_model = "doors/reactor_door"
    geo_texture = "doors/reactor_door"
    geo_animations = "doors/reactor_door"
    default_animation = "idle_closed"

    @mc.on_use
    def on_use(self, ctx):
        is_open = ctx.block_entity.get_bool("open")
        if is_open:
            ctx.block_entity.set_bool("open", False)
            ctx.block_entity.play_animation("close")
        else:
            ctx.block_entity.set_bool("open", True)
            ctx.block_entity.play_animation("open")
        ctx.block_entity.sync()
```

## Notes

- animated blocks automatically get a backing block entity and client renderer
- `has_block_entity = True` is still recommended for readability
- the motion itself is authored in Blockbench/GeckoLib animation JSON
- Python controls when animations start, stop, or switch
- generated projects add GeckoLib automatically when animated blocks are present
- this animation path is currently for blocks, not general item animation
