---
name: seo-checklist
description: Drive every SEO rule into a project's own files - crawlability, head metadata, share cards, document structure, structured data, images, loading, content credibility, AI readers, hreflang and local business signals - as a gate checklist that cannot close while anything is unanswered. Use whenever the user runs /seo-checklist, or asks to "do the SEO", "fix the SEO", "optimise this for search", "add meta tags", "add schema markup", "write a robots.txt", "generate a sitemap", "why isn't this ranking", "make this show up on Google", "add Open Graph tags", "fix the meta descriptions", "get this into AI search", "optimise for AI Overviews", "add llms.txt", "fix Core Web Vitals", "add alt text", "add hreflang", "local SEO", or otherwise wants a project made findable. Works on whatever project it is pointed at - HTML, Next.js, Astro, SvelteKit, Nuxt, Vue, or a React SPA. This is an instruction to change the files, never to produce an audit, a score, or a list of recommendations.
argument-hint: "[path] [--flag international|local|ecommerce|editorial]"
---

# seo-checklist

Every SEO rule this skill knows lives as a gate in `checklist/gates/*.json`, and
`bin/seo-pass.py` decides which of them apply from what the project actually contains,
settles what a script can settle, and refuses to close while anything is unanswered.

## This skill acts

`/seo-checklist` is an instruction to change the project, not to grade it. It does not
produce a score, does not hand back a prioritised list of findings, and does not report
what it would do. It reads what is there, writes the missing markup and the missing
files, and hands back the filled checklist.

That distinction is the whole point. Most SEO tooling fetches a URL and scores it,
which names what is wrong and leaves the work undone — and the next crawl finds the
same list. Every check here reads the project's own source, because that is the only
place a finding can actually be fixed.

Where the brief is silent, the project answers: its existing metadata, its brand, its
routes. Where nothing answers, take the most conservative option that satisfies the
gate and state the assumption in one line at the end — after the work, not instead of
it.


## Running one part of it

A run answers for the whole project by default. A scope narrows it, out loud:

```bash
seo-pass.py scopes                                  # the named scopes
seo-pass.py start --kind site --target . --scope meta
seo-pass.py scan --scope all                        # widen it again
```

`/seo-checklist meta` runs the head-metadata gates and nothing else — thirteen
instead of sixty-eight. The named scopes are crawl, meta, social, schema,
structure, images, speed, content, and local.

Every place a scoped run is shown leads with the narrowing and with what it did
not look at. Editing a crawlable file opens a run over that file alone; only
invoking the skill opens one over the whole project.

## The run protocol

**A gate that is not met is work to do.** The only ways past one are changing the
project, or naming the condition that puts the gate out of scope. A gate the sweep
failed cannot be recorded as passing, and a gate marked fixed reopens if the next
sweep still fails it.

### 0. Find the tool

It ships inside this skill, so it sits beside this file:

```bash
SP="$(dirname "$(realpath "${BASH_SOURCE:-$0}")")/bin/seo-pass.py"
```

On a machine with the synced config that is
`~/.sunday/profile/skills/seo-checklist/bin/seo-pass.py`. If neither resolves, the skill
was installed without its `bin/` directory and the gates cannot run — say so rather
than proceeding by eye.

### 1. Open the run before writing anything

```bash
seo-pass.py start --kind <site|page|app|docs|store|local-business|blog> --target <path> --title "<what this is>"
```

It prints the gates that apply, derived from what the project contains — article gates
when there are articles, product gates when there are products, image gates when there
are images.

Four conditions cannot be read out of source, because a single-locale site and one
whose translations are not built yet look identical. Declare them:

```bash
--flag international    # the site serves more than one locale
--flag local            # the site is a business with a physical place
--flag ecommerce        # the site sells things
--flag editorial        # the site publishes dated articles
```

Opening the run is not a decision. A `PostToolUse` hook opens one when this skill is
invoked, and another opens one the moment a crawlable surface is edited — head
metadata, a template, robots.txt, a sitemap — whether the skill was invoked or not.
The only thing left to you is scoping it properly.

### 2. See what the project actually has

```bash
seo-pass.py pages     # every route, its title, its description, its word count
seo-pass.py verify    # the automated sweep, with the file and line of each failure
```

`pages` is worth reading before anything else. It is where a React SPA with seven
routes and one title becomes visible.

### 3. Change the project until the sweep passes

This is the work. Not a plan for the work.

Four gates are satisfied by files that do not exist yet, and `scripts/emit.py` writes
them from what the project already contains rather than from a template:

```bash
scripts/emit.py robots  --root <path> --site-url <url> --ai training --write
scripts/emit.py sitemap --root <path> --site-url <url> --write
scripts/emit.py llms    --root <path> --site-url <url> --name "<site>" --summary "<one line>" --write
scripts/emit.py schema  --type organization --name "<name>" --site-url <url> --logo <url> --script
```

The sitemap reads the router config rather than the file tree, so a view component
mounted at `/order-success` is listed there and not at the path its directory implies,
and a view the router never mounts is left out instead of published as a 404. Run every
one of these without `--write` first and read the output.

`--ai training` blocks the crawlers that only feed model training and leaves the
fetchers that produce citations alone. `--ai block`, `--ai allow` and `--ai silent`
are the other three stances. Pick one deliberately — the gate is that the choice was
made, not which way it went.

The rest is markup, written into the project's own templates: titles and descriptions
per route, canonicals, the Open Graph set, JSON-LD, alt text, image dimensions, `defer`
on the scripts, `font-display` on the fonts.

Read `references/` for the substance behind any gate. Each gate names its source file.

### 4. Answer every gate

```bash
seo-pass.py verify
seo-pass.py status --full        # every open gate, with its rule, its fix, and what the sweep saw
seo-pass.py resolve --batch - <<'JSON'
[{"id": "HED-04", "status": "fixed", "note": "wrote a 152-character description for every route"},
 {"id": "SCH-05", "status": "na",    "note": "no product pages; the site sells nothing"}]
JSON
seo-pass.py status
```

`--status fixed` for a gate whose failure you removed. `--status na` for one the tool
brought in wrongly, with the condition that puts it out of scope. Answer in batches: the sweep settles what a script can settle in seconds, and the rest is round trips. Every row keeps its own status and note, and a batch with one bad row is refused whole. `--status pass` is
refused where the sweep says otherwise.

Every file under the targets ends either changed or explicitly ruled as needing no SEO
change, and a file cannot be cleared until it has actually been read:

```bash
seo-pass.py files
seo-pass.py file-clear --batch - <<'JSON'
[{"path": "src/lib/api.ts", "note": "read in full; fetch wrappers, nothing a crawler sees"}]
JSON
```

### 5. Report and close

```bash
seo-pass.py report    # the filled checklist, shown in full
seo-pass.py finish
```

`finish` refuses while anything is open. A run that produced no crawlable change closes
with `finish --no-deliverable`, and that works only when the run edited nothing — a
file whose content is back to what git has counts as untouched.

## What holds this in place

- A `PostToolUse` hook on `Skill` opens a run when the skill is invoked.
- A `PostToolUse` hook on `Write` and `Edit` opens one when a crawlable surface is
  edited, so SEO work done without invoking the skill is still under the checklist.
- A `PostToolUse` hook on `Read` and `Bash` credits a file in the ledger once it has
  been read, so an unopened file and a considered one stop looking alike.
- A `Stop` hook refuses to end the session while the run is open.
- A `PreToolUse` hook holds back `git commit` and `gh pr create` while a gate is
  unanswered, so the markup cannot land ahead of the checklist.
- PRC-02 names every route sitting outside the run's targets, so scoping to the page
  the prompt mentioned has to be argued for rather than assumed.


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

## Where this checklist ends

Four checklists govern a project and each owns one question. This one owns whether
anybody finds the thing: crawlability, head metadata, share cards, structure, structured
data, and what an AI reader gets.

| Found this | Goes to |
| --- | --- |
| a route with no title, description, canonical or share card | stays here |
| the page looks wrong, or the type and spacing fight each other | `/design-checklist` |
| it is slow, the bundle is enormous, the fonts block | `/perf-checklist` |
| a key, a service, a branch rule or the TaylorURL bar is not wired up | `/stack-checklist` |

Share cards are this checklist's, including `og:image`. The favicon, the apple-touch
icon and the manifest are not — those are identity rather than metadata, and
`/stack-checklist` holds them.

Hand a finding over rather than fixing it here, and say so in the report. A finding
dropped because it belonged to somebody else is the one nobody comes back for.

## What this skill does not do

It does not fetch live URLs, query rankings, pull backlink data, or call a paid SEO
API. Those produce reports, and a report is the thing this skill exists to replace.
Where a rule can only be settled by field data — the three Core Web Vitals are measured
on real visitors at the 75th percentile — the gates check the causes in source, which
are the part that can be changed.

Nothing here is a recommendation. If a gate applies and the project fails it, the
project changes.
