# Tooling: Figma MCP and Playwright

Both are optional. Use them when available; degrade gracefully when not. Tool names and availability change between clients and releases, so check what is actually in your tool list before assuming.

## Contents
- Figma MCP
- Playwright validation
- The audit script
- Manual verification checklist
- Working without either tool

## Figma MCP

What it gives you: structured design data from Figma so you compare and implement against the real source of truth rather than a guess from a screenshot.

Tools commonly exposed (read side):
- `get_design_context`: layout, styles, and reference code for a selected frame or node. Defaults to React + Tailwind; ask for your framework explicitly. Treat the output as a **starting point**, not final code.
- `get_variable_defs`: variables and styles used in a selection (color, spacing, typography). Use this to reference the design's tokens directly.
- `get_screenshot`: an image of the selection for fidelity comparison.
- `get_metadata`: sparse structure for large frames; use it to find the right node before pulling full context.
- Code Connect tools (`get_code_connect_suggestions`, `send_code_connect_mappings`, and similar): map Figma components to your code components so generated code reuses `<Button>`, `<Card>`, etc. instead of duplicating them.
- `create_design_system_rules`: generate a rules file describing the design system for agents.
- Write-side tools (for example `generate_figma_design`, or canvas-editing tools) may exist on the remote server or in some clients only. They modify shared files; do not use them without the user's explicit go-ahead.

Refactor workflow with Figma:

1. **Tokens first.** Pull variables (`get_variable_defs`) and compare with code tokens. Differences are drift: either the code is stale or the design is. Report both.
2. **Find the frame.** Use `get_metadata` for large files; then `get_design_context` for the target node, plus `get_screenshot`.
3. **Translate, do not paste.** Map the generated structure onto the project's existing components, tokens, and conventions. Replace hard-coded values with tokens.
4. **Compare.** Render the implementation and compare to the Figma screenshot at the same viewport. List deviations as findings (spacing, type, color, states), not as a generic "doesn't match."
5. **Ask when Figma is silent.** Design files rarely specify hover, focus, error, empty, loading, responsive, or motion. Flag these as gaps and propose defaults from `motion-and-interaction.md`.

Tips: files with variables, components, and auto layout give far better results; annotations in Figma (hover, transitions, responsive behavior) reduce guessing.

## Playwright validation

Two ways to read a page:
- **Accessibility snapshot** (structured text of roles, names, states): fast, cheap, stable. Best for verifying semantics, labels, order, and interaction flows.
- **Screenshots** (vision): needed for layout, spacing, color, typography, charts, and anything the accessibility tree cannot express. Use for visual before/after.

Use both: snapshot for structure/a11y, screenshots for appearance. Snapshots can include off-screen elements, so do not assume everything in the tree is visible in the viewport.

What to capture for a refactor:
- Widths: 375, 768, 1280, 1536 (add 320 and ultra-wide when layout is fragile).
- Themes: light and dark (`colorScheme` emulation).
- Preferences: `reducedMotion: 'reduce'`.
- States: hover, keyboard focus (Tab), open menus/modals, error and empty states (seed data or intercept routes to trigger them).
- Full-page and above-the-fold.

Playwright Python essentials:

```python
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b = p.chromium.launch()
    ctx = b.new_context(viewport={"width": 375, "height": 812},
                        color_scheme="dark", reduced_motion="reduce")
    page = ctx.new_page()
    page.goto("http://localhost:3000", wait_until="networkidle")
    page.screenshot(path="m-375-dark.png", full_page=True)
    print(page.locator("body").aria_snapshot())  # accessibility snapshot as YAML text
```

Tips: wait for fonts and images before screenshots (`page.wait_for_load_state("networkidle")`, `document.fonts.ready`); disable or pause animations for stable diffs; hide volatile content (timestamps, ads) or mock it; use identical viewport and device scale factor for before/after.

## The audit script

`scripts/playwright_audit.py` automates the measurable half of a design review.

```
python scripts/playwright_audit.py <url-or-html-file> --out audit/before
python scripts/playwright_audit.py <url> --out audit/after --baseline audit/before
python scripts/playwright_audit.py <url> --viewports 320x640,1440x900 --dark --cookie "session=..."
```

It reports:
- **Layout**: horizontal overflow and the offending elements; missing viewport meta; zoom disabled.
- **Accessibility**: contrast failures (WCAG ratios, computed against effective backgrounds; flags uncertain backgrounds such as images/gradients for manual review), tap targets under 24px (P1) and under 44px on mobile (P2), controls with no accessible name, placeholder-only inputs, images without alt, multiple/skipped headings, missing `lang`, missing visible focus indicator during Tab traversal, infinite animations that ignore reduced motion.
- **Consistency**: counts of distinct font sizes, families, text colors, radii, shadows (design-system drift) with top values.
- **Slop tells**: gradient text, colored side stripes, `transition: all`, very tight display tracking, default-font signal, emoji-as-icons, nested cards, default indigo/violet accents.
- **Runtime**: console errors, page errors, failed requests.
- **Screenshots** for each viewport/theme; with `--baseline`, a percent-changed figure and a diff mask per image.

Limits: it cannot judge hierarchy, rhythm, tone, copy quality, or whether a choice is appropriate. It approximates contrast over images/gradients and cannot see canvas/WebGL content. Treat its output as evidence for findings, then look at the screenshots yourself. Use `--help` for options. If Playwright or a browser is missing, run `pip install playwright` and `python -m playwright install chromium` (needs network access to download the browser); otherwise fall back to the manual checklist.

## Manual verification checklist

- [ ] Screenshots reviewed at every width, both themes
- [ ] Tab through the main flow: order, visible focus, no traps, focus not hidden
- [ ] Every changed component: hover, focus, active, disabled, loading, error, empty
- [ ] Contrast of every changed text/surface pair (numbers, not impressions)
- [ ] 200% zoom and 320px: no clipping or horizontal scroll
- [ ] Reduced motion: no essential info lost, no big movement
- [ ] Long text / missing image / no data behave
- [ ] Console clean; no new layout shift
- [ ] Diff confined to intended areas; brand fingerprint intact

## Working without either tool

- **No browser/URL**: audit from code and any screenshots provided. Grep for `outline: none`, `transition: all`, hard-coded hex, `font-size` values, `border-radius` values, `aria-label` gaps, images without `alt`/dimensions, `user-scalable=no`, `100vh`. Say clearly that findings are code-derived, not rendered.
- **No Figma access**: ask for exports (screenshots, token JSON) or work from code as the source of truth and state that assumption.
- **Sandbox without browser download access**: give the user the script and commands to run locally, and audit statically in the meantime.
