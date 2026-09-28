# Image credits

All photography is sourced from Wikimedia Commons, downloaded and self-hosted in `/public/images`,
resized and re-encoded to WebP/JPEG. None of these are photos of Café Chott's own premises; they are
real, on-location photographs of the old port of Bizerte, the harbor the café's terrace overlooks.
Recommend the owner supply real photos of the terrace, drinks, and food to add to or replace these.

| Used as | Source file | Photographer | License | Source page |
|---|---|---|---|---|
| Hero band (`hero-*`) | Bizerte_old_fishing_port.jpg | khaled abdelmoumen | CC BY 2.0 | https://commons.wikimedia.org/wiki/File:Bizerte_old_fishing_port.jpg |
| About section (`about-port-*`) | Old port of Bizerte, 2008.jpg | Letaief | CC BY 3.0 | https://commons.wikimedia.org/wiki/File:Old_port_of_Bizerte,_2008.jpg |
| Terrace card (`terrace-*`) | RestaurantPhenicienVieuxPortBizerte.jpg | Rais58 | CC BY 2.0 | https://commons.wikimedia.org/wiki/File:RestaurantPhenicienVieuxPortBizerte.jpg |
| Menu section side image (`menu-side-*`) | The old port of Bizerte 02.jpg | Kritzolina | CC BY-SA 4.0 | https://commons.wikimedia.org/wiki/File:The_old_port_of_Bizerte_02.jpg |
| Closing CTA band (`cta-band-*`) | Panoramique 2.jpg | Gigi Sorrentino | CC BY-SA 3.0 | https://commons.wikimedia.org/wiki/File:Panoramique_2.jpg |

CC BY and CC BY-SA both permit commercial use and modification (resizing, cropping, format
conversion) provided attribution is kept. Attribution is given on this page and in the site footer's
"Photo credits" link. No image was cropped in a way that misrepresents the original scene.

## "Le thé à la menthe" 3D teapot pour

The live 3D scene (teapot + gold-rimmed tea glass, `public/models/teapot-pour.glb`, played by
`public/js/teapot-blender.min.js`) was modeled and animated from scratch in Blender via the
`mcp-for-blender` connection: a lathed vessel body and lid, curve-swept spout and handle, a
primitive finial, and two simple leaf shapes, none derived from a photo or downloaded asset. The
pour, fill, and tilt are keyframed object animation, exported with the glTF/GLB animation intact
and driven in the browser by scroll position rather than by time, so it plays forward and back as
the visitor scrolls through the section. Not a photo of Chott's own teapot or glassware; recommend
the owner supply reference photos of their own service ware if a closer match is wanted later.

**Prior attempts, both superseded and archived (not deleted) in `3d-teapot/`:**
1. A procedural Three.js reconstruction via the `img2threejs` skill, built from a cropped market-
   stall photo. Dropped after reviewing the client-supplied workflow guide: that skill is meant for
   rigid objects (a sneaker, a bottle), explicitly not food or drink.
2. A Canva-generated still-image scroll sequence (`public/images/pour/frame-*.webp`, still present
   on disk but no longer referenced by `index.html`) standing in for real product photography.
   Reasonable free-tier substitute, but replaced once the user asked directly for a real Blender-
   built 3D animation instead.
