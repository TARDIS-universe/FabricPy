from __future__ import annotations

import re
from pathlib import Path

from fabricpy.compiler.forge_gen import _uses_geckolib, generate_forge_project
from fabricpy.compiler.versions import NEOFORGE_VERSIONS


def generate_neoforge_project(mod, project_dir: Path):
    version_meta = NEOFORGE_VERSIONS.get(mod.minecraft_version)
    if version_meta is None:
        raise ValueError(f"NeoForge does not support minecraft_version={mod.minecraft_version!r} in this generator.")
    if mod._packets:
        raise ValueError("NeoForge packet generation is not implemented yet; remove mod.packet(...) or target fabric/forge.")

    generate_forge_project(mod, project_dir)
    _rewrite_java_sources(project_dir)
    _rewrite_mods_toml(mod, project_dir, version_meta)
    _write_neoforge_gradle_files(mod, project_dir, version_meta)
    print(f"[fabricpy] NeoForge project generated at {project_dir}")


def _rewrite_java_sources(project_dir: Path):
    replacements = (
        ("net.minecraftforge.fml", "net.neoforged.fml"),
        ("net.minecraftforge.eventbus.api", "net.neoforged.bus.api"),
        ("net.minecraftforge.common.MinecraftForge.EVENT_BUS", "net.neoforged.neoforge.common.NeoForge.EVENT_BUS"),
        ("net.minecraftforge.common.MinecraftForge", "net.neoforged.neoforge.common.NeoForge"),
        ("net.minecraftforge.client.event", "net.neoforged.neoforge.client.event"),
        ("net.minecraftforge.event.", "net.neoforged.neoforge.event."),
        ("net.minecraftforge.registries", "net.neoforged.neoforge.registries"),
        ("net.minecraftforge.network", "net.neoforged.neoforge.network"),
    )
    for path in (project_dir / "src" / "main" / "java").rglob("*.java"):
        text = path.read_text(encoding="utf-8")
        for old, new in replacements:
            text = text.replace(old, new)
        text = text.replace("modId=\"forge\"", "modId=\"neoforge\"")
        path.write_text(text, encoding="utf-8")


def _rewrite_mods_toml(mod, project_dir: Path, version_meta):
    path = project_dir / "src" / "main" / "resources" / "META-INF" / "mods.toml"
    text = path.read_text(encoding="utf-8")
    text = text.replace('modId="forge"', 'modId="neoforge"')
    text = re.sub(r'versionRange="[^"]+"', f'versionRange="{version_meta.neoforge_dep}"', text, count=1)
    text = re.sub(r'loaderVersion="[^"]+"', f'loaderVersion="{version_meta.loader_version}"', text, count=1)
    path.write_text(text, encoding="utf-8")


def _write_neoforge_gradle_files(mod, project_dir: Path, version_meta):
    mc = mod.minecraft_version
    use_geckolib = _uses_geckolib(mod)
    geckolib_repo = (
        "    maven { url = 'https://dl.cloudsmith.io/public/geckolib3/geckolib/maven/' }"
        if use_geckolib
        else ""
    )
    geckolib_dep = (
        f"    implementation 'software.bernie.geckolib:geckolib-neoforge-{mc}:{version_meta.geckolib}'"
        if use_geckolib
        else ""
    )

    build_gradle = f"""\
plugins {{
    id 'java-library'
    id 'maven-publish'
    id 'net.neoforged.moddev' version '{version_meta.plugin}'
}}

version = "{mod.version}"
group = "{mod.package}"

base {{
    archivesName = "{mod.mod_id}-neoforge"
}}

java.toolchain.languageVersion = JavaLanguageVersion.of({version_meta.java})

neoForge {{
    version = "{version_meta.neoforge}"

    runs {{
        client {{
            client()
        }}
        server {{
            server()
            programArgument '--nogui'
        }}
    }}

    mods {{
        "{mod.mod_id}" {{
            sourceSet sourceSets.main
        }}
    }}
}}

repositories {{
{geckolib_repo}
    mavenCentral()
}}

dependencies {{
{geckolib_dep}
}}

tasks.withType(JavaCompile).configureEach {{
    options.encoding = 'UTF-8'
    options.release = {version_meta.java}
}}
"""
    (project_dir / "build.gradle").write_text(build_gradle, encoding="utf-8")
    (project_dir / "settings.gradle").write_text(f"""\
pluginManagement {{
    repositories {{
        maven {{ url = 'https://maven.neoforged.net/releases' }}
        gradlePluginPortal()
        mavenCentral()
    }}
}}
plugins {{
    id 'org.gradle.toolchains.foojay-resolver-convention' version '1.0.0'
}}
rootProject.name = "{mod.mod_id}-neoforge"
""", encoding="utf-8")
    (project_dir / "gradle.properties").write_text(
        "org.gradle.jvmargs=-Xmx2G\n"
        "org.gradle.parallel=true\n",
        encoding="utf-8",
    )
