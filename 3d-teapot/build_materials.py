import json

d = json.load(open('object-sculpt-spec.json'))

satin_metal = {
    "id": "satinMetal",
    "name": "Satin silver-tone metal",
    "type": "standard",
    "shaderModel": "MeshPhysicalMaterial",
    "baseColor": "#B7BCC0",
    "color": "#B7BCC0",
    "albedo": {
        "dominant": "#B7BCC0",
        "secondary": ["#E7E9EA", "#7B8186"],
        "samplingNotes": "Light cool gray-silver base (image-analysis.md Layer 6); highlight near-white along the shoulder ring and spout ridge, darker cool gray in recessed relief."
    },
    "colorVariation": {
        "palette": ["#B7BCC0", "#E7E9EA", "#7B8186"],
        "pattern": "curvature-driven highlight/shadow, not a texture pattern",
        "amplitude": 0.18,
        "heightCorrelation": 0.5
    },
    "textureResolution": 1024,
    "textureProjection": {
        "mode": "uv",
        "repeat": [1.0, 1.0],
        "anisotropy": 8,
        "texelDensityIntent": "Preserve stable world/object-scale detail; do not stretch the medallion relief with component scale."
    },
    "surfaceFrequencyBands": [
        {"id": "macro", "frequency": 1.5, "amplitude": 0.2, "role": "broad curvature shading, no macro color break-up (uniform metal)"},
        {"id": "meso", "frequency": 8.0, "amplitude": 0.12, "role": "shoulder ribbing and medallion relief bands"},
        {"id": "micro", "frequency": 40.0, "amplitude": 0.05, "role": "satin brushing highlight breakup under grazing light"}
    ],
    "roughness": {
        "base": 0.3,
        "variation": 0.08,
        "map": "independent-procedural-field",
        "localResponse": "higher roughness in the recessed medallion grooves, lower (more specular) on the raised shoulder ring and spout ridge"
    },
    "metalness": {"base": 1.0, "variation": 0.0},
    "normal": {
        "pattern": "derived-from-independent-height-field",
        "strength": 0.5,
        "scale": 18.0,
        "space": "tangent"
    },
    "bump": {"pattern": "none", "amplitude": 0.0, "scale": 1.0},
    "displacement": {"pattern": "none", "amplitude": 0.0, "scale": 1.0, "silhouetteAffects": False},
    "ambientOcclusion": {
        "cavityStrength": 0.35,
        "contactShadowBias": 0.3,
        "notes": "Darken the medallion grooves and the lid/body seat seam."
    },
    "wear": {"edgeWear": 0.05, "scratches": [], "chips": []},
    "dirt": {"amount": 0.0, "cavityBias": 0.0, "color": "#2F2A22"},
    "localOverrides": [
        {
            "id": "medallionRelief",
            "description": "Recessed embossed medallion on the body front face: slightly darker, higher roughness in the grooves (image-analysis.md Layer 5/7, detail-inventory zone-r1c1).",
            "region": "body front-face medallion (component: body, localFeature: medallion)",
            "colorShift": "-12% value",
            "roughness": 0.42,
            "normalStrength": 0.7
        },
        {
            "id": "shoulderHighlight",
            "description": "Raised shoulder ring catching direct light: brighter, lower roughness band (image-analysis.md Layer 6).",
            "region": "body shoulder ring, upper third",
            "colorShift": "+10% value",
            "roughness": 0.18
        }
    ],
    "shaderNotes": [
        "MeshPhysicalMaterial with metalness 1.0, no clearcoat (satin brushed finish, not lacquered).",
        "Generate roughness and normal fields independently; do not alias albedo into roughness.",
        "Normal relief only (medallion, ribbing) - no displacement geometry needed at this scale."
    ],
    "notes": "Single uniform material family across body/lid/finial/spout/handle, per image-analysis.md Layer 5 (one dominant material claim, no second material)."
}

d['materials'] = [satin_metal]
json.dump(d, open('object-sculpt-spec.json', 'w'), indent=2)
print("materials written:", [m['id'] for m in d['materials']])
