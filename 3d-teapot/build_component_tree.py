import json, copy

d = json.load(open('object-sculpt-spec.json'))
root_template = d['componentTree'][0]

def make_component(id, name, level, role, primitive, topologyClass, topologyRationale,
                    geometryDescriptor, parent, position, dims, material="satinMetal",
                    evidenceRefs=None, confidence=0.8, importance=1.0, localFeatures=None):
    c = copy.deepcopy(root_template)
    c['id'] = id
    c['name'] = name
    c['level'] = level
    c['role'] = role
    c['importance'] = importance
    c['confidence'] = confidence
    c['primitive'] = primitive
    c['topologyClass'] = topologyClass
    c['topologyRationale'] = topologyRationale
    c['geometryDescriptor'] = geometryDescriptor
    c['parent'] = parent
    c['attachment'] = None if parent is None else {
        "parentSocket": role, "contactType": "rigid-socket", "confidence": confidence
    }
    c['dimensions'] = dims
    c['transform'] = {"position": position, "rotation": [0, 0, 0], "scale": [1, 1, 1]}
    c['actionProfile']['animationRole'] = 'root' if parent is None else 'rigid-attachment'
    c['actionProfile']['sockets'] = []
    c['actionProfile']['destruction']['breakable'] = False
    c['material'] = material
    c['materialLayers'] = [material]
    c['localFeatures'] = localFeatures or []
    c['evidenceRefs'] = evidenceRefs or ["full-object"]
    c['fidelityTier'] = 'refined'
    return c


body = make_component(
    id="body", name="Body", level="macro", role="body", primitive="lathe",
    topologyClass="surface-of-revolution",
    topologyRationale="Radially symmetric bell/onion-shaped vessel wall, correctly modeled as a lathe revolve rather than a box/cylinder blockout (grimoire/intake/surface_topology.md).",
    geometryDescriptor={
        "topologyIntent": "lathe-revolved shell with shoulder ring and neck taper",
        "edgeTreatment": {"type": "fillet", "bevelRadius": 0.01, "segments": 2},
        "deformationStack": [],
        "uvStrategy": "generated procedural coordinates",
        "normalStrategy": "vertex normals from generated geometry",
        "latheProfile": {
            "points": [
                [0.05, -0.50],
                [0.26, -0.46],
                [0.40, -0.28],
                [0.42, -0.06],
                [0.39, 0.08],
                [0.24, 0.24],
                [0.20, 0.30]
            ],
            "segments": 40
        }
    },
    parent=None, position=[0, 0, 0],
    dims={"width": 0.84, "height": 0.80, "depth": 0.84, "units": "relative", "confidence": 0.75},
    evidenceRefs=["zone-r1c1", "zone-r2c0", "zone-r1c0"],
    localFeatures=[
        {"id": "medallion", "description": "Embossed scroll/foliate medallion on the front face, centered on the belly.", "confidence": 0.75}
    ]
)

lid = make_component(
    id="lid", name="Lid", level="meso", role="lid", primitive="lathe",
    topologyClass="surface-of-revolution",
    topologyRationale="Domed, radially symmetric cap; lathe revolve captures the stepped seat ring and dome taper.",
    geometryDescriptor={
        "topologyIntent": "domed lathe cap with a raised seat lip",
        "edgeTreatment": {"type": "fillet", "bevelRadius": 0.006, "segments": 2},
        "deformationStack": [],
        "uvStrategy": "generated procedural coordinates",
        "normalStrategy": "vertex normals from generated geometry",
        "latheProfile": {
            "points": [
                [0.20, 0.0],
                [0.215, 0.03],
                [0.17, 0.09],
                [0.10, 0.18],
                [0.04, 0.245],
                [0.015, 0.27]
            ],
            "segments": 32
        }
    },
    parent="body", position=[0, 0.30, 0],
    dims={"width": 0.43, "height": 0.27, "depth": 0.43, "units": "relative", "confidence": 0.7},
    evidenceRefs=["zone-r0c1", "zone-r0c2"]
)

finial = make_component(
    id="finial", name="Finial knob", level="micro", role="finial", primitive="capsule",
    topologyClass="solid-of-revolution",
    topologyRationale="Small bead-on-stem, approximated as a capsule (sphere-like cap with a short shaft).",
    geometryDescriptor={
        "topologyIntent": "small capped cylinder standing in for a bead-on-stem finial",
        "edgeTreatment": {"type": "none", "bevelRadius": 0.0, "segments": 1},
        "deformationStack": [],
        "uvStrategy": "generated procedural coordinates",
        "normalStrategy": "vertex normals from generated geometry"
    },
    parent="lid", position=[0, 0.27, 0],
    dims={"width": 0.07, "height": 0.09, "depth": 0.07, "units": "relative", "confidence": 0.6},
    importance=0.4,
    evidenceRefs=["zone-r0c1"]
)

spout = make_component(
    id="spout", name="Spout", level="macro", role="spout", primitive="curve-sweep",
    topologyClass="swept-curve-solid",
    topologyRationale="Curved tapering tube emerging from the body wall and sweeping up and outward; a curve-sweep (not a straight tube/cylinder) is required to hold the S-curve silhouette (grimoire/build/geometry_patterns.md).",
    geometryDescriptor={
        "topologyIntent": "hollow-look curved sweep, constant thin cross-section",
        "edgeTreatment": {"type": "none", "bevelRadius": 0.0, "segments": 1},
        "deformationStack": [],
        "uvStrategy": "generated procedural coordinates",
        "normalStrategy": "vertex normals from generated geometry",
        "curveSweep": {
            "spine": [
                [0.0, 0.0, 0.0],
                [0.12, 0.06, 0.0],
                [0.26, 0.16, 0.0],
                [0.36, 0.20, 0.0],
                [0.46, 0.19, 0.0]
            ],
            "crossSection": {
                "points": [
                    [-0.035, -0.022],
                    [0.035, -0.022],
                    [0.045, 0.0],
                    [0.035, 0.022],
                    [-0.035, 0.022],
                    [-0.045, 0.0]
                ]
            },
            "closed": False
        }
    },
    parent="body", position=[0.40, -0.06, 0],
    dims={"width": 0.46, "height": 0.24, "depth": 0.09, "units": "relative", "confidence": 0.65},
    evidenceRefs=["zone-r1c2", "zone-r2c2"]
)

handle = make_component(
    id="handle", name="Handle", level="macro", role="handle", primitive="tube",
    topologyClass="swept-curve-solid",
    topologyRationale="C-loop handle, a thin tube swept along a curved path; geometry inferred from standard convention for this vessel type since the source crop cuts off most of it (see assumptions).",
    geometryDescriptor={
        "topologyIntent": "thin C-loop tube",
        "edgeTreatment": {"type": "none", "bevelRadius": 0.0, "segments": 1},
        "deformationStack": [],
        "uvStrategy": "generated procedural coordinates",
        "normalStrategy": "vertex normals from generated geometry",
        "tubePath": {
            "points": [
                [0.0, 0.0, 0.0],
                [-0.16, -0.04, 0.0],
                [-0.24, -0.20, 0.0],
                [-0.18, -0.36, 0.0],
                [-0.03, -0.44, 0.0]
            ],
            "radius": 0.032,
            "closed": False
        }
    },
    parent="body", position=[-0.34, 0.14, 0],
    dims={"width": 0.24, "height": 0.44, "depth": 0.06, "units": "relative", "confidence": 0.45},
    importance=0.7,
    evidenceRefs=["zone-r1c0"]
)

d['componentTree'] = [body, lid, finial, spout, handle]
json.dump(d, open('object-sculpt-spec.json', 'w'), indent=2)
print("componentTree written:", [c['id'] for c in d['componentTree']])
