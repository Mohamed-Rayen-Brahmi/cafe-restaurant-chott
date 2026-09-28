# Render review — blockout pass

Rendered `createMaghrebTeapotModel()` in a browser (three.js, PMREM room-environment for metal
reflections, reference-mode look-dev lights) and captured screenshots via Chrome at the default
framing (azimuth 25°, elevation 12°) and a second angle (azimuth 115°).

## Comparison against teapot-reference.jpg

| Feature | Reference | Render | Verdict |
|---|---|---|---|
| Overall silhouette (bell body + domed lid + spout + handle) | present | present | match |
| Body proportions (wide shoulder, tapered base) | present | present | match |
| Lid: domed cap with ball finial | rounded dome | rounded dome (fixed from an initial over-conical pass) | match after 1 correction |
| Shoulder ribbing / neck fluting | present | present (vertical panel facets on the neck) | match |
| Spout: S-curve rising from lower body | present | present | match |
| Handle: C-loop opposite the spout | mostly occluded in source, inferred | present, reads correctly from a second angle | plausible match (documented assumption) |
| Medallion relief on body front | present (engraved scrollwork) | represented as a material-level normal/roughness local override, not modeled geometry | approximate (see below) |
| Material: satin silver metal with soft highlights | present | present (PMREM environment gives visible soft reflections, not mirror-sharp) | match |

## Corrections made this pass
1. Finial (capsule primitive) rendered at the primitive's hardcoded native size (0.35 radius x 0.7
   length) instead of the intended small-bead scale, because `transform.scale` was left at
   `[1,1,1]` — capsule/box/sphere-family primitives need an explicit scale relative to their fixed
   base geometry, unlike lathe/curve-sweep/tube which encode real size directly in their profile
   points. Fixed by setting `finial.transform.scale = [0.1, 0.064, 0.1]`.
2. Lid read as too conical/pointed versus the reference's rounder dome. Fixed by adjusting the
   lathe profile's mid-points to retain a wider radius longer before tapering (rounder curve).

## Known approximation
The medallion's engraved scrollwork is represented as a material `localOverride` (darker, higher
roughness in that region) rather than true displaced geometry, per `image-analysis.md`'s
Layer 5 finding that this is physical embossing at a scale better suited to normal-map-level
relief than silhouette-affecting geometry for a "simple" tier decorative hero object. This is a
stated simplification, not a defect: at the on-site display size (roughly 300-450px), true
geometric relief would not read differently from a well-tuned normal map, and it keeps the
triangle budget appropriate for a background decorative element.

## Self-assessed fidelity
Overall: 0.78 (silhouette, proportions, and material all read correctly and are immediately
recognizable as a Maghreb teapot; the medallion and handle are the two knowingly-approximated
areas, both flagged in the spec's `assumptions`). This clears the `qualityTargets.targetFidelity`
of 0.7 set in the spec.

## Decision
`continue` — the blockout/structural/material result is good enough for a decorative site hero
element. Further passes (surface-pass geometric relief, lighting-pass fine-tuning,
optimization-pass triangle reduction) are not warranted for this use case; stopping here to embed
on the actual site rather than continuing to refine a decorative asset indefinitely.
