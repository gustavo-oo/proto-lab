# Landscape report: cheap static-HTML design prototypes from agent skills

Scope: what already exists that overlaps with our planned skill (divergent seeded variants, runtime competitor research,
judge/critique step, lightly-navigable static HTML prototypes). Surveyed Oct 2026 via web search + primary sources.

---

## 1. Official agent-skill ecosystem

- **anthropics/skills** (repo: https://github.com/anthropics/skills)
  Anthropic's reference skill repo (spec + template + example skills). Relevant skills below. All load dynamically by
  description; none is a dedicated prototyping pipeline.

- **anthropics/skills — web-artifacts-builder** (https://github.com/anthropics/skills/tree/main/skills/web-artifacts-builder)
  Scaffolds React+TS+Vite+Tailwind+shadcn/ui, then bundles to a **single self-contained HTML file** via Parcel+html-inline
  for Claude artifacts. Explicit anti-slop guidance in SKILL.md: "avoid excessive centered layouts, purple gradients,
  uniform rounded corners, and Inter font." No variants, no seeding, no research; testing is optional/discouraged upfront.

- **anthropics/skills — frontend-design** (https://github.com/anthropics/skills/blob/main/skills/frontend-design/SKILL.md)
  The most relevant official skill: instructs the model to act as a design lead, ground choices in the subject matter,
  write a token plan (color/type/layout), review it against the brief before coding, and self-critique. Ships a **calibrated
  list of current AI-design clusters** worth stealing: cream #F4F1EA + high-contrast serif + terracotta; near-black +
  acid-green; broadsheet hairline rules; the "SaaS-card kit"; template chrome (ALL-CAPS eyebrows, "A · B · C" meta, "→" links).
  Single-direction; divergence is left to the model's discretion.

- **anthropics/skills — canvas-design** (https://github.com/anthropics/skills/blob/main/skills/canvas-design/SKILL.md)
  Two-step "design philosophy → canvas" workflow for posters/art (md + pdf/png). Interesting precedent for generating a
  *named aesthetic movement* before expressing it (proto "design direction"), but output is static art, not navigable UI.

- **anthropics/skills — webapp-testing** (https://github.com/anthropics/skills/tree/main/skills/webapp-testing)
  Python-Playwright harness for local web apps: server lifecycle, DOM inspection, screenshots, console logs. Usable as the
  verification/QA layer beneath a prototype skill (and the only official "look at it with a browser" skill).

- **obra/superpowers — brainstorming + visual companion** (https://github.com/obra/superpowers/blob/main/skills/brainstorming/SKILL.md,
  guide: .../visual-companion.md)
  The closest existing "show mockups in a browser" mechanic. A local server watches a dir and serves the newest HTML file;
  fragments are auto-wrapped in a frame template providing `.options/.cards/.mockup/.split` CSS and click-selection that is
  recorded to a JSONL events file the agent reads next turn. Rules: offer just-in-time, 2-4 options max, wireframe fidelity,
  real content when it matters. **No navigation between screens** (newest file wins), no variants generator, no seeding;
  the skill itself warns it "can be token-intensive."

- **mattpocock/skills — prototype** (https://github.com/mattpocock/skills/blob/main/skills/engineering/prototype/SKILL.md)
  Model-invoked skill with a UI branch: "generate **several radically different UI variations on a single route**, switchable
  via a URL search param and a floating bottom bar." Throwaway-by-design, no persistence, capture-as-primary-source on a
  branch. Closest published pattern to "divergent variants for one decision," but only within an app's dev server, one screen,
  no judge, no research, "radically different" is unenforced.

- **google-labs-code/stitch-skills** (https://github.com/google-labs-code/stitch-skills)
  Google's skills for its Stitch UI-generation service (MCP-driven). `generate-design` includes an explicit **"Generate
  Variants flow (layout/color/content variations)"**, prompt-enhancement pipeline, and a `design-md` skill that synthesizes
  a semantic "design system as source of truth" (DESIGN.md) from generated screens. Vendor lock-in to Stitch; ~2.4k★.

## 2. Community skill collections (design/prototype/UI relevant)

- **Collections**: karanb192/awesome-claude-skills (lists anti-slop-design, anti-ui-slop), junminhong/awesome-agent-skills
  (lists UIZZE anti-ui-slop), awesome-skills.com / skills.sh / claudeskills.info directories (frontend-design ~954k installs;
  leonxlnx/taste-skill variants 400-570k installs). Mostly catalogs, not pipelines.

- **superdesigndev/superdesign-skill** (https://github.com/superdesigndev/superdesign-skill, ~830★, MIT)
  **The most direct competitor.** Skill + CLI (`@superdesign/cli`) driving a hosted design agent on an infinite canvas.
  `iterate-design-draft --mode branch -p "dark theme" -p "minimal" -p "bold"` generates **one variant per directional
  prompt** (or `--count N` auto-explore); `execute-flow-pages` drafts multi-page flows; `extract-website --design-md` pulls a
  site's "design DNA" (tokens/brand/content); `search-prompts` browses a style/component prompt library; `.superdesign/design-system.md`
  is the persistent contract and a `replica_html_template` captures the current UI as the before-state. Explicit anti-AI-slop
  positioning ("stop shipping AI-slop UI"). Costs: free skill, paid hosted agent; variants are prompt-driven, not seeded;
  judge step is left to the user.

- **zanwei/design-dna** (https://github.com/zanwei/design-dna, ~2k★, MIT)
  Skill that extracts a quantified **Design DNA JSON** (tokens + qualitative style + visual effects) from screenshots/URLs and
  generates self-contained HTML/CSS/JS from it. Notable rigor: `measure-colors.mjs` (deterministic k-means, perceptual ΔE
  merging) and `verify.mjs` scoring generated output vs reference with PASS/FAIL ΔE thresholds — a real automated judge for
  *fidelity* (not for slop or diversity). Extraction-only; no variant seeding or divergence.

- **uizze/uizze — anti-ui-slop** (https://github.com/uizze/uizze, https://github.com/uizze/uizze-ui-slop-gate)
  Free skill (Apache-2.0) that mines 800k+ real web/iOS screens (via UIZZE's paid MCP) to build a product-specific **design
  contract**, then runs a hard **finish gate**. The free GitHub Action "UI Slop Gate" scans changed frontend code for inert
  controls, missing state markers, hardcoded colors, and "combinations of generic dashboard cues" — the only deterministic
  slop-detector found. Research surface is a paid proprietary catalog, not free runtime browsing.

- **tommyjepsen/awesome-ux-skills** (https://github.com/tommyjepsen/awesome-ux-skills)
  Skill pack with strong judgment primitives: `design-analysis` (screenshot → measured typography, OKLCH palette **with area
  shares**, spacing, motion → shadcn tokens), `craft` (12 visual-craft rules: no gradients, no glow, no `transition: all`...),
  Nielsen heuristics, Rams principles, WCAG reviews. Measurement + critique, but no generation pipeline and no seeding.

- **leonxlnx/taste-skill** and **nextlevelbuilder/ui-ux-pro-max** (via claudeskills.info)
  High-install "taste" skills (design-taste-frontend, high-end-visual-design, redesign-existing-projects): prompt packs that
  push output away from defaults. No variants, seeds, research, or judge — pure taste priors.

## 3. Commercial AI design-prototyping tools

- **v0 (Vercel)** (https://v0.dev) — prompt + screenshot → Next.js/Tailwind components; token-based pricing; version history,
  shareable chats, infinite canvas. Single-direction by default; "production code" rather than throwaway divergent options.

- **Lovable** (https://lovable.dev) — full-stack app generator (Supabase backend, credits-based); prompt-to-app with design
  system support mainly on higher tiers. Optimizes for *shipping*, not for cheap divergent mockups; heavier security review
  needed since prototypes hit real data.

- **Magic Patterns** (https://www.magicpatterns.com) — "rapid UI prototyping" for product teams; matches your real design
  system; `/Inspiration` command + collaborative canvas; explicitly markets "**explore multiple directions before committing**"
  and multi-screen flows with share/deploy links; exports React+Tailwind/Figma. Closest commercial analog to our multi-variant
  framing; closed SaaS, per-seat.

- **Galileo AI** (https://www.usegalileo.ai) — early text-to-UI mockup generator (Figma export); single-screen, static; team
  acquired by Google (2024) — effectively a historical baseline for "AI makes pretty screens."

- **Uizard** (https://uizard.io, now under Miro) — Autodesigner 2.0: text/screenshot/wireframe → UI, plus predictive heatmaps.
  Fast ideation; single design per prompt; no divergence control.

- **Figma Make + Dev Mode MCP** (https://developers.figma.com/docs/figma-mcp-server/, https://www.figma.com/blog/4-ways-were-using-our-mcp-server-at-figma/)
  MCP server reads design context into agents (React+Tailwind by default, Code Connect for real components) and **writes to
  the canvas** (frames, components, variables); Figma's design agent has created "72 variants" of a button set in one run.
  Requires paid seats/rate limits (Starter: 6 calls/month); free during the write-beta. Strong for design-system-grounded work,
  not for cheap throwaway HTML divergence.

- **Google Stitch** (https://stitch.withgoogle.com, skills above; CLI proxy https://www.npmjs.com/package/@_davideast/stitch-mcp)
  Generates HTML/CSS screens from prompts/images; SDK returns **many screens per generation**; can serve screens locally and
  build an Astro site mapping screens→routes. Free during preview with quotas; vendor-hosted (Google account).

## 4. Open-source editors & sketch-to-UI tools

- **Onlook** (https://github.com/onlook-dev/onlook, Apache-2.0, ~22-26k★) — open-source visual editor for real Next.js+Tailwind
  codebases: Figma-like canvas editing, AI constrained to your design system, branching for experiments, changes become PRs.
  Iteration-in-place rather than cheap divergent mockups; heavier setup.

- **tldraw make-real** (https://makereal.tldraw.com, starter: https://github.com/tldraw/make-real-starter) — draw a wireframe,
  press Make Real, get working HTML in an iframe **on the canvas**; annotate the iframe and regenerate to iterate. Open-source
  starter; you pay your own model API key. Canvas-centric, one artifact per button-press, no seeding/judge/research.

- **tldraw computer** (https://computer.tldraw.com) — node-graph workflows over an LLM runtime (Google AI collab). Generative-UI
  plumbing, not design prototyping.

## 5. Design homogenization / "AI slop" evidence

- **Design Creativity Bench** (arXiv 2610.11539, https://arxiv.org/html/2610.11539v1) — benchmark measuring **diversity +
  appropriateness** of LLM-generated UI: model outputs are markedly more similar across domains than paired human references;
  proposes an originality-weighted score (0.9 originality / 0.1 range). Direct empirical support for "force divergence."

- **Interrogating Design Homogenization in Web Vibe Coding** (arXiv 2603.13036, https://arxiv.org/pdf/2603.13036) — micro/meso/macro
  case studies showing probabilistic defaults converge designs toward a dominant Western aesthetic; argues for **"productive
  friction"** (e.g., asking cultural/context questions before generating) to preserve diversity. Our "seed + variant" mechanic
  is a friction device; cite this.

- **Measuring Aesthetic Homogenization in Text-to-Image AI** (https://github.com/timothyjgraham/ai_slop_paper_experiments) —
  DALL-E 3/Imagen 4 outputs collapse to ~10 of 768 effective embedding dimensions; independent models converge to cosine 0.86.
  Evidence that homogenization is structural, not a fixable model quirk; relevant to why "just prompt harder" fails.

- **The Homogenization Problem in LLMs** (arXiv 2601.06116, https://arxiv.org/html/2601.06116) — positions mode collapse as a
  safety concern; frames alignment itself as "diversity management." Useful vocabulary for our judge step.

- **AwesomeDesignSystem: ai-slop-vs-human research note** (https://github.com/Yu-aimaker/AwesomeDesignSystem/blob/main/research/ai-slop-vs-human.md)
  Concrete tell-table + pre-ship checklists (font/color/hero/cards/imagery/copy). Also documents Tailwind's creator apologizing
  for `bg-indigo-500` defaults saturating training data — one root cause of "AI purple."

- **Anthropic frontend-design SKILL.md's five AI-design clusters** (see §1) — the single best "slop fingerprint" list composed
  by a frontier lab; overlaps strongly with our intended judge heuristics.

- Practitioner explainers: https://smoothui.dev/blog/ai-design-slop, https://dev.to/voltwake/why-ai-generated-design-all-looks-the-same-3bho
  — popular "closed-loop design quality bar" / "commit to one style" arguments; useful for README positioning.

- **HCI paper**: "Towards Human–AI Synergy in UI Design" (ACM ToCHI, https://dl.acm.org/doi/10.1145/3773035) — intent clarification
  reduced revisions vs Uizard/v0 in a 16-participant study; has a section explicitly on "Balancing Fine-Grained Control and
  Output Diversity in Generative Design."

## 6. Seeded / divergent direction generation tooling

- **No dedicated "seeded design direction" tool was found** in the agent-skill or commercial space. What exists:

- **Superdesign branch mode** — variants come from hand-written directional prompts (`-p "dark theme"`, `--count N`); randomness
  is model sampling; nothing is reproducible across sessions.

- **Stitch "Generate Variants" + multi-screen generations; Magic Patterns `/Inspiration`; mattpocock prototype toggles** — variant
  *counts* exist, but no explicit seed, no guarantee of structural divergence (often color/layout reskins of one cluster).

- **design-dna (JSON DNA)** and **Stitch DESIGN.md** — portable, version-controllable direction *specs* (extraction/synthesis),
  not generators of novel directions; no crossover/mutation of directions.

- **Pre-LLM generators** (Fontjoy font-pairing neural net, Huemint ML palettes) — randomized aesthetics without a coherent,
  replayable multi-axis direction. Nothing ties a single seed to palette + type + layout + motion.

## 7. Runtime UI research sources (competitor pattern mining)

- **Mobbin** (https://mobbin.com, MCP: https://mobbin.com/mcp) — 621k+ shipped screens/flows with natural-language search;
  MCP for agents on Pro/Team plans; first-party guidance: treat as evidence, cite sources, don't infer causality.
- **Refero** (https://refero.design) — curated web/iOS references + first-party MCP; paid.
- **UIZZE** 800k screens — paid MCP behind free skill.
- **Page Flows / UX Archive / Lazyweb** — human-centric; weak agent access.
  Free alternative for our skill: direct browsing/screenshotting of the product's own competitors via Playwright/agent-browser.
  Nobody ships an OSS skill that does runtime, cited, good/bad-pattern extraction from the brief's actual domain for free.

---

## Gaps & opportunities for our skill

1. **Seed → reproducible direction.** Nobody exposes an explicit seed that deterministically maps to a *whole* design
   direction (name, palette, type pairing, layout archetype, density, motion). Existing randomness is sampling noise
   (Superdesign prompts, Stitch variants). Opportunity: direction cards generated from a seed, re-rollable and committed to
   the repo, so sessions diverge by default and are reproducible for review/handoff. This is our strongest differentiator.

2. **Divergence by construction.** Tools either emit one candidate (v0, Lovable, Galileo, Uizard) or ad-hoc variants
   (Superdesign branch, Stitch variants, Magic Patterns inspiration) that usually share one aesthetic cluster. Design
   Creativity Bench shows model designs collapse toward each other. Opportunity: enforce orthogonal axes per decision point
   (layout archetype, type system, density, color temperature...) with a diversity check between variants before showing them.

3. **Free, cited, runtime domain research.** Competitor-UI mining exists only behind paid catalogs (Mobbin/Refero/UIZZE MCPs).
   No OSS skill scrapes the brief's domain at runtime, extracts good/bad patterns with screenshots + citations, and stores
   them as evidence. Opportunity: agent-browser/Playwright screenshots → small cited pattern corpus; keep the "distinguish
   observation from inference" rule from Mobbin's own agent guidance.

4. **Independent judge before the human sees anything.** Existing pieces are partial: UIZZE's finish gate (code-level slop cues),
   design-dna's ΔE verifier (fidelity), Anthropic's frontend-design critique (self-review), ACM ToCHI's clarification loop.
   Nobody bundles a *pre-review* that checks (a) brief fidelity, (b) slop fingerprints against a named defaults list, and
   (c) **cross-variant diversity** (are the variants actually different?). (c) is uniquely absent everywhere.

5. **Lightly-navigable multi-screen static HTML.** superpowers serves only the newest file (no navigation); mattpocock toggles
   variants on one route; Magic Patterns/Stitch flows are paid/cloud. Opportunity: a tiny static manifest/router (links between
   screens, zero build, file://-openable, shareable as a folder or zip) — "lightly navigable" isn't shipped anywhere as a
   primitive.

6. **Cheapness as a feature.** The visual companion admits token-intensity; commercial tools meter messages/tokens/credits;
   Figma MCP ratelimits. Our static-HTML approach (no server, no build, screenshot-based judging, regenerate-from-seed)
   can be genuinely cheap — make cost model explicit in the README (tokens per run, no runtime dependencies).

7. **Direction composition.** Design extraction exists (design-dna, Superdesign extract-website, Stitch DESIGN.md) but no one
   *crosses* extracted DNAs with conflict detection ("start from competitor A's density, but B's type scale"). Seed-based
   direction objects make crossover/mutation trivial; nobody has it.

8. **Decision-point taxonomy.** No published skill enumerates concrete decision points and generates divergent options per
   point; variants are whole-page redraws. A structured "decision → variants → chosen → folded into direction" log doubles as
   the artifact that feeds the judge and the final implementation brief.

9. **Pre-selection feedback loop.** superpowers records raw clicks; ours can record selection rationale → seed evolution
   ("hybrid A+B", "more like C") and a structured decision log committed alongside prototypes.

**What nobody does (one paragraph):** no free, vendor-neutral skill found combines all four of: (seeded, reproducible divergent
direction generation) × (orthogonal multi-variant options per decision point) × (runtime, cited competitor/domain research) ×
(a pre-human judge covering brief fidelity, slop fingerprints, and inter-variant diversity), while emitting lightly-navigable
static HTML with no server or build. The nearest neighbors — Superdesign (paid canvas agent, prompt-driven branches),
Google Stitch (hosted, variants + DESIGN.md), UIZZE (paid research catalog + finish gate), design-dna (fidelity verifier) —
each solve one slice. Our skill's wedge is the combination, with the seed and the diversity judge as the parts nobody ships.
