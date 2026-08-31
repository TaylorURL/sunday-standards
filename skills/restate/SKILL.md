---
name: restate
description: >-
  Say back what the ask actually is, in plain English, before any of it gets
  built. Use whenever the user runs /restate, or says "repeat that back",
  "tell me what you think I'm asking", "what did you understand", "make sure
  you've got this", "before you start, say it back", "did that make sense",
  "am I being clear", or otherwise wants understanding confirmed rather than
  work started. Also use unprompted at the top of any build big enough that a
  misread costs more than a paragraph - a new skill, a new page, a schema
  change, anything touching more than one project.
allowed-tools: Bash, Read, Glob, Grep, Agent
argument-hint: "[the ask, if it is not already in the conversation]"
---

# Say it back first

A misread caught in a paragraph costs a paragraph. The same misread caught
after the build costs the build, and it costs it twice, because the wrong
thing has to come out before the right thing goes in.

This skill is the paragraph.

## What this skill forbids

Nothing is created, edited, committed, published, or deployed while it runs.
Not a file, not a branch, not a scratch draft, not a quick start on the easy
part. Reading is fine and encouraged. The deliverable is prose, and a run that
produced a file did not follow this skill.

That restriction is the point of invoking it. The user reached for it because
they wanted the reading checked before paying for it.

## Read before speaking

A restatement written from the prompt alone is a paraphrase of the prompt, and
it confirms nothing except that the words were received. Ground it first:

- Open the thing being talked about. The repo, the page, the skill, the table.
- Check the pieces the ask assumes already exist. Half of all misreadings are a
  wrong belief about what is already there.
- Where the ask names something by a nickname - "our day plan skill", "the
  status page", "the usual flow" - go and read that thing. Guessing at what a
  nickname points to is the misread this skill exists to catch.

A broad sweep goes to agents rather than thirty inline reads.

## Then say it back

Six things, in this order, and nothing else:

1. **The point.** One sentence on the outcome being chased, not the task list.
   An ask whose point resists a single sentence has a problem, and that is the
   first thing to say.
2. **The pieces.** Each distinct deliverable, one line each, their words
   translated into different ones.
3. **What reads as out of scope.** The near neighbours being deliberately left
   alone. This catches the "I assumed you would also" failure, which no amount
   of restating the ask itself will catch.
4. **The calls about to be made unilaterally.** Every decision the ask left
   open that the run intends to settle on its own, with the answer picked.
   These matter most: nobody objects to a choice they never saw being made,
   and this is the only moment it is cheap.
5. **What is needed from them, and when it blocks.** Credentials, access, a
   decision only they can make. Naming when it blocks is what tells them
   whether to answer now or later.
6. **That the work is proceeding.** Unless the ask was explicitly "just tell me
   what you heard", the restatement is a checkpoint rather than a gate. Say the
   work carries on unless corrected, then carry on.

## How to write it

**Paraphrase, never echo.** Repeating their sentence in their own words proves
the words arrived, not that they landed. Say the same thing in different words,
at a different altitude, with the implied parts made explicit. Against "lean
into Google heavy", the restatement says what leaning in concretely means, and
they get to say no.

**Plain English.** No jargon they did not use first, no library names, no file
paths, no schema, no code. Someone who has never seen the codebase can follow
it. Identifiers belong in the work, not the read-back.

**Concise.** Under a page. The sixth item is one line. A pieces list running
past eight means the ask needs splitting, and that is worth saying out loud.

**One pass at the uncertainty.** Flag the ambiguity that would change the work,
pick the reading that looks right, and move. A restatement asking four questions
has handed the work back.

## What a good one catches

The restatement is working when the reply is "no, not that". So aim it where a
misread hides:

- A word naming two things. Which page. Which site. Which account.
- Scope that could be one project or all of them.
- A verb that could mean build, or could mean check.
- Work being planned that nobody asked for, and work they assume is included
  that nothing was planning to do.
- The shape of the deliverable: a page, a tool, a report, a change to something
  that already exists.

## When not to use it

A small, unambiguous ask does not need one. "Fix the typo on the pricing page"
restated is noise, and noise trains the reader to skip the restatement on the
day it would have mattered. Reach for it when the ask is large, when it is
vague, when it spans projects, or when it names something by a nickname.
