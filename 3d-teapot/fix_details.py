import json

d = json.load(open('object-sculpt-spec.json'))

d['preSpecAssessment']['detailInventory']['details'] = [
    {
        "id": "medallion-relief", "kind": "linework",
        "description": "Embossed scroll/foliate medallion on the body front face.",
        "region": {"x": 0.3333, "y": 0.3333, "width": 0.3333, "height": 0.3333, "units": "normalized"},
        "scale": "micro", "affects": "material-normal",
        "mapsTo": {"type": "material", "ref": "satinMetal/medallionRelief"},
        "evidenceRef": "zone-r1c1", "confidence": 0.8,
    },
    {
        "id": "shoulder-ring", "kind": "bevel",
        "description": "Raised shoulder lip ring where the body transitions into the lid seat.",
        "region": {"x": 0.0, "y": 0.3333, "width": 1.0, "height": 0.05, "units": "normalized"},
        "scale": "meso", "affects": "component-shape",
        "mapsTo": {"type": "component", "ref": "body"},
        "evidenceRef": "zone-r1c1", "confidence": 0.7,
    },
    {
        "id": "lid-seat-groove", "kind": "groove",
        "description": "Recessed seam where the lid seats onto the body's neck.",
        "region": {"x": 0.3333, "y": 0.28, "width": 0.3333, "height": 0.05, "units": "normalized"},
        "scale": "meso", "affects": "material-normal",
        "mapsTo": {"type": "component", "ref": "lid"},
        "evidenceRef": "zone-r0c1", "confidence": 0.65,
    },
    {
        "id": "specular-highlight-band", "kind": "gloss",
        "description": "Bright specular highlight band along the shoulder ring and spout ridge from the overhead market-stall light.",
        "region": {"x": 0.0, "y": 0.3, "width": 1.0, "height": 0.08, "units": "normalized"},
        "scale": "meso", "affects": "material-roughness",
        "mapsTo": {"type": "material", "ref": "satinMetal/shoulderHighlight"},
        "evidenceRef": "zone-r1c1", "confidence": 0.75,
    },
]

# colorMaterialRecipe: quick per-component summary tying back to the single shared material
recipe = {
    "body": "Satin silver-gray base (#B7BCC0) with a darker (-12% value) higher-roughness medallion region and a brighter (+10% value) lower-roughness shoulder band; see materials.satinMetal.",
    "lid": "Same satinMetal base as body; brighter along the dome's upper curve (direct light), darker at the seat groove.",
    "finial": "Same satinMetal base; small scale means it reads mostly as a single specular highlight point.",
    "spout": "Same satinMetal base; brighter along the outer curve ridge, darker on the inner curve (self-shadowed).",
    "handle": "Same satinMetal base; uniform, no local override (occluded region, inferred geometry).",
}
for c in d['componentTree']:
    c['colorMaterialRecipe'] = recipe[c['id']]

# lighting-pass extras
d['lightingFromPhoto'].append({
    "role": "exposure", "type": "tone-mapping", "direction": [0, 0, 0], "intensity": 1.0,
    "colorTemperature": "neutral",
    "notes": "ACESFilmicToneMapping, exposure ~1.0; ground/contact shadow via a simple soft drop shadow blob or ContactShadows-style plane under the component group (no full shadow-map rig needed for a small decorative hero object).",
})

json.dump(d, open('object-sculpt-spec.json', 'w'), indent=2)
print("fix_details applied")
