---
name: design-checklist
description: One stop for every design-flavored task — brand identity & voice, design tokens & systems, UI/UX intelligence (50+ styles, 161 palettes, 57 font pairings, 99 UX guidelines), micro-interaction polish (animation framework, perf rules, navigation/menu motion), shadcn/Tailwind code patterns, logo generation (55 styles, Gemini AI), corporate identity programs (50 deliverables, CIP mockups), HTML presentations (Chart.js), banner design (22 styles, social/ads/web/print), icon design (15 styles, SVG, Gemini), social media photos (HTML→screenshot), and font catalogs. Use whenever the user wants to design, generate, or polish anything visual or brand-related — logos, banners, social images, icons, brand voice, design tokens, design system, color palettes, font choices, presentations, slides, UI intelligence, UX guidelines, animation decisions, polish details, shadcn components, Tailwind patterns, dark/light/gray theming, or wants to "design", "make", "create", or "generate" any visual or brand asset. Triggers on /design-checklist, /design, /brand, /design-system, /ui-styling, /banner-design, /slides, /ui-ux-pro-max, /emil-design-eng, and on phrases like "design a logo", "create a brand identity", "make a banner for X", "generate a social post", "build a pitch deck", "design icons", "set up design tokens", "what palette should I use", "what font pairs with X", "polish this UI", "should this animate", "what easing should I use", "animate this menu/navbar/dropdown/sidebar", "make this feel premium", "shadcn component for X", "tailwind pattern for Y". Platforms: Facebook, Twitter/X, LinkedIn, YouTube, Instagram, Pinterest, TikTok, Threads, Google Ads, print. Stacks: React, Next.js, Vue, Svelte, SwiftUI, React Native, Flutter, Tailwind, shadcn/ui, HTML/CSS.
argument-hint: "[domain] [args]"
---

# design-checklist

The unified design skill. Every domain — brand voice, design tokens, UI intelligence, polish, code patterns, logos, CIPs, slides, banners, icons, social photos — lives here. SKILL.md is a thin router; depth lives in `references/` and `scripts/`.

## This skill acts

`/design-checklist` is an instruction to change the thing, not to plan it. It does not ask
which direction to take, does not produce mockups or proposals for approval, and
does not report what it would do. It reads what is already there, decides, edits
the real files, and hands back the filled checklist.

Where the brief is silent, the project answers: its tokens, its brand, its
existing components. Where nothing answers, take the most conservative option that
satisfies the gates and state the assumption in one line at the end — after the
work, not instead of it. The only thing that stops a run is something
unsafe or destructive, and a design choice is neither.

Mockups, artboards, and canvases are a different skill. If what is loaded here
does those things, it is not this skill.


## Running one part of it

A run answers for the whole deliverable by default, and PRC-08 exists so that is
not narrowed quietly. A scope is the other thing: a narrowing said out loud.

```bash
<design-pass> scopes                                    # the named scopes
<design-pass> start --kind web-ui --target . --scope nav
<design-pass> scan --scope all                          # widen it again
```

`/design-checklist nav` is the same thing: it runs the navigation gates and the
handful of others that bear on a bar, twenty-nine instead of the registry's five
hundred and forty-four, and nothing about how hard any of them is to answer
changes.

Every place a scoped run is shown leads with the narrowing and with what it did
not look at, so a scoped pass can never be read as a full one. The named scopes
are nav, mobile, footer, hero, fields, tables, motion, loading, spacing, colour,
type, copy, a11y, images, pointer, cohesion, plates, tokens, brand, production,
slop, and marketing.

**A project-wide run is something to ask for.** Editing a stylesheet opens a run
over that file, scoped to what the file's name says it is about — `navigation.css`
opens a `nav` run over `navigation.css`. Only invoking the skill opens a run over
the whole project. An edit imposing a four-hundred-gate checklist on a session
that changed one file is how the checklist became something to get around.

## The run protocol

**/design-checklist is an instruction to build, not to review.** The deliverable is the working
thing, changed. The checklist exists to make sure every rule this skill knows actually
lands in it — not to produce a survey of what is wrong.

That distinction is enforced rather than trusted: a gate the sweep failed cannot be
recorded as passing, and a gate marked fixed reopens if the next sweep still fails it.
A gate that is not met is work to do. The only ways past one are changing the code, or
naming the condition that makes it inapplicable to this deliverable.

Every rule lives as a gate in `checklist/gates/*.json`, and a run satisfies every gate
that applies to it — not the ones that came to mind.

**0. Find the tool.** It ships inside this skill, so it is wherever this file is:

```bash
DP="$(dirname "$(realpath "${BASH_SOURCE:-$0}")")/bin/design-pass.py"   # beside SKILL.md
# On a machine with the synced config, this is the same file:
#   <design-pass>   (a wrapper that runs the copy above)
```

Use whichever resolves. If neither does, the skill was installed without its `bin/`
directory and the gates cannot run — say so rather than proceeding by eye.

**1. Open the run before writing anything.**

```bash
<design-pass> start --kind <web-ui|component|logo|icon|banner|social|slides|brand|tokens|cip> --target <path> --title "<what this is>"
```

It prints the gates that apply, derived from what the target actually contains — form gates when there is a form, chart gates when there is a chart, transparency gates when there are PNGs. Add `--flag redesign`, `--flag ad`, or `--flag print` for the conditions that cannot be read out of source.

One derived condition is worth checking on sight: `marketing`. A landing page and an app screen are both `web-ui`, and the fifty Marketing Surfaces gates are right on the first and wrong on the second, so the tool weighs landing-page signals against app signals and prints the verdict in the `Detected:` line. When it has read the target wrong, `--flag marketing` or `--flag app` settles it.

**1b. Record the design read, before the first file.** On a marketing surface TST-62 holds the run open until it exists:

```bash
<design-pass> read --page-kind <landing|portfolio|editorial|product> --audience "<who>" --vibe "<the words the brief used>" --palette "<family>" --face "<display face>"
```

The audience picks the aesthetic. A run that skips this reaches for a default one instead, which is where most bad generated design comes from. `--palette` and `--face` also feed TST-63, which refuses to repeat the last run of the same page kind.

A run opens when this skill is invoked and at no other time. Editing a stylesheet or a styled component records against a run that is already open; it never opens one. The only thing left to you is scoping it properly.

**The prompt sets the work. It never sets the checklist.** A request to change one button still answers for the page that button sits on, and for every gate that page's contents pull in. Scope the run to the deliverable — what the reader ends up seeing — not to the files the request happened to name. Gate PRC-08 lists the files of the same kind sitting outside the targets and will not let them go unmentioned.

**2. Read the domain references the gates point at.** The gate list names its sources. Read those, not a sample of them.

**2b. Read every file in scope, and rule on each one.**

```bash
<design-pass> files
sed -n '1,400p' <path> <path> <path>          # one call reads and credits many
<design-pass> file-clear --batch - <<'JSON'
[{"path": "src/lib/format.ts", "note": "read in full; pure date maths, carries no design"},
 {"path": "src/lib/api.ts",    "note": "read in full; fetch wrappers only, nothing a reader sees"}]
JSON
```

The run keeps a ledger of every file under its targets. Each one ends the run either changed or explicitly ruled as needing no change, with the reason. A file cannot be cleared until the harness has watched it be read — through the Read tool or through `cat`, `sed`, or `head` — so an untouched file and a considered one stop looking alike. No gate in the registry currently reads that ledger, so it is reported rather than holding a run open — read `design-pass.py files` before finishing.

Read in batches and clear in batches. A ledger of two hundred files answered one call at a time is where a run's hours go, and the per-file reason survives the batch unchanged: every row carries its own note, and a batch with one bad row is refused whole.

**3. Build.**

**4. Sweep.**

```bash
<design-pass> verify
```

Every regex-settleable gate is settled here, with file and line. Failures are defects to fix, not observations to record. A check that cannot reach a verdict says so and stays open — it never reads as a pass.

**5. Fix what it found, then account for the rest.**

Every failure is a change to make. Make it, re-run `verify`, and record it:

```bash
<design-pass> status --full        # every open gate, with its rule, its fix, and what the sweep saw
```

Then answer them **in one call**. The sweep settles a few hundred gates in seconds;
what is left is the whole cost of a run, and that cost is round trips rather than
thinking:

```bash
<design-pass> resolve --batch - <<'JSON'
[{"id": "PTR-02", "status": "fixed", "note": "added :active scale(0.97) to every button and row"},
 {"id": "UXA-03", "status": "pass",  "note": "tabbed the page start to end; order matches the visual column"},
 {"id": "SLP-28", "status": "na",    "note": "no hero video; the hero is a single still at 3:2"}]
JSON
```

`fixed` is re-checked on the next sweep, so the claim has to be true. `pass` records
something verified and found already correct; `na` records a condition this
deliverable does not have.

Batching changes the number of calls and nothing else. Every row carries its own
status and its own note, the note minimum applies per row, a gate the sweep failed
cannot be answered `pass`, the bookkeeping gates refuse an attestation, and a batch
containing one bad row is refused whole with every fault named, so nothing lands
beside a failure. "Checked" is not a note; what you looked at and what it showed is.

Answer in chunks of a few dozen and verify between them, so a `fixed` claim is
re-checked while the change is still in front of you.

### What a gate cannot be answered with

Four routes out of a gate are closed, in both this tool and its sibling, because
each of them turned a checklist into a survey:

- **`pass` on a gate the sweep failed.** Already refused before this.
- **`na` on a gate the sweep failed.** This was the open door: a gate would fail,
  `pass` would be refused, and `na` closed it with a one-line note. The sweep
  failing is proof the condition is present and unmet, which is the opposite of
  inapplicable.
- **`na` while the tool can still see the condition.** A gate enters a run because
  its condition was found in the target. If it is still there, not-applicable
  contradicts the tool rather than the gate.
- **A note with no evidence.** An assertion is not a note. It has to name a file, a
  line, a measurement, or quote what was read.

A fifth status exists for the case those four would otherwise trap:

```bash
resolve <ID> --status disputed --note "<what the check reported, what is actually
there, and how that was established>"
```

`disputed` says the rule applies and the automated check measured it wrongly. It
closes the gate, so one bad check cannot jam a build, and it leads the report under
its own heading, because every dispute is either a defect in the check or a rule
that went unenforced. It takes a longer note than the other verdicts and it is
refused on a gate the sweep did not fail.

### The gate for generic

Every other rule in the set measures whether a surface is free of defects. A bar
can pass all of them and still be the shape a generated page reaches for first,
with the project's tokens painted on: `SLP-42` reads surface polish and structural
richness, and a wordmark-left, seven-link, one-CTA bar with a blur satisfies both.

So the shape itself is a gate. The catalog of 14 navigation archetypes and 8 footer
archetypes lives in `references/hallmark/references/components`, and chrome
declares which one it is:

```css
/* nav: n5-floating-pill */
/* footer: ft5-statement */
```

Four things are then checkable, and all four are:

- **NAV-11 / FTR-01** - the stamp exists. No stamp means the shape was arrived at
  rather than chosen, and no other gate can see the difference.
- The stamp names a real archetype. An invented slug is refused against the
  catalog, so the stamp cannot be a sticker.
- **NAV-12 / FTR-02** - the named shape is not the default. `n1b-saas-three-section`,
  `n1-wordmark-2-links`, and `ft3-index-style-category-list` are where a page lands
  when nobody decided.
- **NAV-13** - the shape differs from the last run of the same page kind, recorded
  when a run closes. Two landing pages sharing a nav archetype are one template
  wearing two palettes.

The escape is `--status disputed` with the reason the default shape is right for
this brief, which puts the claim at the top of the report instead of closing the
gate quietly.

### The bar, the panel, and the plates

Three things the bar owes that no archetype stamp can see, each one a gate:

- **The panel is a surface, not a filter.** `NAV-19` refuses an alpha ground or a
  backdrop blur on anything the bar opens. The bar itself may be translucent over a
  hero; the panel behind it may not, because it covers a page of type with a page of
  type and anything showing through puts the two on top of each other at the moment
  a visitor is reading to choose. It also costs a compositor pass on every scroll
  frame behind the largest element on the page.
- **The strip above the bar is decided, not defaulted.** `NAV-20` reads what the bar
  is carrying that does not belong to it — a phone number, hours, a locale switch, a
  store locator, an account link, a second brand — and asks for a rail above the bar
  where any of that exists. It is not owed by every site, and it is owed by more of
  them than have one. Either answer closes the gate; never having asked does not.
- **The page draws something of its own.** The `PLT` group, and `plates` is its
  scope: a marketing surface with a subject draws it, as flat vector plates on one
  viewBox in the project's own inks, kept as files under `public/art` and rendered
  through a single component. Photography shows one afternoon and a library glyph
  shows a generic shape; a plate shows what this business actually moves, weighs a
  kilobyte, and could not have come from anywhere else.

  Four things then decide whether it is a plate or a sticker:

  - **What it draws.** `PLT-04` counts shapes and inks, because a silhouette is one
    outline in one fill and a drawing has the parts the subject has, with a second
    tone wherever a face turns away. Twelve and five is not a standard of taste; it
    is the floor a first pass falls through.
  - **Where its ground lives.** `PLT-05` wants it drawn once. A card behind
    transparent art traces a rectangle the drawing does not fill, and a plate that
    carries its own card wrapped in a second is the same fault costing less. Which
    way round is a real decision: a map without a ground is a set of lines in the
    air, and a scene with one is a block on every surface it meets.
  - **How big it is allowed to be.** `PLT-06`: a plate carrying a section takes a
    width off its column, not a fixed height. Pinned to the height of a heading it
    reads as a mark above one and the eye skips it. Chrome is the exception, because
    a panel has the room it has.
  - **What it is never used as.** `PLT-02` fails art rendered once per menu option,
    and tells the two apart by what the plate sits beside: a key alongside a label
    and a route is a row marker; a key alongside a heading and a sentence is the
    panel's own imagery, however many panels there are. In a mega-menu that is
    `mm2-two-column-split` — destinations listed plainly on one side, one promoted
    block with its plate on the other.

  `TST-48`, which refuses hand-rolled decorative SVG, exempts the files `PLT-01`
  counts as plates. Without that a project failed one gate for satisfying another.

### The phone

`mobile` is a scope and `MOB` is its group, and every rule in it fails against
something that is not in the page. A bar in flow, a menu capped in `vh`, and a rail
with nothing reserving its height all read as correct at every width a reviewer
uses, and all three are broken on the device most visitors arrive on.

What the source gates hold: the bar is reachable from wherever the visitor is
(`MOB-01`), the open menu is measured against the visible viewport rather than the
layout one (`MOB-02`), a menu taller than the screen scrolls inside itself and
contains its overscroll (`MOB-03`), chrome on a viewport edge reads
`env(safe-area-inset-*)` (`MOB-04`), a page whose primary action is a call, a
booking, an order, or an application puts it under a thumb (`MOB-05`), anything
pinned reserves its own height in flow (`MOB-06`), and the small-screen menu reaches
whatever the desktop panels reach (`MOB-07`).

`MOB-05` is the bottom-rail rule and it is an applicability test, not a mandate: the
tool reads the page for a phone-shaped action and only then asks for the rail. An
editorial page has none and passes.

What only the capture holds is `MOB-10` through `MOB-15` — that the bar was still
there a screen down, that every row of the open menu could be reached, that nothing
pinned covered the end of the page, that the page did not scroll sideways, and that
every control was a target a thumb can hit:

```bash
# In the page at 390x844. It opens the menu itself, so it returns a promise:
#   await mobileProbe.scan()
<design-pass> mobile-probe --file capture.json
```

**6. Render the filled checklist and give it to the user.**

```bash
<design-pass> report
<design-pass> finish
```

The report leads with what changed, because that is the point of the run. It is part of the deliverable, not a log. Show it — inline for a short run, published as an artifact for a long one — so the user can see every item and how it was answered. Every gate answered `na` is listed in its own section at the top, because a gate only entered the run when its condition was found in the target, and skipping one is a claim worth reading.

`finish` refuses while anything is open, a `Stop` hook refuses to end the session with a run still going, and `finish --no-deliverable` is available only to a run that edited no design file — once one has been touched, the checklist is the only way out.

Fixing a gate is always the first option. `na` is for a condition that does not exist in this deliverable at all; `pass` is for something verified. Neither is for something that would take a while.

Four sweeps run alongside `verify`, because what they judge is not in one file:

```bash
<design-pass> cohesion        # every file against the others
<design-pass> spacing-probe --file capture.json
<design-pass> skeleton-probe --file capture.json
<design-pass> layout-probe --file capture.json
<design-pass> mobile-probe --file capture.json
```

`cohesion` finds the mismatch no per-file review can see — the one page whose table
has square corners among nine rounded ones, the section on its own spacing rhythm,
the shadow that is deeper in one place. The four probes read a rendered capture,
because a placeholder that matches its content, a panel that keeps its gap, and a
headline that held to two lines are all facts about layout rather than about source.
`layout-probe` is the marketing one: headline wrap, hero fold, nav rows, bar height,
quote length. `mobile-probe` is the phone one, and it is the only capture taken at a
phone width with the menu actually opened, because what breaks a phone is not in the
page: the browser's own retracting toolbar, the home indicator under it, and the
width of a thumb. It refuses a reading taken wider than 500px.

```bash
<design-pass> gates --kind web-ui --full   # the whole registry, any time
```

## Domain map

| Domain | When | Where |
|---|---|---|
| **brand** | Brand voice, identity, messaging, asset management | `references/brand/` |
| **system** | Design tokens (primitive→semantic→component), CSS vars, spacing/typography, component specs | `references/system/` |
| **intelligence** | UI/UX choices: styles, palettes, font pairings, product-type patterns, UX guidelines, chart types | `references/intelligence.md` |
| **polish** | Animation framework, micro-interactions, easing, perf rules, Emil-style craft | `references/polish.md` |
| **code** | shadcn/ui + Radix patterns, Tailwind, accessibility, dark mode, canvas + fonts | `references/code/` |
| **logo** | Logo design — 55 styles, 30 palettes, 25 industries, Gemini AI generation | `references/logo-*.md`, `scripts/logo/` |
| **cip** | Corporate Identity Program — 50 deliverables, HTML mockups | `references/cip-*.md`, `scripts/cip/` |
| **banner** | Banners — social, ads, web hero, print. 22 styles, all platform sizes | `references/banner-sizes-and-styles.md` |
| **slides** | HTML presentations with Chart.js — layouts, copy formulas, strategies | `references/slides-*.md` |
| **icon** | SVG icons — 15 styles, Gemini 3.1 Pro generation | `references/icon-design.md`, `scripts/icon/` |
| **social-photos** | Multi-platform social images — HTML/CSS → screenshot | `references/social-photos-design.md` |
| **macrostructure** | Non-templated web UI — greenfield pages, audits, redesigns, DNA extraction from a URL or screenshot. 21 macrostructures, catalog + custom themes, a 57-gate slop test, pre-emit self-critique | `references/hallmark/SKILL.md` |

Pick the domain that matches the task. Many tasks span multiple domains — read the relevant references together.

## Five principles across all domains

Each of these is a gate the run answers, named in brackets. The prose says why; the gate is what holds.

1. **Read the existing project first.** [PRC-02] Brand voice, design tokens, theme files, sibling components. Never ship a generic template that ignores what's already there.
2. **Three themes always.** [UNI-01, UNI-02, SYS-08] Dark, light, AND gray. Every color, border, shadow, surface must read correctly in all three. Semantic tokens — never hardcode colors that break in one theme.
3. **Behavior preservation when redesigning existing code.** [UNI-05] Only presentation changes. Routes, handlers, contracts, side effects stay identical.
4. **Every word goes through the `avoid-ai-writing` skill.** [PRC-03, PRC-04] Design work produces copy constantly — slide decks, banner headlines, social captions, brand voice documents, UI strings, button labels, mockup text. All of it is words a person reads, and none of it ships until it has been held to the `avoid-ai-writing` skill. Invoke that skill via the Skill tool whenever a deliverable carries text; apply it from the loaded skill, not from memory of its rules. A beautiful deliverable with machine-sounding copy is a failed deliverable — the copy check is part of the design, not a step after it.
5. **UI labels are Title Case.** [UNI-03] Menu items, dropdown entries, buttons, tabs, and column headings are Title Case: "Plugin Library", "Join Our Discord", "Get in Touch" (short prepositions and articles stay lowercase). Sentence case on a control label is a defect, every time. Sentences, descriptions, blurbs, helper text, and headlines that read as prose stay sentence case. Trenton flags this constantly — check every label before delivering.

---

## Brand

Brand voice, visual identity, messaging frameworks, asset management, brand consistency.

Read in order:
- `references/brand/_overview.md` — workflow and decision tree
- The remaining `references/brand/*.md` files for specific deliverables

Scripts: `scripts/brand/`. Templates: `templates/brand/`.

Activate for: branded content, tone of voice, marketing assets, brand compliance, style guides.

Brand deliverables are almost entirely words, so principle 4 hits hardest here: run every voice document, tagline, message framework, and piece of marketing copy through the `avoid-ai-writing` skill before delivering it. A brand voice that reads as machine-written undermines the exact thing the deliverable exists to establish.

---

## System (design tokens)

Three-layer tokens (primitive → semantic → component), CSS variables, spacing/typography scales, component specifications.

Read in order:
- `references/system/_overview.md` — token architecture
- The remaining `references/system/*.md` files for component specs and per-token-type guidance

Scripts: `scripts/system/`. Templates: `templates/system/`. Data: `data/system/`.

Activate for: design tokens, semantic color systems, spacing/type scales, component spec authoring.

---

## Intelligence (UI/UX choices)

Macro design decisions — style language, palette, fonts, product-type patterns, chart types.

Read: `references/intelligence.md` (full library — 50+ styles, 161 palettes, 57 font pairings, 161 product types, 99 UX guidelines, 25 chart types across 10 stacks).

Consult when starting a redesign or new UI and needing direction decisions. Pair with **polish** for micro details.

---

## Polish (micro-interactions)

Polish philosophy, animation decisions, micro-interactions, perf rules.

Read: `references/polish.md`.

Key reference points (always check the file for the full framework):
- **Animation decision tree** — should it animate at all? frequency × purpose
- **Easing curves** — strong custom cubic-beziers; never `ease-in` on UI
- **Durations** — cap UI motion at 300ms; element→duration table
- **Loading states & skeletons** — keep unknown / empty / failed apart; one skeleton primitive shaped
  like its content; content animates in once when the skeleton resolves, with the same entrance used
  for page changes. Applies to any UI that fetches — check it on every build, not just redesigns.
- **Placeholder correspondence** — the placeholder matches the box that replaces it in size, position,
  layout, gap, count, radius, aspect, and padding, and a placeholder is required wherever content
  arrives late: fetches, next pages, route and tab changes, deferred sections, late-measuring widgets,
  and images. The SKL gates settle the measurable half from a browser capture taken with
  `scripts/code/skeleton-probe.js` and fed in with `design-pass.py skeleton-probe`.
- **Polish checklist** — `transition: all` → fix; `scale(0)` entry → fix; missing `:active` → fix
- **Perf rules** — only animate `transform`+`opacity`; full transform strings under Framer Motion load

### Pointer and press are added, not noted

A control with no press feedback is unfinished. When a deliverable is missing any of this,
it gets added in the same pass — never listed as an absence:

`cursor: pointer` on everything clickable · `:active` press scale of 0.95–0.98 with a
100–160ms transform transition · a hover state, and any hover motion gated behind
`@media (hover: hover) and (pointer: fine)` · a `:focus-visible` ring that appears instantly ·
a disabled state with `cursor: not-allowed` and the real attribute ·
`touch-action: manipulation` · `-webkit-tap-highlight-color` · a themed `::selection` ·
`user-select: none` on control labels · 44px hit areas.

And the click itself gets an answer. Press feedback belongs to the control that was hit;
a click effect belongs to the click, fires at the cursor wherever it lands, and is what
separates a page that responds from one that merely accepts input. A site without one gets
one — a ripple from the click point on a fixed `pointer-events: none` layer, accent-coloured,
gone inside 600ms, skipped under `prefers-reduced-motion`. `references/code/click-effect.md`
carries the implementation and the reason the custom-cursor and particle bans do not reach it.

The PTR gates check every one of these against the source, so a missing press state fails the
run rather than shipping. Full set: `<design-pass> gates --kind web-ui --full`.

For **navigation** motion specifically — nav bars, menus, dropdowns, sidebars, hamburger morphs, active indicators, wayfinding — read `references/navigation-menus.md` (Disney's 12 principles applied to navigation: per-element timings, stagger, easing, and CSS patterns).

Always consult alongside `intelligence` on visual work — direction sets where the eye goes; polish makes it feel premium.

---

## Code

shadcn/ui (Radix UI + Tailwind), Tailwind CSS utility-first, canvas-based visuals, accessibility-first patterns.

Read in order:
- `references/code/_overview.md` — workflow and routing
- The remaining `references/code/*.md` files for component patterns (dialogs, forms, tables, dropdowns, dark mode, theming)

Scripts: `scripts/code/`. Font assets: `canvas-fonts/`.

Three areas here get their own gate groups because they are the ones most reliably
left half-done:

- `references/code/fields-and-dropdowns.md` — the field surface, native versus custom selects, the menu surface, option states, and the keyboard contract. **FLD gates.**
- `references/code/tables-and-headers.md` — dense scannable rows, sticky heads, tabular figures, row hover through the cells, and one header rhythm across every surface. **TBL and HDR gates.**
- The same file's spacing section — the space *between* things, as opposed to whether a value is on the scale. Two panels sharing an edge passes every value check ever written. **SPC gates**, settled from `scripts/code/spacing-probe.js`.

Activate for: building UIs, implementing design systems, responsive layouts, accessible components, theme customization, dark mode, visual designs/posters, consistent styling patterns.

---

## Marketing surfaces

A landing page, a portfolio, or a public product page is judged on things an app screen is not, and almost all of them are counts rather than judgements: eyebrows against sections, text elements in the hero, consecutive sections sharing one shape, accent hues on one page, labels per CTA intent. `references/marketing-surfaces.md` holds the rules and **TST gates** hold the counting, scoped by the `marketing` condition so none of it reaches a dashboard.

The ones that ship most often, in rough order of how reliably they appear in generated work:

- **An eyebrow above every section.** The cap is one per three, hero included. TST-08 counts them.
- **A hero that does not fit.** Headline past two lines, subtext past twenty words, the CTA below the fold, top padding floating the whole thing down the page, and six text elements where four is the ceiling. TST-01 through TST-04, measured from `scripts/code/layout-probe.js`.
- **Three consecutive image-and-text splits.** Two is the cap; the third is a different family or it fails. TST-11.
- **Two accents and two themes.** One accent for the whole page, one theme for the whole page. TST-31 and TST-32.
- **Decoration standing in for design.** Scroll cues, locale and weather strips, section numbering, middle dots as the default separator, coloured dots with no state behind them, pills over photographs, build strings in a marketing footer. TST-20 through TST-28.
- **The em-dash**, in any string a reader sees, alt text and button labels included. TST-38.
- **Two labels for one intent.** "Get in touch" in the nav and "Let's talk" in the footer is one action wearing two names. TST-39.

Every rule here came out of repeated rounds of generated landing pages, where these are the tells that survive a per-file review and only show up when the page is read whole.

---

## Macrostructure (non-templated web UI)

The deep web-UI generation engine. It makes pages read as made, not generated, by enforcing structural variety — two briefs never share the same hero → capabilities → CTA → footer rhythm — through a macrostructure pick, a theme (a catalog of 21, or a bespoke OKLCH + free-font route for creative briefs), and a 57-gate slop test with pre-emit self-critique. 

Read `references/hallmark/SKILL.md` first — it is the engine's own router and drives the whole flow, loading the rest of `references/hallmark/references/` on demand (macrostructures, themes, genres, components, anti-patterns, slop-test, responsive, study).

One default behaviour and three verbs:
- **default** — the user wants something new built. Run the engine's Design flow, or its Component-scope flow when the brief is a single element.
- **audit** `<target>` — score existing code against the anti-patterns and return a ranked punch list; edit nothing. `references/hallmark/references/verbs/audit.md`.
- **redesign** `<target>` — rebuild the visual structure inside the existing implementation boundaries, preserving routes, copy intent, brand, and information architecture. `references/hallmark/references/verbs/redesign.md`.
- **study** `<screenshot | URL>` — extract a design's DNA (macrostructure, type pairing, colour anchor), diagnose it, then optionally build with it or lock a portable `design.md`. `references/hallmark/references/study.md`.

Activate for: building a new app or landing page, "make this look less like AI", redesigning how a page looks, auditing a UI for slop, extracting a design's DNA from a reference, or when the user names Macrostructure or types audit / redesign / study.

The **intelligence**, **polish**, and **code** domains still own token systems, animation craft, and shadcn/Tailwind patterns; reach across them when a build needs both. Principle 4 holds here too — every headline, label, and paragraph macrostructure writes goes through the `avoid-ai-writing` skill.

---

## Logo

55+ styles, 30 color palettes, 25 industry guides. Gemini Nano Banana models.

### Generate a design brief

```bash
python3 ~/.sunday/profile/skills/design-checklist/scripts/logo/search.py "tech startup modern" --design-brief -p "BrandName"
```

### Search styles / colors / industries

```bash
python3 ~/.sunday/profile/skills/design-checklist/scripts/logo/search.py "minimalist clean" --domain style
python3 ~/.sunday/profile/skills/design-checklist/scripts/logo/search.py "tech professional" --domain color
python3 ~/.sunday/profile/skills/design-checklist/scripts/logo/search.py "healthcare medical" --domain industry
```

### Generate with AI

Generate on white — the model draws a cleaner mark against a white field than against
nothing — and the background comes off before delivery. `generate.py` runs
`scripts/logo/transparent.py` on every render and writes the transparent twin beside it;
that transparent file is the deliverable, and the white render stays only as a preview.
Gate AST-01 reads the alpha channel and the corner pixels, so a mark handed over on white
fails the run.

```bash
python3 ~/.sunday/profile/skills/design-checklist/scripts/logo/generate.py --brand "TechFlow" --style minimalist --industry tech
python3 ~/.sunday/profile/skills/design-checklist/scripts/logo/generate.py --prompt "coffee shop vintage badge" --style vintage
```

**IMPORTANT:** When scripts fail, fix them directly.

After generation, build the HTML gallery using `intelligence` + `polish`. Do not ask first.

Deeper: `references/logo-design.md`, `references/logo-style-guide.md`, `references/logo-color-psychology.md`, `references/logo-prompt-engineering.md`.

---

## CIP (Corporate Identity Program)

50 deliverables (business cards, letterheads, signage, vehicle wraps, uniforms, swag) across industries and styles, with HTML mockup output.

### Generate a CIP brief

```bash
python3 ~/.sunday/profile/skills/design-checklist/scripts/cip/search.py "tech startup" --cip-brief -b "BrandName"
```

### Search domains

```bash
python3 ~/.sunday/profile/skills/design-checklist/scripts/cip/search.py "business card letterhead" --domain deliverable
python3 ~/.sunday/profile/skills/design-checklist/scripts/cip/search.py "luxury premium elegant" --domain style
python3 ~/.sunday/profile/skills/design-checklist/scripts/cip/search.py "hospitality hotel" --domain industry
python3 ~/.sunday/profile/skills/design-checklist/scripts/cip/search.py "office reception" --domain mockup
```

### Generate

```bash
# Single deliverable
python3 ~/.sunday/profile/skills/design-checklist/scripts/cip/generate.py --brand "TopGroup" --logo /path/to/logo.png --deliverable "business card" --industry "consulting"

# Full set
python3 ~/.sunday/profile/skills/design-checklist/scripts/cip/generate.py --brand "TopGroup" --logo /path/to/logo.png --industry "consulting" --set

# Higher-quality model
python3 ~/.sunday/profile/skills/design-checklist/scripts/cip/generate.py --brand "TopGroup" --logo logo.png --deliverable "business card" --model pro

# Without a brand logo asset
python3 ~/.sunday/profile/skills/design-checklist/scripts/cip/generate.py --brand "TechFlow" --deliverable "business card" --no-logo-prompt
```

Models: `flash` (default, `gemini-2.5-flash-image`), `pro` (`gemini-3-pro-image-preview`).

### Render HTML preview

```bash
python3 ~/.sunday/profile/skills/design-checklist/scripts/cip/render-html.py --brand "TopGroup" --industry "consulting" --images /path/to/cip-output
```

Deeper: `references/cip-design.md`, `references/cip-style-guide.md`, `references/cip-deliverable-guide.md`, `references/cip-prompt-engineering.md`.

---

## Slides (HTML presentations)

Strategic HTML presentations with Chart.js, design tokens, responsive layouts, copywriting formulas.

Load `references/slides-create.md` for the creation workflow.

Slide copy is dense with words a person reads under time pressure, so before presenting any deck, invoke the `avoid-ai-writing` skill and hold every headline, bullet, and speaker note to it. The copywriting formulas below shape the message; the `avoid-ai-writing` pass is what keeps the result from sounding generated.

| Topic | File |
|---|---|
| Creation guide | `references/slides-create.md` |
| Layout patterns | `references/slides-layout-patterns.md` |
| HTML template | `references/slides-html-template.md` |
| Copywriting | `references/slides-copywriting-formulas.md` |
| Strategies | `references/slides-strategies.md` |
| Slide types index | `references/slides.md` |

---

## Banner (social, ads, web hero, print)

22 art-direction styles across social, ads, web, print.

Load `references/banner-sizes-and-styles.md` for complete sizes and styles reference.

### Workflow

1. **Read the brief for what it already says** — purpose, platform, content, brand, style, quantity. Take the defaults from the project's own brand and tokens for anything it does not say, and state the assumption in one line at the end. Do not stop to ask.
2. **Direction** — pull from `intelligence` (palettes/typography) + `brand`
3. **Design** — HTML/CSS banner; generate visuals with `ai-artist`/`ai-multimodal` if available
4. **Export** — screenshot to PNG at exact dimensions
5. **Deliver** — the exported files, with the run's filled checklist

### Quick size reference

| Platform | Type | Size (px) |
|---|---|---|
| Facebook | Cover | 820 × 312 |
| Twitter/X | Header | 1500 × 500 |
| LinkedIn | Personal | 1584 × 396 |
| YouTube | Channel art | 2560 × 1440 |
| Instagram | Story | 1080 × 1920 |
| Instagram | Post | 1080 × 1080 |
| Google Ads | Med Rectangle | 300 × 250 |
| Website | Hero | 1920 × 600–1080 |

### Top styles

| Style | Best for |
|---|---|
| Minimalist | SaaS, tech |
| Bold typography | Announcements |
| Gradient | Modern brands |
| Photo-based | Lifestyle, e-com |
| Geometric | Tech, fintech |
| Glassmorphism | SaaS, apps |
| Neon/Cyberpunk | Gaming, events |

### Design rules

- Safe zones: critical content in central 70–80%
- One CTA per banner, bottom-right, min 44px height
- Max 2 fonts, min 16px body, ≥32px headline
- Text under 20% for ads (Meta penalizes)
- Print: 300 DPI, CMYK, 3–5mm bleed
- Every headline, tagline, and CTA is held to the `avoid-ai-writing` skill before export — banner copy is few words at high visibility, exactly where a tell does the most damage

---

## Icon (SVG, Gemini 3.1 Pro)

15 styles, 12 categories. Gemini 3.1 Pro Preview generates SVG text output.

### Single icon

```bash
python3 ~/.sunday/profile/skills/design-checklist/scripts/icon/generate.py --prompt "settings gear" --style outlined
python3 ~/.sunday/profile/skills/design-checklist/scripts/icon/generate.py --prompt "shopping cart" --style filled --color "#6366F1"
python3 ~/.sunday/profile/skills/design-checklist/scripts/icon/generate.py --name "dashboard" --category navigation --style duotone
```

### Batch variations

```bash
python3 ~/.sunday/profile/skills/design-checklist/scripts/icon/generate.py --prompt "cloud upload" --batch 4 --output-dir ./icons
```

### Multi-size export

```bash
python3 ~/.sunday/profile/skills/design-checklist/scripts/icon/generate.py --prompt "user profile" --sizes "16,24,32,48" --output-dir ./icons
```

Deeper: `references/icon-design.md`.

---

## Social photos (multi-platform HTML→screenshot)

Multi-platform social images: HTML/CSS → screenshot export. Uses **brand**, **system**, **intelligence**.

Read: `references/social-photos-design.md`.

Workflow:
1. **Brand inputs** — pull from `references/brand/`
2. **Token inputs** — pull from `references/system/`
3. **Direction** — pick style/palette/typography from `references/intelligence.md`
4. **Design** — build HTML per idea × platform size
5. **Polish** — apply `references/polish.md` checklist
6. **Copy check** — invoke the `avoid-ai-writing` skill on every caption, overlay line, and hashtag set; a tell baked into an exported image cannot be edited later
7. **Export** — render to images via headless browser

---

## Cross-domain workflows

Common bundles:

- **Brand launch** — brand → logo → cip → system (digital tokens) → social-photos (launch images)
- **Product UI** — intelligence (direction) → polish (micro) → code (implementation) → system (tokens)
- **Pitch deck** — brand (voice) → intelligence (palette/fonts/chart types) → slides (creation)
- **Campaign** — brand → intelligence → banner (multi-platform) → social-photos (companion images)

---

## Coordination with other skills

- **`avoid-ai-writing`** — required companion, not optional. Any deliverable that carries words — deck, banner, caption, brand document, UI string — gets that skill invoked on its copy before it ships. This is principle 4 above; it applies in every domain, every time.
- **Redesigning existing UI** is the `redesign` verb of the macrostructure engine above, which reaches across `intelligence`, `polish`, and `code` from here.
- **Fields and dropdowns** are covered here, in `references/code/fields-and-dropdowns.md` — field surface and states, native versus custom selects, the menu surface, option states, the keyboard contract, and pickers. The FLD gates check it.
- **`stack-checklist`** — the wiring sibling. It asks whether a thing is present and alive; this skill asks how it looks. It hands findings here by name, and anything found here about a key, a service, a branch rule or a missing component goes back the other way.
- **`clean`** — for structure, naming, and dead code. Pair when a redesign also needs file moves or splits.
- **`commit`** — never run git directly. Invoke only when the user explicitly asks to commit, push, or ship.

## Where this checklist ends

Four checklists govern a project and each owns one question. This one owns what a reader
sees.

| Found this | Goes to |
| --- | --- |
| it looks wrong, is misaligned, or the palette fights itself | stays here |
| a route carries no title, description or share card | `/seo-checklist` |
| it is slow, the bundle is enormous, the fonts block | `/perf-checklist` |
| a key, a service, a branch rule or a missing component is not wired up | `/stack-checklist` |

Hand a finding over rather than fixing it here, and say so in the report. A finding
dropped because it belonged to somebody else is the one nobody comes back for.

### The TaylorURL status bar

The standard footer bar every site carries is **Split Rail**: a hairline above it,
attribution and mark on the left, live status and build on the right, 42px tall,
detached from whatever real footer the site has and carrying no client links.

Its whole design contract is that it names no colour of its own. Every tone is mixed from
the ink it inherits — `color-mix(in oklab, currentColor 92%, transparent)` for the ink,
the label beside it at seventy-four percent, the hairline at thirteen, the wash at four —
which darkens a light ground and lightens a dark one without being told which it is
looking at. The ground stays transparent and no tone is a system colour: `Canvas` and its
siblings follow the browser's colour-scheme preference rather than the page, which is how
a bar ends up white under a dark site. `--tu-accent` starts at `currentColor` and
retargets the one accent for a palette it fights.

That contract is what this skill holds it to, and it is why a per-project restyle of the
bar is a defect rather than a customisation: there is one bar, and changing it changes
every site at once. Whether it is present, current and pointing at something that
answers is `/stack-checklist`.

## Reference index

| Path | Content |
|---|---|
| `references/brand/` | Brand voice, identity, messaging (from former `brand` skill) |
| `references/system/` | Design tokens, specs (from former `design-system` skill) |
| `references/code/` | shadcn/Tailwind/Radix patterns, accessibility, theming (from former `ui-styling` skill) |
| `references/intelligence.md` | UI/UX intelligence library (from former `ui-ux-pro-max` skill) |
| `references/polish.md` | Polish philosophy & animation framework (from former `emil-design-eng` skill) |
| `references/navigation-menus.md` | Navigation/menu animation — Disney's 12 principles applied to nav bars, menus, sidebars, wayfinding |
| `references/logo-*.md` | Logo design, style guide, color psychology, prompt engineering |
| `references/cip-*.md` | CIP design, style guide, deliverable guide, prompt engineering |
| `references/slides-*.md` + `references/slides.md` | Slides creation, layouts, template, copy, strategies |
| `references/banner-sizes-and-styles.md` | Banner platform sizes + style catalog |
| `references/icon-design.md` | Icon style catalog + generation guidance |
| `references/social-photos-design.md` | Multi-platform social image workflow |
| `checklist/gates/*.json` | The gate registry — every rule in this skill, as data |
| `checklist/README.md` | How the gates are written, scoped, and checked |
| `scripts/logo/transparent.py` | Strips the generation background; delivers the mark with alpha |
| `scripts/code/skeleton-probe.js` | Measures a placeholder against the content that replaces it |
| `scripts/code/spacing-probe.js` | Measures the space between rendered siblings |
| `scripts/code/layout-probe.js` | Measures headline wrap, hero fold, nav rows, and bar height |
| `references/marketing-surfaces.md` | What a landing page owes that an app screen does not |
| `references/code/fields-and-dropdowns.md` | Field and menu styling, states, and the keyboard contract |
| `references/code/tables-and-headers.md` | Table scan, header rhythm, and spacing relationships |
| `scripts/{logo,cip,icon,brand,system,code}/` | Generation/automation scripts per domain |
| `templates/{brand,system}/` | Reusable templates |
| `data/{logo,cip,icon,system}/` | Domain data (style lists, palettes, presets) |
| `canvas-fonts/` | Font assets for canvas/poster generation |
