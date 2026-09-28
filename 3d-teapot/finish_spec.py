import json

d = json.load(open('object-sculpt-spec.json'))
ids = ["body", "lid", "finial", "spout", "handle"]

d['silhouette'] = {
    "boundingShape": "bell-bodied vessel with a domed lid, one lateral curved spout, one lateral loop handle",
    "aspectRatios": ["height:width approx 1.35:1 (body+lid, excluding spout/handle)"],
    "symmetry": "bilateral about the spout-handle axis; body/lid individually radial (lathe)",
    "dominantCurves": [
        "body profile: wide shoulder tapering to a narrow base (bell/onion curve)",
        "spout: gentle S-curve rising from the body wall to the tip",
        "handle: C-loop from upper shoulder to lower body"
    ],
    "negativeSpaces": ["the open loop of the handle (C-shape) against the body wall"],
    "landmarks": ["shoulder ring (widest point)", "lid seat ring", "medallion center", "finial apex", "spout tip"]
}

d['coordinateFrame']['scaleReference'] = "body height ~0.8 relative units, matches the object's own lathe profile scale; adjust only if the first render reads too large/small next to UI context"

d['assumptions'] = [
    "Handle loop shape follows the standard C-loop convention for this vessel type; the source crop cuts off most of the handle (image-analysis.md Layer 8).",
    "Base/foot underside is not visible in the source image; modeled as a simple flat taper.",
    "Rib count and exact medallion linework are inferred from a single, slightly low-resolution crop, not traced stroke-for-stroke.",
    "A second teapot's lid intrudes at the reference crop's top-left corner; treated as background noise, not part of this object."
]

d['risks'] = [
    "Handle geometry may not match the real object's handle exactly (not visible in source) - acceptable for a decorative hero element, not a manufacturing reference.",
    "Low source-image resolution (500x410 after 2x upscale) limits confidence on fine medallion linework; represented as a normal-map-level relief detail, not exact geometry."
]

# Point componentRefs at the real component ids instead of the generator's placeholder "root"
for bp in d['buildPasses']:
    bp['componentRefs'] = ids
for ft in d['featureReviewTargets']:
    ft['componentRefs'] = ids

d['performanceBudget'] = {
    "qualityPriority": "balanced",
    "targetTriangles": 40000,
    "maxDrawCalls": 8,
    "textureSize": 512,
    "fpsTarget": 60,
    "optimizationPolicy": "Decorative hero element on a marketing site: keep triangle count and draw calls low for fast mobile load, auto-rotate at a slow, cheap frame rate, pause fully when offscreen."
}

json.dump(d, open('object-sculpt-spec.json', 'w'), indent=2)
print("finish_spec applied")
