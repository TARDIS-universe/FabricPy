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
      2. Generate Fabric project (if loader is "fabric" or "both")
      3. Generate Forge project  (if loader is "forge"  or "both")
      4. Run Gradle build(s)
      5. Copy output .jar(s) to output_dir
    """
    from fabricpy.compiler.fabric_gen import generate_fabric_project
    from fabricpy.compiler.forge_gen import generate_forge_project
    from fabricpy.compiler.gradle_runner import run_build

    _validate(mod)

    out = Path(output_dir).resolve()
    out.mkdir(parents=True, exist_ok=True)

    gen_root = Path(".fabricpy_build").resolve()
    gen_root.mkdir(exist_ok=True)

    loaders = _resolve_loaders(mod.loader)

    print(f"[fabricpy] Compiling {mod.name!r} v{mod.version} -> {loaders}")
    print(f"  Blocks:   {len(mod._blocks)}")
    print(f"  Items:    {len(mod._items)}")
    print(f"  Events:   {len(mod._events)}")
    print(f"  Commands: {len(mod._commands)}")
    print(f"  Mixins:   {len(mod._mixins)}")
    print(f"  Recipes:  {len(mod._recipes)}")
    print()

    results = {}

    if "fabric" in loaders:
        fabric_dir = gen_root / f"{mod.mod_id}-fabric"
        generate_fabric_project(mod, fabric_dir)
        success = run_build(fabric_dir, clean=clean, output_dir=out)
        results["fabric"] = success

    if "forge" in loaders:
        forge_dir = gen_root / f"{mod.mod_id}-forge"
        generate_forge_project(mod, forge_dir)
        success = run_build(forge_dir, clean=clean, output_dir=out)
        results["forge"] = success

    print()
    print("=" * 50)
    print(f"[fabricpy] Compilation complete for {mod.name}")
    for loader, ok in results.items():
        status = "SUCCESS" if ok else "FAILED (source generated, check errors above)"
        print(f"  {loader.upper():8} {status}")
    if any(results.values()):
        print(f"  Output: {out}")
    print("=" * 50)


def _resolve_loaders(loader: str) -> list[str]:
    loader = loader.lower()
    if loader == "both":
        return ["fabric", "forge"]
    if loader in ("fabric", "forge"):
        return [loader]
    raise ValueError(f"Invalid loader: {loader!r}. Use 'fabric', 'forge', or 'both'.")


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
    for mx in mod._mixins:
        if not mx.target_class:
            errors.append(f"{mx.__name__} is missing target_class")

    if errors:
        raise ValueError(
            "Mod definition has errors:\n" + "\n".join(f"  - {e}" for e in errors)
        )
