# Critique lenses: the weakness-hunting rubric

Work through every lens. For each: ask the attack questions, note failures with evidence, assign severity. Skip a lens only if it truly does not apply, and say so.

## Contents
- Severity scale
- Evidence standard
- 1 First impression and purpose
- 2 Visual hierarchy
- 3 Layout, alignment, spacing
- 4 Typography
- 5 Color and contrast
- 6 Components and consistency (design-system drift)
- 7 States and edge cases
- 8 Interaction and feedback
- 9 Forms and data entry
- 10 Navigation, IA, wayfinding
- 11 Copy and microcopy
- 12 Accessibility
- 13 Responsive and adaptive
- 14 Performance as UX
- 15 Trust, emotion, distinctiveness
- 16 Global readiness
- 17 Motion
- Consistency audit method

## Severity scale

- **P0** Blocks use or fails baseline accessibility: keyboard trap, text unreadable (<3:1), content cut off or horizontally scrolling on mobile, primary action unreachable, destructive action with no confirm/undo.
- **P1** Clearly hurts task success or trust: weak/absent hierarchy on a key screen, primary CTA unclear, no focus indicator, tap targets <24px, missing error handling, form loses data, misleading copy.
- **P2** Friction or inconsistency users feel: contrast 3-4.5:1 on body text, inconsistent spacing/radii, missing empty state, layout shift, cramped or ragged rhythm.
- **P3** Polish: optical alignment, easing choices, minor copy tightening, icon stroke mismatch.
- **Taste note**: subjective preference. Never mix with the above.

## Evidence standard

Every finding: `where` (file:line, selector, or screenshot region) + `what you measured or saw` + `why it hurts a user` + `specific fix` (target value or markup). "Increase contrast" is not a fix; "change `--muted` from #9aa0a6 to #5f6368 on #fff (2.6:1 to 6.1:1)" is.

## 1. First impression and purpose

Attack: Can a stranger say what this is, who it is for, and the one thing to do next within 5 seconds? Is there a clear primary action? Does the first viewport show real value or just decoration? Does it look like the product's category leader or like a template?
Common failures: vague headline, hero that is only atmosphere, two competing primary CTAs, product hidden behind marketing copy, no visible proof.

## 2. Visual hierarchy

Attack: What is noticed first, second, last, and is that the right order? Count things shouting (bold + color + size + shadow). Does size, weight, color, and position agree on importance, or fight? Are secondary and tertiary actions visibly quieter than primary?
Common failures: everything the same weight; five equally loud buttons; heading barely larger than body (aim for a clear ratio, e.g. 1.25x steps); decorative elements out-shouting content; important info in low-contrast small text.
Method: squint/blur test; count distinct emphasis levels (should be ~3-4, not 8).

## 3. Layout, alignment, spacing

Attack: Does every element align to something (grid, baseline, edge, optical center)? Is spacing from a scale or arbitrary? Does proximity group related things and separate unrelated ones (label near its field, section gaps larger than intra-section gaps)? Is everything centered by default? Is whitespace generous where it aids focus and tight where density is needed?
Common failures: inconsistent padding between similar cards; mixed alignment (centered heading over left-aligned text); off-by-a-few-pixels misalignments; equal spacing everywhere (no rhythm); cards nested in cards; content edge-to-edge with no max width; text lines >75ch.
Method: overlay a 4/8px grid mentally; list distinct padding/margin/gap values (should be a short scale).

## 4. Typography

Attack: Is there a clear type scale with few sizes (roughly 5-7)? Body >=16px on web (>=14px only for dense secondary UI)? Line height 1.4-1.6 body, 1.1-1.3 headings? Line length 45-75ch? Are weights purposeful (2-3)? Do font pairings contrast on a clear axis or clash as near-twins? Are numbers in tables tabular? Is the typeface right for the product's feeling (serif traditional/editorial, sans modern/tech, mono for code/data)?
Common failures: 10+ font sizes; all-caps long text; light gray thin text; centered paragraphs; tight tracking on display text (below -0.04em); orphans/widows in headings (`text-wrap: balance`); straight quotes and `...` instead of typographic ones; italic descenders clipped by tight line-height.

## 5. Color and contrast

Attack: Is there a clear color strategy (restrained / committed / full palette / drenched) or accidental color? Does the accent mark only what matters (actions, links, key data)? Are there defined roles (brand, neutral ramp, semantic success/warning/danger/info, surfaces)? Is meaning ever carried by color alone? Do interaction states raise contrast? Does dark mode work as designed, not as an inversion?
Thresholds (WCAG 2.2 AA): body text 4.5:1; large text (>=24px, or >=18.66px bold) 3:1; UI components and focus indicators 3:1 against adjacent colors. Placeholder text needs 4.5:1 too.
Common failures: gray-on-gray "for elegance"; gray text on colored backgrounds (use a darker shade of that hue); brand color used for everything; red/green as only status signal; more than one accent hue with no roles; pure #000 on #fff glare; borders too faint to see.

## 6. Components and consistency (design-system drift)

Attack: Do same-purpose elements look and behave the same everywhere? How many distinct button styles, radii, shadows, font sizes, text colors exist? Are there one-off values that should be tokens? Do icons come from one family with one stroke width and size grid? Do inputs, selects, and date pickers share height, radius, and focus style?
Common failures: 6 radii and 4 grays that are "almost the same"; primary button differs between pages; icon stroke mismatch beside text; mixed corner styles (pill buttons, sharp cards); hard-coded hex values scattered through components.
Method: see Consistency audit method below.

## 7. States and edge cases

Attack: For each interactive element and data view: default, hover, focus, active/pressed, disabled, loading, success, error, empty, partial, offline, long-content, no-permission. Which are missing or undesigned?
Common failures: only the happy path designed; spinner with no context; skeletons that don't match final layout (layout shift); error text like "Something went wrong" with no exit; empty state that is a blank area instead of an invitation with a next step; disabled controls with no explanation; truncation with no way to read full text.

## 8. Interaction and feedback

Attack: Does every action give immediate, visible acknowledgment (press state, optimistic update, progress)? Are hit targets generous and non-finicky? Are destructive actions confirmed or undoable? Do links behave as links (open in new tab, right-click)? Do gestures have non-gesture alternatives? Are hover-only affordances available on touch?
Common failures: buttons with no `:active` state; `div` used as button; no loading indication after submit; double-submit possible; drag-only interactions; tooltips carrying essential information; hover-revealed actions invisible on mobile.
See `motion-and-interaction.md`.

## 9. Forms and data entry

Attack: Every field labeled (visible label, not placeholder-only)? Right input types, `autocomplete`, and mobile keyboards? Validation timing sensible (not on every keystroke, not only at submit)? Errors next to the field, specific, with a fix? Is submit ever pre-disabled with no explanation? Is pasting allowed (passwords, OTP)? Are required/optional marked? Is the form as short as it can be? Does it keep data on error and warn on unsaved leave?
Common failures: placeholder as label; errors only in a top banner; blocked keystrokes on numeric fields; no inline help; long single-column forms with no grouping or progress; multi-step flows with no way back.

## 10. Navigation, IA, wayfinding

Attack: Can users tell where they are, where they can go, and how to get back? Are labels in user language (not internal jargon)? Does the nav have too many items (Hick's Law)? Do URLs reflect state (filters, tabs, pagination) so Back/Refresh/Share work? Any dead ends (screens with no next step)? Is the current location marked with more than color?
Common failures: mystery-meat icons without labels; deep hidden settings; breadcrumbs missing in deep hierarchies; modals opening modals; "Continue" buttons with no destination hint.

## 11. Copy and microcopy

Attack: Are headings specific and benefit-led, not slogans ("Build the future of work")? Do buttons say what happens ("Save API key" beats "Continue")? Do errors explain cause and exit? Consistent nouns and tone? Any filler verbs (elevate, seamless, unleash)? Fake-precise numbers, "John Doe" data, "Acme" brands in shipped UI? Placeholder lorem left in?
Common failures: generic uplift phrases; passive voice; cute-but-unclear labels; inconsistent terminology for one concept; error messages that blame the user.
Keep the brand's voice; fix clarity, not personality.

## 12. Accessibility

Attack (WCAG 2.2 AA baseline): semantic HTML before ARIA; one h1 and logical heading order; every image has appropriate alt (empty for decorative); every control has an accessible name; visible, unobscured focus for every focusable element; full keyboard operability; skip link; target size >=24px (44px preferred on touch); dragging has an alternative; no info by color alone; text resizes to 200% without loss; reduced motion honored; live regions announce async updates; language attribute set; zoom never disabled.
Common failures: `outline: none` with no replacement; icon-only buttons without labels; low-contrast placeholder; focus hidden under sticky header; modals without focus trap/return; custom selects/menus with no ARIA pattern.

## 13. Responsive and adaptive

Attack: 320px, 375px, 768px, 1024px, 1440px, ultra-wide. Any horizontal scroll? Touch targets >=44px on mobile? Does the layout reflow meaningfully or just shrink? Are tables handled (scroll container, stacked cards)? Are fixed/sticky elements eating the viewport? Safe areas (notches) respected? Input font >=16px to prevent iOS zoom? Hover-only features gated with `(hover: hover)`?
Common failures: desktop layout scaled down; huge hero eating a phone screen; fixed heights clipping text; 100vh problems on mobile (use dvh); nav that wraps to two lines.

## 14. Performance as UX

Attack: Perceived speed: does content appear progressively? Layout shift (images without dimensions, late fonts, injected banners)? Is the largest element preloaded? Heavy animation on main thread? Big unoptimized images or autoplay video? Long tasks blocking input?
Targets: LCP < 2.5s, INP < 200ms, CLS < 0.1. Loading indicators should show after ~150-300ms and stay >=300-500ms to avoid flicker.

## 15. Trust, emotion, distinctiveness

Attack: Does it look credible for its category (finance, health, government need calm and clarity)? Real content and imagery, or stock/placeholder? Consistent polish everywhere, including error pages and emails? Does anything feel unchosen: default framework look, default icon set, default illustration style? Does it have a point of view? See `ai-slop-tells.md`.

## 16. Global readiness

Attack: Layout survives 30-40% longer strings and non-Latin scripts (taller line heights for Ethiopic/Ge'ez, Devanagari, Thai; RTL mirroring for Arabic/Hebrew)? Dates, numbers, currencies, calendars locale-aware? Fonts have fallback stacks covering target scripts? Icons/metaphors culturally safe? Works on low-end Android and slow/metered networks (image weight, font subsets, no giant JS)? Language chosen from user settings, not IP?

## 17. Motion

Attack: Does each animation have a purpose (feedback, spatial continuity, state change, explanation)? Are frequent actions animation-free? Durations under ~300ms for UI? Easing correct (ease-out for entrances)? Only transform/opacity animated? Reduced motion honored? Anything looping forever for no reason?
See `motion-and-interaction.md`.

## Consistency audit method

To measure drift objectively (the Playwright script reports most of this):

1. Collect computed values across the page: font sizes, font families, text colors, background colors, border radii, shadows, padding/margin/gap.
2. Cluster near-duplicates (#6b7280 vs #6c757d vs #71717a are one gray used three ways).
3. Compare to the declared tokens. Anything not in tokens is drift.
4. Reporting thresholds (heuristic): >8 font sizes, >5 radii, >10 text colors, >3 shadows usually signal missing or ignored tokens.
5. Fix by mapping stray values to the nearest token, not by adding tokens.
