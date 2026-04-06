import json
from pathlib import Path


_FACE_NAMES = ("north", "south", "east", "west", "up", "down")
_FACE_NORMALS = {
    "north": (0, 0, -1),
    "south": (0, 0, 1),
    "east": (1, 0, 0),
    "west": (-1, 0, 0),
    "up": (0, 1, 0),
    "down": (0, -1, 0),
}
_NORMAL_TO_FACE = {value: key for key, value in _FACE_NORMALS.items()}
_MODDED_ENTITY_FACE_MAP = {
    "north": "north",
    "south": "south",
    "east": "west",
    "west": "east",
    "up": "up",
    "down": "down",
}


def _float_list(value, length: int) -> list[float] | None:
    if not isinstance(value, list) or len(value) != length:
        return None
    try:
        return [float(v) for v in value]
    except (TypeError, ValueError):
        return None


def _cube_uv_from_box_uv(element: dict) -> list[float] | None:
    uv_offset = _float_list(element.get("uv_offset"), 2)
    if uv_offset:
        return uv_offset
    faces = element.get("faces")
    if isinstance(faces, dict):
        for face_name in _FACE_NAMES:
            face = faces.get(face_name)
            if isinstance(face, dict):
                uv = _float_list(face.get("uv"), 4)
                if uv:
                    return [uv[0], uv[1]]
    return None


def _cube_uv_from_faces(element: dict) -> dict | None:
    faces = element.get("faces")
    if not isinstance(faces, dict):
        return None
    uv_map = {}
    for face_name in _FACE_NAMES:
        face = faces.get(face_name)
        if not isinstance(face, dict):
            continue
        uv = _float_list(face.get("uv"), 4)
        if not uv:
            continue
        entry = {
            "uv": [uv[0], uv[1]],
            "uv_size": [uv[2] - uv[0], uv[3] - uv[1]],
        }
        rotation = face.get("rotation")
        if isinstance(rotation, (int, float)) and rotation:
            entry["uv_rotation"] = float(rotation)
        uv_map[face_name] = entry
    return uv_map or None


def _remap_face_keys(face_uv: dict, mapping: dict[str, str]) -> dict:
    remapped = {}
    for face_name, entry in face_uv.items():
        remapped[mapping.get(face_name, face_name)] = entry
    return remapped


def _quarter_turns(angle: float) -> int | None:
    rounded = round(angle / 90.0)
    if abs(angle - (rounded * 90.0)) > 1e-6:
        return None
    return int(rounded)


def _rotate_normal_x(normal: tuple[int, int, int], turns: int) -> tuple[int, int, int]:
    x, y, z = normal
    turns %= 4
    for _ in range(turns):
        y, z = -z, y
    return (x, y, z)


def _rotate_normal_y(normal: tuple[int, int, int], turns: int) -> tuple[int, int, int]:
    x, y, z = normal
    turns %= 4
    for _ in range(turns):
        x, z = z, -x
    return (x, y, z)


def _rotate_normal_z(normal: tuple[int, int, int], turns: int) -> tuple[int, int, int]:
    x, y, z = normal
    turns %= 4
    for _ in range(turns):
        x, y = -y, x
    return (x, y, z)


def _remap_face_uv_for_rotation(face_uv: dict, rotation: list[float] | None) -> dict:
    if not rotation or len(rotation) != 3:
        return face_uv
    x_turns = _quarter_turns(rotation[0])
    y_turns = _quarter_turns(rotation[1])
    z_turns = _quarter_turns(rotation[2])
    if x_turns is None or y_turns is None or z_turns is None:
        return face_uv

    remapped = {}
    for face_name, entry in face_uv.items():
        normal = _FACE_NORMALS.get(face_name)
        if normal is None:
            remapped[face_name] = entry
            continue
        rotated = _rotate_normal_x(normal, x_turns)
        rotated = _rotate_normal_y(rotated, y_turns)
        rotated = _rotate_normal_z(rotated, z_turns)
        target_face = _NORMAL_TO_FACE.get(rotated, face_name)
        remapped[target_face] = entry
    return remapped


def _convert_cube(element: dict, box_uv_default: bool) -> dict | None:
    from_pos = _float_list(element.get("from"), 3)
    to_pos = _float_list(element.get("to"), 3)
    if not from_pos or not to_pos:
        return None
    cube = {
        "origin": from_pos,
        "size": [to_pos[i] - from_pos[i] for i in range(3)],
    }
    pivot = _float_list(element.get("origin"), 3)
    if pivot:
        cube["pivot"] = pivot
    rotation = _float_list(element.get("rotation"), 3)
    if rotation and any(abs(v) > 1e-6 for v in rotation):
        cube["rotation"] = rotation
    inflate = element.get("inflate")
    if isinstance(inflate, (int, float)) and inflate:
        cube["inflate"] = float(inflate)
    if bool(element.get("mirror_uv")) or bool(element.get("mirror")):
        cube["mirror"] = True

    face_uv = _cube_uv_from_faces(element)
    if face_uv:
        face_uv = _remap_face_uv_for_rotation(face_uv, rotation)
        cube["uv"] = face_uv
    elif bool(element.get("box_uv", box_uv_default)):
        uv = _cube_uv_from_box_uv(element)
        if uv:
            cube["uv"] = uv

    return cube


def _cube_bounds(cube: dict) -> tuple[float, float, float, float, float, float]:
    origin = cube["origin"]
    size = cube["size"]
    return (
        float(origin[0]),
        float(origin[1]),
        float(origin[2]),
        float(origin[0] + size[0]),
        float(origin[1] + size[1]),
        float(origin[2] + size[2]),
    )


def _merge_bounds(bounds: list[tuple[float, float, float, float, float, float]]) -> tuple[float, float, float, float, float, float]:
    xs1 = [b[0] for b in bounds]
    ys1 = [b[1] for b in bounds]
    zs1 = [b[2] for b in bounds]
    xs2 = [b[3] for b in bounds]
    ys2 = [b[4] for b in bounds]
    zs2 = [b[5] for b in bounds]
    return (min(xs1), min(ys1), min(zs1), max(xs2), max(ys2), max(zs2))


def convert_bbmodel_to_geckolib_geo(model: dict, mod_id: str, default_id: str) -> dict:
    meta = model.get("meta") if isinstance(model, dict) else None
    model_format = meta.get("model_format", "") if isinstance(meta, dict) else ""
    resolution = model.get("resolution") if isinstance(model, dict) else None
    texture_width = int(resolution.get("width", 16)) if isinstance(resolution, dict) else 16
    texture_height = int(resolution.get("height", 16)) if isinstance(resolution, dict) else 16
    box_uv_default = bool(meta.get("box_uv")) if isinstance(meta, dict) else False

    elements = model.get("elements") if isinstance(model, dict) else None
    outliner = model.get("outliner") if isinstance(model, dict) else None
    if not isinstance(elements, list):
        elements = []
    if not isinstance(outliner, list):
        outliner = []

    element_map = {}
    converted_cubes = {}
    for index, element in enumerate(elements):
        if not isinstance(element, dict):
            continue
        uuid = str(element.get("uuid") or f"element_{index}")
        element_map[uuid] = element
        cube = _convert_cube(element, box_uv_default)
        if cube:
            if model_format == "modded_entity" and isinstance(cube.get("uv"), dict):
                cube["uv"] = _remap_face_keys(cube["uv"], _MODDED_ENTITY_FACE_MAP)
            converted_cubes[uuid] = cube

    bones: list[dict] = []
    bone_by_name: dict[str, dict] = {}
    used_elements: set[str] = set()
    root_bone: dict | None = None
    synthetic_index = 0

    def ensure_root() -> dict:
        nonlocal root_bone
        if root_bone is None and "root" in bone_by_name:
            root_bone = bone_by_name["root"]
        if root_bone is None:
            root_bone = {"name": "root", "pivot": [0.0, 0.0, 0.0], "cubes": []}
            bones.append(root_bone)
            bone_by_name["root"] = root_bone
        return root_bone

    def new_group_name(raw_name: str | None) -> str:
        nonlocal synthetic_index
        name = (raw_name or "").strip()
        if not name:
            synthetic_index += 1
            name = f"bone_{synthetic_index}"
        existing = {bone["name"] for bone in bones}
        if name not in existing:
            return name
        suffix = 2
        while f"{name}_{suffix}" in existing:
            suffix += 1
        return f"{name}_{suffix}"

    def walk(nodes: list, parent_name: str | None = None):
        nonlocal root_bone
        for node in nodes:
            if isinstance(node, str):
                cube = converted_cubes.get(node)
                if not cube:
                    continue
                used_elements.add(node)
                target = ensure_root() if parent_name is None else bone_by_name.get(parent_name) or ensure_root()
                target.setdefault("cubes", []).append(cube)
                continue

            if not isinstance(node, dict):
                continue

            bone_name = new_group_name(node.get("name"))
            bone = {"name": bone_name}
            if parent_name:
                bone["parent"] = parent_name

            pivot = _float_list(node.get("origin"), 3) or _float_list(node.get("pivot"), 3)
            bone["pivot"] = pivot or [0.0, 0.0, 0.0]

            rotation = _float_list(node.get("rotation"), 3)
            if rotation and any(abs(v) > 1e-6 for v in rotation):
                bone["rotation"] = rotation

            if node.get("visibility") is False:
                bone["neverRender"] = True

            bone["cubes"] = []
            bones.append(bone)
            bone_by_name[bone_name] = bone
            if bone_name == "root" and root_bone is None:
                root_bone = bone
            walk(node.get("children") if isinstance(node.get("children"), list) else [], bone_name)
            if not bone["cubes"]:
                bone.pop("cubes")

    walk(outliner)

    for uuid, cube in converted_cubes.items():
        if uuid not in used_elements:
            ensure_root().setdefault("cubes", []).append(cube)

    if not bones:
        ensure_root()

    bounds = []
    for bone in bones:
        for cube in bone.get("cubes", []):
            bounds.append(_cube_bounds(cube))
    if bounds:
        min_x, min_y, min_z, max_x, max_y, max_z = _merge_bounds(bounds)
        visible_bounds_width = max(1.0, max(max_x - min_x, max_z - min_z) / 16.0)
        visible_bounds_height = max(1.0, (max_y - min_y) / 16.0)
        visible_bounds_offset = [
            (min_x + max_x) / 32.0,
            (min_y + max_y) / 32.0,
            (min_z + max_z) / 32.0,
        ]
    else:
        visible_bounds_width = 1.0
        visible_bounds_height = 1.0
        visible_bounds_offset = [0.0, 0.5, 0.0]

    identifier = model.get("model_identifier") or model.get("geometry_name") or f"geometry.{mod_id}.{default_id.replace('/', '.')}"

    return {
        "format_version": "1.12.0",
        "minecraft:geometry": [
            {
                "description": {
                    "identifier": identifier,
                    "texture_width": texture_width,
                    "texture_height": texture_height,
                    "visible_bounds_width": visible_bounds_width,
                    "visible_bounds_height": visible_bounds_height,
                    "visible_bounds_offset": visible_bounds_offset,
                },
                "bones": bones,
            }
        ],
    }


def compile_bbmodel_file(src: Path, dest: Path, mod_id: str, default_id: str) -> None:
    model = json.loads(src.read_text(encoding="utf-8"))
    geo = convert_bbmodel_to_geckolib_geo(model, mod_id, default_id)
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(geo, indent=2), encoding="utf-8")


def compile_bbmodels_in_assets(assets_mod_dir: Path, mod_id: str) -> list[Path]:
    compiled = []
    geo_root = assets_mod_dir / "geo"
    if not geo_root.exists():
        return compiled
    for src in geo_root.rglob("*.bbmodel"):
        rel = src.relative_to(geo_root).with_suffix("")
        dest = src.with_suffix(".geo.json")
        compile_bbmodel_file(src, dest, mod_id, rel.as_posix())
        compiled.append(dest)
    return compiled
