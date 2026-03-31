# Mod API

`mc.Mod(...)` is the root object for a mod definition.

Constructor arguments:

- `mod_id`: lowercase identifier used for registry names and asset/data paths
- `name`: display name shown in the mod list
- `version`: mod version string, default `1.0.0`
- `description`: short description
- `authors`: list of author names
- `minecraft_version`: target Minecraft version, default `1.20.1`
- `loader`: `fabric`, `quilt`, `forge`, `neoforge`, `both`, or `all`
- `package`: Java package root, defaults to `com.generated.<mod_id>`
- `website`: optional homepage URL
- `license`: license string, default `MIT`

Main methods:

- `mod.register(cls)`: register a `mc.Block`, `mc.Item`, or `mc.Mixin`
- `mod.event(name)`: register a mod event handler
- `mod.command(name, permission_level=0, aliases=None)`: register a slash command
- `mod.add_recipe(recipe_id, data)`: register raw recipe JSON
- `mod.shaped_recipe(recipe_id, result, pattern, key, count=1)`: register a shaped recipe
- `mod.shapeless_recipe(recipe_id, result, ingredients, count=1)`: register a shapeless recipe
- `mod.add_sound(sound_id, sounds, subtitle="", replace=False)`: register a sound event for `sounds.json`
- `mod.add_dimension_type(type_id, data)`: register a dimension type JSON
- `mod.add_dimension(dimension_id, dimension_type, generator=None, data=None)`: register a dimension JSON
- `mod.add_structure(structure_id, nbt_path)`: copy an NBT structure template into the generated datapack
- `mod.compile(output_dir="./dist", clean=False)`: generate projects and build jars

Registration styles:

```python
mod.register(MyBlock)

@mod.register
class MyItem(mc.Item):
    item_id = "my_item"
```

Example:

```python
import fabricpy as mc

mod = mc.Mod(
    mod_id="mymod",
    name="My Mod",
    version="1.0.0",
    description="Example mod",
    authors=["You"],
    minecraft_version="1.20.1",
    loader="both",
)
```

Generated project layout:

- jars are copied to `dist/` by default
- generated projects live under `.fabricpy_build/`
- repo assets are sourced from `assets/<modid>/...`
- repo data files are sourced from `data/<modid>/...`
- dimension JSON goes under `data/<modid>/dimension_type` and `data/<modid>/dimension`
- structure NBT files go under `data/<modid>/structures`

Loader matrix:

- `1.20.1`: `fabric`, `quilt`, `forge`
- `1.21.1`: `fabric`, `quilt`, `forge`, `neoforge`
- `both`: always means `fabric+forge`
- `all`: every supported loader for the selected Minecraft version
