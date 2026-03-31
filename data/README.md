# Data Folder

Put source data-pack files here, namespaced by `mod_id`.

Example:

```text
data/
  test/
    recipes/
      pickle.json
    loot_tables/
      blocks/
        block.json
    tags/
      items/
        pickles.json
```

During compile, `fabricpy` copies `data/<modid>/...` into both generated projects:

- `src/main/resources/data/<modid>/...` for Fabric
- `src/main/resources/data/<modid>/...` for Forge

Copied files override generated defaults when paths collide.
