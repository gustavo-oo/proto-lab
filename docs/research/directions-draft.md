# Prototype skill — Design Directions & AI-Slop Fingerprints (draft v0.1)

Purpose: a seed picks ONE direction below (closed system), then varies only the orthogonal knobs in section C. Grounded in: Swiss/ITP (Müller-Brockmann, Helvetica/Univers), print editorial (Monocle, Kinfolk, Editorial Luxe), Apple HIG, Bloomberg terminal practice, NN/g + neobrutalism.com, Typewolf font data, vocab.design, Risograph print references, and 2025–26 AI-slop discourse (925studios, ahd/SLOP_TAXONOMY, unslop-ui). Galleries scanned: Godly, Land-book, Minimal Gallery, Brutalist Websites, Awwwards, Typewolf.

Rules used below: **Type** = class + 2–3 concrete faces (free alt in parens). **Shape** = radius/shadow language. Directions are closed systems; mixing happens only via C.

---

## A. DESIGN DIRECTIONS (22)

### D01 · Swiss International — the grid is the argument; neutrality is a stance
- **Type**: one neo-grotesque — Helvetica Now/Neue Haas (free alt: Instrument Sans, Archivo), Univers; 2–3 sizes per page max, flush-left ragged-right, baseline rhythm.
- **Color**: black on white + ONE red (#E60000) as warning/emphasis, never a field; no tints, no gradients, colour never carries hierarchy.
- **Layout / density**: 8pt modular grid, asymmetric columns, hierarchy via size + position only; medium density with ruthless, deliberate whitespace.
- **Shape / motion**: 0 radius; 1px hairlines ARE the structure; no shadows; motion = a cut (instant), at most one wipe.
- **Imagery**: documentary B/W photo pinned to grid; illustration is avoided on principle.
- **Exemplars**: Müller-Brockmann posters, SBB wayfinding, "Swiss modernism 2.0" product sites.
- **Fits**: docs, design systems, transport/logistics, portfolios. **Fails**: gridlines drawn but nothing aligned to them (most common failure); warm/humorous brands; with an undeliberate default sans it collapses into generic clean SaaS.

### D02 · Editorial Luxe — a fashion spread: type at scale, air around it
- **Type**: Didone display (Bodoni Moda, Playfair Display) at 56–96px, often one italic word; text serif for reading (Newsreader, Source Serif); tiny tracked captions.
- **Color**: quiet — oxblood/stone/sumi ink on paper (#F4F1EA); no web-bright accents; colour never competes with images.
- **Layout / density**: asymmetric spreads (5fr/7fr), headline overlapping tall portrait crops, off-axis captions, deep indents, big display→deck drop; low–medium density.
- **Shape / motion**: 0 radius, no shadows; rules as section breaks; slow mask reveals, parallax on imagery only (400–800ms).
- **Imagery**: art-directed tall portrait crops, B/W or muted; photography IS the product.
- **Exemplars**: fashion-house sites (The Row register), magazine redesigns, agency portfolios.
- **Fits**: fashion, fragrance, hospitality, premium editorial. **Fails**: stock photography kills it instantly; 10px captions and 96px headlines fail a11y if clamped wrong; wrong for any dense product UI.

### D03 · Broadsheet Newsprint — newspaper front page, taken literally
- **Type**: newsy grotesque headlines (Franklin Gothic, Helvetica) + text serif body (Times, Publico); italics for bylines; wildly varying headline sizes.
- **Color**: newsprint off-white (#F5F2EC) + ink; one masthead red; reverse (dark) variant allowed as "night edition".
- **Layout / density**: 5–6 column broadsheet, column rules, dense decks and jump lines, "above the fold" hierarchy; HIGH density.
- **Shape / motion**: 0 radius; hairline rules everywhere; motion = none (a ticker at most).
- **Imagery**: B/W halftone photos, hairline-axis charts, pull-quote boxes.
- **Exemplars**: NYT/FT front pages, FT.com, Monocle web, newsprint newsletters.
- **Fits**: news, publications, data journalism, institutional homepages. **Fails**: consumer apps, luxury; columns collapse badly on mobile unless deliberately single-column.

### D04 · Quiet Luxury / Stealth Wealth — expensive through omission, not ornament
- **Type**: light high-contrast serif display (Cormorant 300, Canela-class) + one neutral companion; wide-tracked uppercase micro-labels; generous leading.
- **Color**: near-monochrome warm neutrals; ONE muted metallic accent (e.g. brass #A08B62) used ≤3 times per page; no bright fills.
- **Layout / density**: narrow single reading column, 80–140px section gaps, centred or calm-symmetric; VERY low density; whitespace is the material.
- **Shape / motion**: 2–4px max radius or none; no shadows; hairline rules; unhurried 400–800ms fades, zero bounce; "pace of a deep breath".
- **Imagery**: material close-ups (cashmere, brass, leather), blown highlights, no smiling stock people.
- **Exemplars**: The Row-style fashion, Loro Piana, high jewellery, boutique hotel sites.
- **Fits**: premium retail, hotels, private services, fragrance. **Fails**: has become its own second-order slop when reduced to "cream + Playfair + gold on near-black" — needs a real material differentiator; unusable for dense apps/bookings tables.

### D05 · Scandinavian Slow-Living (Kinfolk) — warm paper, soft earth, quiet serif
- **Type**: transitional serif display (DM Serif Display, Spectral) + humanist sans (DM Sans); single weight 400 discipline; tracked uppercase captions.
- **Color**: warm earth system — linen #F3EDE4, parchment, clay, sage #DBDED5, ink #1A1714; no cool accents, no pure white.
- **Layout / density**: generous air, asymmetric but calm, full-bleed photo bands alternating with text; LOW density; ~170px vertical section padding.
- **Shape / motion**: 0 radius, no shadows; image-only cards; slow barely-perceptible reveals; photography desaturated ~(-18%) to integrate.
- **Imagery**: soft natural light, objects on surfaces, no hard shadows, no digital gloss.
- **Exemplars**: kinfolk.com, Nordic Society-style sites, ceramics/wellness brands.
- **Fits**: lifestyle, wellness, food, indie publishing. **Fails**: tech/SaaS, urgent CTA product flows; if the body font is swapped for Inter the warmth dies (the classic "almost Kinfolk" tell); adjacent to D04 — do not blend both (C3).

### D06 · Neo-brutalism — visible structure, hard edges, zero blur
- **Type**: heavy grotesque only (Space Grotesk 700–900, Archivo Black) or bold mono; uppercase labels; body deliberately boring for scannability.
- **Color**: flat saturated fills (lime, canary, hot pink) + pure black #000; NO gradients; ≤1 primary + 2 fills, used as blocks.
- **Layout / density**: blocky compartmentalized grid, every element boxed; medium–high density; structure is never implied, always drawn.
- **Shape / motion**: 0–8px radius (pick one per project); 2–5px borders; hard offset shadows (e.g. 6px 6px 0 #000); press-down translate on active; motion instant/mechanical.
- **Imagery**: flat chunky illustration, stickers, badge seals; no photography.
- **Exemplars**: neobrutalism.dev components, feastables.com; note Gumroad is cited everywhere but its current homepage no longer uses the hard-offset shadow.
- **Fits**: indie SaaS, dev tools, event pages, personality brands. **Fails**: enterprise/finance; softening the shadows makes it generic playful SaaS; border+shadow+fill on every node at once = noise.

### D07 · Raw Web / True Brutalism — the document IS the interface
- **Type**: system/UA defaults used knowingly (Times, Verdana) or one grotesque; underlined blue links; no custom type load.
- **Color**: white page, black text, classic link blue; maybe `<mark>` yellow; nothing else.
- **Layout / density**: single column, default document flow, `<hr>` dividers, tables for real structure; text-dense.
- **Shape / motion**: no radius, no boxes, no shadows, no motion; zero decoration by rule.
- **Imagery**: none, or one unedited image; content carries everything.
- **Exemplars**: berkshirehathaway.com, craigslist, Hacker News, brutalistwebsites.com entries.
- **Fits**: manifestos, self-hosted tools, anti-marketing products, engineer portfolios. **Fails**: consumer products; reads as laziness if not deliberate; default link colours often fail contrast audits.

### D08 · Terminal / CLI — command in, output out; monospace discipline
- **Type**: ONE mono family (IBM Plex Mono, JetBrains Mono, Berkeley Mono; VT323 only for CRT variants); same size mostly; ASCII dividers and box-drawing as ornament.
- **Color**: shell dark (#0A0A0A–#1A1A1A) + a single phosphor accent (green #00FF41 or amber #FFB000) + 2 dim levels; ANSI colours reserved for real semantics.
- **Layout / density**: single-column prompt/log rhythm; panels as bordered ASCII cells; HIGH text density; content framed as commands and responses.
- **Shape / motion**: 0 radius, 1px panel borders, no shadows (a subtle glow is allowed); typing reveals, cursor blink, instant data — all reduced-motion aware.
- **Imagery**: none — ASCII art, box-drawing, status glyphs.
- **Exemplars**: developer CLI launch sites (Ghostty, uv, warp-style), man pages as design language.
- **Fits**: dev tools, security, API docs, changelogs. **Fails**: non-technical audiences; small green-on-black text below contrast; frosted glass or rounded cards mixed in instantly break the register.

### D09 · Data Control Room (Bloomberg lineage) — dense scans under pressure; panes, not cards
- **Type**: mono tabular numerals (IBM Plex Mono, SF Mono) + compact sans; 11–13px data, micro uppercase labels; no oversized hero text ever.
- **Color**: graphite/near-black surfaces (or amber #FFB000 on #0A0A0A variant); semantic only (green/red/amber) + one cool secondary; zero decoration.
- **Layout / density**: rigid pane lattice with 1px seams, fixed columns, summary→detail adjacency, keyboard-first; VERY high density.
- **Shape / motion**: 0 radius, flat panes, borders do hierarchy, no shadows; updates are instant; subtle blink on new data only.
- **Imagery**: data as imagery — sparklines, dense tables, no photography.
- **Exemplars**: Bloomberg Terminal, Grafana dense themes, trading/ops dashboards, flight ops.
- **Fits**: fintech, observability, admin consoles, ops tooling. **Fails**: marketing pages; fake-CRT nostalgia as costume; consumer onboarding.

### D10 · Blueprint / Schematic — the technical drawing about the product IS the page
- **Type**: technical mono (Space Mono, IBM Plex Mono) + condensed sans labels; dimension values as ambient text everywhere.
- **Color**: Prussian/navy field with cyan linework (#0A1628 bg, #1A3A5C grid, #00E5FF highlights) or reversed white-blue; annotation red + approval green for status.
- **Layout / density**: visible graph-paper substrate (~5–8% opacity), corner brackets instead of borders, crosshairs, dimension callouts, title-block footer; HIGH info density.
- **Shape / motion**: 0 radius; uniform 1–2px lines, hierarchy by opacity; draw-on line tracing and a scanline sweep; nothing bounces or sparkles.
- **Imagery**: exploded views, wireframes, crop marks; no photos.
- **Exemplars**: CAD/schematic display references, hardware docs, blueprint design systems (e.g. chrislemke's Blueprint Technical).
- **Fits**: hardware, dev tools, infrastructure, construction/logistics. **Fails**: lifestyle brands; over-annotation becomes noise; grid opacity that competes with content.

### D11 · Art Deco — machine-age glamour via geometry + gold
- **Type**: geometric all-caps display (Cinzel, Poiret One, Bifur-like), wide-tracked (≥0.15em); never in body weight; small-caps labels.
- **Color**: void black/ivory cream + ONE gold (#C9A84C) with opacity steps; jewel tones only as rare fields; a second accent breaks the spell.
- **Layout / density**: symmetric, centred compositions; double-border frames (outer solid + inner faint, inset ~5px); fan/sunburst/chevron/diamond motifs; deco-rule dividers; medium, ceremonial density.
- **Shape / motion**: 0 radius; ornament built from CSS geometry; cinematic 400ms+ fades, optional gold shimmer; no bounce.
- **Imagery**: monogram/graphic ornament, silhouettes; photography rare and toned.
- **Exemplars**: hotel/cocktail brands, Gatsby ephemera, 1920s posters as UI.
- **Fits**: hospitality, spirits, events, premium launches. **Fails**: sans-serif body copy erases the period voice; ornament density past legibility; gold-on-gold contrast failures.

### D12 · Space Age / Retro-Futurism — the future as predicted by 1960s optimism; chrome & curves
- **Type**: geometric/rounded display (Futura-like, space-age alternates) wide-tracked caps; body in a clean grotesque; occasional script accent.
- **Color**: 60s print palette (cream, burnt orange, teal) OR chrome + pastels; sunburst gradients allowed as scenic imagery, not UI chrome.
- **Layout / density**: capsules, boomerangs, orbital compositions, off-centre heroes, dotted star fields; medium poster-like density.
- **Shape / motion**: pills and capsule panels, huge radii (24–999px), no hard borders; floating drift and slow orbits; optimistic easing.
- **Imagery**: checkered patterns, starbursts, atomic dots, halftone space scenes, rayguns.
- **Exemplars**: Googie architecture, NASA-era poster programs, Fallout-adjacent brand sites.
- **Fits**: playful product launches, music/events, food & bev, games. **Fails**: bolted onto flat SaaS components; chrome text used at reading sizes.

### D13 · Analog 70s / Groovy — sun-faded print warmth with groovy geometry
- **Type**: fat groovy serif (Cooper Black, Recoleta-class), chunky rounded lettering, arc-set headlines; body serif or warm sans.
- **Color**: burnt orange, harvest gold, avocado, chocolate on cream; airbrush halos; grain overlay; nothing cool-toned.
- **Layout / density**: stacked arcing headlines, radial compositions, badges/seals, striped borders; medium, cozy density.
- **Shape / motion**: rounded blobs, sticker shapes, big radii; warm bounces, slow spins; static grain texture.
- **Imagery**: airbrush illustration, mushrooms/rainbows/suns, textured paper.
- **Exemplars**: 70s packaging and music posters; modern DTC food/coffee brands.
- **Fits**: food & bev, music, lifestyle, community apps. **Fails**: B2B; over-saturated "vintage theme" effect; any technical/table UI.

### D14 · Risograph / Zine — two ink drums, misregistered, printed not rendered
- **Type**: ultra-heavy poster display (Bowlby One-class) + mono for listings; type often printed in the second ink; titles cropped/overlapped on purpose.
- **Color**: 2–3 spot inks (fluoro pink, federal blue, sunflower — e.g. #F237A1 / #2C40A7) overprinting via `mix-blend-mode: multiply`; kraft/paper base #F2EDE4; grain 4–10%.
- **Layout / density**: poster collage — rotated bands, sticker blocks, programme listings, mixed centred/flush-left on purpose; registration crosshairs kept; medium–high density.
- **Shape / motion**: hard edges; 1–3px layer offsets = "misregistration"; offset duplicate layers instead of shadows; pixel reveals, marquees, displacement hovers.
- **Imagery**: duotone/screened photos, halftone dots, cut-and-paste collage.
- **Exemplars**: indie presses (Pulpline-style two-ink studios), zine fairs, band merch sites.
- **Fits**: indie publishing, music, art events, community orgs. **Fails**: enterprise/finance; fake distress (torn paper, stains) reads as a filter; crisp digital shadows next to overprint break the illusion.

### D15 · Memphis / Playful Toy — 1980s anti-functional play; geometry with jokes
- **Type**: quirky geometric sans + allowed clash with a chunky serif; squiggles/arrows used where icons would be; all-caps shouts mixed with lowercase.
- **Color**: primary-ish brights + black/white patterns (terrazzo, squiggle, confetti, checker); clashing by design but capped at ~4–5 hues.
- **Layout / density**: asymmetric playful placements, floating shapes, diagonal energy — loud islands in whitespace; medium, scattered density.
- **Shape / motion**: circles/triangles/squiggle ribbons, large radii on cards, patterned fills; springy bouncy easings, hover wiggles.
- **Imagery**: flat vector doodads, plastic-laminate texture, sticker sheets.
- **Exemplars**: Memphis Group furniture/print, 80s Saved-by-the-Bell print, modern kids/toy brands.
- **Fits**: kids/edu, games, events, creative tools. **Fails**: enterprise; decoration without hierarchy = noise; done timidly it looks like a template.

### D16 · Y2K Gloss — millennium optimism; chrome + translucency
- **Type**: stretched/wide techy sans; liquid or outlined display; "bubbly" headings, clean small text.
- **Color**: chrome silver gradients (#C0C0C0 family), electric blue, hot pink #FF1493, lime; iridescent/holographic accents on a dark or neutral base.
- **Layout / density**: glossy pill buttons with highlight bands, frosted panels, bubbly 24px+ radii, star sparkles, faux window frames; low–medium density, maximal surfaces.
- **Shape / motion**: extreme blobs, chrome borders, gloss highlight sweeps, sparkle particles; shimmer on hover; shine sweeps.
- **Imagery**: chrome blobs, early-3D renders, CDs, flip phones, butterflies, scanner-photo effects.
- **Exemplars**: iMac G3-era hardware, rave flyers, 2000s tech-mag layouts revived.
- **Fits**: music, streetwear, clubs/events, youth brands. **Fails**: a11y (gloss and holographic text have no stable contrast); enterprise; without chrome/period specificity it degrades into default glassmorphism slop.

### D17 · Vaporwave / Synthwave Grid — ironic mall nostalgia; pink–cyan haze
- **Type**: 80s display faces + bitmap/pixel cuts; fullwidth "ｖａｐｏｒｗａｖｅ" type as ornament; katakana accents (decorative, not readable content).
- **Color**: neon pink #FF71CE, cyan #01CDFE, violet, sunset gradient with striped sun; perspective grid lines in cyan/pink.
- **Layout / density**: cinematic hero (sun + grid horizon), then a deliberately QUIET product area in ordinary type — loud hero, quiet body; low–medium density.
- **Shape / motion**: 0 radius in the "screen" motifs; slow pans, scanline flicker, glitch on hover; reduced-motion path mandatory (grid + flicker are motion-heavy).
- **Imagery**: Greco-Roman busts, palms, VHS artifacts, Windows 95 chrome — deliberate era collision.
- **Exemplars**: Bandcamp album art, itch.io game pages, synthwave artist sites.
- **Fits**: music, games, streaming overlays, niche community. **Fails**: serious products; magenta-on-cyan text is unreadable at any size; when the joke outlives the content.

### D18 · macOS Native — an app that belongs to the OS; materials + restraint
- **Type**: SF Pro with optical sizing (never disable it), SF Mono for data, New York for documents; 11–17px desktop scale.
- **Color**: system grays + ONE system tint per surface, as accent not fill; vibrancy (alpha + backdrop blur) instead of solid chrome fills; never pure black.
- **Layout / density**: sidebar (240–320px) / toolbar / content split views; 8pt spacing; dense-but-comfortable desktop rows (≥28pt targets); keyboard navigable.
- **Shape / motion**: 6–12px radii; materials replace card borders and shadows; don't shadow over a material; 0.2–0.3s standard easings.
- **Imagery**: SF Symbols (never emoji icons), album-art-like imagery, no card borders on content.
- **Exemplars**: Things, Bear, Raycast, Apple's own Settings panes as reference.
- **Fits**: desktop-first tools, pro utility web demos, dense dashboards. **Fails**: marketing pages (platform feel needs real chrome); "fake macOS window" cliché; substituting Inter kills the platform instantly.

### D19 · Instrument Dark — precision-instrument dark UI (Linear/Raycast lineage); high risk, needs density to escape slop
- **Type**: one grotesque with tight display tracking (Söhne/Untitled-class; free alt: Instrument Sans, Schibsted Grotesk) + mono data voice; kbd chips for shortcuts.
- **Color**: layered graphite — base #0B0C0E, elevated #16181C, hairline #262A31 — not "one black + neon"; ONE non-purple accent; semantics via icon+colour.
- **Layout / density**: product-first: dense lists, command menu, keyboard hints, small or absent hero; 1px low-alpha borders define geometry; HIGH density.
- **Shape / motion**: consistent 6–10px radii; no glow spam; 120–200ms transitions, subtle spring; staggered list reveals only.
- **Imagery**: product screenshots and diagram ghosts; no stock people.
- **Exemplars**: Linear, Raycast, Arc-era marketing, Vercel dashboard surfaces.
- **Fits**: dev tools, infra, productivity. **Fails**: it IS the default LLM dark mode — purple gradient glow + #0f172a + glass cards turns it into 2019-era slop; only density, restraint, and real product specificity redeem it.

### D20 · Academic Preprint (LaTeX) — a paper, taken seriously as an interface
- **Type**: Computer Modern/Latin Modern (or Charter, STIX); italic theorem voice; footnote-grade labels; math as legitimate ornament.
- **Color**: black on white; one link blue; red strictly for editorial comments; no brand decoration.
- **Layout / density**: single-column reading measure for narrative, two-column for lists/tables; numbered sections; footnotes as marginalia; booktabs-style tables (top/bottom rules only); high text density, medium air.
- **Shape / motion**: none — rules ARE section breaks; no radius, no shadows, no animation.
- **Imagery**: captioned figures ("Figure 1:"), TikZ-aesthetic diagrams, plots with hairline axes.
- **Exemplars**: arXiv landing pages, distill.pub as the refined web cousin, gwern.net.
- **Fits**: research tools, ML products, databases, technical essays, anything claiming rigor. **Fails**: consumer products; fake greeked math reads as parody; two-column on mobile.

### D21 · Field Guide / Naturalist — botanical plate + specimen label
- **Type**: old-style/transitional serif for prose (EB Garamond, Source Serif), italics for taxonomy, small caps for labels; hand-annotated feel allowed.
- **Color**: aged paper #EFE7D8, sepia ink, muted botanicals (sage, ochre, madder); duotone plates; no screen-bright hues.
- **Layout / density**: framed specimen plates with numbers/labels, margin notes, index lists, caption bands; medium, curated density.
- **Shape / motion**: 0 radius; thin double borders or corner ticks on plates; crossfades only; nothing modern-feeling moves.
- **Imagery**: scientific illustration, engravings, maps, specimen photos with scale bars.
- **Exemplars**: herbarium archives, WPA national-park posters, indie nature/provision brands.
- **Fits**: outdoors, food/provisions, botanical skincare, museums, education. **Fails**: tech; stock photos in sepia; when every element is textured without a grid underneath.

### D22 · Fashion Type-First (Poster) — type IS the campaign; huge, condensed, cropped
- **Type**: massive condensed grotesque (Druk-class; free alt: Archivo Black/Black Condensed, Anton) at 10–20vw, cropped and overlapping; body in tiny neutral sans.
- **Color**: high-contrast duotone (black/white + one hot accent such as Klein blue or signal red) or monochrome; imagery B/W-duotoned with grain.
- **Layout / density**: full-bleed type blocks, edge-to-edge crops, extreme scale jumps, poster stacking, marquees; heroes maximal, lists minimal.
- **Shape / motion**: sharp corners everywhere; no shadows; marquee scrolls, mask reveals, fast cuts.
- **Imagery**: art-directed, blown-out or duotone; grain; no clip-art.
- **Exemplars**: fashion-week sites, SSENSE-style campaign pages, festival identity systems.
- **Fits**: fashion, music, agencies, drop/campaign pages. **Fails**: dense product UI; a11y at extreme scale/crop; loud-but-empty if the copy is generic.

---

## B. AI-SLOP FINGERPRINTS (26) — detect before generating, verify after

| # | Fingerprint | Detection test (HTML/CSS/JS) | Why it reads generic |
|---|---|---|---|
| 1 | Inter/Roboto/system-ui as the only family | `grep -i "font-family"` returns one family and it's Inter/Roboto/system-ui; `document.fonts` shows no custom face loaded | "A font no one chose"; training-data average |
| 2 | Indigo→purple gradient hero/CTA/glow | `grep -Ei "6366f1\|8b5cf6\|7c3aed\|a855f7\|from-indigo\|violet-"`; diagonal `linear-gradient` on hero/buttons | Tailwind's accidental default flooded training data ("vibecode purple") |
| 3 | Gradient-clipped headline text | `-webkit-background-clip:text` + `background-image:linear-gradient` on h1/h2 | Decorative rainbow replaces hierarchy; legibility sacrificed |
| 4 | Dark mode = #0a0a0a/#0f172a + one neon accent | body bg ∈ {#000,#0a0a0a,#0f172a,#111827}, exactly one saturated hue, no midtones/warm blacks | "Dark" treated as a colour, not a system |
| 5 | Identical soft shadow on every card | ≥5 `box-shadow` occurrences, all blur 8–24px/opacity ~0.1/`shadow-lg\|xl`; no distinct elevation roles | Decorative depth, not an elevation system |
| 6 | rounded-2xl on everything | `border-radius: 12–16px` (or tailwind `rounded-2xl`) on buttons+cards+inputs+images; ≤2 distinct radius values page-wide | No sharp/soft contrast — nothing is ever deliberately sharp |
| 7 | Exactly three equal feature cards | `grid-template-columns:repeat(3,1fr)` with exactly 3 card children right after the hero | The most-copied macrostructure |
| 8 | Lucide icon in a rounded square per card | repeated 24px `stroke="currentColor"` svg in a padded/rounded div; icons = zap/shield/sparkles | Placeholder iconography; "Sparkles" for anything AI |
| 9 | Emoji as icons/bullets | unicode emoji ranges (✨🚀⚡🎯) in headings, list bullets, buttons | Unearned playfulness; breaks the font system |
| 10 | "Now in beta" pill over the hero headline | small `border-radius:9999px` span with tracked micro-text immediately before h1, centred | Copied hero scaffold |
| 11 | Centred hero stack: eyebrow → 64px h1 → subhead → 2 CTAs | container ~768px, `text-align:center`, h1 clamp 60–72px, filled+ghost button pair | The single most-copied macrostructure |
| 12 | Glassmorphism by default | `backdrop-filter: blur()` + `rgba(255,255,255,.1)` bg + `.2` border on a panel containing body text | Frosted for no reason; fake material |
| 13 | Blob/mesh/aurora/"dot-grid" backgrounds | `filter:blur(60–120px)` on absolutely-positioned gradient circles; repeating radial-gradient dot field | Atmosphere that signifies nothing |
| 14 | Cream + amber "warm" second-wave palette | bg ∈ {#faf8f4,#f5f0e8} + amber/stone accent + Inter body | The new purple — "warm" converged just as hard |
| 15 | Grey body text below contrast | body text lightness >45% on white (#6b7280, #9ca3af); contrast <4.5:1 | Hierarchy via wimpy grey instead of size/weight/space |
| 16 | Cards nested in cards (3–5 deep) | count ancestor chain of bg+border+radius+padding: `.card > .card > .card` | The most recognizable AI UI signature |
| 17 | Coloured-left-border callout boxes | `border-left: 2–4px` + tinted bg, repeated ≥2, hues uncoordinated with brand | Traffic-light alerts standing in for a design system |
| 18 | Uniform 8px spacing; identical section padding | ≤3 distinct padding values; every section `py-24`-equivalent; one gap everywhere | Template rhythm; no editorial pacing (compress/expand) |
| 19 | shadcn defaults shipped as-is | CSS vars `--primary: 221.2 83.2% 53.3%` (blue-600), `--radius:.5rem`, slate/zinc neutrals | Library defaults, zero customisation |
| 20 | "Trusted by" logo bar with grey fake logos | row of 4–6 monochrome svg wordmarks at opacity ~0.5, unlinked, post-hero | Social-proof theatre, never actually trusted by anyone |
| 21 | Invented stat row (10×, 99.9%) | three number+label pairs; numbers round and absent from any copy/source | Borrowed credibility without a source |
| 22 | No imagery, or suspiciously smooth synthetic imagery | zero raster assets in hero; or uniformly smooth 3D blobs/clay characters/mesh gradients | Signals no real product, team, or art direction |
| 23 | Fade-up on everything | one `@keyframes` translateY(8–16px)+opacity applied to every section via IO; no other motion vocabulary | Motion as uniform decoration, not communication |
| 24 | Theme toggle on a marketing page | `localStorage.getItem('theme')` + sun/moon in nav of a landing page | Dark mode as virtue signal, not product need |
| 25 | Glowing status dot + "All systems operational" | pulsing `.dot` with green #22c55e + box-shadow glow | Ornamental liveness gone product-wide |
| 26 | Gradient-border "AI card" glow | `border:1px solid transparent` + double `background-clip: padding-box,border-box` gradient border; hover glow lift | The 2024–26 "premium AI" template |

Top offenders by community consensus: #2, #1, #7, #11, #4, #12 (purple gradient > Inter > three cards > centred hero > slate-900 dark > glass). Rule: any single item can be a legitimate choice; ≥4 in one page (especially 2+1+7+11 together) = slop.

---

## C. COHERENCE RULES

**C1 · What varies independently (seed knobs) vs what the direction owns**
- Direction owns: grid/layout paradigm, type class, radius/material language, motion feel, imagery genre. Do NOT re-roll these per section.
- Seed varies orthogonally: accent hue within the direction's logic (e.g. Swiss red→black-only for one seed), light/dark inversion where the direction supports both, density ±1 step, odd/even rhythm choices, imagery subject, micro-copy voice.
- Typeface substitution allowed only within the same class (two grotesques ≠ Didone + grotesque) and must swap display AND body consistently.

**C2 · Conflicts — resolve deliberately; never average two registers**
Mixing two directions is only legal role-scoped (one framing device, one data module), never systemic. Default resolutions:
- Material: hard offset shadows (D06) vs glass/vibrancy (D16/D18/D19), and grain/halftone (D13/D14/D21) vs engineering hairlines (D01/D10) — pick ONE surface logic for the page; the other may appear once, as a single element (one modal, one panel), never as page chrome.
- Type register: mono-everything (D08/D09) vs display-serif (D02/D04/D11) — if mixed, mono stays a data voice; dark inversions of D02/D04 must keep Didones display-size with weight compensation.
- Motion: springy (D15), unhurried 400–800ms (D04), instant (D08/D09) — the page gets ONE easing character; 30–80ms component state feedback is exempt.
- Luxury register: ornament rhythm (D11) vs omission (D04) — choose one; averaging yields "luxury dark", i.e. second-order slop.
- Density: tables inside slow-living layouts (D04/D05) live in a data island with its own treatment; never blended inline.

**C3 · Neighbours — disambiguate before seeding**
- Quiet family: D04 vs D05 vs D02. Differentiators: D04 = metallic accent + narrow centred column + 2–4px radius; D05 = warm earth tones + no cool accent + photo bands; D02 = editorial asymmetry + huge display serif + captions. Never blend two of these.
- Dark family: D19 vs D08 vs D09 vs D17. D19 = product density + soft radii + one tint; D08/D09 = mono, 0 radius, semantic-only colour; D17 = era collage + grid sun.
- Retro family: D12 vs D13 vs D15 vs D16 vs D17 — separated by palette system, geometry (curve vs blob vs grid), and motion; at most one per batch.
- Print family: D14 vs D21 vs D03 vs D02 — separated by ink system (spot overprint vs sepia plate vs column rules vs asymmetric spread).

**C4 · Seeding algorithm (for the skill)**
1. Pick ONE direction; refuse ambiguous hybrids.
2. Draw an accent from that direction's allowed logic; verify against section B (no fingerprint #2/#14 by accident).
3. Set type from the class list; load ≤2 families + ≤1 mono; prefer free alts: New Haas→Instrument Sans/Archivo, Druk→Archivo Black/Anton, Tiempos→Source Serif 4/Newsreader, Canela→Cormorant/DM Serif, SF Pro→system stack with `-apple-system`, Söhne→Instrument Sans/Schibsted Grotesk. Space Grotesk allowed ONLY in D06/D08 contexts (it is otherwise a tell).
4. Set density + radius + motion from the direction, not per-section.
5. Write copy in the direction's voice (news headline ≠ CLI man-page ≠ fashion statement).
6. Batch diversity: at most one prototype per family (C3) in each generation run; vary orthogonal knobs across runs.
7. Post-check: run section B; ≥3 hits → regenerate that dimension; also check second-order slop (cream+Playfair+gold, false distress, chrome-on-everything).
8. Motion budget: ≤2 behaviours per page + `prefers-reduced-motion` path; easing character comes from the direction.

**C5 · Failure-mode audit (per direction, condensed)**
- Cheap most often when: D01 grid-as-decoration; D02/D04 stock photos; D05 Inter body; D06 softened shadows; D08/D09 small low-contrast mono; D10 opacity overdrive; D11 sans body; D12 flat-SaaS bolt-on; D13 over-saturation; D14 fake distress; D15 timid clash; D16 unstable contrast; D17 magenta-on-cyan; D18 fake window chrome; D19 glow+purple (default slop regression); D20 parody math; D21 sepia-everything; D22 generic loud copy.
