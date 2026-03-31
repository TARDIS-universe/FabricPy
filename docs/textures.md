# Textures

Texture PNG files live in the repo root under `assets/<modid>/textures/...`.

Common paths:

- blocks: `assets/<modid>/textures/block/...`
- items: `assets/<modid>/textures/item/...`

Examples:

- item `texture = "food/pickle"` resolves to `assets/<modid>/textures/item/food/pickle.png`
- block `texture = "decor/lamp"` resolves to `assets/<modid>/textures/block/decor/lamp.png`

Compile behavior:

- repo textures are copied into both generated loader projects
- textures in the repo are the source of truth
- `.fabricpy_build/` should be treated as generated output, not as the place to author assets

Recommended sizes:

- `16x16`
- `32x32`
- `64x64`

If a texture path is correct but the block or item still renders with missing textures, check whether a repo-level model JSON is overriding the generated model and pointing at the wrong texture id.
