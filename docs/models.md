# Models And Blockstates

`fabricpy` can generate default blockstate and model JSON, and you can override those defaults from Python or from repo files.

Repo folders:

- blockstates: `assets/<modid>/blockstates/...`
- block models: `assets/<modid>/models/block/...`
- item models: `assets/<modid>/models/item/...`

Block Python fields:

- `texture`
- `textures`
- `model`
- `blockstate`
- `item_model`

Item Python fields:

- `texture`
- `textures`
- `model`

Default generation behavior:

- a block with only `texture = "foo/bar"` gets:
  - a default blockstate pointing to `<modid>:block/<block_id>`
  - a default block model using `minecraft:block/cube_all`
  - a default block item model with parent `<modid>:block/<block_id>`
- an item with only `texture = "foo/bar"` gets:
  - a default item model using `minecraft:item/generated`
  - `layer0` set to `<modid>:item/foo/bar`

Reference rules inside JSON:

- namespaced ids like `"mymod:block/fancy_block"` are used exactly as written
- if you are writing raw JSON yourself, always be explicit about `block/` vs `item/`
- Python `texture = ...` is path-like input; JSON `textures` values are texture ids

Example block:

```python
@mod.register
class FancyBlock(mc.Block):
    block_id = "fancy_block"
    texture = "custom/fancy_block"
    blockstate = {
        "variants": {
            "": {"model": "mymod:block/fancy_block"}
        }
    }
    model = {
        "parent": "minecraft:block/cube_all",
        "textures": {
            "all": "mymod:block/custom/fancy_block",
            "particle": "mymod:block/custom/fancy_block"
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
    texture = "food/pickle"
    model = {
        "parent": "minecraft:item/generated",
        "textures": {
            "layer0": "mymod:item/food/pickle"
        }
    }
```

Manual override rules:

- generated defaults are written first
- repo files under `assets/<modid>/models/...` and `assets/<modid>/blockstates/...` are copied after generation
- repo files override generated JSON when the paths match

Important particle note:

- if you use a custom block model JSON, add a `particle` texture entry unless the chosen parent already handles it the way you want
- without a valid `particle` entry, block breaking particles can appear as missing textures even if the block itself renders correctly

Common mistake:

- Python says `texture = "food/pickle"` and you then write a manual item model with `"layer0": "mymod:food/pickle"`
- that is wrong for item textures
- the correct texture id is `"mymod:item/food/pickle"`
