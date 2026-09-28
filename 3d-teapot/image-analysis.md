# Image analysis — teapot-reference.jpg

Cropped from a market-stall photo of Maghreb metal teapots (CC BY-SA 4.0, Wikimedia Commons,
"A traditional Moroccan tea, silver version.jpg"). One teapot is isolated as the primary subject;
a second teapot's dome lid intrudes at the top-left corner (occlusion, noted in Layer 8).

## Layer 1 — Identification
Work type: teapot (Maghreb/North African style, "berrad"). Broad classification: metal vessel /
tableware. primaryDomain: object. Confidence: 0.9 (clear silhouette, minor neighbor occlusion at
one corner only).

## Layer 2 — Form & silhouette
Primitives: a bell/onion-shaped lofted body (wide shoulder, tapering to a narrower flat-ish
base — a lofted curve, not a simple sphere or cylinder), a domed conical lid with a small finial
knob, a curved tapering spout (a swept tube, curving upward and outward from the body's lower
third), a loop handle (partially visible at the left edge — inferred as a C-shaped tube/strap
attached opposite the spout, standard for this vessel type). Bilateral symmetry through the
spout-handle axis; the body itself is a radial (lathe-turned) form.

## Layer 3 — Macro → meso → micro decomposition
- Macro: body (the bell-shaped shell), lid (dome + finial), spout, handle.
- Meso: shoulder band (where body transitions from wide to the lid seat, has a raised ring lip),
  body medallion (a large embossed scroll/foliate roundel centered on the front face), lid seat
  ring (where lid meets body).
- Micro: finial knob (small sphere/bead on a short stem, top of lid), lid ribbing (faint vertical
  fluting on the dome, visible as tonal bands), medallion scrollwork (a repeating engraved
  arabesque/foliate motif inside the medallion, symmetric about the vertical centerline), spout
  tip (a slightly flared opening at the far end).

## Layer 4 — Spatial relationships
`<lid, sits-on, body>` (above, flush at the shoulder ring — contact type: seated/removable).
`<finial, attached-to, lid>` (above, top of dome, contact type: butt/rigid).
`<spout, attached-to, body>` (lateral-right, emerges from lower-third of the body, contact type:
  socket/rigid, curves upward away from the body wall).
`<handle, attached-to, body>` (lateral-left, opposite the spout, contact type: socket/rigid,
  inferred as a C-loop — not fully visible in this crop).
`<medallion, embossed-into, body-front-face>` (embedded/relief, not a separate part).

## Layer 5 — Materials & surface (PBR)
Uniform metal finish across body, lid, spout, handle: metalness ~1, roughness low-to-mid
(0.25-0.35 — a satin/brushed-silver finish, not a mirror polish; specular highlights are broad
and soft rather than pinpoint), specular F0 typical of a silver-tone alloy (likely nickel-plated
brass or alpaca/nickel silver, common for this vessel type, not sterling). Relief detail (the
medallion scrollwork, shoulder ribbing) reads through normal/bump displacement, not a texture
map — it is physical embossing, not paint.

## Layer 6 — Color & finish
Base color: cool light gray-silver, mid-value, low saturation. Finish: satin metallic, with
warmer/brighter specular highlights along the shoulder ring and spout ridge (direct light
catching the curvature) and darker gray-blue in the recessed medallion grooves (ambient
occlusion in the relief). Not a flat single gray — a value gradient from highlight (near-white)
to core shadow (mid-dark gray) typical of a curved metal surface.

## Layer 7 — Identity-defining features
- The embossed scroll/foliate medallion on the body front — the single most identity-defining
  feature; a plain unadorned body would read as a generic pot, not this object. → critical.
- The stepped dome lid with a small ball finial. → critical.
- The long curved spout silhouette (proportionally long relative to body height, gently
  S-curved). → critical.
- Shoulder ribbing / raised lip ring at the lid seat. → important.
No inscriptions, no maker's mark visible in this crop.

## Layer 8 — Uncertainty & single-image limits
- The handle is only partially visible (cropped at the left edge) — its exact loop shape is
  inferred from the standard convention for this vessel type, not measured from this image;
  flagged as an assumption, not a fact.
- A second teapot's golden dome lid overlaps the top-left corner of the crop (occlusion) — does
  not affect the primary subject's silhouette, ignored as background noise.
- Base/foot underside not visible (object sits on cloth); modeled as a simple flat foot,
  inferred.
- Source crop is small (500x410 after 2x upscale from a 250x205 region) — fine engraved
  linework inside the medallion is inferred as "scrollwork," not traced exactly stroke-for-stroke.

Complexity tier: **simple** (single dominant material family, four macro parts, one identity
medallion, no character/skin domain applies).
