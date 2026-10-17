# Design Directions Catalog — 22 directions (closed system)

The seed picks **exactly ONE** direction from this catalog, then varies only the
orthogonal knobs described in `references/seed-algorithm.md`. Directions are
closed systems: mixing two registers is never averaged (see **Families and
neighbours** below, and coherence rules C1–C5 in
`docs/research/directions-draft.md`).

**How this document is read.** The 22 prose sections (`D01` … `D22`, each opening
with a `### D<nn> · <name>` heading) are the source of truth for the generator: type, colour logic, layout, density, shape,
motion, imagery, fits, fails, failure modes and forbidden moves. The machine
block between `<!-- CATALOG_JSON_START -->` and `<!-- CATALOG_JSON_END -->` is the
same catalog for scripts: it carries `id`, `name`, `family`, `fits`, `fails`,
`forbidden_moves`, `type{display,body,mono,fallback_stack}`, `palette_logic`,
`density`, `motion`, `voice`, `imagery_options`, `inversion_allowed` and
`system_font_first`. Both halves always describe the same 22 ids and names.

**Type rules.** At most 2 families plus at most 1 mono per page. A fallback stack
of the **same class** is mandatory in every direction, because the prototype must
survive going offline: every Google font below is paired with a locally installed
face of the same class (e.g. `Cormorant` → `Georgia, 'Times New Roman', serif`).
A typeface substitution is only legal inside the same class, and it must swap
display *and* body consistently.

**Fails.** `fails` entries are also the tags consumed by the domain filter: a
direction is excluded when any tag is a case-insensitive substring of the
declared `--domain`. Tags are therefore short and literal (e.g. `dense tables`).

## Machine block

<!-- CATALOG_JSON_START -->
[
  {
    "id": "D01",
    "name": "Swiss International",
    "family": "print",
    "fits": [
      "docs",
      "design systems",
      "transport and logistics",
      "portfolios"
    ],
    "fails": [
      "gridlines drawn but nothing aligned to them",
      "warm or humorous brands",
      "undeliberate default sans that collapses into generic clean saas"
    ],
    "forbidden_moves": [
      "gradients, tints or any colour field",
      "rounded corners or drop shadows",
      "centred hero stacks",
      "display type larger than the grid allows",
      "two sans families pretending to be one"
    ],
    "type": {
      "display": "Instrument Sans / Archivo, neo-grotesque, 2-3 sizes per page",
      "body": "the same neo-grotesque at reading size, flush left ragged right",
      "mono": "IBM Plex Mono for tabular data and captions",
      "fallback_stack": "Helvetica Neue, Helvetica, Arial, sans-serif"
    },
    "palette_logic": "black on white plus ONE red (#E60000) as warning or emphasis, never as a field; no tints, no gradients; colour never carries hierarchy",
    "density": "medium - 8pt modular grid, asymmetric columns, hierarchy by size and position, deliberate whitespace",
    "motion": "a cut: instant state change, at most one wipe; no easing flourishes",
    "voice": "neutral and declarative, third person; labels and captions, no adjectives of enthusiasm",
    "imagery_options": [
      "documentary black and white photograph pinned to the grid",
      "typographic specimen",
      "wayfinding glyph set"
    ],
    "inversion_allowed": false,
    "system_font_first": false
  },
  {
    "id": "D02",
    "name": "Editorial Luxe",
    "family": "editorial",
    "fits": [
      "fashion",
      "fragrance",
      "hospitality",
      "premium editorial"
    ],
    "fails": [
      "stock photography",
      "dense product ui",
      "app dashboards",
      "captions and headlines that fail a11y contrast when clamped wrong"
    ],
    "forbidden_moves": [
      "stock photography",
      "card grids or rounded panels",
      "bright web accents",
      "more than one display size jump per screen",
      "centred symmetry across the whole page"
    ],
    "type": {
      "display": "Bodoni Moda / Playfair Display, Didone, 56-96px, often one italic word",
      "body": "Newsreader / Source Serif 4 text serif",
      "mono": "IBM Plex Mono for captions, credits and credits lines",
      "fallback_stack": "Didot, 'Bodoni MT', Georgia, 'Times New Roman', serif"
    },
    "palette_logic": "quiet - oxblood, stone and sumi ink on paper (#F4F1EA); one accent at most; colour never competes with images",
    "density": "low to medium - asymmetric 5fr/7fr spreads, headline overlapping tall portrait crops, off-axis captions, deep indents",
    "motion": "slow mask reveals 400-800ms, parallax on imagery only; nothing bounces",
    "voice": "editorial caption voice: short declarative lines, an occasional italic word, no marketing claims",
    "imagery_options": [
      "art-directed tall portrait crops",
      "black and white or muted photography",
      "fabric and detail macros"
    ],
    "inversion_allowed": false,
    "system_font_first": false
  },
  {
    "id": "D03",
    "name": "Broadsheet Newsprint",
    "family": "print",
    "fits": [
      "news",
      "publications",
      "data journalism",
      "institutional homepages"
    ],
    "fails": [
      "consumer apps",
      "luxury brands",
      "multi-column layouts on mobile"
    ],
    "forbidden_moves": [
      "rounded anything",
      "photographic full-bleed heroes",
      "gradient or luminous accents",
      "one giant headline per screen",
      "vertical whitespace as the main device"
    ],
    "type": {
      "display": "Libre Franklin / Franklin Gothic newsy grotesque, wildly varying sizes",
      "body": "Source Serif 4 / Publico-class text serif, italics for bylines",
      "mono": "IBM Plex Mono for tickers and jump lines",
      "fallback_stack": "'Libre Franklin', 'Franklin Gothic Medium', 'Helvetica Neue', Arial, sans-serif"
    },
    "palette_logic": "newsprint off-white (#F5F2EC) plus ink and one masthead red; a reversed dark 'night edition' variant is allowed",
    "density": "high - 5-6 column broadsheet, column rules, dense decks and jump lines, above-the-fold hierarchy",
    "motion": "none; at most a ticker",
    "voice": "news headline voice: active verbs, datelines, bylines, no first person",
    "imagery_options": [
      "black and white halftone photograph",
      "hairline-axis chart",
      "pull-quote box"
    ],
    "inversion_allowed": true,
    "system_font_first": false
  },
  {
    "id": "D04",
    "name": "Quiet Luxury / Stealth Wealth",
    "family": "quiet",
    "fits": [
      "premium retail",
      "hotels",
      "private services",
      "fragrance"
    ],
    "fails": [
      "dense tables",
      "booking and scheduling apps",
      "spreadsheet-like product ui",
      "cream-plus-gold second-order luxe slop"
    ],
    "forbidden_moves": [
      "ornament or logo density",
      "bright fills and saturated accents",
      "drop shadows",
      "more than three metallic accent uses per page",
      "stock smiling people"
    ],
    "type": {
      "display": "Cormorant 300 / Canela-class light high-contrast serif",
      "body": "one neutral companion, wide-tracked uppercase micro-labels, generous leading",
      "mono": "IBM Plex Mono for micro-labels only",
      "fallback_stack": "Georgia, 'Times New Roman', serif"
    },
    "palette_logic": "near-monochrome warm neutrals; ONE muted metallic accent (brass #A08B62) used at most three times per page; no bright fills",
    "density": "very low - narrow single reading column, 80-140px section gaps, centred or calm-symmetric, whitespace is the material",
    "motion": "unhurried 400-800ms fades, zero bounce; the pace of a deep breath",
    "voice": "sparse, restrained, materially specific; one sentence where two would do",
    "imagery_options": [
      "material close-ups (cashmere, brass, leather)",
      "blown-highlight still life",
      "no people, or hands only"
    ],
    "inversion_allowed": false,
    "system_font_first": false
  },
  {
    "id": "D05",
    "name": "Scandinavian Slow-Living",
    "family": "quiet",
    "fits": [
      "lifestyle",
      "wellness",
      "food",
      "indie publishing"
    ],
    "fails": [
      "dense tables",
      "tech and saas product flows",
      "urgent cta funnels",
      "inter body copy that kills the warmth"
    ],
    "forbidden_moves": [
      "cool-toned accents",
      "pure white #FFFFFF surfaces",
      "more than one font weight",
      "hard shadows",
      "high-contrast digital gloss"
    ],
    "type": {
      "display": "DM Serif Display / Spectral transitional serif",
      "body": "DM Sans at weight 400 only, tracked uppercase captions",
      "mono": "IBM Plex Mono for small captions",
      "fallback_stack": "'DM Sans', system-ui, -apple-system, 'Segoe UI', sans-serif"
    },
    "palette_logic": "warm earth system - linen #F3EDE4, parchment, clay, sage #DBDED5, ink #1A1714; no cool accents, no pure white",
    "density": "low - generous air, asymmetric but calm, full-bleed photo bands alternating with text, ~170px vertical section padding",
    "motion": "slow barely-perceptible reveals; photography desaturated about 18% to integrate with the paper",
    "voice": "warm and unhurried, first-person plural, everyday nouns",
    "imagery_options": [
      "soft natural-light objects on surfaces",
      "desaturated lifestyle photography",
      "ceramics and textiles"
    ],
    "inversion_allowed": false,
    "system_font_first": false
  },
  {
    "id": "D06",
    "name": "Neo-brutalism",
    "family": "brutalist",
    "fits": [
      "indie saas",
      "dev tools",
      "event pages",
      "personality brands"
    ],
    "fails": [
      "enterprise",
      "finance",
      "corporate marketing pages"
    ],
    "forbidden_moves": [
      "soft blurred shadows",
      "gradients",
      "photography",
      "border plus shadow plus fill on every node at once",
      "rounded-2xl on everything"
    ],
    "type": {
      "display": "Space Grotesk 700-900 / Archivo Black, heavy grotesque",
      "body": "a deliberately boring grotesque for scannability",
      "mono": "any one bold mono for labels",
      "fallback_stack": "'Archivo Black', 'Arial Black', Impact, sans-serif"
    },
    "palette_logic": "flat saturated fills (lime, canary, hot pink) plus pure black #000; at most one primary and two fills used as blocks; no gradients",
    "density": "medium to high - blocky compartmentalised grid, every element boxed, structure always drawn",
    "motion": "instant and mechanical; press-down translate on active; 0-8px radius and hard offset shadows",
    "voice": "loud and plain-spoken, uppercase labels, one exclamation allowed",
    "imagery_options": [
      "flat chunky vector illustration",
      "sticker and badge seals",
      "no photography"
    ],
    "inversion_allowed": true,
    "system_font_first": false
  },
  {
    "id": "D07",
    "name": "Raw Web / True Brutalism",
    "family": "brutalist",
    "fits": [
      "manifestos",
      "self-hosted tools",
      "anti-marketing products",
      "engineer portfolios"
    ],
    "fails": [
      "consumer products",
      "marketing campaigns",
      "brands that need warmth"
    ],
    "forbidden_moves": [
      "custom webfont loading",
      "border-radius",
      "box-shadow",
      "decorative imagery",
      "layout that implies structure instead of using rules and tables"
    ],
    "type": {
      "display": "UA default serif (Times) used knowingly, or one grotesque",
      "body": "UA default serif, underlined blue links",
      "mono": "platform monospace for code",
      "fallback_stack": "Times, 'Times New Roman', 'Liberation Serif', serif"
    },
    "palette_logic": "white page, black text, classic link blue; at most a <mark> yellow; nothing else",
    "density": "text-dense - single column, default document flow, <hr> dividers, tables for real structure",
    "motion": "none; zero decoration by rule",
    "voice": "blunt, technical, lower-case, no marketing register at all",
    "imagery_options": [
      "none",
      "one unedited image",
      "content carries everything"
    ],
    "inversion_allowed": false,
    "system_font_first": true
  },
  {
    "id": "D08",
    "name": "Terminal / CLI",
    "family": "dark",
    "fits": [
      "dev tools",
      "security",
      "api docs",
      "changelogs"
    ],
    "fails": [
      "non-technical audiences",
      "consumer marketing",
      "retail checkout flows"
    ],
    "forbidden_moves": [
      "frosted glass",
      "rounded cards",
      "photography",
      "more than one phosphor accent",
      "colour used decoratively"
    ],
    "type": {
      "display": "IBM Plex Mono / JetBrains Mono, ONE mono family",
      "body": "the same mono, mostly one size",
      "mono": "same family; VT323 only for CRT variants (Space Grotesk allowed here)",
      "fallback_stack": "'IBM Plex Mono', 'JetBrains Mono', ui-monospace, SFMono-Regular, Menlo, monospace"
    },
    "palette_logic": "shell dark (#0A0A0A-#1A1A1A) plus ONE phosphor accent (green #00FF41 or amber #FFB000) plus two dim levels; ANSI colour reserved for real semantics",
    "density": "high text density - single-column prompt and log rhythm, panels as bordered ASCII cells, content framed as commands and responses",
    "motion": "typing reveals, cursor blink, instant data; all reduced-motion aware",
    "voice": "man-page register: imperative, terse, literal; commands and responses",
    "imagery_options": [
      "ASCII art",
      "box-drawing dividers",
      "status glyphs"
    ],
    "inversion_allowed": false,
    "system_font_first": false
  },
  {
    "id": "D09",
    "name": "Data Control Room",
    "family": "systemic",
    "fits": [
      "fintech",
      "observability",
      "admin consoles",
      "ops tooling"
    ],
    "fails": [
      "marketing pages",
      "consumer onboarding",
      "editorial storytelling",
      "hero-driven landing pages"
    ],
    "forbidden_moves": [
      "oversized hero type",
      "rounded cards",
      "photography",
      "decorative colour",
      "fake CRT nostalgia as costume"
    ],
    "type": {
      "display": "no display role; compact sans labels only",
      "body": "compact sans at 11-13px with micro uppercase labels",
      "mono": "IBM Plex Mono / SF Mono with tabular numerals",
      "fallback_stack": "'IBM Plex Mono', ui-monospace, SFMono-Regular, Menlo, monospace"
    },
    "palette_logic": "graphite and near-black surfaces (or amber #FFB000 on #0A0A0A); semantic green/red/amber plus one cool secondary; zero decoration",
    "density": "very high - rigid pane lattice with 1px seams, fixed columns, summary next to detail, keyboard-first",
    "motion": "updates are instant; a subtle blink on new data only",
    "voice": "operator log: abbreviations, numbers, units, no adjectives",
    "imagery_options": [
      "sparklines",
      "dense data tables",
      "heat and status grids"
    ],
    "inversion_allowed": true,
    "system_font_first": false
  },
  {
    "id": "D10",
    "name": "Blueprint / Schematic",
    "family": "technical",
    "fits": [
      "hardware",
      "dev tools",
      "infrastructure",
      "construction and logistics"
    ],
    "fails": [
      "lifestyle brands",
      "fashion and beauty",
      "retail storefronts"
    ],
    "forbidden_moves": [
      "soft shadows",
      "photography",
      "rounded corners",
      "gradients that read as UI chrome",
      "annotation density past legibility"
    ],
    "type": {
      "display": "condensed sans labels only",
      "body": "technical mono with dimension values as ambient text",
      "mono": "Space Mono / IBM Plex Mono",
      "fallback_stack": "'Space Mono', 'IBM Plex Mono', ui-monospace, monospace"
    },
    "palette_logic": "Prussian/navy field with cyan linework (#0A1628 background, #1A3A5C grid, #00E5FF highlights) or a reversed white-blue; annotation red and approval green for status only",
    "density": "high info density - visible graph-paper substrate at 5-8% opacity, corner brackets instead of borders, crosshairs, dimension callouts, title-block footer",
    "motion": "draw-on line tracing and a scanline sweep; nothing bounces or sparkles",
    "voice": "spec-sheet voice: part numbers, tolerances, units, imperative notes",
    "imagery_options": [
      "exploded technical views",
      "wireframes",
      "crop marks"
    ],
    "inversion_allowed": true,
    "system_font_first": false
  },
  {
    "id": "D11",
    "name": "Art Deco",
    "family": "luxe",
    "fits": [
      "hospitality",
      "spirits",
      "events",
      "premium launches"
    ],
    "fails": [
      "dense product ui",
      "playful youth brands",
      "technical documentation"
    ],
    "forbidden_moves": [
      "sans-serif body copy",
      "a second accent colour",
      "photographic heroes",
      "interior page asymmetry",
      "gold on gold contrast failures"
    ],
    "type": {
      "display": "Cinzel / Poiret One geometric all-caps, tracked at least 0.15em",
      "body": "small-caps serif or a quiet grotesque at reading weight",
      "mono": "no mono role",
      "fallback_stack": "'Cinzel', 'Trajan Pro', Georgia, serif"
    },
    "palette_logic": "void black or ivory cream plus ONE gold (#C9A84C) with opacity steps; jewel tones only as rare fields; a second accent breaks the spell",
    "density": "medium and ceremonial - symmetric centred compositions, double-border frames inset about 5px, fan/sunburst/chevron/diamond motifs, deco-rule dividers",
    "motion": "cinematic 400ms+ fades, optional gold shimmer; no bounce",
    "voice": "ceremonial and formal: 'presenting', 'since', 'the collection'",
    "imagery_options": [
      "monogram and graphic ornament",
      "silhouettes",
      "rare, heavily toned photography"
    ],
    "inversion_allowed": true,
    "system_font_first": false
  },
  {
    "id": "D12",
    "name": "Space Age / Retro-Futurism",
    "family": "retro",
    "fits": [
      "playful product launches",
      "music and events",
      "food and beverage",
      "games"
    ],
    "fails": [
      "enterprise software",
      "fintech",
      "serious documentation"
    ],
    "forbidden_moves": [
      "flat saas components with a retro sticker bolted on",
      "chrome text at reading sizes",
      "hard 1px borders",
      "grey stock photography"
    ],
    "type": {
      "display": "Jost / Futura-like geometric display, wide-tracked caps",
      "body": "clean grotesque, occasional script accent",
      "mono": "no mono role",
      "fallback_stack": "'Jost', Futura, 'Century Gothic', 'Avenir Next', sans-serif"
    },
    "palette_logic": "1960s print palette (cream, burnt orange, teal) or chrome plus pastels; sunburst gradients allowed as scenic imagery only, never as UI chrome",
    "density": "medium poster density - capsules, boomerangs, orbital compositions, off-centre heroes, dotted star fields",
    "motion": "pills with huge 24-999px radii, floating drift and slow orbits, optimistic easing",
    "voice": "optimistic pitch grounded in concrete nouns: 'the future of', 'journey'",
    "imagery_options": [
      "starbursts and atomic dots",
      "halftone space scenes",
      "rayguns and checkered patterns"
    ],
    "inversion_allowed": true,
    "system_font_first": false
  },
  {
    "id": "D13",
    "name": "Analog 70s / Groovy",
    "family": "retro",
    "fits": [
      "food and beverage",
      "music",
      "lifestyle",
      "community apps"
    ],
    "fails": [
      "b2b software",
      "technical or table ui",
      "enterprise dashboards"
    ],
    "forbidden_moves": [
      "cool-toned colours",
      "crisp digital shadows",
      "thin geometric type",
      "over-saturated vintage effects applied uniformly"
    ],
    "type": {
      "display": "Fraunces / Cooper Black-class fat groovy serif, arc-set headlines",
      "body": "warm serif or warm sans",
      "mono": "no mono role",
      "fallback_stack": "'Fraunces', 'Cooper Black', Georgia, serif"
    },
    "palette_logic": "burnt orange, harvest gold, avocado and chocolate on cream with airbrush halos and a grain overlay; nothing cool-toned",
    "density": "medium and cosy - stacked arcing headlines, radial compositions, badges and seals, striped borders",
    "motion": "warm bounces and slow spins; static grain texture",
    "voice": "friendly and conversational, exclamation tolerated, product as friend",
    "imagery_options": [
      "airbrush illustration",
      "mushrooms, rainbows and suns",
      "textured paper"
    ],
    "inversion_allowed": false,
    "system_font_first": false
  },
  {
    "id": "D14",
    "name": "Risograph / Zine",
    "family": "print",
    "fits": [
      "indie publishing",
      "music",
      "art events",
      "community organisations"
    ],
    "fails": [
      "enterprise and finance",
      "dense product ui",
      "luxury retail"
    ],
    "forbidden_moves": [
      "fake distress (torn paper, stains)",
      "crisp digital drop shadows",
      "more than three spot inks",
      "perfect registration everywhere"
    ],
    "type": {
      "display": "Bowlby One-class ultra-heavy poster display, cropped or overlapped on purpose",
      "body": "mono for listings; titles printed in the second ink",
      "mono": "Space Mono / IBM Plex Mono",
      "fallback_stack": "'Bowlby One SC', 'Arial Black', Impact, sans-serif"
    },
    "palette_logic": "two to three spot inks (fluoro pink, federal blue, sunflower - e.g. #F237A1 / #2C40A7) overprinting via mix-blend-mode: multiply; kraft base #F2EDE4; grain 4-10%",
    "density": "medium to high - poster collage, rotated bands, sticker blocks, programme listings, registration crosshairs kept",
    "motion": "1-3px layer offsets as misregistration, pixel reveals, marquees, displacement hovers",
    "voice": "DIY and exclamatory; programme listings mixed with slogans",
    "imagery_options": [
      "duotone and screened photographs",
      "halftone dots",
      "cut-and-paste collage"
    ],
    "inversion_allowed": false,
    "system_font_first": false
  },
  {
    "id": "D15",
    "name": "Memphis / Playful Toy",
    "family": "playful",
    "fits": [
      "kids and education",
      "games",
      "events",
      "creative tools"
    ],
    "fails": [
      "enterprise",
      "finance",
      "compliance-heavy products"
    ],
    "forbidden_moves": [
      "timid clash (one pastel shape in a clean layout)",
      "decoration without hierarchy",
      "stock photography",
      "flat single-hue palettes"
    ],
    "type": {
      "display": "quirky geometric sans, allowed to clash with a chunky serif",
      "body": "readable grotesque; squiggles and arrows where icons would be",
      "mono": "no mono role",
      "fallback_stack": "'Rubik', 'Trebuchet MS', Verdana, sans-serif"
    },
    "palette_logic": "primary-ish brights plus black and white patterns (terrazzo, squiggle, confetti, checker); clashing by design but capped at four or five hues",
    "density": "medium and scattered - loud islands in whitespace, asymmetric playful placements, diagonal energy",
    "motion": "springy bouncy easings, hover wiggles, floating shapes",
    "voice": "playful and direct, verbs first, second person",
    "imagery_options": [
      "flat vector doodads",
      "plastic-laminate texture",
      "sticker sheets"
    ],
    "inversion_allowed": true,
    "system_font_first": false
  },
  {
    "id": "D16",
    "name": "Y2K Gloss",
    "family": "retro",
    "fits": [
      "music",
      "streetwear",
      "clubs and events",
      "youth brands"
    ],
    "fails": [
      "enterprise",
      "finance",
      "accessibility-critical products",
      "serious documentation"
    ],
    "forbidden_moves": [
      "holographic or gloss text at reading sizes",
      "default glassmorphism without chrome specificity",
      "soft corporate shadows",
      "flat matte surfaces everywhere"
    ],
    "type": {
      "display": "Michroma / wide techy sans, liquid or outlined, bubbly headings",
      "body": "clean small sans",
      "mono": "no mono role",
      "fallback_stack": "'Michroma', 'Eurostile', 'Arial Black', sans-serif"
    },
    "palette_logic": "chrome silver gradients (#C0C0C0 family), electric blue, hot pink #FF1493, lime; iridescent accents on a dark or neutral base",
    "density": "low to medium, maximal surfaces - glossy pill buttons with highlight bands, frosted panels, 24px+ radii, star sparkles, faux window frames",
    "motion": "gloss highlight sweeps, shimmer on hover, sparkle particles",
    "voice": "hyper and abbreviated: 'now', 'new!', period slang allowed",
    "imagery_options": [
      "chrome blobs",
      "early-3D renders",
      "CDs, flip phones, butterflies"
    ],
    "inversion_allowed": true,
    "system_font_first": false
  },
  {
    "id": "D17",
    "name": "Vaporwave / Synthwave Grid",
    "family": "retro",
    "fits": [
      "music",
      "games",
      "streaming overlays",
      "niche community"
    ],
    "fails": [
      "serious products",
      "enterprise dashboards",
      "accessibility-critical flows"
    ],
    "forbidden_moves": [
      "magenta text on cyan at any size",
      "the joke outliving the content",
      "motion without a reduced-motion path",
      "era collisions that mean nothing"
    ],
    "type": {
      "display": "80s display faces plus bitmap/pixel cuts; fullwidth ornament type",
      "body": "ordinary quiet type in the product area",
      "mono": "bitmap or pixel mono for ornament",
      "fallback_stack": "'Audiowide', 'Trebuchet MS', sans-serif"
    },
    "palette_logic": "neon pink #FF71CE, cyan #01CDFE, violet and a sunset gradient with striped sun; perspective grid lines in cyan and pink",
    "density": "low to medium - a cinematic hero (sun plus grid horizon) then a deliberately quiet product area in ordinary type",
    "motion": "slow pans, scanline flicker, glitch on hover; reduced-motion path mandatory",
    "voice": "ironic and wistful; katakana and fullwidth type are decoration, not readable content",
    "imagery_options": [
      "Greco-Roman busts",
      "palms and VHS artefacts",
      "Windows 95 chrome"
    ],
    "inversion_allowed": false,
    "system_font_first": false
  },
  {
    "id": "D18",
    "name": "macOS Native",
    "family": "systemic",
    "fits": [
      "desktop-first tools",
      "pro utility web demos",
      "dense dashboards"
    ],
    "fails": [
      "marketing pages",
      "consumer landing pages",
      "mobile-first web apps"
    ],
    "forbidden_moves": [
      "fake macOS window chrome as a marketing frame",
      "Inter instead of the system face",
      "card borders on content",
      "shadows over a material",
      "emoji as icons"
    ],
    "type": {
      "display": "SF Pro with optical sizing, never disabled",
      "body": "SF Pro at 11-17px desktop scale",
      "mono": "SF Mono for data; New York for documents",
      "fallback_stack": "-apple-system, BlinkMacSystemFont, system-ui, 'Helvetica Neue', sans-serif"
    },
    "palette_logic": "system grays plus ONE system tint per surface, as accent not fill; vibrancy (alpha plus backdrop blur) instead of solid chrome fills; never pure black",
    "density": "dense but comfortable - sidebar 240-320px, toolbar, content split views, 8pt spacing, rows at least 28pt, keyboard navigable",
    "motion": "0.2-0.3s standard easings; 6-12px radii; materials replace borders and shadows",
    "voice": "utility copy: labels, verbs, affordances, sentence case, no exclamation",
    "imagery_options": [
      "SF Symbols",
      "album-art-like imagery",
      "no borders on content"
    ],
    "inversion_allowed": true,
    "system_font_first": true
  },
  {
    "id": "D19",
    "name": "Instrument Dark",
    "family": "dark",
    "fits": [
      "dev tools",
      "infrastructure",
      "productivity"
    ],
    "fails": [
      "marketing-heavy brands",
      "consumer social",
      "print-like editorial"
    ],
    "forbidden_moves": [
      "purple gradient glow",
      "glass cards",
      "glow spam",
      "oversized hero type",
      "stock people"
    ],
    "type": {
      "display": "Instrument Sans / Schibsted Grotesk with tight display tracking",
      "body": "the same grotesque; kbd chips for shortcuts",
      "mono": "one mono data voice",
      "fallback_stack": "'Instrument Sans', 'Helvetica Neue', Arial, sans-serif"
    },
    "palette_logic": "layered graphite - base #0B0C0E, elevated #16181C, hairline #262A31 - not one black plus neon; ONE non-purple accent; semantics via icon plus colour",
    "density": "high - product-first: dense lists, command menu, keyboard hints, small or absent hero, 1px low-alpha borders define geometry",
    "motion": "120-200ms transitions with a subtle spring; staggered list reveals only",
    "voice": "precise and terse; feature verbs, no adjectives, shortcut-first",
    "imagery_options": [
      "product screenshots",
      "diagram ghosts",
      "no stock people"
    ],
    "inversion_allowed": false,
    "system_font_first": false
  },
  {
    "id": "D20",
    "name": "Academic Preprint",
    "family": "technical",
    "fits": [
      "research tools",
      "ml products",
      "databases",
      "technical essays"
    ],
    "fails": [
      "consumer products",
      "retail",
      "playful marketing"
    ],
    "forbidden_moves": [
      "fake greeked math as parody",
      "two-column layout on mobile",
      "rounded cards",
      "decorative gradients",
      "brand ornaments"
    ],
    "type": {
      "display": "Latin Modern Roman / Computer Modern, math as legitimate ornament",
      "body": "Latin Modern or Charter / STIX, italic theorem voice, footnote-grade labels",
      "mono": "one mono for code and listings",
      "fallback_stack": "'Latin Modern Roman', 'STIX Two Text', Georgia, 'Times New Roman', serif"
    },
    "palette_logic": "black on white, one link blue; red strictly for editorial comments; no brand decoration",
    "density": "high text density, medium air - single-column measure for narrative, two columns for lists and tables, numbered sections, footnotes as marginalia, booktabs-style tables",
    "motion": "none - rules are section breaks; no radius, no shadows, no animation",
    "voice": "theorem-and-proof register: 'we show', 'Figure 1:', hedged claims",
    "imagery_options": [
      "captioned figures",
      "TikZ-aesthetic diagrams",
      "plots with hairline axes"
    ],
    "inversion_allowed": false,
    "system_font_first": false
  },
  {
    "id": "D21",
    "name": "Field Guide / Naturalist",
    "family": "print",
    "fits": [
      "outdoors",
      "food and provisions",
      "botanical skincare",
      "museums and education"
    ],
    "fails": [
      "tech and saas",
      "enterprise dashboards",
      "dense product ui"
    ],
    "forbidden_moves": [
      "stock photography in sepia",
      "texture without a grid underneath",
      "screen-bright hues",
      "modern soft shadows",
      "rounded cards"
    ],
    "type": {
      "display": "EB Garamond / Source Serif old-style, italics for taxonomy",
      "body": "EB Garamond, small caps for labels, hand-annotated feel allowed",
      "mono": "no mono role",
      "fallback_stack": "'EB Garamond', 'Adobe Garamond Pro', Garamond, Georgia, serif"
    },
    "palette_logic": "aged paper #EFE7D8, sepia ink, muted botanicals (sage, ochre, madder); duotone plates; no screen-bright hues",
    "density": "medium and curated - framed specimen plates with numbers and labels, margin notes, index lists, caption bands",
    "motion": "0 radius with thin double borders or corner ticks; crossfades only; nothing modern-feeling moves",
    "voice": "naturalist label voice: latin binomials in italics, precise nouns, observation",
    "imagery_options": [
      "scientific illustration and engravings",
      "maps",
      "specimen photos with scale bars"
    ],
    "inversion_allowed": false,
    "system_font_first": false
  },
  {
    "id": "D22",
    "name": "Fashion Type-First",
    "family": "editorial",
    "fits": [
      "fashion",
      "music",
      "agencies",
      "drop and campaign pages"
    ],
    "fails": [
      "dense product ui",
      "forms and checkout flows",
      "accessibility-critical interfaces"
    ],
    "forbidden_moves": [
      "clip-art",
      "loud-but-empty copy",
      "rounded corners",
      "shadows",
      "small timid type"
    ],
    "type": {
      "display": "Anton / Archivo Black condensed grotesque at 10-20vw, cropped and overlapping",
      "body": "tiny neutral sans",
      "mono": "no mono role",
      "fallback_stack": "'Anton', 'Archivo Black', Impact, 'Arial Narrow', sans-serif"
    },
    "palette_logic": "high-contrast duotone (black and white plus one hot accent such as Klein blue or signal red) or monochrome; imagery black and white duotoned with grain",
    "density": "polarised - heroes maximal and full-bleed, lists minimal, poster stacking, marquees",
    "motion": "marquee scrolls, mask reveals, fast cuts",
    "voice": "statement and slogan: one line, imperative, no explanation",
    "imagery_options": [
      "art-directed blown-out or duotone photography",
      "grain",
      "edge-to-edge crops"
    ],
    "inversion_allowed": true,
    "system_font_first": false
  }
]
<!-- CATALOG_JSON_END -->

---

## Directions

### D01 · Swiss International — the grid is the argument; neutrality is a stance

- **Type** — one neo-grotesque: Instrument Sans or Archivo (free alternatives to
  Helvetica Now / Neue Haas), Univers as the reference. 2–3 sizes per page max,
  flush-left ragged-right, baseline rhythm. Mono: IBM Plex Mono for tabular data
  and captions. **Fallback stack**: `Helvetica Neue, Helvetica, Arial, sans-serif`.
- **Color** — black on white plus ONE red (#E60000) as warning or emphasis, never
  as a field; no tints, no gradients; colour never carries hierarchy.
- **Layout** — 8pt modular grid, asymmetric columns, hierarchy via size and
  position only; medium density with ruthless, deliberate whitespace.
- **Density** — medium; the whitespace is composed, never leftover.
- **Shape** — 0 radius; 1px hairlines ARE the structure; no shadows.
- **Motion** — a cut (instant), at most one wipe.
- **Imagery** — documentary black and white photo pinned to the grid;
  illustration is avoided on principle.
- **Fits** — docs, design systems, transport and logistics, portfolios.
- **Fails** — gridlines drawn but nothing aligned to them; warm or humorous
  brands; an undeliberate default sans that collapses the page into generic
  clean SaaS.
- **Failure modes** — grid-as-decoration is the classic tell: rulers, ticks and
  column rules that no element actually obeys. The fix is to make one visible
  alignment the page's argument, not an ornament.
- **Forbidden moves** — gradients, tints or any colour field; rounded corners or
  drop shadows; centred hero stacks; display type larger than the grid allows;
  two sans families pretending to be one.

### D02 · Editorial Luxe — a fashion spread: type at scale, air around it

- **Type** — Didone display (Bodoni Moda, Playfair Display) at 56–96px, often one
  italic word; text serif for reading (Newsreader, Source Serif 4); tiny tracked
  captions in mono. **Fallback stack**: `Didot, 'Bodoni MT', Georgia, 'Times New Roman', serif`.
- **Color** — quiet: oxblood, stone and sumi ink on paper (#F4F1EA); no
  web-bright accents; colour never competes with images.
- **Layout** — asymmetric spreads (5fr/7fr), headline overlapping tall portrait
  crops, off-axis captions, deep indents, a big display→deck drop.
- **Density** — low to medium.
- **Shape** — 0 radius, no shadows; rules as section breaks.
- **Motion** — slow mask reveals (400–800ms), parallax on imagery only.
- **Imagery** — art-directed tall portrait crops, black and white or muted;
  photography IS the product.
- **Fits** — fashion, fragrance, hospitality, premium editorial.
- **Fails** — stock photography kills it instantly; 10px captions next to 96px
  headlines fail a11y if clamped wrong; wrong for any dense product UI.
- **Failure modes** — the register collapses the moment an image is not
  art-directed, or the display/body contrast is tuned by eye without checking the
  smallest caption's contrast and the largest headline's crop.
- **Forbidden moves** — stock photography; card grids or rounded panels; bright
  web accents; more than one display size jump per screen; centred symmetry
  across the whole page.

### D03 · Broadsheet Newsprint — newspaper front page, taken literally

- **Type** — newsy grotesque headlines (Libre Franklin / Franklin Gothic,
  Helvetica) plus text serif body (Source Serif 4, Publico-class); italics for
  bylines; wildly varying headline sizes. Mono for tickers and jump lines.
  **Fallback stack**: `'Libre Franklin', 'Franklin Gothic Medium', 'Helvetica Neue', Arial, sans-serif`.
- **Color** — newsprint off-white (#F5F2EC) plus ink; one masthead red; a
  reversed dark variant is allowed as a "night edition".
- **Layout** — 5–6 column broadsheet, column rules, dense decks and jump lines,
  "above the fold" hierarchy.
- **Density** — high.
- **Shape** — 0 radius; hairline rules everywhere.
- **Motion** — none (a ticker at most).
- **Imagery** — black and white halftone photos, hairline-axis charts,
  pull-quote boxes.
- **Fits** — news, publications, data journalism, institutional homepages.
- **Fails** — consumer apps; luxury brands; multi-column layouts on mobile
  (columns collapse badly unless deliberately single-column).
- **Failure modes** — importing the grid without the editorial pacing: every
  section at the same weight and the fold stops meaning anything.
- **Forbidden moves** — rounded anything; photographic full-bleed heroes;
  gradient or luminous accents; one giant headline per screen; vertical
  whitespace as the main device.

### D04 · Quiet Luxury / Stealth Wealth — expensive through omission, not ornament

- **Type** — light high-contrast serif display (Cormorant 300, Canela-class) plus
  one neutral companion; wide-tracked uppercase micro-labels; generous leading.
  **Fallback stack**: `Georgia, 'Times New Roman', serif`.
- **Color** — near-monochrome warm neutrals; ONE muted metallic accent (brass
  #A08B62) used at most three times per page; no bright fills.
- **Layout** — narrow single reading column, 80–140px section gaps, centred or
  calm-symmetric.
- **Density** — very low; whitespace is the material.
- **Shape** — 2–4px max radius or none; no shadows; hairline rules.
- **Motion** — unhurried 400–800ms fades, zero bounce; "the pace of a deep
  breath".
- **Imagery** — material close-ups (cashmere, brass, leather), blown highlights,
  no smiling stock people.
- **Fits** — premium retail, hotels, private services, fragrance.
- **Fails** — `dense tables`; booking and scheduling apps; spreadsheet-like
  product UI; and the second-order slop of "cream + Playfair + gold on
  near-black" reduced to a formula without a real material differentiator.
- **Failure modes** — the direction has become its own cliché. It passes only
  when a real material, object or photograph carries the luxury; ornament-free is
  not the same as unconsidered.
- **Forbidden moves** — ornament or logo density; bright fills and saturated
  accents; drop shadows; more than three metallic accent uses per page; stock
  smiling people.

### D05 · Scandinavian Slow-Living — warm paper, soft earth, quiet serif

- **Type** — transitional serif display (DM Serif Display, Spectral) plus
  humanist sans (DM Sans); single weight 400 discipline; tracked uppercase
  captions. **Fallback stack**: `'DM Sans', system-ui, -apple-system, 'Segoe UI', sans-serif`.
- **Color** — warm earth system: linen #F3EDE4, parchment, clay, sage #DBDED5,
  ink #1A1714; no cool accents, no pure white.
- **Layout** — generous air, asymmetric but calm, full-bleed photo bands
  alternating with text; ~170px vertical section padding.
- **Density** — low.
- **Shape** — 0 radius, no shadows; image-only cards.
- **Motion** — slow barely-perceptible reveals; photography desaturated ~18% to
  integrate with the paper.
- **Imagery** — soft natural light, objects on surfaces, no hard shadows, no
  digital gloss.
- **Fits** — lifestyle, wellness, food, indie publishing.
- **Fails** — `dense tables`; tech and SaaS product flows; urgent CTA funnels;
  Inter body copy, which kills the warmth (the classic "almost Kinfolk" tell).
- **Failure modes** — adjacent to D04, so the two must never blend (averaging
  them yields "luxury dark", i.e. second-order slop). Swapping the body face for
  a neutral grotesque is enough to lose the register.
- **Forbidden moves** — cool-toned accents; pure white #FFFFFF surfaces; more
  than one font weight; hard shadows; high-contrast digital gloss.

### D06 · Neo-brutalism — visible structure, hard edges, zero blur

- **Type** — heavy grotesque only (Space Grotesk 700–900, Archivo Black) or bold
  mono; uppercase labels; body deliberately boring for scannability.
  **Fallback stack**: `'Archivo Black', 'Arial Black', Impact, sans-serif`.
- **Color** — flat saturated fills (lime, canary, hot pink) plus pure black #000;
  NO gradients; at most 1 primary and 2 fills, used as blocks.
- **Layout** — blocky compartmentalised grid, every element boxed; structure is
  never implied, always drawn.
- **Density** — medium to high.
- **Shape** — 0–8px radius (pick ONE per project); 2–5px borders; hard offset
  shadows (e.g. `6px 6px 0 #000`); press-down translate on active.
- **Motion** — instant and mechanical.
- **Imagery** — flat chunky illustration, stickers, badge seals; no photography.
- **Fits** — indie SaaS, dev tools, event pages, personality brands.
- **Fails** — enterprise; finance; corporate marketing pages.
- **Failure modes** — softening the shadows turns it into generic playful SaaS;
  border + shadow + fill on every node at once is noise, not structure. Space
  Grotesk is a tell anywhere outside D06/D08 contexts.
- **Forbidden moves** — soft blurred shadows; gradients; photography; border plus
  shadow plus fill on every node at once; `rounded-2xl` on everything.

### D07 · Raw Web / True Brutalism — the document IS the interface

- **Type** — system/UA defaults used knowingly (Times, Verdana) or one grotesque;
  underlined blue links; no custom type load. **Fallback stack**: `Times, 'Times New Roman', 'Liberation Serif', serif`.
  `system_font_first` is true: the UA face is the design, not a degradation.
- **Color** — white page, black text, classic link blue; maybe a `<mark>` yellow;
  nothing else.
- **Layout** — single column, default document flow, `<hr>` dividers, tables for
  real structure.
- **Density** — text-dense.
- **Shape** — no radius, no boxes, no shadows.
- **Motion** — none; zero decoration by rule.
- **Imagery** — none, or one unedited image; content carries everything.
- **Fits** — manifestos, self-hosted tools, anti-marketing products, engineer
  portfolios.
- **Fails** — consumer products; marketing campaigns; brands that need warmth.
- **Failure modes** — reads as laziness when it is not deliberate; default link
  colours often fail contrast audits, so the "no styling" claim still needs a
  contrast pass.
- **Forbidden moves** — custom webfont loading; `border-radius`; `box-shadow`;
  decorative imagery; layout that implies structure instead of using rules and
  tables.

### D08 · Terminal / CLI — command in, output out; monospace discipline

- **Type** — ONE mono family (IBM Plex Mono, JetBrains Mono, Berkeley Mono;
  VT323 only for CRT variants); mostly one size; ASCII dividers and box-drawing
  as ornament. **Fallback stack**: `'IBM Plex Mono', 'JetBrains Mono', ui-monospace, SFMono-Regular, Menlo, monospace`.
- **Color** — shell dark (#0A0A0A–#1A1A1A) plus a single phosphor accent (green
  #00FF41 or amber #FFB000) plus two dim levels; ANSI colours reserved for real
  semantics.
- **Layout** — single-column prompt/log rhythm; panels as bordered ASCII cells;
  content framed as commands and responses.
- **Density** — high text density.
- **Shape** — 0 radius, 1px panel borders, no shadows (a subtle glow is allowed).
- **Motion** — typing reveals, cursor blink, instant data; all reduced-motion
  aware.
- **Imagery** — none: ASCII art, box-drawing, status glyphs.
- **Fits** — dev tools, security, API docs, changelogs.
- **Fails** — non-technical audiences; consumer marketing; retail checkout
  flows.
- **Failure modes** — small green-on-black text below contrast; frosted glass or
  rounded cards mixed in instantly break the register.
- **Forbidden moves** — frosted glass; rounded cards; photography; more than one
  phosphor accent; colour used decoratively.

### D09 · Data Control Room — dense scans under pressure; panes, not cards

- **Type** — mono tabular numerals (IBM Plex Mono, SF Mono) plus a compact sans;
  11–13px data, micro uppercase labels; no oversized hero text ever.
  **Fallback stack**: `'IBM Plex Mono', ui-monospace, SFMono-Regular, Menlo, monospace`.
- **Color** — graphite/near-black surfaces (or amber #FFB000 on #0A0A0A variant);
  semantic only (green/red/amber) plus one cool secondary; zero decoration.
- **Layout** — rigid pane lattice with 1px seams, fixed columns,
  summary→detail adjacency, keyboard-first.
- **Density** — very high.
- **Shape** — 0 radius, flat panes, borders do hierarchy, no shadows.
- **Motion** — updates are instant; subtle blink on new data only.
- **Imagery** — data as imagery: sparklines, dense tables, no photography.
- **Fits** — fintech, observability, admin consoles, ops tooling.
- **Fails** — marketing pages; consumer onboarding; editorial storytelling;
  hero-driven landing pages.
- **Failure modes** — fake-CRT nostalgia as costume; a pane lattice that is not
  actually fixed-column, so the eye cannot build a scan path.
- **Forbidden moves** — oversized hero type; rounded cards; photography;
  decorative colour; fake CRT nostalgia as costume.

### D10 · Blueprint / Schematic — the technical drawing about the product IS the page

- **Type** — technical mono (Space Mono, IBM Plex Mono) plus condensed sans
  labels; dimension values as ambient text everywhere. **Fallback stack**:
  `'Space Mono', 'IBM Plex Mono', ui-monospace, monospace`.
- **Color** — Prussian/navy field with cyan linework (#0A1628 bg, #1A3A5C grid,
  #00E5FF highlights) or reversed white-blue; annotation red plus approval green
  for status.
- **Layout** — visible graph-paper substrate (~5–8% opacity), corner brackets
  instead of borders, crosshairs, dimension callouts, title-block footer.
- **Density** — high info density.
- **Shape** — 0 radius; uniform 1–2px lines, hierarchy by opacity.
- **Motion** — draw-on line tracing and a scanline sweep; nothing bounces or
  sparkles.
- **Imagery** — exploded views, wireframes, crop marks; no photos.
- **Fits** — hardware, dev tools, infrastructure, construction and logistics.
- **Fails** — lifestyle brands; fashion and beauty; retail storefronts.
- **Failure modes** — opacity overdrive: the grid competes with the content, and
  over-annotation becomes noise. Opacity is a hierarchy tool, not a texture.
- **Forbidden moves** — soft shadows; photography; rounded corners; gradients
  that read as UI chrome; annotation density past legibility.

### D11 · Art Deco — machine-age glamour via geometry and gold

- **Type** — geometric all-caps display (Cinzel, Poiret One, Bifur-like),
  wide-tracked (≥0.15em); never in body weight; small-caps labels. **Fallback
  stack**: `'Cinzel', 'Trajan Pro', Georgia, serif`.
- **Color** — void black/ivory cream plus ONE gold (#C9A84C) with opacity steps;
  jewel tones only as rare fields; a second accent breaks the spell.
- **Layout** — symmetric, centred compositions; double-border frames (outer solid
  plus inner faint, inset ~5px); fan/sunburst/chevron/diamond motifs; deco-rule
  dividers.
- **Density** — medium, ceremonial.
- **Shape** — 0 radius; ornament built from CSS geometry.
- **Motion** — cinematic 400ms+ fades, optional gold shimmer; no bounce.
- **Imagery** — monogram/graphic ornament, silhouettes; photography rare and
  toned.
- **Fits** — hospitality, spirits, events, premium launches.
- **Fails** — dense product UI; playful youth brands; technical documentation.
- **Failure modes** — sans-serif body copy erases the period voice; ornament
  density past legibility; gold-on-gold contrast failures.
- **Forbidden moves** — sans-serif body copy; a second accent colour;
  photographic heroes; interior page asymmetry; gold on gold.

### D12 · Space Age / Retro-Futurism — the future as predicted by 1960s optimism

- **Type** — geometric/rounded display (Jost / Futura-like, space-age
  alternates) wide-tracked caps; body in a clean grotesque; occasional script
  accent. **Fallback stack**: `'Jost', Futura, 'Century Gothic', 'Avenir Next', sans-serif`.
- **Color** — 60s print palette (cream, burnt orange, teal) OR chrome plus
  pastels; sunburst gradients allowed as scenic imagery, not UI chrome.
- **Layout** — capsules, boomerangs, orbital compositions, off-centre heroes,
  dotted star fields.
- **Density** — medium, poster-like.
- **Shape** — pills and capsule panels, huge radii (24–999px), no hard borders.
- **Motion** — floating drift and slow orbits; optimistic easing.
- **Imagery** — checkered patterns, starbursts, atomic dots, halftone space
  scenes, rayguns.
- **Fits** — playful product launches, music and events, food and beverage,
  games.
- **Fails** — enterprise software; fintech; serious documentation (a flat-SaaS
  bolt-on is the usual disaster).
- **Failure modes** — retro chrome bolted onto flat SaaS components; chrome text
  used at reading sizes.
- **Forbidden moves** — flat SaaS components with a retro sticker bolted on;
  chrome text at reading sizes; hard 1px borders; grey stock photography.

### D13 · Analog 70s / Groovy — sun-faded print warmth with groovy geometry

- **Type** — fat groovy serif (Fraunces, Cooper Black-class), chunky rounded
  lettering, arc-set headlines; body warm serif or warm sans. **Fallback
  stack**: `'Fraunces', 'Cooper Black', Georgia, serif`.
- **Color** — burnt orange, harvest gold, avocado, chocolate on cream; airbrush
  halos; grain overlay; nothing cool-toned.
- **Layout** — stacked arcing headlines, radial compositions, badges/seals,
  striped borders.
- **Density** — medium, cosy.
- **Shape** — rounded blobs, sticker shapes, big radii.
- **Motion** — warm bounces, slow spins; static grain texture.
- **Imagery** — airbrush illustration, mushrooms/rainbows/suns, textured paper.
- **Fits** — food and beverage, music, lifestyle, community apps.
- **Fails** — B2B software; technical or table UI; enterprise dashboards.
- **Failure modes** — over-saturation and a uniform "vintage theme" effect: the
  grain and glow are applied everywhere instead of being composed.
- **Forbidden moves** — cool-toned colours; crisp digital shadows; thin geometric
  type; over-saturated vintage effects applied uniformly.

### D14 · Risograph / Zine — two ink drums, misregistered, printed not rendered

- **Type** — ultra-heavy poster display (Bowlby One-class) plus mono for
  listings; type often printed in the second ink; titles cropped/overlapped on
  purpose. **Fallback stack**: `'Bowlby One SC', 'Arial Black', Impact, sans-serif`.
- **Color** — 2–3 spot inks (fluoro pink, federal blue, sunflower — e.g. #F237A1
  / #2C40A7) overprinting via `mix-blend-mode: multiply`; kraft/paper base
  #F2EDE4; grain 4–10%.
- **Layout** — poster collage: rotated bands, sticker blocks, programme listings,
  mixed centred/flush-left on purpose; registration crosshairs kept.
- **Density** — medium to high.
- **Shape** — hard edges; 1–3px layer offsets = "misregistration"; offset
  duplicate layers instead of shadows.
- **Motion** — pixel reveals, marquees, displacement hovers.
- **Imagery** — duotone/screened photos, halftone dots, cut-and-paste collage.
- **Fits** — indie publishing, music, art events, community organisations.
- **Fails** — enterprise and finance; dense product UI; luxury retail.
- **Failure modes** — fake distress (torn paper, stains) reads as a filter; crisp
  digital shadows next to overprint break the illusion.
- **Forbidden moves** — fake distress; crisp digital drop shadows; more than
  three spot inks; perfect registration everywhere.

### D15 · Memphis / Playful Toy — 1980s anti-functional play; geometry with jokes

- **Type** — quirky geometric sans plus an allowed clash with a chunky serif;
  squiggles/arrows used where icons would be; all-caps shouts mixed with
  lowercase. **Fallback stack**: `'Rubik', 'Trebuchet MS', Verdana, sans-serif`.
- **Color** — primary-ish brights plus black/white patterns (terrazzo, squiggle,
  confetti, checker); clashing by design but capped at ~4–5 hues.
- **Layout** — asymmetric playful placements, floating shapes, diagonal energy —
  loud islands in whitespace.
- **Density** — medium, scattered.
- **Shape** — circles/triangles/squiggle ribbons, large radii on cards,
  patterned fills.
- **Motion** — springy bouncy easings, hover wiggles.
- **Imagery** — flat vector doodads, plastic-laminate texture, sticker sheets.
- **Fits** — kids and education, games, events, creative tools.
- **Fails** — enterprise; finance; compliance-heavy products.
- **Failure modes** — decoration without hierarchy is noise; done timidly it
  looks like a template with one pastel shape pasted in.
- **Forbidden moves** — timid clash (one pastel shape in a clean layout);
  decoration without hierarchy; stock photography; flat single-hue palettes.

### D16 · Y2K Gloss — millennium optimism; chrome and translucency

- **Type** — stretched/wide techy sans (Michroma); liquid or outlined display;
  "bubbly" headings, clean small text. **Fallback stack**:
  `'Michroma', 'Eurostile', 'Arial Black', sans-serif`.
- **Color** — chrome silver gradients (#C0C0C0 family), electric blue, hot pink
  #FF1493, lime; iridescent/holographic accents on a dark or neutral base.
- **Layout** — glossy pill buttons with highlight bands, frosted panels, bubbly
  24px+ radii, star sparkles, faux window frames.
- **Density** — low to medium, maximal surfaces.
- **Shape** — extreme blobs, chrome borders, gloss highlight sweeps, sparkle
  particles.
- **Motion** — shimmer on hover, shine sweeps.
- **Imagery** — chrome blobs, early-3D renders, CDs, flip phones, butterflies,
  scanner-photo effects.
- **Fits** — music, streetwear, clubs and events, youth brands.
- **Fails** — enterprise; finance; accessibility-critical products (gloss and
  holographic text have no stable contrast); serious documentation.
- **Failure modes** — without chrome/period specificity it degrades into default
  glassmorphism slop; contrast is unstable by construction, so the base surface
  must carry the reading text.
- **Forbidden moves** — holographic or gloss text at reading sizes; default
  glassmorphism without chrome specificity; soft corporate shadows; flat matte
  surfaces everywhere.

### D17 · Vaporwave / Synthwave Grid — ironic mall nostalgia; pink–cyan haze

- **Type** — 80s display faces plus bitmap/pixel cuts; fullwidth "ｖａｐｏｒｗａｖｅ"
  type as ornament; katakana accents (decorative, not readable content).
  **Fallback stack**: `'Audiowide', 'Trebuchet MS', sans-serif`.
- **Color** — neon pink #FF71CE, cyan #01CDFE, violet, sunset gradient with
  striped sun; perspective grid lines in cyan/pink.
- **Layout** — cinematic hero (sun plus grid horizon), then a deliberately QUIET
  product area in ordinary type: loud hero, quiet body.
- **Density** — low to medium.
- **Shape** — 0 radius in the "screen" motifs.
- **Motion** — slow pans, scanline flicker, glitch on hover; reduced-motion path
  mandatory (grid plus flicker are motion-heavy).
- **Imagery** — Greco-Roman busts, palms, VHS artifacts, Windows 95 chrome —
  deliberate era collision.
- **Fits** — music, games, streaming overlays, niche community.
- **Fails** — serious products; enterprise dashboards; accessibility-critical
  flows (magenta-on-cyan is unreadable at any size).
- **Failure modes** — the joke outlives the content; era collisions accumulate
  without meaning; motion without a reduced-motion path.
- **Forbidden moves** — magenta text on cyan at any size; the joke outliving the
  content; motion without a reduced-motion path; era collisions that mean
  nothing.

### D18 · macOS Native — an app that belongs to the OS; materials and restraint

- **Type** — SF Pro with optical sizing (never disabled), SF Mono for data, New
  York for documents; 11–17px desktop scale. **Fallback stack**:
  `-apple-system, BlinkMacSystemFont, system-ui, 'Helvetica Neue', sans-serif`.
  `system_font_first` is true: the platform face is the platform.
- **Color** — system grays plus ONE system tint per surface, as accent not fill;
  vibrancy (alpha + backdrop blur) instead of solid chrome fills; never pure
  black.
- **Layout** — sidebar (240–320px) / toolbar / content split views; 8pt spacing;
  dense-but-comfortable desktop rows (≥28pt targets); keyboard navigable.
- **Density** — dense but comfortable.
- **Shape** — 6–12px radii; materials replace card borders and shadows; don't
  shadow over a material.
- **Motion** — 0.2–0.3s standard easings.
- **Imagery** — SF Symbols (never emoji icons), album-art-like imagery, no card
  borders on content.
- **Fits** — desktop-first tools, pro utility web demos, dense dashboards.
- **Fails** — marketing pages (the platform feel needs real chrome); consumer
  landing pages; mobile-first web apps.
- **Failure modes** — the "fake macOS window" cliché; substituting Inter kills
  the platform instantly; card borders layered over a material.
- **Forbidden moves** — fake macOS window chrome as a marketing frame; Inter
  instead of the system face; card borders on content; shadows over a material;
  emoji as icons.

### D19 · Instrument Dark — precision-instrument dark UI (Linear/Raycast lineage)

- **Type** — one grotesque with tight display tracking (Instrument Sans,
  Schibsted Grotesk as free alternatives to Söhne/Untitled) plus a mono data
  voice; kbd chips for shortcuts. **Fallback stack**:
  `'Instrument Sans', 'Helvetica Neue', Arial, sans-serif`.
- **Color** — layered graphite — base #0B0C0E, elevated #16181C, hairline
  #262A31 — not "one black plus neon"; ONE non-purple accent; semantics via icon
  plus colour.
- **Layout** — product-first: dense lists, command menu, keyboard hints, small or
  absent hero; 1px low-alpha borders define geometry.
- **Density** — high.
- **Shape** — consistent 6–10px radii; no glow spam.
- **Motion** — 120–200ms transitions, subtle spring; staggered list reveals only.
- **Imagery** — product screenshots and diagram ghosts; no stock people.
- **Fits** — dev tools, infrastructure, productivity.
- **Fails** — marketing-heavy brands; consumer social; print-like editorial.
- **Failure modes** — this IS the default LLM dark mode: purple gradient glow
  plus #0f172a plus glass cards regresses to 2019-era slop. Only density,
  restraint and real product specificity redeem it.
- **Forbidden moves** — purple gradient glow; glass cards; glow spam; oversized
  hero type; stock people.

### D20 · Academic Preprint — a paper, taken seriously as an interface

- **Type** — Latin Modern Roman / Computer Modern (or Charter, STIX); italic
  theorem voice; footnote-grade labels; math as legitimate ornament. **Fallback
  stack**: `'Latin Modern Roman', 'STIX Two Text', Georgia, 'Times New Roman', serif`.
- **Color** — black on white; one link blue; red strictly for editorial comments;
  no brand decoration.
- **Layout** — single-column reading measure for narrative, two columns for
  lists/tables; numbered sections; footnotes as marginalia; booktabs-style tables
  (top/bottom rules only).
- **Density** — high text density, medium air.
- **Shape** — none: rules ARE section breaks; no radius, no shadows.
- **Motion** — none.
- **Imagery** — captioned figures ("Figure 1:"), TikZ-aesthetic diagrams, plots
  with hairline axes.
- **Fits** — research tools, ML products, databases, technical essays, anything
  claiming rigor.
- **Fails** — consumer products; retail; playful marketing.
- **Failure modes** — fake greeked math reads as parody; two-column layout
  imported onto mobile.
- **Forbidden moves** — fake greeked math as parody; two-column layout on mobile;
  rounded cards; decorative gradients; brand ornaments.

### D21 · Field Guide / Naturalist — botanical plate and specimen label

- **Type** — old-style/transitional serif for prose (EB Garamond, Source Serif),
  italics for taxonomy, small caps for labels; a hand-annotated feel is allowed.
  **Fallback stack**: `'EB Garamond', 'Adobe Garamond Pro', Garamond, Georgia, serif`.
- **Color** — aged paper #EFE7D8, sepia ink, muted botanicals (sage, ochre,
  madder); duotone plates; no screen-bright hues.
- **Layout** — framed specimen plates with numbers/labels, margin notes, index
  lists, caption bands.
- **Density** — medium, curated.
- **Shape** — 0 radius; thin double borders or corner ticks on plates.
- **Motion** — crossfades only; nothing modern-feeling moves.
- **Imagery** — scientific illustration, engravings, maps, specimen photos with
  scale bars.
- **Fits** — outdoors, food and provisions, botanical skincare, museums and
  education.
- **Fails** — tech and SaaS; enterprise dashboards; dense product UI.
- **Failure modes** — sepia-everything: every element is textured without a grid
  underneath, so the page reads as a filter rather than a plate.
- **Forbidden moves** — stock photography in sepia; texture without a grid
  underneath; screen-bright hues; modern soft shadows; rounded cards.

### D22 · Fashion Type-First — type IS the campaign; huge, condensed, cropped

- **Type** — massive condensed grotesque (Anton, Archivo Black as free
  alternatives to Druk-class) at 10–20vw, cropped and overlapping; body in tiny
  neutral sans. **Fallback stack**: `'Anton', 'Archivo Black', Impact, 'Arial Narrow', sans-serif`.
- **Color** — high-contrast duotone (black/white plus one hot accent such as
  Klein blue or signal red) or monochrome; imagery black and white duotoned with
  grain.
- **Layout** — full-bleed type blocks, edge-to-edge crops, extreme scale jumps,
  poster stacking, marquees; heroes maximal, lists minimal.
- **Density** — polarised.
- **Shape** — sharp corners everywhere; no shadows.
- **Motion** — marquee scrolls, mask reveals, fast cuts.
- **Imagery** — art-directed, blown-out or duotone; grain; no clip-art.
- **Fits** — fashion, music, agencies, drop and campaign pages.
- **Fails** — dense product UI; forms and checkout flows;
  accessibility-critical interfaces (extreme scale/crop).
- **Failure modes** — loud but empty when the copy is generic; a11y breaks at
  extreme scale and crop if the tiny body text and alt text are an afterthought.
- **Forbidden moves** — clip-art; loud-but-empty copy; rounded corners; shadows;
  small timid type.

---

## Families and neighbours

At most **one prototype per family** per generation run, and never blend two
neighbours. The `family` field in the machine block uses this closed set:

| Family | Members |
| --- | --- |
| `print` | D01 Swiss International, D03 Broadsheet Newsprint, D14 Risograph / Zine, D21 Field Guide / Naturalist |
| `quiet` | D04 Quiet Luxury / Stealth Wealth, D05 Scandinavian Slow-Living |
| `editorial` | D02 Editorial Luxe, D22 Fashion Type-First |
| `luxe` | D11 Art Deco |
| `retro` | D12 Space Age / Retro-Futurism, D13 Analog 70s / Groovy, D16 Y2K Gloss, D17 Vaporwave / Synthwave Grid |
| `brutalist` | D06 Neo-brutalism, D07 Raw Web / True Brutalism |
| `dark` | D08 Terminal / CLI, D19 Instrument Dark |
| `systemic` | D09 Data Control Room, D18 macOS Native |
| `technical` | D10 Blueprint / Schematic, D20 Academic Preprint |
| `playful` | D15 Memphis / Playful Toy |

Neighbour disambiguation (from rules C3):

- **Quiet neighbours** — D04 vs D05 vs D02. D04 = metallic accent + narrow
  centred column + 2–4px radius; D05 = warm earth tones + no cool accent + photo
  bands; D02 = editorial asymmetry + huge display serif + captions.
- **Dark neighbours** — D19 vs D08 vs D09 vs D17. D19 = product density + soft
  radii + one tint; D08/D09 = mono, 0 radius, semantic-only colour; D17 = era
  collage + grid sun.
- **Retro neighbours** — D12 vs D13 vs D15 vs D16 vs D17, separated by palette
  system, geometry (curve vs blob vs grid) and motion; at most one per batch.
- **Print neighbours** — D14 vs D21 vs D03 vs D02, separated by ink system (spot
  overprint vs sepia plate vs column rules vs asymmetric spread).
