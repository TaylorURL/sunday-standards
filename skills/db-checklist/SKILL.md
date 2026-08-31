---
name: db-checklist
description: Drive a project's database and its code into agreement - tables and functions nothing reads any more, deployed functions with no source, scheduled jobs firing at work that has been removed, row-level security and grants, bloat and unpruned housekeeping tables, statements slow enough to time out their neighbours, and whether every table traces back to a migration - as a gate checklist that cannot close while anything is unanswered. Use whenever the user runs /db-checklist, or asks to "check the database", "are there unused tables", "clean up the schema", "does the database match the code", "why is the database so big", "check RLS", "is anything still writing to X", "audit the schema", "find dead tables", "what is this table for", "check the cron jobs", "is anything unused in Supabase", or otherwise wants the database held against the code rather than read on its own. This is an instruction to change the database and the repository, never to produce an audit or a list of recommendations.
---

# The database checklist

A feature is removed from an application in an afternoon. Its schema stays for a
year.

Nothing breaks, so nothing reports it. The tables keep their rows, the edge
functions keep answering, the scheduled jobs keep firing, and every one of those
reads as healthy from any angle you can see from inside the repository. The only
symptoms are a bill nobody can account for and, eventually, an error on a page
that has nothing to do with any of it - because a relation nobody looks at has
grown large enough that the queries running alongside it start hitting the
statement timeout.

That is the failure this checklist exists to catch, and it is invisible to both
halves on their own. A schema read says a table exists. A repository read says a
name is absent. Only the pairing says a table is standing that nothing reads.

## Run it

```bash
$(sunday tool db-pass.py) start --target <path> --project-ref <ref>
~/.sunday/profile/skills/db-checklist/scripts/probe.py all --root <path>
$(sunday tool db-pass.py) probe --file <the path the probe printed>
$(sunday tool db-pass.py) verify | status --full | tables
$(sunday tool db-pass.py) resolve --batch - | report | finish
```

`--project-ref` may be left off when the repository names one; the probe records
which file it took the ref from, so a wrong guess is visible rather than silent.

The probe needs `SUPABASE_ACCESS_TOKEN` in the environment at the point of use.
Pull it from the vault and pass it on the command; this skill never stores a
credential, and the probe scrubs anything key-shaped out of its own output before
writing it.

## What it will not let you do

**Answer a gate the probe failed.** A gate whose verdict came back `fail` cannot
be recorded as `pass` or `na`. Change the database and re-verify, which records
`fixed`, or dispute the reading and say why.

**Attest to something the probe answers.** The gates in the orphan, access,
health and provenance groups refuse `pass` and `na` outright. Their whole subject
is outside the repository: a table created by hand in the dashboard is invisible
to any number of migration files read carefully, so nothing but a query against
the catalogue settles them.

**Skip a table.** Every table in the probe ends either dropped or explicitly kept
with its reader named. A table nobody looked at and a table considered and kept
are indistinguishable afterwards, and the second is the whole point of the run.

**Drop without a backup.** A run that dropped anything stays open until it records
where the rows went. This is the one verb here with no undo.

**Close quietly.** The `Stop` hook refuses to end a session with a run open, and
the `PreToolUse` hook refuses `git commit` and `gh pr create` while a gate is
unanswered.

## The groups

**PRC - Run Protocol.** The bookkeeping that stops the checklist becoming a
survey: the run was opened before the work, the database was read rather than
reasoned about, every table was ruled on, nothing was dropped without a backup,
findings belonging to another checklist were handed over.

**ORP - What The Code No Longer Reads.** Tables with no reader. Deployed functions
with no source in the repository, and deployed functions with no caller. Scheduled
jobs pointing at things that are gone. Database functions nothing calls. And the
same drift from the other side: code reading a table that no longer exists, which
is the half that fails at runtime rather than quietly.

**SEC - Who Can Reach What.** Every table in the public schema is served over HTTP
the moment it exists, so row-level security is not something to switch on later.
RLS on every table, a policy behind it, no blanket `true` standing in for one, the
anonymous role reaching only what a signed-out visitor should, and no service-role
key behind a client-side prefix.

**HLT - What The Instance Is Carrying.** Relations that are mostly empty space,
because a delete frees room for reuse and never gives it back. Housekeeping tables
nothing prunes. Tables autovacuum has stopped reaching. Statements slow enough to
queue their neighbours. Tables rewritten far more than they are read. Replication
slots holding write-ahead log for a reader that has gone. Indexes never scanned.

**MIG - Where The Schema Came From.** Every table created by a migration, every
migration applied, and every destructive migration saying where the rows went.

## Where the findings go

This checklist asks one question: does the database match what the code does. A
service that will not answer at all belongs to `/stack-checklist`; how long a page
takes belongs to `/perf-checklist`. Each is named through `delegate --to` and
carried in the report, never resolved here and never dropped. PRC-05 holds the run
open until a handover or `delegate --none` is recorded.

## After a drop

Removing a table is a schema change like any other: it goes into
`supabase/migrations/` and lands through a pull request. Apply it, then re-run the
probe - the run's verdicts are only as current as the last sweep, and a gate
marked fixed reopens if the next one still fails it.
