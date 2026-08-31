---
name: perf-checklist
description: Drive loading and responsiveness fixes into a project's own files - redirects, compression, caching, bundle splitting, duplicate dependencies, the critical path to first paint, fonts, responsive images, main-thread work and Core Web Vitals - as a gate checklist that cannot close while anything is unanswered, and that proves the page still renders exactly as it did. Use whenever the user runs /perf-checklist, or asks to "speed up this site", "improve the PageSpeed score", "fix Core Web Vitals", "why is my site slow", "reduce the bundle size", "improve LCP", "fix INP", "the site takes forever to load", "make it load faster", "optimise performance", "my Lighthouse score is bad", "reduce Total Blocking Time", "code split this", "lazy load the images", or otherwise wants a site made faster. Works on whatever project it is pointed at - HTML, Vite, Next.js, Astro, SvelteKit, Nuxt, Vue, or a React SPA. This is an instruction to change the files, never to produce an audit, a score, or a list of recommendations, and never to change what a reader sees.
argument-hint: "[path] [--url https://host] [--scope delivery|js|render|media|inp|measure]"
---

# perf-checklist

Every performance rule this skill knows lives as a gate in `checklist/gates/*.json`, and
`bin/perf-pass.py` decides which of them apply from what the project actually contains,
settles what a script can settle, and refuses to close while anything is unanswered.

## Two things hold this together

**This skill acts.** It does not produce a score, does not hand back a prioritised list
of findings, and does not report what it would do. Most performance tooling fetches a
URL and grades it, which names what is wrong and leaves the work undone, so the next
run finds the same list. Every check here reads the project's own source and its build
output, because that is the only place a finding can be fixed.

**Nothing a reader sees may change.** Every rule is a change to how bytes reach the
browser, never to what those bytes describe. A route is split, an image is offered at
more widths, a slide is expressed as a transform: the reader sees the page they saw
before, sooner. That invariant is what lets this run unattended, and it is the easiest
thing here to break by accident, so it is measured rather than promised. The rendered
page is captured before the work and again after; any element that moved, any computed
style that changed, any route that stopped rendering, any error that appeared holds the
run open.

The second rule outranks the first. A faster page that looks different is a failed run.

## A score is not a diagnosis

Two numbers travel under the word performance and confusing them wastes days.

The **lab score** is Lighthouse run once on a simulated slow connection. It is
reproducible, it is dominated by loading, and nobody experienced it. On a
JavaScript-heavy page it swings by tens of points between consecutive runs, which is
wider than most of the improvements this checklist produces - so every measurement here
is a median of several.

The **field record** is the Chrome UX Report: real visits over the previous 28 days at
the 75th percentile. It is what describes the site and what search ranks.

A site can sit at 95 in the lab and be rated poor in the field. So the first thing a
run does is read the field record and name the metric that is actually failing:

```bash
scripts/psi.py measure --url https://<host> --runs 3 --out before.json
```

If that says INP, no amount of image work will move it. Loading fixes and main-thread
fixes are different halves of this checklist and only one of them is your problem.

## The run protocol

**A gate that is not met is work to do.** The only ways past one are changing the
project, or naming the condition that puts the gate out of scope. A gate the sweep
failed cannot be recorded as passing, and a gate marked fixed reopens if the next sweep
still fails it.

### 0. Find the tool

It ships inside this skill, so it sits beside this file:

```bash
PP="$(dirname "$(realpath "${BASH_SOURCE:-$0}")")/bin/perf-pass.py"
```

On a machine with the synced config that is
`~/.sunday/profile/skills/perf-checklist/bin/perf-pass.py`. If neither resolves, the skill
was installed without its `bin/` directory and the gates cannot run - say so rather than
proceeding by eye.

### 1. Open the run

```bash
perf-pass.py start --kind <site|app|spa|docs|store|landing> --target <path> --url https://<host>
```

It prints the gates that apply, derived from what the project contains - router gates
when there is a router, font gates when there are fonts, animation gates when something
animates. The URL is what the delivery gates read: redirects, compression, cache
headers and time to first byte cannot be answered from a repository.

A `PostToolUse` hook opens a run when this skill is invoked. Unlike its siblings,
editing a file does **not** open one - a stylesheet edit is not a request to have a
whole site's loading behaviour checked.

### 2. Take the baseline and the before capture, before touching anything

Both are unanswerable after the fact, so a `PreToolUse` hook refuses to edit a source
file until both exist.

```bash
scripts/psi.py measure --url https://<host> --runs 3 --out before.json
perf-pass.py measure --file before.json --label before
perf-pass.py scan --metric <the metric psi named>
```

Then the page itself, at a phone width and a desktop width, across every route:

```bash
node scripts/capture.js --url https://<host> --out before-capture.json --built
perf-pass.py parity --phase before --file before-capture.json
```

`capture.js` drives Chrome over the DevTools protocol using nothing but what Node
ships with. It discovers the routes from the first page's own links, or takes them as
`--route` arguments.

Where the site is not deployed yet, or the change should be proved before it ships,
`scripts/lighthouse.py` runs the same engine locally against a preview server. It
answers the lab half; only PSI can read the field record.

All three of those reach Chrome, and Chrome is refused on every machine here with no
exemption and no override, so on any machine carrying `chrome-guard.py` they do not
run. That is not a run that stalls: a machine with nothing to render with cannot take
a reading, and the run records the absence rather than waiting for one.

```bash
perf-pass.py uninstrumented --reason "chrome-guard refuses every rendering engine on this machine"
```

That stands the edit guard down and lets each parity gate take `unmeasured` with its
own reason, and the report carries the gap so it is read rather than inferred. The
field record and the lab score go unread on such a run; say so in the report rather
than substituting a number from somewhere else.

### 3. See what the project actually ships

```bash
perf-pass.py routes
scripts/bundle-probe.py chunks --root .
scripts/bundle-probe.py deps --root .
perf-pass.py verify
```

`routes` lists every route and what the build weighs. `chunks` shows what the entry
document pulls and what it defers. `deps` names duplicated, unused and server-only
dependencies. `verify` is the sweep, with the file and line of each failure.

Half the gates read the build rather than the source, and the two differ by everything
the bundler did. **Build first.** A stale build answers those gates about a page nobody
is served, and the sweep says so before anything else.

### 4. Change the project until the sweep passes

This is the work. Not a plan for the work.

Read `references/` for the substance behind any gate; each gate names its source file.
The shape of most fixes:

- **A blank shell** is the single largest cost on a client-rendered site. Nothing paints
  until the bundle has downloaded, parsed, executed and rendered. Prerendering the routes
  at build time emits exactly the markup the client would have produced.
- **One chunk** means a visitor to the home page downloads the checkout and the admin
  panel. Route components move behind a dynamic import, with a fallback that occupies
  the same space the route will.
- **A hero drawn as a CSS background** cannot be discovered until the stylesheet naming
  it has parsed and can carry no fetch priority. An `img` with `fetchpriority="high"`
  shows the same picture.
- **One image for every device** sends a desktop file to a 390 point screen. `srcset`
  and `sizes` change which file is chosen and nothing else.
- **A WebGL field or a scroll effect** that never stops competes with every interaction
  for the length of the visit. Cancelling it off-screen keeps the effect and returns the
  thread.

### 5. Prove the page did not change, and that something got faster

Build, serve the build, and capture it again at the same routes and widths:

```bash
node scripts/capture.js --url http://localhost:4173 --out after-capture.json --built
perf-pass.py parity --phase after --file after-capture.json
perf-pass.py parity --diff
```

`--diff` names every element that moved, vanished, or changed computed style. Then the
numbers, taken the same way as the baseline:

```bash
scripts/psi.py measure --url https://<host> --runs 3 --out after.json
perf-pass.py measure --file after.json --label after
```

The parity gates cannot be answered by hand. `pass` and `na` are both refused on them:
an attestation that the page looks the same is exactly the thing the captures replace.

### 6. Answer every gate

```bash
perf-pass.py verify
perf-pass.py status --full
perf-pass.py resolve --batch - <<'JSON'
[{"id": "JSB-01", "status": "fixed", "note": "17 routes moved behind React.lazy; first load 204KB -> 61KB"},
 {"id": "IMG-07", "status": "na",    "note": "no embeds; the only iframe is the map on /contact, behind a click"}]
JSON
```

`fixed` for a gate whose failure you removed. `na` for one the tool brought in wrongly,
with the condition that puts it out of scope. `disputed` for a check that measured
wrongly, with what you measured instead - it closes the gate so one bad check cannot jam
a build, and it leads the report under its own heading. Answer in batches: the sweep
settles what a script can settle in seconds, and the rest is round trips. A batch with
one bad row is refused whole.

Every file under the targets ends either changed or explicitly ruled as needing no
performance change, and a file cannot be cleared until it has actually been read:

```bash
perf-pass.py files
perf-pass.py file-clear --batch - <<'JSON'
[{"path": "src/lib/format.js", "note": "read in full; three pure string helpers, nothing on the critical path"}]
JSON
```

### 7. Report and close

```bash
perf-pass.py budget --write
perf-pass.py report
perf-pass.py finish
```

`budget --write` records the current weights as the ceiling, keeping the lower of the
existing and the new one so recording after a regression cannot raise it. `report`
renders the filled checklist with the before and after numbers and the parity result.
`finish` refuses while anything is open. A run that changed nothing closes with
`finish --no-deliverable`, and that works only when the run edited nothing - a file
whose content is back to what git has counts as untouched.

## Running one part of it

A run answers for the whole project by default. A scope narrows it, out loud:

```bash
perf-pass.py scopes
perf-pass.py start --kind spa --target . --url https://<host> --scope js
perf-pass.py scan --scope all
```

The named scopes are delivery, js, render, media, inp, measure and parity. **Parity is
never narrowed out**: it answers for every change the run made, whatever the run scoped
to. Every report leads with the narrowing and with what it did not look at.

## The API key

`scripts/psi.py` uses the PageSpeed Insights API, which is free. Without a key it runs
against a shared anonymous quota that is usually exhausted, so it wants one - the free
tier is 25,000 queries a day and the same key reads the field record.

On this setup the key is in CryptoFort as `google-pagespeed-api-key`. Read it there at
the point of use and pass it through the environment; it does not go in a file, a repo,
or the synced config:

```bash
GOOGLE_PAGESPEED_API_KEY=<from CryptoFort> scripts/psi.py measure --url https://<host>
```

## What holds this in place

- A `PostToolUse` hook on `Skill` opens a run when the skill is invoked.
- A `PreToolUse` hook on `Write` and `Edit` refuses a source edit while a run is open and
  the baseline or the before capture is missing. Both are unanswerable afterwards, so a
  rule saying to capture first would be a reminder; refusing the first edit is what makes
  the capture exist.
- A `PostToolUse` hook on `Read` and `Bash` credits a file in the ledger once it is read.
- A `Stop` hook refuses to end the session while the run is open.
- A `PreToolUse` hook holds back a commit and a PR while a gate is unanswered, and names
  the parity gates separately when those are the ones open.
- PRC-03 names every route sitting outside the run's targets, so scoping to the page the
  prompt mentioned has to be argued for rather than assumed.

### What a gate cannot be answered with

Five routes out of a gate are closed, because each turned a checklist into a survey:

- **`pass` on a gate the sweep failed.**
- **`na` on a gate the sweep failed.** The sweep failing is proof the condition is
  present and unmet, which is the opposite of inapplicable.
- **`na` while the tool can still see the condition.** A gate enters a run because its
  condition was found in the project. If it is still there, not-applicable contradicts
  the tool rather than the gate.
- **A note with no evidence.** An assertion is not a note. It has to name a file, a line,
  a measurement, or quote what was read.
- **Any hand answer on a parity gate.** Those answer to the captures and to nothing else.

## Where this checklist ends

Four checklists govern a project and each owns one question. This one owns how long a
visitor waits: bytes, the critical path, the main thread, and the three Core Web Vitals.

| Found this | Goes to |
| --- | --- |
| the bundle is enormous, the fonts block, an image is unsized | stays here |
| the page looks wrong, or a change here would cost the appearance | `/design-checklist` |
| a route carries no title, description or share card | `/seo-checklist` |
| a service is paused, a key is wrong, a deploy never built | `/stack-checklist` |

The last row matters more here than anywhere. A site can be slow because the bundle is
badly split, and it can be slow because production is serving a three-week-old
deployment or a third party stopped answering. Those are wiring, and no amount of code
splitting moves them.

Hand a finding over rather than fixing it here, and say so in the report.

## What this skill does not do

It does not redesign, restyle, rewrite copy, cut anything the site does, or drop an
effect to make
a number move. Where the only way past a gate would cost the appearance, the gate is
answered `na` with that reason and the appearance wins.

It does not chase the lab score. Where a rule can only be settled by field data, the
gates check the causes in source, which are the part that can be changed - and the run
reports which metric it set out to fix and whether it moved.
