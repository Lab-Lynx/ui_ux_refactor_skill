# UX laws, heuristics, and perceptual principles

Use these to explain *why* something fails and to predict how users will behave. Each entry: the idea, what to check in a review, and a caution against misuse. They are heuristics from research and practice, not physics; when a principle conflicts with evidence about your actual users, the evidence wins.

## Contents
- Part A: Visual design lessons (color, alignment, hierarchy, whitespace, type, contrast)
- Part B: Laws of UX
- Part C: Gestalt principles
- Part D: Nielsen's 10 usability heuristics
- Part E: Norman's interaction concepts
- Part F: Cognitive and behavioral concepts
- Part G: WCAG 2.2 quick reference

---

## Part A: Visual design lessons

### Color proportion: 60-30-10
A guideline for balance: roughly 60% dominant surface (background/white space), 30% secondary (text, dark content, panels), 10% accent/brand for what matters most (primary buttons, key icons, links, highlights). Color does not mean flooding the page with brand color.
Check: Is the accent used on more than the few things that deserve attention? Is there a clear dominant surface?
Caution: It is a starting ratio. Product UIs are often 85-95% neutral with a tiny accent (restrained); brand pages may be deliberately drenched in one color (committed/drenched). Judge by whether emphasis is *legible*, not by the arithmetic.

### Color psychology
Colors carry associations (blue: trust/calm; red: urgency/danger/energy; green: success/growth/go; yellow/orange: caution/warmth; black: premium/serious; purple: creative/luxury). Pick color knowing what it signals and whether it fits the product and audience.
Caution: associations are culturally variable and context-dependent; the research evidence is weaker than design folklore claims. Use as a prompt to be intentional, not as proof. Never rely on a color's "meaning" without a text/icon backup.

### Color hierarchy (roles)
Colors have jobs. Define and keep them distinct:
- **Brand / primary**: identity and the main action.
- **Secondary / accent**: supporting emphasis, kept rare.
- **Neutrals**: a ramp (about 9-11 steps) for text, borders, surfaces; tint slightly toward the brand hue.
- **Semantic**: success, warning, danger/error, info. Consistent everywhere, never reused decoratively.
- **Surfaces / elevation**: background, raised, overlay layers.
- **Interactive states**: hover/active/focus/disabled variants of the above.
Check: Does any color do two jobs (e.g., brand red also used for errors)? Is the same job colored two ways?

### Alignment and patterns
Clear alignment and spacing rules make a design feel organized: repetition, straight lines, consistent patterns. Common mistakes: centering everything, inconsistent padding, mixing alignment styles in one block.
Check: Every element aligns to a grid line, baseline, edge, or a deliberate optical center. Repeated components have identical internal spacing.

### Visual hierarchy
Make it obvious what to notice first, second, last using size, weight, spacing, color, position, and scanning patterns (F-pattern for text-heavy pages, Z-pattern for sparse pages with a CTA).
Check: Does the eye path match the intended task path? Are size/weight/color voting for the same thing?

### White space
Empty space separates elements, reduces visual pressure, and reveals structure. More content is not better design. Macro space (between sections) and micro space (between lines, label and field) both matter.
Check: Is spacing rhythmic and purposeful? Is density right for the task (dashboards can be dense; landing pages usually should not)?

### Typography
Type sets tone. Serif: books, academic, traditional, editorial. Sans-serif: modern web, technology, mobile UI. Display for headlines; script sparingly; monospace for code and tabular data.
Check: Pairing has contrast on an axis (serif + sans, geometric + humanist) or uses one family in several weights; not two near-identical sans faces.

### Contrast
Create difference with dark/light, big/small, bold/thin, near/far, saturated/muted. Text, icons, and UI parts need enough contrast to be readable and accessible.
Check: Measured ratios against WCAG thresholds (Part G); interactive states have *more* contrast than rest.

---

## Part B: Laws of UX

**Hick's Law**: decision time grows with the number and complexity of choices. Check: nav items, menu options, pricing tiers, form choices. Fix: group, prioritize, progressive disclosure, sensible defaults. Caution: not "hide everything"; experts want direct access to frequent actions.

**Jakob's Law**: users spend most of their time on other sites, so they expect yours to work like those. Check: unconventional patterns for standard tasks (nav placement, form behavior, icons). Fix: use familiar patterns; innovate only where it earns its cost.

**Law of Prägnanz**: people interpret ambiguous or complex images in the simplest form possible. Check: needless visual complexity, decorative noise. Fix: simplify shapes, reduce elements, clear structure.

**Law of Proximity**: near things are perceived as related. Check: label-to-input gap smaller than field-to-field gap; headings closer to their content than to the previous section.

**Law of Common Region**: things inside the same boundary are perceived as grouped. Check: cards, containers, background panels group the right things. Caution: over-boxing ("cardocalypse") flattens hierarchy; nested containers are almost always wrong.

**Miller's Law**: working memory is limited. The often-quoted "7 plus or minus 2" is a loose figure; modern work suggests fewer chunks (about 4) for novel information. Check: long ungrouped lists, dense forms, strings of numbers. Fix: chunk, group, label sections. Caution: it is about *memory*, not a cap on menu items.

**Fitts's Law**: time to reach a target grows with distance and shrinks with size. Check: small targets, far-apart sequential actions, primary buttons in hard-to-reach spots on large phones. Fix: bigger hit areas (>=44px touch), edges/corners on desktop, place related actions close.

**Doherty Threshold**: responses under about 400ms keep users in flow. Check: latency without feedback. Fix: immediate acknowledgment, optimistic updates, skeletons, progress.

**Aesthetic-Usability Effect**: attractive interfaces are perceived as more usable and forgiven for minor issues. Caution: this can mask real usability problems in testing; do not let polish hide friction.

**Von Restorff (Isolation) Effect**: the item that differs is remembered. Check: is the one thing that should stand out actually unique? If five things are highlighted, none is.

**Serial Position Effect**: first and last items are remembered best. Fix: put key actions/nav items at the ends.

**Peak-End Rule**: people judge experiences by the peak moment and the end. Fix: polish success states, confirmations, offboarding; make errors recoverable.

**Zeigarnik Effect / Goal-Gradient Effect**: unfinished tasks are remembered; motivation rises near a goal. Use: progress indicators, checklists, endowed progress. Caution: manipulative dark patterns (fake urgency) erode trust.

**Tesler's Law (Conservation of Complexity)**: every system has irreducible complexity; someone must handle it. Ask whether the system or the user carries it; smart defaults move it to the system.

**Postel's Law**: be liberal in what you accept, conservative in what you send. Fix: accept varied input formats (phone, dates, pasted spaces), normalize behind the scenes.

**Occam's Razor / Parkinson's Law / Pareto**: prefer the simplest solution that works; tasks expand to fill time (set sensible defaults, autofill); ~80% of use comes from ~20% of features (surface those).

**Cognitive load** (intrinsic / extraneous / germane): remove extraneous load (visual noise, unclear labels, unnecessary steps) so users spend effort on the task. Progressive disclosure, chunking, and recognition over recall reduce it.

**Choice architecture and defaults**: most people keep defaults. Set defaults that serve the user; make the safe choice easy, the destructive choice deliberate.

---

## Part C: Gestalt principles

- **Similarity**: alike things group (same style = same function). Do not style unlike things alike.
- **Proximity / Common region / Uniform connectedness**: see Part B; lines or containers link items.
- **Continuity**: the eye follows lines and curves; align items along paths so the eye flows.
- **Closure**: minds complete incomplete shapes; use for lightweight icons and skeleton UIs.
- **Figure/ground**: content must separate cleanly from background (overlays need scrims; text over images needs contrast control).
- **Symmetry and order / Focal point**: balanced order reads as stable; one focal point directs attention.

---

## Part D: Nielsen's 10 usability heuristics

1. **Visibility of system status**: users always know what is happening (loading, saved, selected, step 2 of 4).
2. **Match between system and real world**: language and metaphors users know (a trash can for delete).
3. **User control and freedom**: undo, cancel, back, clearly marked exits.
4. **Consistency and standards**: same words/actions mean the same thing; follow platform conventions.
5. **Error prevention**: constraints, confirmations for risky actions, good defaults, forgiving formats.
6. **Recognition rather than recall**: show options, recent items, labels; do not make users memorize.
7. **Flexibility and efficiency of use**: shortcuts, bulk actions, saved filters for experts without burdening novices.
8. **Aesthetic and minimalist design**: every extra unit of information competes with the relevant ones.
9. **Help users recognize, diagnose, and recover from errors**: plain language, precise cause, constructive fix.
10. **Help and documentation**: searchable, task-focused, contextual; inline help before tooltips before docs.

Review use: score each 0-4 for severity (0 none, 4 catastrophic) and list violations with evidence.

---

## Part E: Norman's interaction concepts

- **Affordances and signifiers**: what an element allows vs how it signals that. If it is clickable it should look clickable; if it looks clickable it must be.
- **Feedback**: every action gets a perceivable, timely response.
- **Mapping**: controls relate naturally to effects (a slider's direction matches the change).
- **Constraints**: make wrong actions impossible or hard.
- **Conceptual model**: the user's mental picture of how it works must match how it works.
- **Gulfs of execution and evaluation**: can users figure out how to do it, and can they tell what happened?

---

## Part F: Other behavioral concepts worth checking

- **Progressive disclosure**: reveal complexity as needed.
- **Recognition over recall**: menus, autocomplete, history.
- **Loss aversion**: warn on unsaved work; make undo available.
- **Social proof and authority**: real, specific evidence (not fake counters) builds trust.
- **Friction budgeting**: add friction only where it protects the user (destructive, financial); remove it elsewhere.
- **Dark patterns**: confirmshaming, hidden costs, forced continuity, disguised ads, fake scarcity. Flag as P1 trust issues.

---

## Part G: WCAG 2.2 quick reference (AA baseline)

- **1.4.3 Contrast (minimum)**: text 4.5:1; large text 3:1.
- **1.4.11 Non-text contrast**: UI components and meaningful graphics 3:1.
- **1.4.4 Resize text**: usable at 200%.
- **1.4.10 Reflow**: no horizontal scroll at 320 CSS px width for vertical content.
- **1.4.1 Use of color**: not the only means of conveying information.
- **2.1.1 Keyboard**: all functionality via keyboard; **2.1.2** no keyboard trap.
- **2.4.7 Focus visible** and **2.4.11 Focus not obscured (minimum)** (new in 2.2): focused element not entirely hidden by sticky/overlay content.
- **2.5.7 Dragging movements** (new in 2.2): a non-drag alternative for drag actions.
- **2.5.8 Target size (minimum)** (new in 2.2): at least 24x24 CSS px, with spacing exceptions and exemptions for inline text links.
- **3.3.7 Redundant entry** (new in 2.2): do not ask users to re-enter information already provided in the same process.
- **3.3.8 Accessible authentication (minimum)** (new in 2.2): no cognitive-function tests (e.g., must-transcribe puzzles) without an alternative; allow paste and password managers.
- **4.1.3 Status messages**: announce async updates via live regions.
- **Reduced motion**: honor `prefers-reduced-motion`.

APCA (the contrast model proposed for WCAG 3) predicts perceived legibility better than the 2.x ratio, especially for dark mode and thin text. Use it as a second opinion; the 2.x ratios remain the compliance baseline.
