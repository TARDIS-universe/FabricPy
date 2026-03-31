"""
Mod — the central object you configure and call .compile() on.

Usage:
    mod = mc.Mod(
        mod_id="tardismod",
        name="TARDIS Mod",
        version="1.0.0",
        description="Bigger on the inside.",
        authors=["DJ"],
        minecraft_version="1.20.1",
        loader="both",          # "fabric", "forge", or "both"
    )

    mod.register(MyBlock)
    mod.register(MyItem)

    @mod.event("player_join")
    def on_join(ctx):
        ctx.player.send_message("Welcome!")

    @mod.command("mycommand")
    def my_cmd(ctx):
        ctx.source.send_message("Hello from command!")

    if __name__ == "__main__":
        mod.compile(output_dir="./dist")
"""

import inspect
from typing import List, Optional, Type


class Mod:
    def __init__(
        self,
        mod_id: str,
        name: str,
        version: str = "1.0.0",
        description: str = "",
        authors: Optional[List[str]] = None,
        minecraft_version: str = "1.20.1",
        loader: str = "fabric",
        package: Optional[str] = None,
        website: str = "",
        license: str = "MIT",
    ):
        """
        Args:
            mod_id:             Short lowercase ID, e.g. "tardismod"
            name:               Human-readable mod name
            version:            Semantic version string
            description:        Short description shown in mod list
            authors:            List of author names
            minecraft_version:  Target MC version (default: "1.20.1")
            loader:             "fabric", "forge", or "both"
            package:            Java package root (default: com.generated.<mod_id>)
            website:            Optional homepage URL
            license:            License identifier (default: "MIT")
        """
        if not mod_id or not mod_id.isidentifier():
            raise ValueError(f"mod_id must be a valid identifier, got: {mod_id!r}")
        if " " in mod_id or mod_id != mod_id.lower():
            raise ValueError(f"mod_id must be lowercase with no spaces, got: {mod_id!r}")

        self.mod_id = mod_id
        self.name = name
        self.version = version
        self.description = description
        self.authors = authors or []
        self.minecraft_version = minecraft_version
        self.loader = loader.lower()
        self.package = package or f"com.generated.{mod_id}"
        self.website = website
        self.license = license

        self._blocks: list = []
        self._items: list = []
        self._mixins: list = []
        self._events: list = []
        self._commands: list = []
        self._recipes: list = []

    # ------------------------------------------------------------------ #
    # Registration
    # ------------------------------------------------------------------ #

    def register(self, cls):
        """
        Register a Block, Item, or Mixin class with this mod.
        Can be used as a decorator or called directly.

        Example:
            mod.register(MyBlock)

            @mod.register
            class MyOtherBlock(mc.Block):
                ...
        """
        from fabricpy.block import Block
        from fabricpy.item import Item
        from fabricpy.mixin import Mixin

        if isinstance(cls, type):
            if issubclass(cls, Block) and cls is not Block:
                cls.namespace = self.mod_id
                self._blocks.append(cls)
            elif issubclass(cls, Item) and cls is not Item:
                cls.namespace = self.mod_id
                self._items.append(cls)
            elif issubclass(cls, Mixin) and cls is not Mixin:
                self._mixins.append(cls)
            else:
                raise TypeError(f"Cannot register {cls}: must be a Block, Item, or Mixin subclass.")
        return cls

    # ------------------------------------------------------------------ #
    # Recipe system
    # ------------------------------------------------------------------ #

    def add_recipe(self, recipe_id: str, data: dict):
        """
        Register a raw recipe JSON object to be emitted under
        data/<modid>/recipes/<recipe_id>.json.
        """
        if not recipe_id:
            raise ValueError("recipe_id is required")
        if not isinstance(data, dict):
            raise TypeError("recipe data must be a dict")

        recipe_path = recipe_id.replace("\\", "/").strip("/")
        self._recipes.append({
            "id": recipe_path,
            "data": data,
        })
        return data

    def shaped_recipe(self, recipe_id: str, result: str, pattern: list[str], key: dict, count: int = 1):
        """Register a standard shaped crafting recipe."""
        data = {
            "type": "minecraft:crafting_shaped",
            "pattern": pattern,
            "key": key,
            "result": {
                "item": result,
                "count": count,
            },
        }
        self.add_recipe(recipe_id, data)
        return data

    def shapeless_recipe(self, recipe_id: str, result: str, ingredients: list[dict], count: int = 1):
        """Register a standard shapeless crafting recipe."""
        data = {
            "type": "minecraft:crafting_shapeless",
            "ingredients": ingredients,
            "result": {
                "item": result,
                "count": count,
            },
        }
        self.add_recipe(recipe_id, data)
        return data

    # ------------------------------------------------------------------ #
    # Event system
    # ------------------------------------------------------------------ #

    def event(self, event_name: str):
        """
        Decorator to register an event handler function.

        Supported event names:
            "player_join"       — ServerPlayConnectionEvents.JOIN
            "player_leave"      — ServerPlayConnectionEvents.DISCONNECT
            "player_death"      — ServerEntityCombatEvents.AFTER_KILLED_OTHER_ENTITY  (ctx: player, attacker)
            "player_respawn"    — ServerPlayerEvents.AFTER_RESPAWN
            "block_break"       — PlayerBlockBreakEvents.AFTER  (ctx: player, world, pos, state)
            "server_start"      — ServerLifecycleEvents.SERVER_STARTED
            "server_stop"       — ServerLifecycleEvents.SERVER_STOPPED

        Example:
            @mod.event("player_join")
            def on_join(ctx):
                ctx.player.send_message("Welcome!")
        """
        def decorator(func):
            self._events.append({
                "event": event_name,
                "func": func,
                "source": inspect.getsource(func),
            })
            return func
        return decorator

    # ------------------------------------------------------------------ #
    # Command system
    # ------------------------------------------------------------------ #

    def command(self, name: str, permission_level: int = 0, aliases: Optional[List[str]] = None):
        """
        Decorator to register a slash command via Brigadier.

        Args:
            name:               Command name (no slash), e.g. "tardis"
            permission_level:   0=everyone, 1=trusted, 2=ops, 3=game master, 4=owner
            aliases:            Optional list of alias strings

        Example:
            @mod.command("tardis", permission_level=0)
            def tardis_cmd(ctx):
                ctx.source.send_message("TARDIS systems nominal.")
        """
        def decorator(func):
            self._commands.append({
                "name": name,
                "permission_level": permission_level,
                "aliases": aliases or [],
                "func": func,
                "source": inspect.getsource(func),
            })
            return func
        return decorator

    # ------------------------------------------------------------------ #
    # Compile
    # ------------------------------------------------------------------ #

    def compile(self, output_dir: str = "./dist", clean: bool = False):
        """
        Compile this mod into a .jar file.

        Generates a complete Gradle project, transpiles Python to Java,
        then runs `gradlew build`. Output .jar is placed in output_dir.

        Args:
            output_dir: Where to put the finished .jar (default: ./dist)
            clean:      If True, runs `gradlew clean build` instead of just `gradlew build`
        """
        from fabricpy.compiler import compile_mod
        compile_mod(self, output_dir=output_dir, clean=clean)

    # ------------------------------------------------------------------ #
    # Repr
    # ------------------------------------------------------------------ #

    def __repr__(self):
        return (
            f"<Mod id={self.mod_id!r} name={self.name!r} "
            f"loader={self.loader!r} mc={self.minecraft_version!r} "
            f"blocks={len(self._blocks)} items={len(self._items)} "
            f"events={len(self._events)} commands={len(self._commands)} "
            f"recipes={len(self._recipes)}>"
        )
