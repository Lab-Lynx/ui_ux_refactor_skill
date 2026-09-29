# ui-ux-refactor

An [Agent Skill](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview) that makes your AI act like a senior product designer when **reviewing and refactoring existing interfaces**.

It does two jobs, in order:

1. **Find every real weakness**, ranked P0-P3, each backed by evidence (a measured contrast ratio, a target size, a file and line).
2. **Fix the highest-impact ones with the smallest change that keeps what already works**: brand, information architecture, copy voice, analytics hooks.

Most AI redesigns fail by restyling by reflex or by throwing away what users already know. This skill is built to prevent both.

## What it does

- Picks a mode: review only, targeted refactor, redesign-preserve, or redesign-overhaul
- Records the product's "identity fingerprint" before touching anything
- Renders the UI and runs an automated Playwright audit (contrast, tap targets, overflow, unlabeled controls, focus rings, design-system drift, AI-slop tells)
- Runs attack tests: 5-second, squint, grayscale, keyboard-only, worst-case content, 320px / 200% zoom, pre-mortem
- Fixes in leverage order: tokens, type, spacing, color, states, layout, motion, copy
- Verifies with before/after screenshots and an audit diff, then hands off a Before / After / Why table

## Install

**Claude Code (personal, all projects)**

```bash
git clone https://github.com/Lab-Lynx/ui_ux_refactor_skill.git
cp -r ui-ux-refactor/skills/ui-ux-refactor ~/.claude/skills/
```

**Claude Code (one project, shareable with your team)**

```bash
cp -r ui-ux-refactor/skills/ui-ux-refactor <your-project>/.claude/skills/
```

**Via the skills CLI**

```bash
npx skills add https://github.com/Lab-Lynx/ui_ux_refactor_skill
```

**claude.ai**: zip the `skills/ui-ux-refactor` folder so the folder itself is the zip root, then upload it in Settings under Skills.

## Use

Just ask. The skill triggers on requests like:

- "Audit this page and tell me everything wrong with it"
- "Why does this look amateur / AI-generated?"
- "Fix the spacing, hierarchy and colors on the dashboard"
- "Modernize this landing page but keep our brand"
- "Compare my implementation against this Figma frame"

Run the audit directly:

```bash
pip install playwright pillow
python -m playwright install chromium
python skills/ui-ux-refactor/scripts/playwright_audit.py http://localhost:3000 --out audit/before
# ...make changes...
python skills/ui-ux-refactor/scripts/playwright_audit.py http://localhost:3000 --out audit/after --baseline audit/before
```

Options: `--viewports 320x640,1440x900`, `--dark`, `--cookie "session=..."`, `--wait 1000`. See `--help`.

## Layout

```
skills/ui-ux-refactor/
├── SKILL.md                         workflow, stance, report format
├── references/
│   ├── critique-lenses.md           17 lenses for the weakness hunt + severity scale
│   ├── ux-laws-and-heuristics.md    color/type/hierarchy lessons, Laws of UX, Gestalt, Nielsen, Norman, WCAG 2.2
│   ├── visual-foundations.md        concrete numbers: spacing, type scale, contrast, dark mode, radii, shadows
│   ├── ai-slop-tells.md             AI-generated UI tells and how to fix them without losing the brand
│   ├── motion-and-interaction.md    animation decisions, easing, forms, loading, keyboard and focus
│   ├── refactor-protocol.md         preservation rules, "never change silently", sequencing, hand-off template
│   └── tooling-figma-playwright.md  Figma MCP and Playwright workflows, and fallbacks without them
└── scripts/
    └── playwright_audit.py          automated audit + screenshot diff
```

The skill uses progressive disclosure: only `SKILL.md` loads on trigger; references load when the task needs them.

## Limits

- The audit covers the **measurable** half of a review. It cannot judge hierarchy, rhythm, tone, copy quality, or whether a choice suits the product. The skill tells the model to look at the screenshots itself.
- Contrast over background images and gradients is approximated; over images it is flagged for manual review. Canvas and WebGL content is invisible to it.
- Figma MCP tool names and availability vary by client and change over time; the skill tells the model to check its actual tool list.
- This is v0.1. It has been tested on synthetic pages, not yet across many real projects. Issues and PRs welcome.

## Credits and inspiration

This skill is an original synthesis. It draws on ideas from the following public work; no source text is reproduced, apart from a few factual values (for example, easing-curve constants). Credit to:

- [Impeccable](https://github.com/pbakaus/impeccable) by Paul Bakaus (Apache-2.0)
- [Taste Skill](https://github.com/Leonxlnx/taste-skill) by Leonxlnx (MIT)
- [Emil Kowalski's skills](https://github.com/emilkowalski/skills) for animation and polish principles
- [Vercel Web Interface Guidelines](https://vercel.com/design/guidelines) for interaction, forms, and performance rules
- Stripe's ["Designing accessible color systems"](https://stripe.com/blog/accessible-color-systems) for perceptually uniform color
- @OnyxDesignx's [UI/UX lessons](https://www.youtube.com/@onyxdesignx), plus the Laws of UX, Nielsen's heuristics, Norman's concepts, and WCAG 2.2

This project is not affiliated with or endorsed by any of the above.

## License

MIT. See [LICENSE](LICENSE).
