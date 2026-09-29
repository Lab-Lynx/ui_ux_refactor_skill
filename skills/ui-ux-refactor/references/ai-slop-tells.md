# AI-generated UI tells (and how to fix them without losing the brand)

"AI slop" is the look a model produces when it fills in taste decisions nobody made: the statistical center of its training data. Nothing is broken; it just "doesn't come from anywhere." The goal of this file is to detect unchosen defaults and replace them with real decisions.

## Contents
- How to judge a tell
- Visual tells
- Layout tells
- Typography and color tells
- Motion tells
- Content and copy tells
- Mobile tells
- The second-order trap
- Fixing a tell: the procedure

## How to judge a tell

- A tell is a **choice nobody made**, not a forbidden element. One of these can be deliberate. Four or more together indicates unguided generation.
- Ask of each: *Did this come from the brand or product, or from the model's reflex?* If the product has a reason (a fintech using deep blue, a brand that really is purple), it is not a defect.
- Severity is usually **P2-P3** individually, **P1** when the accumulation makes the product indistinguishable or untrustworthy.
- Sources for these lists: Impeccable (Paul Bakaus), Taste Skill (Leonxlnx), community teardowns of AI-generated sites, and Draftbit's mobile-taste-skill. Some bans there are house style; treat those as prompts, not law.

## Visual tells

- Purple/indigo-to-blue gradient in the hero or primary buttons with no brand reason (the Tailwind indigo default feedback loop).
- **Gradient text** (`background-clip: text` with a gradient), especially on a big number or headline.
- **Colored side-stripe** (3-4px `border-left`/`border-right`) on cards, callouts, alerts, list items. One of the most reliable tells.
- Glassmorphism used decoratively (blur + translucent card + faint glow) rather than to solve a legibility or layering problem.
- Neon or colored outer glows; glowing accents behind hero elements.
- Same soft shadow and same corner radius on every element; the untouched `rounded-2xl shadow-lg p-6` card.
- Flat 1px gray border on every card; pure #fff/#000 with no depth.
- Decorative mesh/aurora gradients behind a centered hero.
- Div-built fake product screenshots (fake dashboards, fake terminals) in the hero instead of real product.

## Layout tells

- **Three identical feature cards** in a row: icon on top, heading, two lines of text.
- Centered hero over a dark or gradient backdrop, always.
- **Cardocalypse**: every block boxed, cards nested inside cards.
- Identical card grids repeated endlessly; section after section with the same layout family.
- Strict zigzag of image-left/text-right then reversed, three or more in a row.
- Middle pricing tier highlighted in a three-tier table by default.
- "Hero metric" template: big number, small label, supporting stats, accent gradient.
- Split section header: big headline left, small floating explainer paragraph right.
- Empty or uneven bento cells added only to fill a grid.

## Typography and color tells

- **Inter (or Poppins / Space Grotesk / Geist) as the only typeface**, unchanged from default, in every weight.
- **Tiny uppercase tracked eyebrow above every section** (`ABOUT`, `PROCESS`, `PRICING`), or numbered markers (01 / 02 / 03) as scaffolding when the sections are not a real sequence.
- Timid, even palette with no dominant color and no accent; or default shadcn gray + Tailwind blue.
- Display headline set enormous with very tight tracking.
- **Gray text on colored backgrounds** and muted-gray body text "for elegance" that fails contrast.

## Motion tells

- Every section fades/slides up identically on scroll (uniform entrance reflex).
- Infinite looping micro-animations (pulses, floats, shimmer) on informational content.
- Bounce or elastic easing on hover nobody asked for.
- Parallax/scroll-hijack with no narrative reason; multiple marquees on one page.
- Reveal animations that gate content visibility (page ships blank if the trigger never fires).

## Content and copy tells

- Headlines that mean nothing: "Build the future of work", "Elevate your workflow", "Seamless experiences."
- Filler verbs and adjectives: elevate, seamless, unleash, next-gen, revolutionize, effortless.
- Fake-perfect or fake-precise data: 99.99%, 1234567, "10x faster", invented stats presented as real.
- Placeholder people and brands in shipped UI: "John Doe", "Sarah Chan", "Acme", "Nexus", "Cloudly".
- Pretentious micro-labels: "Field notes", "Currently on the bench", photo-credit captions on stock images, version stamps or "last sync 4s ago" footers on marketing pages.
- Locale/time/weather strips, scroll cues ("Scroll to explore"), decorative status dots on every row.
- Overused prose rhythms (em-dash-heavy sentences, "not X, but Y", triplets everywhere). Mention as a copy note; do not rewrite the user's voice wholesale without asking.

## Mobile tells

- Indigo gradients; a five-tab bar with a floating action button.
- Screens made of stacked white rounded cards; emoji as icons.
- "Welcome back, John! 👋" greetings; the same greeting-plus-stats header on every home screen.
- Generic bottom sheets and toasts with identical motion everywhere.

## The second-order trap

Anti-slop advice becomes the new slop. As of 2026 the fastest-rising tell is the "tasteful default": cream/sand/paper background, an editorial serif headline, and a sage or terracotta accent. Avoiding purple gradients by reaching for cream + serif is still a reflex.
- **First-order test**: could someone guess the palette and theme from the product category alone?
- **Second-order test**: could someone guess it from the category *plus* the anti-references ("AI tool that isn't purple-gradient" leads to cream-and-serif)? If yes, it is still a reflex.
- Fix by starting from something true about the product (audience, environment, tone, a real artifact) and letting that drive the choice.

## Fixing a tell: the procedure

1. **Name the decision.** What was this element supposed to do (group, emphasize, delight)?
2. **Check identity.** Is it part of the existing brand? If yes, keep it and fix execution (consistency, contrast, restraint).
3. **Write a scene sentence** for palette/theme: who uses this, where, in what light, in what mood. If the sentence does not force the answer, add detail.
4. **Make one deliberate move** rather than adding effects: a real photo, a committed accent, an asymmetrical layout, a distinctive typeface pairing, removal of the container.
5. **Prefer subtraction.** Removing the gradient, the card, the eyebrow, or the animation is often the entire fix.
6. **Recheck** that the result still passes contrast, hierarchy, and consistency; anti-slop must never cost accessibility.
