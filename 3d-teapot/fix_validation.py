import json

d = json.load(open('object-sculpt-spec.json'))

# 1. viewEvidence registry (matches detail-inventory zones from di.json)
zones = {
    "zone-r0c0": (0.0, 0.0, 0.3333, 0.3333),
    "zone-r0c1": (0.3333, 0.0, 0.3333, 0.3333),
    "zone-r0c2": (0.6667, 0.0, 0.3333, 0.3333),
    "zone-r1c0": (0.0, 0.3333, 0.3333, 0.3333),
    "zone-r1c1": (0.3333, 0.3333, 0.3333, 0.3333),
    "zone-r1c2": (0.6667, 0.3333, 0.3333, 0.3333),
    "zone-r2c0": (0.0, 0.6667, 0.3333, 0.3333),
    "zone-r2c1": (0.3333, 0.6667, 0.3333, 0.3333),
    "zone-r2c2": (0.6667, 0.6667, 0.3333, 0.3333),
}
d['viewEvidence'] = [
    {
        "id": zid,
        "confidence": 0.55 if zid in ("zone-r0c0", "zone-r2c1") else 0.8,
        "imageRegion": {"x": x, "y": y, "width": w, "height": h},
    }
    for zid, (x, y, w, h) in zones.items()
]
d['viewEvidence'].append({"id": "full-object", "confidence": 0.85, "imageRegion": {"x": 0.0, "y": 0.0, "width": 1.0, "height": 1.0}})

# 2. topologyClass fixes (valid enum only)
topo = {"body": "continuous-sculpt", "lid": "continuous-sculpt", "finial": "assembled-solid",
        "spout": "continuous-sculpt", "handle": "fiber-strand"}
rationale = {
    "body": "Revolved vessel shell, no internal seams - lathe, per surface_topology.md's own 'revolved vessel' example.",
    "lid": "Revolved domed cap, same class as body.",
    "finial": "Small discrete capsule primitive with simply-curved faces - a genuine assembled-solid part.",
    "spout": "Curve-sweep following a 3D path, one continuous smoothly-varying mass, not a discrete box/cylinder part.",
    "handle": "Long, thin tube following a curved path - fiber-strand per the decision tree ('long, thin, follows a path -> tube'), matching the antenna-wire/paracord-wrap worked examples.",
}

# 3. attachment completion for children + componentCount clamp
attach_geo = {
    "lid":    {"localStart": [0, 0.30, 0], "localEnd": [0, 0.30, 0], "contactNormal": [0, 1, 0], "embedDepth": 0.008, "gapTolerance": 0.004},
    "finial": {"localStart": [0, 0.27, 0], "localEnd": [0, 0.27, 0], "contactNormal": [0, 1, 0], "embedDepth": 0.01, "gapTolerance": 0.004},
    "spout":  {"localStart": [0.40, -0.06, 0], "localEnd": [0.40, -0.06, 0], "contactNormal": [1, 0, 0], "overlap": 0.015, "gapTolerance": 0.006},
    "handle": {"localStart": [-0.34, 0.14, 0], "localEnd": [-0.34, 0.14, 0], "contactNormal": [-1, 0, 0], "overlap": 0.012, "gapTolerance": 0.006},
}

for c in d['componentTree']:
    cid = c['id']
    c['topologyClass'] = topo[cid]
    c['topologyRationale'] = rationale[cid]
    if c['parent'] is not None:
        extra = attach_geo[cid]
        c['attachment'] = {
            "parentId": c['parent'],
            "parentSocket": c['role'],
            "contactType": "rigid-socket",
            "confidence": c['confidence'],
            "evidenceRefs": c['evidenceRefs'],
            **extra,
        }

# 4. componentCount score must be an int 0-3 (a scaled score, not a literal count)
d['preSpecAssessment']['complexity']['scores']['componentCount'] = 3

# 5. detailInventory.details on the spec's own preSpecAssessment (mirrors di.json zone findings,
#    only the ones that are real identity features, not the two occlusion-neighbor zones)
d['preSpecAssessment']['detailInventory']['details'] = [
    {
        "id": "medallion-relief", "kind": "relief-detail",
        "description": "Embossed scroll/foliate medallion on the body front face.",
        "region": {"x": 0.3333, "y": 0.3333, "width": 0.3333, "height": 0.3333, "units": "normalized"},
        "scale": "micro", "affects": "material-normal",
        "mapsTo": {"type": "material", "ref": "satinMetal/medallionRelief"},
        "evidenceRef": "zone-r1c1", "confidence": 0.8,
    },
    {
        "id": "lid-finial", "kind": "geometry-feature",
        "description": "Domed lid with a small ball finial on a short stem.",
        "region": {"x": 0.3333, "y": 0.0, "width": 0.3333, "height": 0.3333, "units": "normalized"},
        "scale": "meso", "affects": "component-shape",
        "mapsTo": {"type": "component", "ref": "lid"},
        "evidenceRef": "zone-r0c1", "confidence": 0.8,
    },
    {
        "id": "spout-curve", "kind": "geometry-feature",
        "description": "Long S-curved spout sweeping up and outward from the body's lower third.",
        "region": {"x": 0.6667, "y": 0.3333, "width": 0.3333, "height": 0.3333, "units": "normalized"},
        "scale": "macro", "affects": "component-shape",
        "mapsTo": {"type": "component", "ref": "spout"},
        "evidenceRef": "zone-r1c2", "confidence": 0.8,
    },
    {
        "id": "shoulder-ring", "kind": "geometry-feature",
        "description": "Raised shoulder lip ring where the body transitions into the lid seat.",
        "region": {"x": 0.0, "y": 0.3333, "width": 1.0, "height": 0.05, "units": "normalized"},
        "scale": "meso", "affects": "component-shape",
        "mapsTo": {"type": "component", "ref": "body"},
        "evidenceRef": "zone-r1c1", "confidence": 0.7,
    },
]

# 6. lighting-pass needs concrete light entries (observed from the reference photo: soft,
#    fairly diffuse daylight from slightly above-camera-left, typical of an outdoor market stall)
d['lightingFromPhoto'] = [
    {"role": "key", "type": "directional", "direction": [-0.4, 0.8, 0.4], "intensity": 1.0,
     "colorTemperature": "neutral daylight", "notes": "Broad soft highlight along the shoulder ring and spout ridge; outdoor overcast/shaded market stall light, not a hard point source."},
    {"role": "fill", "type": "ambient", "direction": [0, 1, 0], "intensity": 0.4,
     "colorTemperature": "neutral", "notes": "Keeps the medallion grooves and handle-side shadow from going fully black."},
    {"role": "rim", "type": "environment", "direction": [0, 0, -1], "intensity": 0.25,
     "colorTemperature": "cool", "notes": "Subtle cool reflection typical of a satin metal surface under open sky."},
]

# 7. Resolve the remaining unknownsToResolveBeforeImplementation warning: they're intentionally
#    documented assumptions (not blockers) - keep them, this is a warning we accept and explain
#    rather than a defect to silently clear.

json.dump(d, open('object-sculpt-spec.json', 'w'), indent=2)
print("fix_validation applied")
