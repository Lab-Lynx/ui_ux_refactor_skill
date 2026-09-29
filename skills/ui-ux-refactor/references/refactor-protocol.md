# Refactor protocol

How to change an existing UI without breaking what already works. The most common redesign failures are losing brand identity, silently changing IA/URLs/analytics, regressing accessibility, and producing a diff too large to review.

## Contents
- Audit before touching
- Identity fingerprint
- Preservation rules
- Never change silently
- Leverage order (what to change first)
- Targeted evolution vs full redesign
- Diff discipline
- Design-system consolidation
- Regression risks and checks
- Hand-off template

## Audit before touching

Document the current state before proposing changes:

- **Brand tokens**: primary/accent colors, neutrals, type stack, logo treatment, radii, shadows.
- **Information architecture**: page tree, primary nav, key conversion paths, URL patterns.
- **Content blocks**: what exists, what does work, what is filler.
- **Patterns to preserve**: signature interactions, recognizable hero, copy voice, anything users have learned.
- **Patterns to retire**: slop tells, broken layouts, dead links, generic stock imagery, performance traps.
- **Dial reading** of the current design (rough 1-10 for each): *variance* (symmetry to asymmetry), *motion* (static to cinematic), *density* (airy to packed). This is your starting point, not a baseline to overwrite.
- **Baseline metrics and screenshots**: run the Playwright audit and keep the `before` folder. Also note SEO (ranking pages, meta titles, structured data, OG cards) and analytics events, since these are the top redesign risks.

## Identity fingerprint

Write down, in a few lines, what makes this product recognizable: colors, type, shape language (sharp/soft), density, voice, one or two signature moments. After refactoring, check the fingerprint against the result. If someone who knew the product would not recognize it, and the user did not ask for that, you over-changed.

## Preservation rules

- Extract brand colors and fonts from the code before applying any palette advice. A brand that is already purple stays purple; fix how it is used, not that it is purple.
- Keep copy voice unless asked to rewrite. Visual modernization is not a content rewrite.
- Honor existing accessibility wins. Do not regress focus states, alt text, keyboard navigation, or contrast.
- Respect existing components and conventions in the codebase. Use them; extend them; do not create parallel ones.
- Do not add dependencies (animation libs, icon packs, UI kits) without stating why and getting agreement.

## Never change silently

Ask or flag before modifying:

- URL structure, route slugs, anchor IDs
- Primary nav labels and order
- Form field names, order, and validation semantics (breaks analytics, autofill, backend)
- Analytics event names and `data-*` hooks, test IDs (`data-testid`), element IDs used by scripts
- Brand logo or wordmark
- Legal, consent, and cookie copy
- Pricing, plan names, or claims
- Anything that changes an API contract or data shape

## Leverage order

Apply in this order; stop when the brief is satisfied. Earlier steps make later ones cheaper, and they carry the least risk per unit of visual lift.

1. **Tokens**: consolidate stray hex, font sizes, radii, spacing into the existing token set (or create a minimal set if none exists).
2. **Typography**: scale, weights, line height, measure. Usually the biggest visible improvement.
3. **Spacing and rhythm**: move to the scale; fix proximity; add vertical rhythm.
4. **Color and contrast**: fix failing pairs; give the accent one job; define semantic colors.
5. **States**: hover, focus-visible, active, disabled, loading, empty, error, success.
6. **Hierarchy and layout recomposition**: restructure the top of the funnel and key screens.
7. **Motion**: add only motivated motion; remove gratuitous motion; honor reduced motion.
8. **Copy**: fix only what blocks understanding.
9. **Full block replacement**: only when the existing block is unsalvageable.

## Targeted evolution vs full redesign

- IA, content, and SEO sound and visuals just dated/inconsistent: **targeted evolution** (levers 1-5). Typically most of the value at a fraction of the risk.
- Structural visual debt (no design system, broken mobile, chaotic layouts) but content is good: **redesign with strict content preservation**.
- The brand itself is changing: treat as greenfield for visuals; still preserve IA, URLs, and content unless told otherwise.

## Diff discipline

- One concern per change (tokens, then type, then spacing...). Reviewers should be able to verify each step against the audit.
- Change the source of truth (tokens, base components) rather than patching call sites.
- Prefer deleting overrides and one-off styles to adding new ones.
- Do not reformat unrelated files. Do not rename things for taste.
- If a change would exceed roughly a few hundred lines of visual diff, split it or confirm scope first.
- Where possible, ship behind a flag or in a preview branch for side-by-side review.

## Design-system consolidation

1. Inventory computed values (the audit script reports font sizes, families, colors, radii, shadows).
2. Cluster near-duplicates (three grays that are "the same").
3. Map each cluster to a token; add a token only if none fits and the value is used in 3+ places.
4. Replace stray values with tokens, starting from base components.
5. Add a lint or grep check to prevent regression (for example, forbid raw hex outside the tokens file).
6. Document the tokens and rules in `DESIGN.md` (colors with roles, type scale, spacing scale, radii, elevation, components, do/don't).

## Regression risks and checks

| Risk | Check |
|---|---|
| Layout breaks at some viewport | Screenshots at 375/768/1280/1536 vs baseline |
| Contrast regressions | Audit script contrast section, both themes |
| Focus/keyboard regressions | Tab through key flows; audit focus-indicator check |
| Analytics/tests break | Grep for changed IDs, classes, `data-*`; run test suite |
| SEO regressions | Titles, headings, canonical/meta unchanged; slugs unchanged |
| Performance regressions | LCP/CLS/INP, image and font weight, animation cost |
| Dark mode or reduced-motion broken | Emulate `prefers-color-scheme` and `prefers-reduced-motion` |
| Copy/i18n overflow | Long strings, non-Latin scripts, RTL if supported |

## Hand-off template

```
## UI refactor: <surface>
Mode: <targeted | preserve | overhaul>   Design Read: <one line>

### Findings addressed
| # | Issue | Sev | Before -> After |

### What changed (by leverage step)
1. Tokens: ...
2. Typography: ...

### Deliberately not changed
- <IA / URLs / brand / copy> and why

### Verification
- Playwright audit: <N> findings -> <M>; screenshots in audit/before, audit/after
- Manually checked: keyboard flow, dark mode, reduced motion, 375px
- Could not verify: <...>

### Follow-ups (P2/P3)
- ...
```
