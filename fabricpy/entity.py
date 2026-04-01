"""
Entity base class. Subclass this to create a custom non-block entity.

This first-pass API focuses on registration, ticking, and basic size/category
metadata. Custom rendering is not yet exposed as a Python-side API.
"""

from fabricpy.decorators import on_tick


class EntityMeta(type):
    def __new__(mcs, name, bases, namespace):
        cls = super().__new__(mcs, name, bases, namespace)
        hooks = {}
        for _, val in namespace.items():
            if callable(val) and hasattr(val, "_fabricpy_hook"):
                hooks[val._fabricpy_hook] = val
        cls._hooks = hooks
        return cls


class Entity(metaclass=EntityMeta):
    entity_id: str = ""
    display_name: str = ""
    namespace: str = ""

    width: float = 0.6
    height: float = 1.8
    tracking_range: int = 8
    update_rate: int = 3
    spawn_group: str = "misc"
    fireproof: bool = False
    summonable: bool = True
    max_health: float = 20.0
    movement_speed: float = 0.25
    attack_damage: float = 2.0
    follow_range: float = 16.0
    knockback_resistance: float = 0.0

    _hooks: dict = {}

    @classmethod
    def get_hooks(cls) -> dict:
        return cls._hooks

    @classmethod
    def get_class_name(cls) -> str:
        return cls.__name__

    @classmethod
    def get_display_name(cls) -> str:
        if cls.display_name:
            return cls.display_name
        return cls.entity_id.replace("_", " ").title()

    @classmethod
    def get_full_id(cls) -> str:
        ns = cls.namespace or "modid"
        return f"{ns}:{cls.entity_id}"
