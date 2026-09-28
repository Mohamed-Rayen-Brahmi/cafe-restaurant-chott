#!/usr/bin/env python3
"""Rebuild the pour animation of the Blender teapot GLB.

The Blender export (blender-teapot/teapot-pour.glb) has good meshes but a broken
animation:
  * it is split into five separate clips (one per object), and the site only
    played the first one (a mint leaf), so the teapot never moved;
  * the teapot rotated +55 degrees around Z, which tips the spout up and away
    from the glass, around the centre of its base;
  * the pour stream hung at x=0.20, outside the glass (x 0.242 to 0.318).

This script keeps every mesh and material from the export, drops the old
clips, and writes one "Pour" clip computed from the real geometry: the teapot
lifts and tilts so its spout lip sits over the glass, the stream runs from the
spout lip down to the tea surface on every frame, the tea fills the glass and
the mint leaves float up with it. It also checks that the teapot never goes
through the table or the glass.

Pure standard library. Usage:
    python3 scripts/fix-teapot-animation.py
"""
import json
import math
import struct
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "blender-teapot" / "teapot-pour.glb"
DST = ROOT / "public" / "models" / "teapot-pour.glb"

FPS = 24
FRAMES = 100

# Scene facts, measured from the export.
SPOUT_LIP = (0.203, 0.137)       # teapot-local x, y of the spout's lower lip
GLASS_X, GLASS_R, GLASS_TOP = 0.28, 0.038, 0.077
LIQUID_R, LIQUID_H, LIQUID_BASE = 0.027, 0.065, 0.002
STREAM_LEN = 0.135               # stream mesh hangs from y=0 to y=-0.135
FILL_MAX = 0.92

# Pour pose.
TILT_DEG = 50.0
LIP_TARGET = (0.262, 0.128)      # world x, y of the spout lip while pouring


def smooth(a, b, u):
    """Smoothstep from 0 at u=a to 1 at u=b."""
    if u <= a:
        return 0.0
    if u >= b:
        return 1.0
    t = (u - a) / (b - a)
    return t * t * (3 - 2 * t)


def ease_out(a, b, u):
    if u <= a:
        return 0.0
    if u >= b:
        return 1.0
    t = (u - a) / (b - a)
    return 1 - (1 - t) ** 2


def teapot_pose(u):
    """Return (angle_rad, tx, ty) of the Teapot node at normalized time u."""
    k = smooth(0.12, 0.38, u) * (1 - smooth(0.78, 0.96, u))
    theta = -math.radians(TILT_DEG) * k
    c, s = math.cos(theta), math.sin(theta)
    lx, ly = SPOUT_LIP
    # Where the lip would land with rotation alone, and where we want it.
    rx, ry = c * lx - s * ly, s * lx + c * ly
    wx = lx + (LIP_TARGET[0] - lx) * k
    wy = ly + (LIP_TARGET[1] - ly) * k
    return theta, wx - rx, wy - ry


def lip_world(u):
    theta, tx, ty = teapot_pose(u)
    c, s = math.cos(theta), math.sin(theta)
    lx, ly = SPOUT_LIP
    return c * lx - s * ly + tx, s * lx + c * ly + ty


def fill(u):
    return FILL_MAX * ease_out(0.39, 0.80, u)


def surface_y(u):
    return LIQUID_BASE + LIQUID_H * fill(u)


def stream_state(u):
    """Return (visible_len, thickness) of the pour stream."""
    lx, ly = lip_world(u)
    full = max(ly - surface_y(u), 0.0)
    # Tea reaches the spout, then the stream's front falls to the glass.
    grow = smooth(0.34, 0.40, u)
    # At the end the stream thins out before the teapot tips back.
    thin = 1 - smooth(0.74, 0.80, u)
    if grow <= 0 or thin <= 0:
        return 0.0, 0.0
    return full * grow, thin


# ---------------------------------------------------------------- GLB I/O

def read_glb(path):
    data = path.read_bytes()
    jlen = struct.unpack_from("<I", data, 12)[0]
    gltf = json.loads(data[20:20 + jlen])
    off = 20 + jlen
    blen = struct.unpack_from("<I", data, off)[0]
    return gltf, bytearray(data[off + 8:off + 8 + blen])


def write_glb(path, gltf, binary):
    js = json.dumps(gltf, separators=(",", ":")).encode()
    js += b" " * (-len(js) % 4)
    binary = bytes(binary) + b"\0" * (-len(binary) % 4)
    total = 12 + 8 + len(js) + 8 + len(binary)
    out = struct.pack("<III", 0x46546C67, 2, total)
    out += struct.pack("<II", len(js), 0x4E4F534A) + js
    out += struct.pack("<II", len(binary), 0x004E4942) + binary
    path.write_bytes(out)


def positions(gltf, binary, mesh_index):
    out = []
    for prim in gltf["meshes"][mesh_index]["primitives"]:
        acc = gltf["accessors"][prim["attributes"]["POSITION"]]
        bv = gltf["bufferViews"][acc["bufferView"]]
        base = bv.get("byteOffset", 0) + acc.get("byteOffset", 0)
        stride = bv.get("byteStride", 12)
        for k in range(acc["count"]):
            out.append(struct.unpack_from("<3f", binary, base + k * stride))
    return out


def strip_animations(gltf, binary):
    """Remove all animations and the accessors/bufferViews only they used."""
    anim_acc = set()
    for anim in gltf.get("animations", []):
        for smp in anim["samplers"]:
            anim_acc.update((smp["input"], smp["output"]))
    gltf["animations"] = []

    keep_acc = [i for i in range(len(gltf["accessors"])) if i not in anim_acc]
    acc_map = {old: new for new, old in enumerate(keep_acc)}
    used_bv = sorted({gltf["accessors"][i]["bufferView"] for i in keep_acc
                      if "bufferView" in gltf["accessors"][i]})
    bv_map = {}
    new_bin = bytearray()
    new_bvs = []
    for old in used_bv:
        bv = dict(gltf["bufferViews"][old])
        start = bv.get("byteOffset", 0)
        chunk = binary[start:start + bv["byteLength"]]
        new_bin += b"\0" * (-len(new_bin) % 4)
        bv["byteOffset"] = len(new_bin)
        new_bin += chunk
        bv_map[old] = len(new_bvs)
        new_bvs.append(bv)

    new_accs = []
    for i in keep_acc:
        acc = dict(gltf["accessors"][i])
        if "bufferView" in acc:
            acc["bufferView"] = bv_map[acc["bufferView"]]
        new_accs.append(acc)

    for mesh in gltf["meshes"]:
        for prim in mesh["primitives"]:
            prim["attributes"] = {k: acc_map[v] for k, v in prim["attributes"].items()}
            if "indices" in prim:
                prim["indices"] = acc_map[prim["indices"]]
            for tgt in prim.get("targets", []):
                for k in tgt:
                    tgt[k] = acc_map[tgt[k]]
    for img in gltf.get("images", []):
        if "bufferView" in img:
            img["bufferView"] = bv_map[img["bufferView"]]

    gltf["accessors"] = new_accs
    gltf["bufferViews"] = new_bvs
    return new_bin


def add_accessor(gltf, binary, values, kind):
    width = {"SCALAR": 1, "VEC3": 3, "VEC4": 4}[kind]
    binary += b"\0" * (-len(binary) % 4)
    offset = len(binary)
    flat = [c for v in values for c in (v if width > 1 else (v,))]
    binary += struct.pack("<%df" % len(flat), *flat)
    gltf["bufferViews"].append({"buffer": 0, "byteOffset": offset,
                                "byteLength": 4 * len(flat)})
    acc = {"bufferView": len(gltf["bufferViews"]) - 1, "componentType": 5126,
           "count": len(values), "type": kind}
    if kind == "SCALAR":
        acc["min"], acc["max"] = [min(values)], [max(values)]
    gltf["accessors"].append(acc)
    return len(gltf["accessors"]) - 1


# ---------------------------------------------------------------- main

def main():
    gltf, binary = read_glb(SRC)
    nodes = {n["name"]: i for i, n in enumerate(gltf["nodes"])}
    leaf_rest = {name: gltf["nodes"][nodes[name]]["translation"]
                 for name in ("MintLeaf1", "MintLeaf2")}

    # Collision check against the teapot's real vertices.
    teapot_pts = []
    for child in gltf["nodes"][nodes["Teapot"]]["children"]:
        node = gltf["nodes"][child]
        t = node.get("translation", [0, 0, 0])
        teapot_pts += [(x + t[0], y + t[1], z + t[2])
                       for x, y, z in positions(gltf, binary, node["mesh"])]

    # The handle already dips ~3mm below the table in the authored rest pose;
    # only flag poses that go lower than that.
    rest_floor = min(y for _, y, _ in teapot_pts)

    us = [k / (FRAMES - 1) for k in range(FRAMES)]
    times = [(k + 1) / FPS for k in range(FRAMES)]
    worst_floor, worst_glass = 1.0, 1.0
    for u in us:
        theta, tx, ty = teapot_pose(u)
        c, s = math.cos(theta), math.sin(theta)
        for x, y, z in teapot_pts:
            wx, wy = c * x - s * y + tx, s * x + c * y + ty
            worst_floor = min(worst_floor, wy)
            if wy < GLASS_TOP + 0.004:
                worst_glass = min(worst_glass,
                                  math.hypot(wx - GLASS_X, z) - GLASS_R)
    assert worst_floor > rest_floor - 1e-4, "teapot goes through the table: %.4f" % worst_floor
    assert worst_glass > 0.002, "teapot hits the glass: %.4f" % worst_glass

    tea_rot, tea_pos = [], []
    str_pos, str_scale = [], []
    liq_scale = []
    leaf_pos = {name: [] for name in leaf_rest}
    for u in us:
        theta, tx, ty = teapot_pose(u)
        tea_rot.append((0.0, 0.0, math.sin(theta / 2), math.cos(theta / 2)))
        tea_pos.append((tx, ty, 0.0))

        lx, ly = lip_world(u)
        length, thick = stream_state(u)
        if length <= 1e-5:
            str_pos.append((lx, ly, 0.0))
            str_scale.append((0.0, 0.0, 0.0))
        else:
            assert abs(lx - GLASS_X) < LIQUID_R, "stream misses the tea at u=%.2f" % u
            str_pos.append((lx, ly, 0.0))
            str_scale.append((thick, length / STREAM_LEN, thick))

        f = fill(u)
        liq_scale.append((1.0, max(f, 1e-4), 1.0))
        for name, rest in leaf_rest.items():
            y = max(rest[1], surface_y(u) + 0.0005)
            leaf_pos[name].append((rest[0], y, rest[2]))

    binary = strip_animations(gltf, binary)
    t_acc = add_accessor(gltf, binary, times, "SCALAR")
    channels, samplers = [], []

    def track(node_name, path, values):
        kind = "VEC4" if path == "rotation" else "VEC3"
        out = add_accessor(gltf, binary, values, kind)
        samplers.append({"input": t_acc, "output": out, "interpolation": "LINEAR"})
        channels.append({"sampler": len(samplers) - 1,
                         "target": {"node": nodes[node_name], "path": path}})

    track("Teapot", "rotation", tea_rot)
    track("Teapot", "translation", tea_pos)
    track("PourStream", "translation", str_pos)
    track("PourStream", "scale", str_scale)
    track("TeaLiquid", "scale", liq_scale)
    for name, values in leaf_pos.items():
        track(name, "translation", values)
    gltf["animations"] = [{"name": "Pour", "channels": channels, "samplers": samplers}]

    # Rest pose = first frame, so a static render before scrolling is correct.
    gltf["nodes"][nodes["PourStream"]]["scale"] = [0, 0, 0]
    gltf["nodes"][nodes["PourStream"]]["translation"] = list(str_pos[0])
    gltf["nodes"][nodes["TeaLiquid"]]["scale"] = [1, 1e-4, 1]

    # Amber mint tea rather than pale yellow once seen through the glass.
    for mat in gltf["materials"]:
        if mat["name"] == "TeaLiquid":
            mat["pbrMetallicRoughness"]["baseColorFactor"] = [0.40, 0.15, 0.02, 0.92]

    gltf["buffers"] = [{"byteLength": len(binary)}]
    write_glb(DST, gltf, binary)
    print("wrote %s (%d bytes), 1 clip, %d frames, %.2fs" %
          (DST.relative_to(ROOT), DST.stat().st_size, FRAMES, times[-1]))
    print("lowest point %.4f (rest %.4f), glass clearance %.4f" %
          (worst_floor, rest_floor, worst_glass))


if __name__ == "__main__":
    main()
