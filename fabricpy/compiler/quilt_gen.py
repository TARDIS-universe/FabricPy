"""
Quilt mod project generator.

This reuses the Fabric-style Java/code generation path and swaps the
Gradle loader dependency to Quilt Loader. Quilt can load Fabric-style
metadata, so the generated project still emits `fabric.mod.json`.
"""

from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from fabricpy.mod import Mod

from fabricpy.compiler.fabric_gen import (
    JavaTranspiler,
    FABRIC_API_MAP,
    _write_main_class,
    _write_mod_blocks,
    _write_mod_items,
    _write_block_classes,
    _write_item_classes,
    _write_events,
    _write_commands,
    _write_mixins,
    _write_resources,
    _write_text,
)


def generate_quilt_project(mod: "Mod", project_dir: Path):
    pkg = mod.package
    pkg_path = pkg.replace(".", "/")
    src = project_dir / "src" / "main"
    java_root = src / "java" / pkg_path
    res_root = src / "resources"

    java_root.mkdir(parents=True, exist_ok=True)
    res_root.mkdir(parents=True, exist_ok=True)

    transpiler = JavaTranspiler(FABRIC_API_MAP)

    _write_main_class(mod, java_root, pkg)
    _write_mod_blocks(mod, java_root, pkg)
    _write_mod_items(mod, java_root, pkg)
    _write_block_classes(mod, java_root, pkg, transpiler)
    _write_item_classes(mod, java_root, pkg, transpiler)
    _write_events(mod, java_root, pkg, transpiler)
    _write_commands(mod, java_root, pkg, transpiler)
    _write_mixins(mod, java_root, pkg, transpiler)
    _write_resources(mod, res_root, pkg)
    _write_quilt_gradle_files(mod, project_dir)

    print(f"[fabricpy] Quilt project generated at {project_dir}")


def _write_quilt_gradle_files(mod: "Mod", project_dir: Path):
    mc = mod.minecraft_version
    version_map = {
        "1.20.1": {
            "loom": "1.6-SNAPSHOT",
            "quilt_loader": "0.29.2",
            "fabric_api": "0.92.7+1.20.1",
            "yarn": "1.20.1+build.10",
            "java": 17,
        },
        "1.21.1": {
            "loom": "1.7-SNAPSHOT",
            "quilt_loader": "0.30.0-beta.3",
            "fabric_api": "0.116.9+1.21.1",
            "yarn": "1.21.1+build.3",
            "java": 21,
        },
    }
    if mc not in version_map:
        raise ValueError(f"Quilt does not support minecraft_version={mc!r} in this generator.")
    v = version_map[mc]

    build_gradle = f"""\
plugins {{
    id 'fabric-loom' version '{v["loom"]}'
    id 'maven-publish'
}}

version = "{mod.version}"
group = "{mod.package}"

base {{
    archivesName = "{mod.mod_id}-quilt"
}}

repositories {{
    maven {{ url = "https://maven.fabricmc.net/" }}
    maven {{ url = "https://maven.quiltmc.org/repository/release/" }}
    mavenCentral()
}}

dependencies {{
    minecraft "com.mojang:minecraft:{mc}"
    mappings "net.fabricmc:yarn:{v['yarn']}:v2"
    modImplementation "org.quiltmc:quilt-loader:{v['quilt_loader']}"
    modImplementation "net.fabricmc.fabric-api:fabric-api:{v['fabric_api']}"
}}

processResources {{
    inputs.property "version", version

    filesMatching("fabric.mod.json") {{
        expand "version": version
    }}
}}

tasks.withType(JavaCompile).configureEach {{
    it.options.release = {v['java']}
}}

java {{
    withSourcesJar()
    toolchain.languageVersion = JavaLanguageVersion.of({v['java']})
}}
"""
    _write_text(project_dir / "build.gradle", build_gradle)

    _write_text(project_dir / "settings.gradle", f"""\
pluginManagement {{
    repositories {{
        maven {{ url = "https://maven.fabricmc.net/" }}
        maven {{ url = "https://maven.quiltmc.org/repository/release/" }}
        mavenCentral()
        gradlePluginPortal()
    }}
}}
plugins {{
    id 'org.gradle.toolchains.foojay-resolver-convention' version '0.8.0'
}}
rootProject.name = "{mod.mod_id}-quilt"
""")

    _write_text(project_dir / "gradle.properties", "org.gradle.jvmargs=-Xmx1G\n")
    _write_text(project_dir / ".gitignore", ".gradle/\nbuild/\n*.jar\n!gradle/wrapper/gradle-wrapper.jar\n")
