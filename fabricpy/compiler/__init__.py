"""
Main compiler entry point.

Called by Mod.compile(). Generates Fabric and/or Forge project trees,
then invokes Gradle to produce .jar files.
"""

from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from fabricpy.mod import Mod


def compile_mod(mod: "Mod", output_dir: str = "./dist", clean: bool = False):
    """
    Compile a Mod into .jar files.

    Steps:
      1. Validate the mod definition
      2. Generate loader project(s)
      4. Run Gradle build(s)
      5. Copy output .jar(s) to output_dir
    """
    from fabricpy.compiler.fabric_gen import generate_fabric_project
    from fabricpy.compiler.forge_gen import generate_forge_project
    from fabricpy.compiler.quilt_gen import generate_quilt_project
    from fabricpy.compiler.neoforge_gen import generate_neoforge_project
    from fabricpy.compiler.gradle_runner import run_build

    _validate(mod)

    out = Path(output_dir).resolve()
    out.mkdir(parents=True, exist_ok=True)

    gen_root = Path(".fabricpy_build").resolve()
    gen_root.mkdir(exist_ok=True)

    loaders = _resolve_loaders(mod.loader, mod.minecraft_version)

    print(f"[fabricpy] Compiling {mod.name!r} v{mod.version} -> {loaders}")
    print(f"  Blocks:   {len(mod._blocks)}")
    print(f"  Items:    {len(mod._items)}")
    print(f"  Entities: {len(mod._entities)}")
    print(f"  Events:   {len(mod._events)}")
    print(f"  Commands: {len(mod._commands)}")
    print(f"  Mixins:   {len(mod._mixins)}")
    print(f"  Recipes:  {len(mod._recipes)}")
    print(f"  Sounds:   {len(mod._sounds)}")
    print(f"  Dimension Types: {len(mod._dimension_types)}")
    print(f"  Dimensions:      {len(mod._dimensions)}")
    print(f"  Structures:      {len(mod._structures)}")
    print()

    results = {}

    if "fabric" in loaders:
        fabric_dir = gen_root / f"{mod.mod_id}-fabric"
        generate_fabric_project(mod, fabric_dir)
        success = run_build(fabric_dir, mod.minecraft_version, "fabric", clean=clean, output_dir=out)
        results["fabric"] = success

    if "forge" in loaders:
        forge_dir = gen_root / f"{mod.mod_id}-forge"
        generate_forge_project(mod, forge_dir)
        success = run_build(forge_dir, mod.minecraft_version, "forge", clean=clean, output_dir=out)
        results["forge"] = success

    if "quilt" in loaders:
        quilt_dir = gen_root / f"{mod.mod_id}-quilt"
        generate_quilt_project(mod, quilt_dir)
        success = run_build(quilt_dir, mod.minecraft_version, "quilt", clean=clean, output_dir=out)
        results["quilt"] = success

    if "neoforge" in loaders:
        neoforge_dir = gen_root / f"{mod.mod_id}-neoforge"
        generate_neoforge_project(mod, neoforge_dir)
        success = run_build(neoforge_dir, mod.minecraft_version, "neoforge", clean=clean, output_dir=out)
        results["neoforge"] = success

    print()
    print("=" * 50)
    print(f"[fabricpy] Compilation complete for {mod.name}")
    for loader, ok in results.items():
        status = "SUCCESS" if ok else "FAILED (source generated, check errors above)"
        print(f"  {loader.upper():8} {status}")
    if any(results.values()):
        print(f"  Output: {out}")
    print("=" * 50)


def _resolve_loaders(loader: str, minecraft_version: str) -> list[str]:
    loader = loader.lower().strip()

    supported_by_version = {
        "1.20.1": ["fabric", "quilt", "forge"],
        "1.21.1": ["fabric", "quilt", "forge", "neoforge"],
    }
    supported = supported_by_version.get(minecraft_version)
    if not supported:
        raise ValueError(
            f"Unsupported minecraft_version: {minecraft_version!r}. "
            "Use one of: '1.20.1', '1.21.1'."
        )

    alias_map = {
        "both": ["fabric", "forge"],
        "all": list(supported),
    }

    if loader in alias_map:
        return alias_map[loader]

    requested = [part.strip() for part in loader.replace("+", ",").split(",") if part.strip()]
    if not requested:
        raise ValueError("loader is required")

    invalid = [name for name in requested if name not in supported]
    if invalid:
        raise ValueError(
            f"Invalid loader(s) for Minecraft {minecraft_version}: {invalid!r}. "
            f"Supported loaders: {supported!r}."
        )

    seen = []
    for name in requested:
        if name not in seen:
            seen.append(name)
    return seen


def _validate(mod: "Mod"):
    """Basic sanity checks before compiling."""
    errors = []

    if not mod.mod_id:
        errors.append("mod_id is required")
    if not mod.name:
        errors.append("name is required")
    for block in mod._blocks:
        if not block.block_id:
            errors.append(f"{block.__name__} is missing block_id")
    for item in mod._items:
        if not item.item_id:
            errors.append(f"{item.__name__} is missing item_id")
    for entity in mod._entities:
        if not entity.entity_id:
            errors.append(f"{entity.__name__} is missing entity_id")
    for mx in mod._mixins:
        if not mx.target_class:
            errors.append(f"{mx.__name__} is missing target_class")
    for structure in mod._structures:
        if not Path(structure["path"]).exists():
            errors.append(f"structure source file does not exist: {structure['path']}")

    if errors:
        raise ValueError(
            "Mod definition has errors:\n" + "\n".join(f"  - {e}" for e in errors)
        )
