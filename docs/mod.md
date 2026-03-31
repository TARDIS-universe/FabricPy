# Mod API

`mc.Mod(...)` is the root object for a mod definition.

Constructor arguments:

- `mod_id`: lowercase identifier used for registry names and asset/data paths
- `name`: display name shown in the mod list
- `version`: mod version string, default `1.0.0`
- `description`: short description
- `authors`: list of author names
- `minecraft_version`: target Minecraft version, default `1.20.1`
- `loader`: `fabric`, `forge`, or `both`
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
