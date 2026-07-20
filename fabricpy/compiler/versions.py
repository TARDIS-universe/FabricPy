from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass(frozen=True)
class FabricVersion:
    loom: str
    fabric_loader: str
    fabric_api: str
    yarn: str
    java: int
    geckolib: str
    pack_format: int


@dataclass(frozen=True)
class ForgeVersion:
    forge: str
    java: int
    plugin: str
    settings_plugin: str
    geckolib: str
    loader_version: str
    forge_dep: str
    pack_format: int


@dataclass(frozen=True)
class QuiltVersion:
    loom: str
    quilt_loader: str
    quilted_fabric_api: str
    yarn: str
    java: int
    geckolib: str
    pack_format: int


@dataclass(frozen=True)
class NeoForgeVersion:
    neoforge: str
    java: int
    plugin: str
    geckolib: str
    loader_version: str
    neoforge_dep: str
    pack_format: int


def version_tuple(version: str) -> tuple[int, ...]:
    return tuple(int(part) for part in re.findall(r"\d+", version))


def is_at_least(version: str, minimum: str) -> bool:
    return version_tuple(version) >= version_tuple(minimum)


FABRIC_VERSIONS: dict[str, FabricVersion] = {
    "1.20.1": FabricVersion("1.6-SNAPSHOT", "0.19.3", "0.92.9+1.20.1", "1.20.1+build.10", 17, "4.8.3", 15),
    "1.21": FabricVersion("1.7-SNAPSHOT", "0.19.3", "0.102.0+1.21", "1.21+build.9", 21, "4.8.4", 34),
    "1.21.1": FabricVersion("1.7-SNAPSHOT", "0.19.3", "0.116.12+1.21.1", "1.21.1+build.3", 21, "4.8.4", 34),
    "1.21.2": FabricVersion("1.7-SNAPSHOT", "0.19.3", "0.106.1+1.21.2", "1.21.2+build.1", 21, "4.8.4", 42),
    "1.21.3": FabricVersion("1.7-SNAPSHOT", "0.19.3", "0.114.1+1.21.3", "1.21.3+build.2", 21, "4.8.4", 42),
    "1.21.4": FabricVersion("1.7-SNAPSHOT", "0.19.3", "0.119.4+1.21.4", "1.21.4+build.8", 21, "4.8.4", 46),
    "1.21.5": FabricVersion("1.7-SNAPSHOT", "0.19.3", "0.128.2+1.21.5", "1.21.5+build.1", 21, "4.8.4", 55),
    "1.21.6": FabricVersion("1.7-SNAPSHOT", "0.19.3", "0.128.2+1.21.6", "1.21.6+build.1", 21, "4.8.4", 63),
    "1.21.7": FabricVersion("1.7-SNAPSHOT", "0.19.3", "0.129.0+1.21.7", "1.21.7+build.8", 21, "4.8.4", 64),
    "1.21.8": FabricVersion("1.7-SNAPSHOT", "0.19.3", "0.136.1+1.21.8", "1.21.8+build.1", 21, "4.8.4", 64),
}


FORGE_VERSIONS: dict[str, ForgeVersion] = {
    "1.20.1": ForgeVersion("47.4.20", 17, "6.0.51", "0.8.0", "4.8.3", "[47,)", "[47,)", 15),
    "1.21.1": ForgeVersion("52.1.14", 21, "[7.0.3,8)", "1.0.0", "4.8.4", "[52,)", "[52,)", 34),
}


QUILT_VERSIONS: dict[str, QuiltVersion] = {
    "1.20.1": QuiltVersion("1.7.3", "0.30.0-beta.8", "7.7.0+0.92.2-1.20.1", "1.20.1+build.10", 17, "4.8.3", 15),
}


NEOFORGE_VERSIONS: dict[str, NeoForgeVersion] = {
    "1.21.1": NeoForgeVersion("21.1.233", 21, "2.0.141", "4.8.4", "[4,)", "[21.1,)", 34),
}


def required_java_major(minecraft_version: str) -> int:
    candidates = (
        FABRIC_VERSIONS.get(minecraft_version),
        FORGE_VERSIONS.get(minecraft_version),
        QUILT_VERSIONS.get(minecraft_version),
        NEOFORGE_VERSIONS.get(minecraft_version),
    )
    for candidate in candidates:
        if candidate is not None:
            return candidate.java
    return 21 if is_at_least(minecraft_version, "1.20.5") else 17


def required_gradle_version(loader: str, minecraft_version: str) -> str:
    loader = loader.lower().strip()
    if loader in {"forge", "neoforge"} and is_at_least(minecraft_version, "1.21"):
        return "9.3.0"
    return "8.8"
