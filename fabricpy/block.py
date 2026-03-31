"""
Block base class. Subclass this to create a custom block.

Class attributes (all optional except block_id):
    block_id        str     Registry ID, e.g. "cool_block"         (required)
    display_name    str     In-game display name                    (default: title-cased block_id)
    hardness        float   Mining hardness (-1 = unbreakable)      (default: 1.5)
    resistance      float   Blast resistance                        (default: 6.0)
    luminance       int     Light level emitted (0-15)              (default: 0)
    slipperiness    float   Ice-like slipperiness (0.6-0.98)        (default: 0.6)
    sound_group     str     Sound type: "stone","wood","sand","wool","metal","glass","grass" (default: "stone")
    material        str     Block material hint for properties      (default: "stone")
    requires_tool   bool    Only drops if mined with correct tool   (default: False)
    drops_self      bool    Drops itself when broken               (default: True)
    has_block_entity bool   Whether this block has a block entity   (default: False; required for on_tick)
    opaque          bool    Whether the block is fully opaque       (default: True)
    collidable      bool    Whether players can walk through it     (default: True)

Hook decorators (import from fabricpy):
    @mc.on_use       — player right-clicks the block
    @mc.on_place     — block is placed
    @mc.on_break     — block is broken
    @mc.on_tick      — game tick (requires has_block_entity=True)
"""

import inspect
from fabricpy.decorators import on_use, on_place, on_break, on_tick


class BlockMeta(type):
    """Metaclass that collects hook methods."""
    def __new__(mcs, name, bases, namespace):
        cls = super().__new__(mcs, name, bases, namespace)
        hooks = {}
        for attr_name, val in namespace.items():
            if callable(val) and hasattr(val, "_fabricpy_hook"):
                hooks[val._fabricpy_hook] = val
        cls._hooks = hooks
        return cls


class Block(metaclass=BlockMeta):
    # ---- Registry ----
    block_id: str = ""                  # REQUIRED: e.g. "cool_block"
    display_name: str = ""              # Defaults to title-cased block_id
    namespace: str = ""                 # Set automatically from mod_id

    # ---- Physics / Material ----
    hardness: float = 1.5
    resistance: float = 6.0
    luminance: int = 0
    slipperiness: float = 0.6
    material: str = "stone"
    sound_group: str = "stone"

    # ---- Behavior ----
    requires_tool: bool = False
    drops_self: bool = True
    has_block_entity: bool = False
    opaque: bool = True
    collidable: bool = True

    # ---- Assets ----
    texture: str = ""                   # Shortcut for cube_all texture
    textures: dict = {}                 # Full block model texture map override
    model: dict | None = None           # Full block model JSON override
    blockstate: dict | None = None      # Full blockstate JSON override
    item_model: dict | None = None      # Full block item model JSON override

    # ---- Internal ----
    _hooks: dict = {}  # populated by BlockMeta

    @classmethod
    def get_hooks(cls) -> dict:
        """Return dict of {hook_type: method} for this block."""
        return cls._hooks

    @classmethod
    def get_class_name(cls) -> str:
        return cls.__name__

    @classmethod
    def get_display_name(cls) -> str:
        if cls.display_name:
            return cls.display_name
        return cls.block_id.replace("_", " ").title()

    @classmethod
    def get_full_id(cls) -> str:
        ns = cls.namespace or "modid"
        return f"{ns}:{cls.block_id}"
