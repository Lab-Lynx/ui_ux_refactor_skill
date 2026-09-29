# Visual foundations: numbers and rules to fix things with

Concrete values to reach for when a finding says "fix the spacing / type / color." Adapt to the project's existing tokens first; these are defaults for when none exist or existing ones are broken.

## Contents
- Spacing and layout
- Typography
- Color
- Dark mode
- Radius, borders, shadows
- Icons and imagery
- Density and register

## Spacing and layout

- Use a **4px base, mostly 8px multiples**: 4, 8, 12, 16, 24, 32, 48, 64, 96. Everything on the scale; any off-scale value needs a reason.
- **Proximity ratio**: space inside a group < space between groups < space between sections. A common progression is 8 (label-field), 16 (field-field), 32-48 (group-group), 64-96 (section-section).
- **Vary spacing for rhythm.** Uniform spacing everywhere reads as flat and templated.
- **Max content widths**: prose 60-75ch; app content 1100-1280px; wide marketing up to ~1400px. Always constrain and center the container.
- **Grid**: 12-column (or fewer) with consistent gutters (16/24/32). Use CSS Grid for 2D, Flexbox for 1D. `repeat(auto-fit, minmax(280px, 1fr))` gives responsive grids with no breakpoints.
- **Do not use `100vh` for full-height mobile layouts;** use `100dvh` / `min-h-[100dvh]`.
- **Z-index**: a semantic scale (dropdown < sticky < modal-backdrop < modal < toast < tooltip). Never 999/9999.
- **Overflow**: dropdowns inside `overflow: hidden/auto` get clipped; use the Popover API, `<dialog>`, `position: fixed`, or a portal.

## Typography

- **Scale**: pick a ratio (1.125 for dense UI, 1.2-1.25 for balanced, 1.333 for expressive). Example at 1.25 from 16px: 12.8, 16, 20, 25, 31, 39, 49. Use 5-7 sizes, not 12.
- **Body**: 16px (never below 14px except captions/legal); line-height 1.5-1.6; length 45-75ch.
- **Headings**: line-height 1.1-1.3; use `text-wrap: balance`. Long prose: `text-wrap: pretty`.
- **Display ceiling**: `clamp()` max around 6rem (96px). Above that the page shouts. Tracking on display no tighter than -0.04em.
- **Weights**: 2-3 per family (e.g., 400, 500/600, 700). Hierarchy through size + weight + color together, not size alone.
- **Pairing**: one family in multiple weights, or pair on a contrast axis (serif + sans, geometric + humanist, sans + mono). Avoid two near-identical sans faces.
- **Numbers**: `font-variant-numeric: tabular-nums` in tables, prices, timers. Separate number and unit with a non-breaking space (`10&nbsp;MB`).
- **Details**: typographic quotes, real ellipsis character, `text-wrap` to avoid orphans, adequate italic descender room (leading >= 1.1 on display italics).
- **Fonts loading**: self-host or `next/font`, `font-display: swap`, preload critical fonts, subset with `unicode-range`; always a real fallback stack.
- **Non-Latin scripts**: verify glyph coverage, taller line-height (Ethiopic/Ge'ez, Devanagari, Thai often need 1.6-1.8), and no all-caps or letter-spacing tricks that do not apply.

## Color

- **Work in a perceptual space (OKLCH)** for palettes. Equal lightness steps look equal, so contrast is predictable and you avoid muddy tints (the reason Stripe moved to perceptually uniform color for accessible palettes).
- **Neutral ramp**: 9-11 steps (50-950). Tint neutrals slightly toward the brand hue (chroma around 0.005-0.015). One neutral family per project; do not mix warm and cool grays.
- **Brand/accent ramp**: same steps; note which are text-safe on white and on dark surfaces.
- **Choose a color strategy deliberately**:
  - *Restrained*: tinted neutrals + one accent under ~10%. Default for product UI.
  - *Committed*: one saturated color carries 30-60% of the surface. Identity-driven pages.
  - *Full palette*: 3-4 named roles used on purpose. Data-heavy and campaign work.
  - *Drenched*: the surface is the color. Brand heroes and campaigns.
- **Contrast targets**: body 4.5:1; large text 3:1; UI components, icons, focus rings 3:1 against neighbors; placeholder 4.5:1. Hover/active/focus should have **more** contrast than rest.
- **Gray text on colored backgrounds** looks washed out; use a darker shade of that background's hue or the text color at partial opacity.
- **Hue consistency**: on tinted backgrounds, tint borders, shadows, and text toward that hue.
- **Semantic colors**: fixed roles; pair every color signal with an icon or text.
- **Charts**: color-blind-safe palettes (avoid red/green pairs), direct labels over legends where possible.
- **Avoid unchosen defaults**: framework blue/indigo, shadcn gray, and violet-to-blue gradients are usually accidents. Keep them only if they came from a decision.

## Dark mode

- **Not an inversion.** Redesign surfaces: elevate with *lighter* surfaces, not shadows alone. A typical stack is near-black base, then progressively lighter panels.
- **Avoid pure #000 backgrounds and #fff text**; use near-black (about L 0.12-0.18) and off-white (about L 0.92-0.96) to reduce glare and halation.
- **Desaturate and slightly lighten accents**; saturated colors vibrate on dark.
- **Recheck contrast** for every text/surface pair; thin light text on dark can fail perceptually even when the ratio passes (APCA helps).
- Set `color-scheme: dark`, `<meta name="theme-color">`, and test scrollbars, form controls, and images (logos may need a dark variant).
- Token strategy: semantic CSS variables (`--surface`, `--text`, `--accent`) swapped under `prefers-color-scheme` and a manual `data-theme` override.

## Radius, borders, shadows

- **One radius scale** (e.g., 4 / 8 / 12 / 16 / full) with a rule per component type. Mixed corner logic with no rule reads as broken.
- **Nested radii**: inner radius = outer radius minus the padding between them, so curves stay concentric.
- **Borders**: 1px, low-contrast but visible (>=3:1 where the border is the only boundary of a control). Semi-transparent borders sharpen edges on varied backgrounds.
- **Shadows**: at least two layers (a tight contact shadow plus a soft ambient one), tinted to the surface hue, low opacity. Avoid a single heavy black drop shadow.
- **Do not stack border + shadow + gradient + blur on the same element.** Pick the elevation cue.
- **Cards**: use only when a boundary carries meaning. Otherwise group with spacing, dividers, or background shifts. Never nest cards.

## Icons and imagery

- **One icon family**, one stroke width, one size grid (16/20/24). Optically balance icon weight against adjacent text weight.
- **Icon buttons always have an accessible name.** Icons paired with text where meaning is not universal.
- **Emoji are not icons** in product UI (inconsistent rendering, tone mismatch).
- **Imagery**: real and specific beats stock and abstract. Set explicit width/height (or aspect-ratio) to prevent layout shift; lazy-load below the fold; provide alt text.
- **Text over images** needs a scrim, blur-with-solid-fallback, or a placed text zone; check contrast against the *worst* region of the image.

## Density and register

- **Product UI** (dashboards, tools, admin): favor familiarity, density, speed, keyboard support, quiet color. Data-heavy views: tabular numerals, dividers over cards, tight but readable rhythm (row height 32-44px).
- **Brand UI** (landing, portfolio, campaign): favor point of view, narrative, imagery, typography, motion with purpose. Hero must show the value in the first viewport.
- **Trust-critical** (finance, health, government): calm, high contrast, conventional patterns, explicit copy, no gimmicks.
- **Density check**: if users scan many rows, tighten; if they decide once, loosen.
