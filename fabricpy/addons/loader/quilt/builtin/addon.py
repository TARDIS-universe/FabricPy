from fabricpy.compiler.versions import QUILT_VERSIONS

ADDON_KIND = "loader"
ADDON_TARGET = "quilt"
MINECRAFT_VERSIONS = sorted(QUILT_VERSIONS)
ADDON_NAME = "builtin"
ADDON_PRIORITY = -90


def generate_project(mod, project_dir):
    from fabricpy.compiler.quilt_gen import generate_quilt_project

    return generate_quilt_project(mod, project_dir)

