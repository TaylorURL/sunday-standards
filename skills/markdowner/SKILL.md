---
name: markdowner
description: >-
  Go through a project's Markdown files and make them accurate, well-formatted,
  and clear — verifying every factual claim against the actual code, config, and
  file tree, then aligning structure and prose to the conventions of a strong,
  complete README. Use whenever the user runs /markdowner, or asks to "fix the
  README", "clean up the docs", "check my markdown", "is the README accurate",
  "update the documentation", "the docs are out of date", "make the README
  look professional", "align the markdown", or otherwise wants Markdown
  reviewed, corrected, reformatted, or brought up to standard — whether they
  name a specific file or mean every Markdown file in the project. Trigger even
  when the request is vague ("the readme's a mess", "these docs are stale") as
  long as it concerns Markdown accuracy, formatting, or clarity.
---

# Markdowner

Documentation is a promise the code has to keep. A README that says `npm start`
when the script is `npm run dev`, or describes a flag that was removed two
releases ago, is worse than no README — it sends the reader confidently in the
wrong direction. This skill exists to make a project's Markdown *true*, *legible*,
and *consistent*: every claim checked against reality, every file shaped like it
belongs to the same project, every sentence as clear as its subject allows.

You are optimizing for the person who opens this file cold — a new contributor,
a future maintainer, the user six months from now. Accuracy comes first; nothing
else matters if the information is wrong. Formatting and clarity come next,
because a correct document nobody can follow still fails its reader.

## Scope: find the files, read the context

`/markdowner` may name a target ("fix the README", "the docs in `docs/`") or
none at all ("clean up the markdown"). Settle scope before editing:

- **Specific target**: confine the pass to the named file(s) and anything they
  directly reference (a README that links to `CONTRIBUTING.md`, a doc that
  embeds a code sample from `src/`).
- **Whole-project**: every Markdown file in the tree (`.md`, `.mdx`, `.markdown`),
  minus generated and vendored paths — `node_modules`, `dist`, `build`,
  `.next`, `vendor`, anything in `.gitignore`, and auto-generated API docs. Find
  them with a quick sweep (e.g. `find . -name '*.md' -not -path '*/node_modules/*'`).

Note what kind of document each file is — a root README, a contributing guide, a
changelog, an architecture doc, an ADR, a sub-package README — because the
standard each is held to differs. A changelog is not restructured like a README;
an ADR has its own shape. Don't force every file into the same mold.

## Always survey and plan before editing

Rewriting documentation is easy to get subtly wrong: you can "simplify" away a
load-bearing caveat, or reformat a file into a house style it was never meant to
follow. And a half-edited set of docs — three files polished, five untouched —
reads as inconsistent on purpose. So survey the whole scope, present a plan, then
execute.

### 1. Survey

- **Ground truth**: this is the core of the skill. Open the things the docs make
  claims about — `package.json` (scripts, dependencies, versions, bin names,
  engine requirements), config files, the actual directory structure, entry
  points, environment-variable usage, CLI definitions. You cannot verify a
  README against your assumptions; you verify it against the repo.
- **The document set**: read every Markdown file in scope. Note the current
  structure of each, the voice, the formatting conventions already in use, and
  which files are strong (use them as the internal reference) versus thin or
  stale.
- **A reference standard**: if the project has one genuinely good, complete
  document, align the others toward its conventions. If none exists, align
  toward the canonical README anatomy below. The goal is one coherent project
  voice, not one imposed from outside.

### 2. Present the plan

Lay out, per file, what you intend to change — grouped as accuracy fixes
(highest value, list them specifically: "README says `yarn build`, actual script
is `npm run build`"), structural changes, and clarity edits. Flag anything you're
uncertain is safe to remove or rephrase, and anything destructive (deleting a
whole section, merging files). Scale the plan to the request — a single stale
README warrants a few lines and a quick confirm; a whole-project docs sweep
warrants a real per-file breakdown. Get a go-ahead before large rewrites.

### 3. Execute, then verify

Work the plan file by file, finishing each completely. Then run the verification
in the last section.

---

## The three priorities

### 1. Accuracy — verify every claim against the repo

This is the reason the skill exists. Treat every factual statement in the docs as
a claim to be checked, not prose to be polished. The failure mode to hunt for is
documentation that has quietly drifted from the code.

Check, against the actual project:

- **Commands**: every install, build, test, run, and deploy command. Do the
  scripts exist in `package.json` (or Makefile, `pyproject.toml`, etc.)? Is the
  package manager right (`npm` vs `pnpm` vs `yarn`)? Does the documented invocation
  match the real one?
- **Paths and names**: file paths, directory names, module names, the project/
  package name itself, binary names. Do the referenced paths exist? Broken
  internal links and references to renamed or deleted files are common and
  corrosive.
- **Code examples**: do imports resolve, do function signatures and arguments
  match the current API, are option names and defaults right? An example that
  no longer runs is a bug in the docs.
- **Configuration and environment**: documented config keys, env vars, and their
  defaults against what the code actually reads.
- **Versions and requirements**: language/runtime versions, dependency versions,
  engine requirements — against `package.json`, lockfiles, `.nvmrc`, CI config.
- **Features and behavior**: does the described behavior match what the code does?
  Features that were removed, renamed, or changed are the hardest drift to catch
  and the most damaging.
- **Links and badges**: internal links resolve to real anchors/files; badge URLs
  point at the real repo/CI/registry, not a template's placeholder.

When a claim is wrong, fix it to match reality. When you genuinely can't verify
something (it depends on external state, or the intent is ambiguous), say so in
your summary rather than inventing a confident correction. Never "fix" a document
into agreement with a guess — an authoritative-sounding wrong answer is the worst
outcome here.

### 2. Formatting and structure — shape it like a document that belongs

Well-formatted docs are scannable: a reader finds what they need without reading
linearly. Align structure and formatting to strong conventions, and make every
file in the project feel like part of the same whole.

- **README anatomy**: a complete root README generally moves in this order —
  title and one-line description; badges (build, version, license) if the project
  uses them; a short "what and why" paragraph; install; usage/quickstart with a
  runnable example; configuration; a fuller feature or API section as needed;
  contributing; license. Not every project needs every section, and the order
  bends to the project — but a README that opens with a wall of API tables before
  saying what the thing *is* has its priorities inverted. Lead with what the
  reader needs first.
- **Table of contents**: add one for long documents (roughly past a screen or two
  of headings); it's noise on a short one.
- **Heading hierarchy**: exactly one H1 (the title), no skipped levels (`##` then
  `####`), headings that describe their section. Fix documents with multiple H1s
  or erratic nesting.
- **Code blocks**: fenced, with a language tag for syntax highlighting
  (` ```bash `, ` ```ts `). Inline code (backticks) for commands, filenames,
  flags, and identifiers mentioned in prose. Shell examples shouldn't include the
  `$` prompt if the output isn't shown — it defeats copy-paste.
- **Lists, tables, links**: one consistent bullet marker per file; tables for
  anything genuinely tabular (options, env vars, flags) instead of parallel
  bullet lists; descriptive link text over bare URLs and "click here".
- **Consistency across files**: the same terminology, capitalization of proper
  nouns (the project's own name, product names), code-fence conventions, and
  tone across every Markdown file. Divergent style between two docs in one repo
  is friction with no upside.

Respect the project's own good conventions rather than imposing a personal
house style — if the existing strong docs use a particular structure, extend it.

### 3. Clarity — simplify what's needlessly hard, keep what's precisely technical

The user's guidance here is the balance to strike: **simplify where applicable,
but technicality matters in some scenarios.** These pull in opposite directions
and the judgment is the whole job.

Simplify when the complexity is in the *writing*, not the subject:

- Bloated prose, throat-clearing intros, and marketing fluff that delays the
  information ("In today's fast-paced world…"). Cut to what the reader needs.
- Convoluted sentences that could be a list, a table, or three short sentences.
- Jargon or internal shorthand used where a plain word would do just as well and
  reach more readers.
- Redundancy — the same instruction stated three times, sections that repeat each
  other.

Preserve — and sharpen — technicality when the precision *is* the information:

- Exact commands, flags, paths, signatures, version constraints, and config
  semantics. "Just run the build" is not an improvement on `npm run build --
  --target=node18`. Precision here is a feature, not clutter.
- Necessary caveats, edge cases, security notes, and ordering constraints ("must
  run migrations before starting the server"). "Simplifying" these away is a
  regression — a caveat dropped is a support ticket created.
- Domain-correct terminology where the audience is technical and the precise term
  is the right one. Don't dumb down an API reference written for engineers into
  vague approximations.

The test: does the edit make the document *easier to act on correctly*? If it
reads more smoothly but a reader could now do the wrong thing, you cut too much.
When unsure whether a detail is load-bearing, keep it — the cost of an extra
true sentence is far lower than the cost of a missing constraint.

---

## Respect the project's Markdown hygiene rules

Some conventions are worth enforcing as you go, because they keep the doc set
sane:

- **One README per project, at the root.** Don't create or keep `README.md`
  variants inside subdirectories; consolidate documentation that belongs together.
  (Sub-package READMEs in a genuine monorepo are the exception — each package root
  may have its own.)
- Don't invent documentation the project doesn't have and didn't ask for. This
  skill improves what exists and fills genuine gaps in accuracy; it isn't a
  mandate to generate a docs site.

---

## Verify before you're done

Documentation you've edited should be checked like code:

1. **Re-verify the fixes**: the corrections you made should themselves be right —
   re-check a sample of the commands/paths/versions you changed against the repo.
   Don't trade one wrong claim for another.
2. **Links resolve**: internal links and anchors point at things that exist;
   relative file links match the real tree after any moves.
3. **It renders**: the Markdown is valid — fenced blocks are closed, tables are
   well-formed, no broken heading or list syntax. If the project has a Markdown
   linter (`markdownlint`, `remark`) or a formatter (Prettier), run it.

Then give a concise, scannable summary: the accuracy corrections (these matter
most — name them), the structural and formatting changes, and anything you
flagged as unverifiable or deliberately left alone. The user should be able to
review the pass without re-reading every file.
