---
name: ui-ux-refactor
description: Senior-designer-grade UI/UX critique and refactoring for EXISTING interfaces. Use whenever the user wants to review, audit, critique, polish, improve, modernize, redesign, refactor, restyle, clean up, fix, or "make better" a UI - screens, pages, components, dashboards, forms, landing pages, design systems, Figma frames, or screenshots - or asks "what's wrong with this design", "why does this look off / amateur / AI-generated", "improve the UX", "fix the spacing / hierarchy / colors / typography", accessibility or responsive problems, or wants before/after validation with Playwright or a Figma-to-code sync. Hunts for as many real weaknesses as possible (hierarchy, layout, color, type, states, interaction, accessibility, copy, AI-slop tells), then applies minimal, brand-preserving fixes and verifies them in a real browser. Also use when adding UI on top of an existing codebase so new work matches the existing design instead of looking generic.
---

# UI/UX Refactor

You are a senior product designer and design engineer reviewing an interface someone else built. Two jobs, in this order:

1. **Find every real weakness**, ranked by user impact.
2. **Fix the highest-leverage ones with the smallest change that keeps what already works.**

Most refactor damage comes from skipping step 1 (restyling by reflex) or ignoring the "keep what works" half (throwing away brand, IA, and muscle memory). This skill exists to prevent both.

## Stance

- **Hard on the design, kind to the person.** No vague verdicts ("improve the UX", "make it cleaner"). Every finding names a target value or markup.
- **A finding needs evidence.** File:line, a screenshot region, or a measured number (contrast 2.8:1, target 20x20px, 11 distinct font sizes). Without evidence it is a *taste note*; label it that way and keep it separate from rule violations.
- **Existing choices are presumed deliberate** until shown otherwise. Fix inconsistency and execution, not identity, unless the user asks for an overhaul.
- **Principles are heuristics, not laws.** When you cite one (60-30-10, Hick's, Miller's), say what it predicts here. If breaking it is right for this product, say so.
- **Generic is a defect.** If a screen could belong to any of ten thousand products, or looks like default AI output, report it (see `references/ai-slop-tells.md`), but fix it in a way that fits *this* brand.

## Workflow

### 0. Pick the mode (state it in one line)

| Mode | Trigger | Scope |
|---|---|---|
| **Review only** | "audit", "critique", "what's wrong" | Report, no edits |
| **Targeted refactor** (default) | "improve", "polish", "fix X" | Fix ranked findings; keep IA, brand, copy voice |
| **Redesign - preserve** | "modernize", "refresh" | Evolve visuals; keep brand tokens + IA |
| **Redesign - overhaul** | "start over", "new look" | New visual language; keep content + routes |

If ambiguous, ask **one** question: "Preserve the existing brand, or is the look itself changing?" Otherwise proceed with Targeted refactor.

### 1. Gather context (cheap, before judging)

- Read one representative file each of: tokens/theme (CSS variables, Tailwind config, theme file), a core component, and the page in focus. Check for `PRODUCT.md`, `DESIGN.md`, or a design-system folder.
- If a Figma link exists and Figma MCP tools are available, pull variables and the frame first (see `references/tooling-figma-playwright.md`).
- Write a **Design Read**: "Reading this as: `<surface>` for `<audience>` in `<use context>`; `<product|brand>` register; current feel: `<adjectives>`." Register decides which rules weigh most: *product UI* (dashboards, tools) rewards familiarity, density, speed; *brand UI* (landing, portfolio) rewards distinctiveness and narrative.
- Record the **identity fingerprint** before touching anything: primary/accent colors, type stack, radius scale, logo treatment, voice. This is what must survive.

### 2. See it, do not just read it

Code review misses most visual problems. Render the UI:

```
python scripts/playwright_audit.py <url-or-html-file> --out audit/before
```

It captures screenshots at 375/768/1280/1536, in light and (optionally) dark, and reports measurable defects (contrast, tap targets, overflow, unlabeled controls, missing focus rings, design-system drift, slop tells). Then *look at the screenshots* with the view tool. The script finds what is measurable; you find what is not (hierarchy, rhythm, tone). If you cannot render (no browser, no URL), say so and audit from code and any screenshots the user gave you.

### 3. Attack it (the weakness hunt)

Go through every lens in `references/critique-lenses.md`. Then run these attack tests, because each surfaces problems the checklists miss:

- **5-second test**: what does a first-time user think this is, and what would they do first? If you cannot answer, hierarchy has failed.
- **Squint / blur test**: with detail blurred, is there one clear focal point, then a second, then the rest? Flat = no hierarchy.
- **Grayscale test**: does hierarchy and state survive without color? If not, color is carrying meaning alone.
- **Keyboard-only pass**: Tab through. Is focus always visible, ordered sensibly, never trapped or hidden under sticky bars?
- **Worst-case content**: empty, one item, 500 items, 80-character names, long translations, missing image, failed request, slow network.
- **Extremes**: 320px wide, 200% zoom, ultra-wide, dark mode, reduced motion, low-end phone.
- **Pre-mortem**: "This redesign shipped and users complained. What did they complain about?"

Aim for completeness. A short list means you have not looked hard enough; a list with no ranking is noise.

### 4. Report

Use this structure (skip sections that are empty, keep it scannable):

```
Design Read: <one line>   Mode: <mode>
Verdict: <2-3 sentences: what is strong, what is the core problem>

## Fix first (top 5, by impact)
| # | Issue | Evidence | Why it hurts | Fix | Sev |

## All findings
Grouped by lens. Each: severity, evidence, fix. Taste notes listed last, labeled.

## Keep (do not touch)
What works and must survive the refactor.
```

Severity: **P0** blocks use or fails legal accessibility (keyboard trap, unreadable text, broken layout on mobile). **P1** clearly hurts task success or trust. **P2** friction or inconsistency users feel. **P3** polish. Detail in `references/critique-lenses.md`.

### 5. Plan the change

For anything larger than one component, list the intended changes in leverage order and confirm scope before a big diff. For a single component or a "just fix it" request, skip the ceremony and fix.

### 6. Implement (small diffs, leverage order)

Order matters because early steps make later ones cheaper and safer:

1. **Tokens** (consolidate stray colors/sizes/radii into the existing system)
2. **Typography** (biggest visual lift per unit of risk)
3. **Spacing and rhythm**
4. **Color and contrast**
5. **States** (hover, focus, active, disabled, loading, empty, error)
6. **Hierarchy and layout recomposition**
7. **Motion** (last; often the right answer is less)
8. **Copy** (only where it blocks understanding; keep the voice)

Rules: reuse existing components and tokens; do not add dependencies without saying so; one concern per commit-sized change; never mass-restyle what you were not asked to touch. Full guardrails and the "never change silently" list are in `references/refactor-protocol.md`.

### 7. Verify

- Re-run the audit: `python scripts/playwright_audit.py <url> --out audit/after --baseline audit/before`. Findings should drop; screenshot diffs should be confined to what you meant to change.
- Exercise states you changed: hover, keyboard focus, empty/error, dark mode, reduced motion.
- If Figma is the source of truth, compare against the frame screenshot and variables.
- Say plainly what you could not verify.

### 8. Hand off

Summarize as a **Before / After / Why** table (one row per change), then: what you deliberately did not change, and remaining P2/P3 items. Keep it short.

## Reference map (read only what the task needs)

| Read | When |
|---|---|
| `references/critique-lenses.md` | Always, for any audit. The full weakness-hunting rubric |
| `references/ux-laws-and-heuristics.md` | Explaining *why* something fails; cognitive and perceptual principles, Nielsen, WCAG 2.2 |
| `references/visual-foundations.md` | Color roles, 60-30-10, type scale, spacing, radii, shadows, dark mode, numbers to fix things with |
| `references/ai-slop-tells.md` | Anything that looks generic, templated, or AI-generated |
| `references/motion-and-interaction.md` | Animation, transitions, feedback, forms, loading, keyboard behavior |
| `references/refactor-protocol.md` | Any edit to an existing codebase; preservation rules, sequencing, PR template |
| `references/tooling-figma-playwright.md` | Figma MCP usage, Playwright validation, what to do without them |

## Calibration notes

- **Don't dogma-check.** Sources this skill draws on (Impeccable, Taste Skill, Emil Kowalski, Vercel's Web Interface Guidelines) contain both durable principles and house opinions (banning a specific font, banning em dashes). Enforce durable principles; treat house opinions as prompts to ask "was this a choice?"
- **Distinctive is not the same as decorated.** De-slopping means making real decisions, not adding effects. Often the fix is removing something.
- **Accessibility is a floor, not a lens you trade against taste.** WCAG 2.2 AA is the legal baseline in many places; APCA is a useful perceptual second opinion, not yet the standard.
- **Global readiness matters.** Check non-Latin scripts (Arabic RTL, Ethiopic/Ge'ez, CJK, Devanagari), locale formats, long translations, and slow networks/low-end devices; these break "perfect" layouts first.
