from fabricpy.compiler.versions import NEOFORGE_VERSIONS

ADDON_KIND = "loader"
ADDON_TARGET = "neoforge"
MINECRAFT_VERSIONS = sorted(NEOFORGE_VERSIONS)
ADDON_NAME = "builtin"
ADDON_PRIORITY = -90


def generate_project(mod, project_dir):
    from fabricpy.compiler.neoforge_gen import generate_neoforge_project

    return generate_neoforge_project(mod, project_dir)

