# Sunday standards

Checklists and standards for [Sunday](https://github.com/TaylorURL/sunday),
published from the profile they are used in daily.

## Adding them

    sunday profile add https://github.com/TaylorURL/sunday-standards.git

They load underneath your own profile, so a rule, checklist or skill of yours
with the same name wins. Nothing here replaces what you already have.

## What is here

Four checklists — design, SEO, performance and database — each a set of gates a
run has to answer before work lands, and the engine that runs them.

The writing and comment standards, a cleanup pass, a Markdown pass, and the
smaller skills that shape how work is stated rather than what it does.

Two rules: nothing lands naming an assistant as its author, and browsing goes
through the in-app browser.

`tools/` holds the programs those skills and rules call. A skill arriving
without the program it runs fails on the machine it lands on, so the two travel
together. The four `*-pass.py` entries there are thin wrappers: each checklist's
real engine ships inside its own skill, beside the gates it reads, and the
wrapper only finds it. The rest stand alone: the writing and comment ledgers,
the documentation ledger, the run sweep, the version and badge steps, and a
preflight that refuses to build from a checkout a sibling has moved past.

## What is not here

Anything answering to one company's own services, hosts, clients or schedules.
The stack checklist is the clearest example and it stays where it is: it holds
a project against one particular footer, one status page and one set of
services, which is worth nothing on somebody else's machine.

Some gates cite real cases by name — a site that shipped share cards pointing
at its deployment host, another that hardcoded a year as a string. Those are
what the gate is for, told through what went wrong.
