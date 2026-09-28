---
version: 1
name: Chott-design-system
description: A sun-bleached port-town café on the old harbour of Bizerte. Sand canvas, harbour-teal dark bands, and one red accent taken from the terrace's bistro chairs. Fraunces display over Work Sans body. Real harbour photography carries the mood; type stays warm and quiet. Radii are small (4 / 8 / 16px); nothing is pill-shaped except a single round call icon.

colors:
  canvas: "#FAF5E9"
  surface: "#F1E7D2"
  ink: "#22271F"
  muted: "#5B6152"
  hairline: "#DCCDA6"
  accent: "#C4462A"
  accent-hover: "#A83A21"
  on-accent: "#FAF5E9"
  harbor: "#17323A"
  harbor-surface: "#1E3D46"
  on-harbor: "#F1E7D2"
  on-harbor-muted: "#AFC2BF"
  on-harbor-accent: "#E0A98F"
  photo-scrim: "rgba(15,30,34,0.72)"

typography:
  display:
    fontFamily: "Fraunces, Georgia, 'Times New Roman', serif"
    fontWeight: 600
    lineHeight: 1.1
    letterSpacing: -0.02em
  display-italic:
    fontFamily: "Fraunces, Georgia, serif"
    fontStyle: italic
    fontWeight: 500
    use: menu category titles only
  body:
    fontFamily: "'Work Sans', -apple-system, 'Segoe UI', sans-serif"
    fontWeight: 400
    lineHeight: 1.6
  label:
    fontFamily: "'Work Sans', sans-serif"
    fontWeight: 600
    textTransform: uppercase
    letterSpacing: 0.08em
  scale:
    step--1: "clamp(0.85rem, 0.82rem + 0.14vw, 0.95rem)"
    step-0: "clamp(1rem, 0.96rem + 0.2vw, 1.125rem)"
    step-1: "clamp(1.2rem, 1.12rem + 0.4vw, 1.5rem)"
    step-2: "clamp(1.5rem, 1.34rem + 0.8vw, 2.1rem)"
    step-3: "clamp(1.9rem, 1.6rem + 1.5vw, 2.9rem)"
    step-4: "clamp(2.4rem, 1.9rem + 2.4vw, 3.8rem)"
    step-5: "clamp(3rem, 2.1rem + 4.2vw, 5.2rem)"

rounded:
  sm: 4px
  md: 8px
  lg: 16px

spacing:
  base: 4px
  container: 1240px
  gutter: 24px
  section: 96px
  section-narrow: 72px
  section-mobile: 64px
---

# Chott design system

The source of truth for the code is `public/css/styles.css` (`:root` tokens). The reasoning behind
each choice is in `DIRECTION.md`. This file is the version an agent reads before it designs a new
screen for Chott (a QR menu, a promo page, a printed card) so the new screen matches the site.

## Overview

A small, family-run tea house and café-restaurant on the quay of the old port of Bizerte. The page
should feel like sitting on its terrace: sun-warmed, unpretentious and local, never a glossy hotel
brand. Real photos of the harbour do the heavy lifting; the UI stays out of their way.

## Colors

### Brand and accent
- `accent` #C4462A is the red of the terrace's plastic bistro chairs. It is used only for the primary
  CTA (Itinéraire), the `o` in the wordmark, list bullets and the focus ring. Keep it under 10% of
  any screen.
- `accent-hover` #A83A21 is the pressed/hover state and the colour of the one eyebrow on light
  surfaces.

### Surfaces
- `canvas` #FAF5E9 is the page. `surface` #F1E7D2 is for cards, the pour section and the footer.
- `harbor` #17323A is the full-bleed dark band (the menu strip), the port water at dusk. Cards
  inside it use `harbor-surface` #1E3D46.

### Text
- `ink` #22271F for headings and strong text on light surfaces, `muted` #5B6152 for body copy.
- On harbour and photo surfaces: `on-harbor` #F1E7D2 for headings, `on-harbor-muted` #AFC2BF for
  body, `on-harbor-accent` #E0A98F for the eyebrow.

### Hairlines
- `hairline` #DCCDA6, 1px, for card borders, section rules and the scrolled header.

### Text on photos
Text never sits on a raw photo. The hero uses a top-to-bottom scrim from 0.3 to 0.82 of
`rgba(15,30,34)`. The closing band uses a flat 0.72 scrim.

## Typography

- Display: Fraunces 600, tight tracking (-0.02em), line height 1.1. Hero h1 at `step-5` (drops to
  `step-4` under 780px), section h2 at the browser default (1.5em).
- Menu category titles are the only place Fraunces italic appears. It gives the menu strip its
  chalkboard feel.
- Body: Work Sans 400 at `step-0`, line height 1.6, max 68ch.
- Labels (info card titles, footer column titles): Work Sans, uppercase, 0.08em tracking, `step--1`,
  `muted` colour.
- Self-hosted woff2 fonts in `public/fonts/`. No Google Fonts request.

## Layout

- 4px spacing base. Container 1240px with 24px side padding.
- Section rhythm alternates on purpose: full-bleed hero photo, surface-tinted pour section,
  two-column story, full-bleed harbour menu strip, offset terrace gallery, three info cards,
  full-bleed closing photo band, footer.
- Two-column grids collapse to one column under 860px. The nav collapses to a toggle under 780px.
- Headlines are left-aligned. Only the closing CTA band is centred.

## Elevation

Flat. The only shadow is the scrolled header (`0 4px 16px rgba(23,50,58,0.06)`). Depth comes from
surface colour changes and photography, not shadows.

## Components

### Buttons
- Radius `sm` (4px), padding 13px 24px, Work Sans 600 at `step--1`.
- `btn-primary`: `accent` fill, `on-accent` text. One per view.
- `btn-ghost`: transparent, `hairline` border, `ink` text. On photos use `btn-ghost-light` with a
  40% `on-harbor` border.
- Hover lifts 1px and changes colour in 160ms. Nav link hover colours never apply to buttons.

### Header
Sticky, 90% `canvas` with an 8px blur. Wordmark "Ch**o**tt" in Fraunces with the `o` in `accent`.
Right side: four anchor links and the Itinéraire button.

### Menu strip
Dark `harbor` band. Three category cards separated by 1px hairlines inside an 8px-radius frame.
Each row is name left, price right (price in `on-harbor` 600). Only show a price that the owner has
confirmed (today: Citronade 4 DT).

### Info cards
`surface` fill, `hairline` border, `md` radius, 28px padding, uppercase label title.

### Eyebrows
At most one eyebrow per three sections (Taste rule). Today the page has one, "À la carte", on the
menu strip. Do not add eyebrows above the hero or above every section heading.

## Motion

Two ideas, no more:
1. The hero photo drifts from scale 1.0 to 1.05 over 24s.
2. Content reveals once on scroll (opacity plus 12px rise, 60ms stagger).

Plus the signature piece: the Blender teapot pour, scrubbed by scroll. Everything else is a
120 to 200ms transition. All motion stops under `prefers-reduced-motion`.

## Voice

French, warm, first-person plural ("on", "nous"). Short sentences. Name real things (the quay, the
fishing boats, citronade at 4 DT). No invented reviews, awards or prices. No em dashes.

## Responsive behavior

- Tested at 1440px laptop and iPhone 15 (393px). No horizontal scroll.
- Touch targets at least 40px. The mobile menu closes when a link is tapped or Escape is pressed.

## Known gaps

- Photos show the old port, not the café's own terrace or drinks. Replace them with the owner's
  photos when available.
- Taste and Impeccable both flag Fraunces and the cream canvas as common AI defaults. They are kept
  for now because they come from the venue's own look (see `DIRECTION.md`). Revisit if the site
  starts to read as generic.
