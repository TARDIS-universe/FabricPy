from fabricpy.compiler.versions import FORGE_VERSIONS

ADDON_KIND = "loader"
ADDON_TARGET = "forge"
MINECRAFT_VERSIONS = sorted(FORGE_VERSIONS)
ADDON_NAME = "builtin"
ADDON_PRIORITY = -90


def generate_project(mod, project_dir):
    from fabricpy.compiler.forge_gen import generate_forge_project

    return generate_forge_project(mod, project_dir)

