# Direction — Café Chott

## Brief
Café Chott (listed on Google Maps as "cafe restaurant chot", Facebook page "Cafe resto CHOTT") is a
tea house and café-restaurant on the old port waterfront of Bizerte, Tunisia (Harbor Drive, Bizerte
7000). Real facts gathered from Google Maps and Facebook on 2026-09-28:
- Category: tea house / café-restaurant, 4.3★ on Google (22 reviews)
- Dine-in, kerbside pickup, no-contact delivery
- Open, closes 10 PM
- Phone 55 891 298, Facebook facebook.com/cafe.chot (2,302 likes, 507 check-ins)
- Real menu detail confirmed from an owner review reply: citronade is 4 DT
- Owner replies to reviews personally and invites guests to reach out on WhatsApp: warm,
  small-business, personal tone, not corporate
- Visual identity from the venue's own Maps cover photo: harbourside terrace, mismatched colourful
  plastic bistro chairs (red, green), white round tables, paved terrace, fishing boats and the old
  port water right behind the seating

Audience: locals and visitors walking the old port promenade, families and groups who want tea,
coffee, or a light meal with a harbour view. One action: come by, or call ahead. Tone: unpretentious,
sun-warmed, port-town café, not a glossy corporate hospitality brand.

No existing logo or brand file was provided by the client, so the wordmark is a simple set typographic
treatment, not an invented emblem.

## 1. Typeface
Fraunces (display, a warm slab-serif with real personality, used at soft weight for headlines and
italic for the menu) paired with Work Sans (body and UI, humanist and legible). Serif display against
grotesque-leaning humanist body gives real contrast without reaching for Inter.

## 2. Color
Pulled from the venue's own terrace photo, not a generic hospitality palette:
- `--bg`: #FAF5E9 (sun-bleached sand)
- `--surface`: #F1E7D2
- `--text`: #22271F
- `--text-muted`: #5B6152
- `--border`: #DCCDA6
- `--accent`: #C4462A (the red bistro chair)
- `--accent-contrast`: #FAF5E9
- `--harbor` (dark band surface): #17323A (the port water at dusk)
- `--harbor-text`: #F1E7D2

Accent used only for the primary CTA and small emphasis marks, under 10% of any screen.

## 3. Radius and borders
`--r-sm: 4px; --r-md: 8px; --r-lg: 16px`. Buttons and inputs at `--r-sm`. Image panels at `--r-lg`.
Nothing at 9999px except the single circular WhatsApp/call icon button.

## 4. Spacing and layout
4px base scale. Hero band is full-bleed and breaks the container. Section rhythm varies: full-bleed
hero, contained two-column story, full-bleed menu strip on the harbor-dark surface, offset gallery,
contained hours/contact, full-bleed closing band, footer.

## 5. Motion budget (two ideas, no more)
1. The hero photo does a slow 20s drift (scale 1.0 to 1.05), paused if `prefers-reduced-motion`.
2. Menu items and section headings reveal with a small opacity and 12px translate on first scroll
   into view, once, staggered by 60ms via IntersectionObserver. No animation library.
Everything else (hover states, nav condensing) is a 120 to 200ms transform/opacity transition.

## 6. The specific move
A full-bleed real photograph of the old port of Bizerte, the actual harbor the terrace sits on
(sourced from Wikimedia Commons, not a generic beach stock photo), plus a menu section styled as a
harbor-dark chalkboard strip rather than generic pricing cards. This is unmistakably a port-town café
in Bizerte and could not be swapped onto another business.

Implemented by explicit user request: a real 3D teapot pouring tea into the same gold-rimmed glass
established elsewhere on the site, modeled and animated in Blender (via the `mcp-for-blender` MCP
connection, not a downloaded asset), exported to GLB with the bake animation intact, and played
live in-browser with three.js — the animation's playback time is driven directly by scroll
position within the section, starting only once the section is scrolled into view
(`IntersectionObserver`-gated lazy load) and staying static at one `prefers-reduced-motion` frame
for users who've asked for less motion. This superseded two earlier attempts at the same "signature
moment" idea: a procedural img2threejs reconstruction (wrong tool for a food/drink subject) and a
Canva AI-generated still-image scroll sequence (a reasonable free-tier stand-in, but not what was
asked for). Build record: `blender-teapot/` (the exported GLB) and `3d-teapot/src/blender-pour.ts`
(the three.js integration). Earlier attempts archived, not deleted, in `3d-teapot/`.

## Imagery
Two sources, kept separate and disclosed differently:
- Harbor/location photography is real, on-location photography of the actual old port of Bizerte,
  sourced from Wikimedia Commons under CC BY / CC BY-SA licenses, downloaded and self-hosted,
  converted to responsive WebP + JPEG. Full credits in `IMAGE-CREDITS.md`.
- The teapot-and-glass 3D scene is an original model built from scratch in Blender (lathed body/
  lid profiles, curve-swept spout/handle, primitive finial/leaves), not derived from any reference
  photo or downloaded asset. Disclosed as a from-scratch 3D build in `IMAGE-CREDITS.md`.
Neither set shows this specific café's own interior or drinks; the handoff flags this and recommends
the owner supply real photos of the terrace and drinks to replace both over time.

## Stack
Plain HTML, CSS, and a little vanilla JS. No framework needed for a five-section marketing site;
fastest to review and cheapest to host.
