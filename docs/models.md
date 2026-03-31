# Models And Blockstates

`fabricpy` can generate default model and blockstate JSON, and you can override those defaults from Python or from repo files.

Repo source folders:

- `assets/<modid>/blockstates/...`
- `assets/<modid>/models/block/...`
- `assets/<modid>/models/item/...`

Block-side Python fields:

- `texture`
- `textures`
- `model`
- `blockstate`
- `item_model`

Item-side Python fields:

- `texture`
- `textures`
- `model`

Reference rules:

- namespaced values like `"mymod:block/fancy_block"` are used as-is
- values with `/` but no namespace are treated as `<modid>:<value>`
- bare values are expanded to the matching default block or item path

Example block:

```python
@mod.register
class FancyBlock(mc.Block):
    block_id = "fancy_block"
    blockstate = {
        "variants": {
            "": {"model": "mymod:block/fancy_block"}
        }
    }
    model = {
        "parent": "minecraft:block/cube_all",
        "textures": {
            "all": "mymod:block/custom/fancy_block"
        }
    }
    item_model = {
        "parent": "mymod:block/fancy_block"
    }
```

Example item:

```python
@mod.register
class Pickle(mc.Item):
    item_id = "pickle"
    model = {
        "parent": "minecraft:item/generated",
        "textures": {
            "layer0": "mymod:item/food/pickle"
        }
    }
```

Override order:

- generated defaults are written first
- repo files are copied after generation
- repo files override generated JSON when the paths match
