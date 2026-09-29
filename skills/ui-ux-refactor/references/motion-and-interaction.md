# Motion and interaction

Synthesized from Emil Kowalski's design-engineering skill (animation decisions, component polish) and Vercel's Web Interface Guidelines (interaction, forms, performance). Cite the reasoning, not the author, when reporting findings.

## Contents
- Should it animate at all?
- Easing and duration
- Rules that catch most bugs
- Springs and gestures
- Feedback and states
- Forms
- Loading and perceived performance
- Keyboard, focus, hit targets
- Review table format

## Should it animate at all?

Ask in order:

1. **How often will users see this?**

| Frequency | Decision |
|---|---|
| 100+/day (keyboard shortcuts, command palette toggle) | No animation |
| Tens/day (hover effects, list navigation) | Remove or drastically reduce |
| Occasional (modals, drawers, toasts) | Standard animation |
| Rare / first-time (onboarding, celebration) | Delight is allowed |

2. **What is the purpose?** Valid: spatial consistency (toast exits the way it entered), state indication, explanation, feedback (press), preventing jarring appear/disappear. Invalid: "it looks cool" on something seen often.
3. **Never animate keyboard-initiated actions.** They repeat constantly and animation makes them feel laggy.

## Easing and duration

- **Ease-out for anything entering or exiting or user-triggered** (starts fast, feels responsive). **Never ease-in for UI**: it delays the first moment the user watches most closely.
- Moving or morphing on screen: ease-in-out. Hover/color change: ease. Constant motion (progress, marquee): linear.
- Built-in CSS easings are weak. Use stronger custom curves:
  - `--ease-out: cubic-bezier(0.23, 1, 0.32, 1)`
  - `--ease-in-out: cubic-bezier(0.77, 0, 0.175, 1)`
  - `--ease-drawer: cubic-bezier(0.32, 0.72, 0, 1)`
- **Durations**: button press 100-160ms; tooltips/small popovers 125-200ms; dropdowns/selects 150-250ms; modals/drawers 200-500ms. Keep UI motion under ~300ms. A 180ms dropdown feels more responsive than a 400ms one.
- **Asymmetry**: slow where the user is deciding (hold-to-delete 2s linear), fast where the system responds (release 200ms). Exits are usually faster than entrances.
- **Stagger**: 30-80ms between items; decorative only, never block interaction while it plays.

## Rules that catch most bugs

| Smell | Fix |
|---|---|
| `transition: all` | List exact properties (`transform 200ms ease-out`) |
| Animate from `scale(0)` | Start at `scale(0.95)` with `opacity: 0` |
| `ease-in` on UI | `ease-out` or a custom curve |
| Popover scales from center | `transform-origin` at the trigger (modals stay centered) |
| Animating width/height/top/left/padding | Animate `transform` and `opacity` only (skip layout/paint) |
| No press feedback | `:active { transform: scale(0.97) }` on pressable elements (0.95-0.98) |
| Keyframes on rapidly triggered UI (toasts) | CSS transitions, which retarget mid-flight; keyframes restart |
| Hover animation on touch | Gate with `@media (hover: hover) and (pointer: fine)` |
| JS-driven animation janking during page load | CSS or WAAPI (off main thread); prefer CSS > WAAPI > JS libraries |
| Framer Motion `x`/`y` shorthand under load | Use full `transform` strings for hardware acceleration |
| Duration >300ms on small UI | Reduce to 150-250ms |
| Enter and exit same speed | Make exit faster |
| Reveal gated on a class-triggered transition | Reveals must enhance an already-visible default (hidden tabs/headless renderers pause transitions) |
| No reduced-motion path | `@media (prefers-reduced-motion: reduce)`: keep opacity/color fades that aid comprehension, remove movement |

Other useful techniques: `@starting-style` for enter states; `clip-path: inset()` for reveals and tab color transitions; a subtle `filter: blur(2px)` to mask an imperfect crossfade (keep blur <20px, expensive on Safari); percentages in `translate()` so motion adapts to element size.

## Springs and gestures

- Springs suit drag with momentum, interruptible gestures, and "alive" elements; they keep velocity when interrupted. Keep bounce subtle (0.1-0.3) or none.
- **Dismiss by velocity**, not only distance (a quick flick should work). Apply damping/friction at boundaries instead of hard stops. Capture pointer events during drag; ignore extra touches once a drag begins.
- **Every gesture needs a non-gesture alternative** (tap/click + keyboard). Disable text selection and set `inert` on content while dragging.

## Feedback and states

- Every action gets an acknowledgment: press state, progress, optimistic update with rollback/undo on failure.
- Design all states: default, hover, focus-visible, active, disabled, loading, success, error, empty, sparse, dense.
- Interactions should **increase** contrast (hover/active/focus more visible than rest).
- Confirm destructive actions or provide Undo with a safe window.
- Tooltips: delay the first, instant for adjacent peers; never the only home for essential information (inline help first).
- No dead zones: if something looks interactive it is; checkboxes/radios share one generous hit target with their label.

## Forms

- Every control has a real label; placeholders are examples (end with an ellipsis for input, use an example value), not labels.
- Correct `type`, `inputmode`, `autocomplete`, and meaningful `name`; disable spellcheck on emails/codes/usernames.
- Enter submits when it is the only input; in `<textarea>`, Cmd/Ctrl+Enter submits.
- **Do not block typing or paste.** Accept input and show validation instead. Do not pre-disable submit; show what is missing on submit and focus the first error.
- Errors next to their fields, specific, with a fix. Keep submit enabled until submission starts, then disable with a spinner and use an idempotency key.
- Warn before navigating away with unsaved changes. Trim trailing whitespace from IME/text-replacement input.
- Mobile inputs at >=16px to avoid iOS zoom.

## Loading and perceived performance

- Show a spinner/skeleton only after ~150-300ms, and keep it visible >=300-500ms to avoid flicker.
- Skeletons mirror the final layout exactly (no layout shift). Loading buttons keep their label and add an indicator.
- Faster-feeling beats faster-measuring: instant feedback, optimistic UI, progressive rendering.
- Persist state in the URL (filters, tabs, pagination) so refresh, Back, and Share work; restore scroll on Back.
- Network latency budget: POST/PATCH/DELETE under ~500ms perceived; virtualize long lists; reserve image space.

## Keyboard, focus, hit targets

- Everything operable by keyboard following WAI-ARIA Authoring Practices; visible, unobscured focus via `:focus-visible` (and `:focus-within` for groups); sticky bars never cover the focused element.
- Manage focus in modals/menus: trap, move in, return on close.
- Visual target under 24px gets an expanded hit area of at least 24px; 44px on mobile.
- Links are `<a>` (middle-click, Cmd-click work); buttons are `<button>`. Never a `div` for either.
- `touch-action: manipulation` on controls to prevent double-tap zoom; `overscroll-behavior: contain` in modals/drawers.
- Announce async updates with polite `aria-live`.

## Review table format

When reviewing UI code for motion/interaction, report as one table with one row per issue:

| Before | After | Why |
|---|---|---|
| `transition: all 300ms` | `transition: transform 200ms ease-out` | Name exact properties; avoid layout jank |
| No `:active` state on button | `transform: scale(0.97)` on `:active` | Pressables must feel responsive |
