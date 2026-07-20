from fabricpy.compiler.versions import FABRIC_VERSIONS

ADDON_KIND = "loader"
ADDON_TARGET = "fabric"
MINECRAFT_VERSIONS = sorted(FABRIC_VERSIONS)
ADDON_NAME = "builtin"
ADDON_PRIORITY = -90


def generate_project(mod, project_dir):
    from fabricpy.compiler.fabric_gen import generate_fabric_project

    return generate_fabric_project(mod, project_dir)

