# Decorators

`fabricpy` exposes these decorators at the top level:

- `@mc.on_use`
- `@mc.on_right_click`
- `@mc.on_place`
- `@mc.on_break`
- `@mc.on_tick`
- `@mc.inject(...)`

Block hook decorators:

- `@mc.on_use`: block right click
- `@mc.on_place`: block placement hook
- `@mc.on_break`: block break hook
- `@mc.on_tick`: per-tick block hook, intended for advanced cases

Item hook decorators:

- `@mc.on_right_click`: item use hook

Mixin decorator:

- `@mc.inject(method, at="HEAD", cancellable=False)`

Example:

```python
@mod.register
class Bell(mc.Block):
    block_id = "bell"

    @mc.on_use
    def on_use(self, ctx):
        ctx.player.send_message("dong")
```
