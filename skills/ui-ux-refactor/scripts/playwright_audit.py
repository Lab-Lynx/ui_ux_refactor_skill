#!/usr/bin/env python3
"""Playwright UI audit: the measurable half of a design review.

Usage:
  python playwright_audit.py <url-or-html-file> --out audit/before
  python playwright_audit.py <url> --out audit/after --baseline audit/before
  python playwright_audit.py <url> --viewports 320x640,1440x900 --dark

Outputs (in --out): screenshots, report.json, report.md. Prints report.md.
Requires: pip install playwright && python -m playwright install chromium
"""
import argparse
import json
import re
import sys
from pathlib import Path

AUDIT_JS = r"""
() => {
  const out = { findings: [], metrics: {} };
  const add = (id, sev, title, detail, items) => out.findings.push({
    id, sev, title, detail, count: items ? items.length : 0, samples: (items || []).slice(0, 6)
  });
  const vw = window.innerWidth;
  const cs = (e) => getComputedStyle(e);
  const sel = (e) => {
    let s = e.tagName.toLowerCase();
    if (e.id) s += '#' + e.id;
    else if (e.classList && e.classList.length) s += '.' + Array.from(e.classList).slice(0, 2).join('.');
    return s.slice(0, 60);
  };
  const visible = (e) => {
    const r = e.getBoundingClientRect(); const c = cs(e);
    return r.width > 0 && r.height > 0 && c.visibility !== 'hidden' && c.display !== 'none' && parseFloat(c.opacity) > 0.01;
  };
  const canvas = document.createElement('canvas'); canvas.width = canvas.height = 1;
  const ctx = canvas.getContext('2d', { willReadFrequently: true });
  const num = (t) => t.endsWith('%') ? parseFloat(t) / 100 : parseFloat(t);
  const toRGBA = (c) => {
    if (!c || c === 'transparent') return [0, 0, 0, 0];
    const m = c.match(/^rgba?\(([^)]+)\)/);
    if (m) {
      const p = m[1].split(/[,\s/]+/).filter(Boolean);
      return [num(p[0]), num(p[1]), num(p[2]), p.length > 3 ? num(p[3]) : 1];
    }
    ctx.clearRect(0, 0, 1, 1); ctx.fillStyle = '#000';
    try { ctx.fillStyle = c; } catch (e) { return null; }
    ctx.fillRect(0, 0, 1, 1);
    const d = ctx.getImageData(0, 0, 1, 1).data;
    return [d[0], d[1], d[2], d[3] / 255];
  };
  const lin = (v) => { v /= 255; return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); };
  const lum = (c) => 0.2126 * lin(c[0]) + 0.7152 * lin(c[1]) + 0.0722 * lin(c[2]);
  const ratio = (a, b) => { const x = lum(a), y = lum(b); return (Math.max(x, y) + 0.05) / (Math.min(x, y) + 0.05); };
  const over = (f, b) => { const a = f[3]; return [f[0] * a + b[0] * (1 - a), f[1] * a + b[1] * (1 - a), f[2] * a + b[2] * (1 - a), 1]; };
  const hex = (c) => '#' + c.slice(0, 3).map(v => Math.round(v).toString(16).padStart(2, '0')).join('');
  const effBg = (el) => {
    const chain = []; for (let n = el; n; n = n.parentElement) chain.push(n);
    let base = [255, 255, 255, 1], stops = null, hasUrl = false;
    for (const n of chain.reverse()) {
      const c = cs(n);
      const bg = toRGBA(c.backgroundColor);
      if (bg && bg[3] > 0) base = over(bg, base);
      if (c.backgroundImage && c.backgroundImage !== 'none') {
        if (/url\(/.test(c.backgroundImage)) { hasUrl = true; stops = null; }
        else {
          const m = c.backgroundImage.match(/(rgba?\([^)]*\)|color\([^)]*\)|oklch\([^)]*\)|hsla?\([^)]*\))/g);
          if (m && m.length) { stops = m.map(x => toRGBA(x)).filter(Boolean).map(x => over(x, base)); hasUrl = false; }
        }
      }
    }
    return { rgb: base, stops, hasUrl };
  };

  const all = Array.from(document.body.querySelectorAll('*')).filter(visible);

  // ---- Page-level
  const de = document.documentElement;
  if (de.scrollWidth > vw + 1) {
    const off = all.map(e => ({ e, r: e.getBoundingClientRect() }))
      .filter(o => o.r.right > vw + 1 || o.r.left < -1)
      .sort((a, b) => (b.r.right - vw) - (a.r.right - vw)).slice(0, 8)
      .map(o => `${sel(o.e)} (right=${Math.round(o.r.right)}px, viewport=${vw}px)`);
    add('overflow-x', 'P0', 'Horizontal scroll', `Page is ${de.scrollWidth}px wide in a ${vw}px viewport.`, off);
  }
  const vp = document.querySelector('meta[name=viewport]');
  if (!vp) add('viewport-meta', 'P1', 'Missing viewport meta', 'Mobile browsers will render a desktop-width layout.', []);
  else if (/user-scalable\s*=\s*(no|0)/i.test(vp.content)) add('zoom-disabled', 'P2', 'Pinch-zoom disabled', vp.content, []);
  if (!de.lang) add('html-lang', 'P2', 'Missing <html lang>', 'Screen readers and translation need the language.', []);
  if (!document.title.trim()) add('title', 'P3', 'Empty <title>', '', []);

  // ---- Headings
  const hs = Array.from(document.querySelectorAll('h1,h2,h3,h4,h5,h6')).filter(visible);
  const h1 = hs.filter(h => h.tagName === 'H1').length;
  if (h1 !== 1) add('h1-count', 'P2', `Found ${h1} <h1> elements (expected 1)`, '', hs.filter(h => h.tagName === 'H1').map(sel));
  let prev = 0; const skips = [];
  hs.forEach(h => { const l = +h.tagName[1]; if (prev && l > prev + 1) skips.push(`${sel(h)} after h${prev}`); prev = l; });
  if (skips.length) add('heading-skip', 'P3', 'Skipped heading levels', '', skips);

  // ---- Contrast
  const groups = {}; const overImg = [];
  all.forEach(e => {
    const hasText = Array.from(e.childNodes).some(n => n.nodeType === 3 && n.textContent.trim().length > 0);
    if (!hasText) return;
    const c = cs(e); const fg0 = toRGBA(c.color); if (!fg0) return;
    const fill = toRGBA(c.webkitTextFillColor);
    if (fg0[3] === 0 || (fill && fill[3] === 0)) return; // transparent/gradient-clipped text: reported separately
    const bg = effBg(e);
    if (bg.hasUrl) { overImg.push(`${sel(e)}: "${e.textContent.trim().slice(0, 30)}"`); return; }
    const size = parseFloat(c.fontSize); const weight = parseInt(c.fontWeight) || 400;
    const large = size >= 24 || (size >= 18.66 && weight >= 700);
    const need = large ? 3 : 4.5;
    const bgs = bg.stops && bg.stops.length ? bg.stops : [bg.rgb];
    let worst = Infinity, worstBg = bg.rgb, worstFg = fg0;
    bgs.forEach(b => { const fg = over(fg0, b); const r = ratio(fg, b); if (r < worst) { worst = r; worstBg = b; worstFg = fg; } });
    if (worst < need - 0.01) {
      const key = `${hex(worstFg)}|${hex(worstBg)}|${Math.round(size)}|${!!bg.stops}`;
      (groups[key] = groups[key] || { fg: hex(worstFg), bg: hex(worstBg), r: worst.toFixed(2), need, size: Math.round(size), grad: !!bg.stops, items: [] })
        .items.push(`${sel(e)}: "${e.textContent.trim().slice(0, 30)}"`);
    }
  });
  Object.values(groups).forEach(g => {
    const sev = parseFloat(g.r) < 3 ? 'P0' : 'P1';
    add('contrast', sev, `Low contrast ${g.r}:1 (needs ${g.need}:1)`,
      `${g.fg} on ${g.bg}, ${g.size}px${g.grad ? ' | worst point of a gradient background' : ''}`, g.items);
  });
  if (overImg.length) add('text-over-image', 'P3', 'Text over background images: verify contrast manually (worst region)', 'Add a scrim or move text to a quiet zone.', overImg);

  // ---- Interactive: targets, names, focus prep
  const interSel = 'a[href],button,input:not([type=hidden]),select,textarea,summary,[role=button],[role=link],[role=tab],[role=menuitem],[tabindex]:not([tabindex="-1"])';
  const inter = Array.from(document.querySelectorAll(interSel)).filter(visible);
  const small = [], mid = [], noName = [], phOnly = [];
  const nameOf = (e) => {
    const t = (e.getAttribute('aria-label') || '').trim(); if (t) return t;
    const lb = e.getAttribute('aria-labelledby');
    if (lb) { const s = lb.split(/\s+/).map(i => (document.getElementById(i) || {}).textContent || '').join(' ').trim(); if (s) return s; }
    if (e.labels && e.labels.length) { const s = Array.from(e.labels).map(l => l.textContent).join(' ').trim(); if (s) return s; }
    if (['INPUT'].includes(e.tagName) && ['button', 'submit', 'reset'].includes(e.type) && e.value) return e.value;
    const txt = (e.textContent || '').trim(); if (txt) return txt;
    const im = e.querySelector('img[alt]'); if (im && im.alt.trim()) return im.alt.trim();
    const sv = e.querySelector('svg title'); if (sv && sv.textContent.trim()) return sv.textContent.trim();
    return (e.getAttribute('title') || '').trim();
  };
  inter.forEach(e => {
    const r = e.getBoundingClientRect(); const m = Math.min(r.width, r.height);
    const inlineLink = e.tagName === 'A' && cs(e).display === 'inline' && e.parentElement && (e.parentElement.textContent || '').trim().length > (e.textContent || '').trim().length + 10;
    if (!inlineLink) {
      if (m < 24) small.push(`${sel(e)} ${Math.round(r.width)}x${Math.round(r.height)}`);
      else if (vw <= 820 && m < 44) mid.push(`${sel(e)} ${Math.round(r.width)}x${Math.round(r.height)}`);
    }
    if (!nameOf(e)) {
      if (['INPUT', 'TEXTAREA', 'SELECT'].includes(e.tagName) && e.getAttribute('placeholder')) phOnly.push(sel(e));
      else noName.push(sel(e));
    }
  });
  if (small.length) add('target-24', 'P1', 'Targets under 24x24px (WCAG 2.2 AA 2.5.8; spacing exceptions may apply)', '', small);
  if (mid.length) add('target-44', 'P2', 'Touch targets under 44px on mobile viewport', '', mid);
  if (noName.length) add('no-name', 'P1', 'Controls with no accessible name', 'Icon-only buttons need aria-label; inputs need a label.', noName);
  if (phOnly.length) add('placeholder-label', 'P2', 'Inputs labeled only by placeholder', 'Placeholders vanish on input and are low contrast.', phOnly);
  const smallInput = inter.filter(e => ['INPUT', 'TEXTAREA', 'SELECT'].includes(e.tagName) && vw <= 820 && parseFloat(cs(e).fontSize) < 16).map(sel);
  if (smallInput.length) add('input-font', 'P3', 'Input font under 16px on mobile (iOS zooms on focus)', '', smallInput);

  // Images
  const imgs = Array.from(document.querySelectorAll('img')).filter(visible);
  const noAlt = imgs.filter(i => !i.hasAttribute('alt')).map(i => (i.currentSrc || i.src || '').slice(-50));
  if (noAlt.length) add('img-alt', 'P1', 'Images missing alt attribute', 'Use alt="" for decorative images.', noAlt);
  const noDim = imgs.filter(i => !(i.getAttribute('width') && i.getAttribute('height')) && cs(i).aspectRatio === 'auto').map(i => (i.currentSrc || i.src || '').slice(-50));
  if (noDim.length) add('img-dim', 'P3', 'Images without width/height or aspect-ratio (layout shift risk)', '', noDim);

  // ---- Typography and consistency metrics
  const textEls = all.filter(e => Array.from(e.childNodes).some(n => n.nodeType === 3 && n.textContent.trim()));
  const tally = (arr) => { const m = {}; arr.forEach(v => m[v] = (m[v] || 0) + 1); return Object.entries(m).sort((a, b) => b[1] - a[1]); };
  const sizes = tally(textEls.map(e => Math.round(parseFloat(cs(e).fontSize) * 10) / 10 + 'px'));
  const fams = tally(textEls.map(e => cs(e).fontFamily.split(',')[0].replace(/["']/g, '').trim()));
  const tcolors = tally(textEls.map(e => hex(over(toRGBA(cs(e).color) || [0, 0, 0, 1], [255, 255, 255, 1]))));
  const radii = tally(all.map(e => cs(e).borderTopLeftRadius).filter(v => v && v !== '0px'));
  const shadows = tally(all.map(e => cs(e).boxShadow).filter(v => v && v !== 'none'));
  out.metrics = {
    fontSizes: sizes.length, fontFamilies: fams.map(f => f[0]), textColors: tcolors.length, radii: radii.length, shadows: shadows.length,
    top: { sizes: sizes.slice(0, 8), radii: radii.slice(0, 6), colors: tcolors.slice(0, 8) }
  };
  const drift = [];
  if (sizes.length > 8) drift.push(`${sizes.length} distinct font sizes (aim for 5-7)`);
  if (fams.length > 3) drift.push(`${fams.length} font families: ${fams.map(f => f[0]).join(', ')}`);
  if (tcolors.length > 10) drift.push(`${tcolors.length} distinct text colors`);
  if (radii.length > 5) drift.push(`${radii.length} distinct border radii`);
  if (shadows.length > 3) drift.push(`${shadows.length} distinct box shadows`);
  if (drift.length) add('drift', 'P2', 'Possible design-system drift (values likely bypass tokens)', 'Cluster near-duplicates and map to tokens.', drift);
  const tiny = textEls.filter(e => parseFloat(cs(e).fontSize) < 12).map(e => `${sel(e)} ${cs(e).fontSize}`);
  if (tiny.length) add('tiny-text', 'P2', 'Text under 12px', '', tiny);
  const bodySize = parseFloat(cs(document.body).fontSize);
  if (bodySize < 16) add('body-size', 'P3', `Body font size is ${bodySize}px (16px recommended for web)`, '', []);
  const measure = Array.from(document.querySelectorAll('p,li')).filter(visible).filter(p => p.textContent.trim().length > 200)
    .filter(p => p.getBoundingClientRect().width / (parseFloat(cs(p).fontSize) * 0.5) > 90).map(sel);
  if (measure.length) add('measure', 'P3', 'Line length above ~90 characters', 'Aim for 45-75ch (max-width: 65ch).', measure);
  const centered = Array.from(document.querySelectorAll('p')).filter(visible).filter(p => cs(p).textAlign === 'center' && p.textContent.trim().length > 180).map(sel);
  if (centered.length) add('center-para', 'P3', 'Long centered paragraphs (hard to scan)', '', centered);

  // ---- Slop tells
  const gradText = all.filter(e => { const c = cs(e); return (c.webkitBackgroundClip === 'text' || c.backgroundClip === 'text') && /gradient/.test(c.backgroundImage); }).map(sel);
  if (gradText.length) add('gradient-text', 'P2', 'Gradient text (decorative; a common AI tell)', 'Use a solid color; emphasize with weight/size.', gradText);
  const stripes = all.filter(e => {
    const c = cs(e); const w = ['Left', 'Right'].map(s => parseFloat(c['border' + s + 'Width']) || 0);
    const other = ['Top', 'Bottom'].map(s => parseFloat(c['border' + s + 'Width']) || 0);
    const sideCol = (w[0] >= 3 && c.borderLeftStyle !== 'none' ? c.borderLeftColor : (w[1] >= 3 ? c.borderRightColor : null));
    return sideCol && Math.max(...other) === 0 && (w[0] === 0 || w[1] === 0) && (parseFloat(c.borderTopLeftRadius) > 0 || e.getBoundingClientRect().height > 40);
  }).map(sel);
  if (stripes.length) add('side-stripe', 'P2', 'Colored side-stripe borders on containers (AI tell)', 'Use a full border, background tint, or leading icon.', stripes);
  const tall = all.filter(e => { const c = cs(e); return c.transitionProperty === 'all' && c.transitionDuration.split(',').some(d => parseFloat(d) > 0); }).map(sel);
  if (tall.length) add('transition-all', 'P3', '`transition: all` (animates layout properties, jank)', 'List exact properties.', tall);
  const tight = hs.filter(h => { const c = cs(h); const fs = parseFloat(c.fontSize); const ls = parseFloat(c.letterSpacing); return fs >= 32 && !isNaN(ls) && ls / fs < -0.04; }).map(sel);
  if (tight.length) add('tight-tracking', 'P3', 'Display tracking tighter than -0.04em', '', tight);
  if (fams.length && /^inter($|\s)/i.test(fams[0][0])) add('default-font', 'P3', 'Primary font is Inter (verify it is a choice)', 'Fine if deliberate; a common unchosen default.', []);
  const emojiRe = /\p{Extended_Pictographic}/u;
  const emo = Array.from(document.querySelectorAll('button,a,h1,h2,h3,h4,li,th,label')).filter(visible).filter(e => emojiRe.test(e.textContent)).map(e => `${sel(e)}: "${e.textContent.trim().slice(0, 24)}"`);
  if (emo.length) add('emoji-icons', 'P3', 'Emoji used in UI controls/headings (icon-like use is a tell)', '', emo);
  const isCard = (e) => { const c = cs(e); const r = e.getBoundingClientRect();
    return r.width * r.height > 10000 && parseFloat(c.borderTopLeftRadius) >= 6 && (c.boxShadow !== 'none' || (parseFloat(c.borderTopWidth) > 0 && c.borderTopStyle !== 'none')); };
  const cards = all.filter(isCard).slice(0, 400); const cardSet = new Set(cards);
  const nested = cards.filter(e => { for (let p = e.parentElement; p; p = p.parentElement) if (cardSet.has(p)) return true; return false; }).map(sel);
  if (nested.length) add('nested-cards', 'P2', 'Cards nested inside cards', 'Flatten: use spacing/dividers for the inner group.', nested);
  const purple = inter.filter(e => e.tagName === 'BUTTON' || e.tagName === 'A').filter(e => {
    const b = toRGBA(cs(e).backgroundColor); if (!b || b[3] < 0.5) return false;
    const [r, g, bl] = b.map(v => v / 255); const mx = Math.max(r, g, bl), mn = Math.min(r, g, bl); const d = mx - mn; if (d < 0.25) return false;
    let h = mx === r ? ((g - bl) / d) % 6 : mx === g ? (bl - r) / d + 2 : (r - g) / d + 4; h = (h * 60 + 360) % 360; return h >= 235 && h <= 290; }).map(sel);
  if (purple.length) add('default-indigo', 'P3', 'Indigo/violet button fills (confirm this is the brand, not a framework default)', '', purple);

  // ---- Animations
  const infinite = document.getAnimations().filter(a => { try { return a.effect && a.effect.getComputedTiming().iterations === Infinity; } catch (e) { return false; } })
    .map(a => a.effect.target ? sel(a.effect.target) : 'unknown');
  out.metrics.infiniteAnimations = infinite.length;
  if (infinite.length) add('infinite-anim', 'P3', 'Infinite animations running', 'Ensure each has a purpose and a reduced-motion path.', infinite);
  return out;
}
"""

FOCUS_PREP_JS = r"""
() => {
  const sel = 'a[href],button,input:not([type=hidden]),select,textarea,summary,[role=button],[role=tab],[tabindex]:not([tabindex="-1"])';
  const snap = (e) => { const c = getComputedStyle(e); return [c.outlineStyle, c.outlineWidth, c.outlineColor, c.boxShadow, c.borderTopColor, c.backgroundColor, c.textDecorationLine, c.transform].join('|'); };
  window.__aud = {};
  let i = 0;
  document.querySelectorAll(sel).forEach(e => {
    const r = e.getBoundingClientRect(); const c = getComputedStyle(e);
    if (r.width > 0 && r.height > 0 && c.visibility !== 'hidden' && c.display !== 'none') { e.setAttribute('data-aud', i); window.__aud[i] = snap(e); i++; }
  });
  window.__snap = snap;
  return i;
}
"""

FOCUS_CHECK_JS = r"""
() => {
  const e = document.activeElement; if (!e || e === document.body || !e.hasAttribute('data-aud')) return null;
  const id = e.getAttribute('data-aud'); const now = window.__snap(e);
  const name = e.tagName.toLowerCase() + (e.id ? '#' + e.id : '') + (e.classList.length ? '.' + e.classList[0] : '');
  const r = e.getBoundingClientRect();
  return { id, name, changed: now !== window.__aud[id], offscreen: r.bottom < 0 || r.top > innerHeight };
}
"""

RUNNING_ANIM_JS = r"""
() => document.getAnimations().filter(a => { try { const t = a.effect.getComputedTiming();
  return a.playState === 'running' && (t.iterations === Infinity || t.iterations > 1); } catch (e) { return false; } })
  .map(a => a.effect.target ? a.effect.target.tagName.toLowerCase() + (a.effect.target.className ? '.' + String(a.effect.target.className).split(' ')[0] : '') : 'unknown').slice(0, 6)
"""

SEV_ORDER = {"P0": 0, "P1": 1, "P2": 2, "P3": 3}


def parse_viewports(s):
    out = []
    for part in s.split(","):
        m = re.match(r"^\s*(\d+)x(\d+)\s*$", part)
        if not m:
            sys.exit(f"Bad viewport '{part}'. Use WIDTHxHEIGHT, e.g. 375x812")
        out.append((int(m.group(1)), int(m.group(2))))
    return out


def to_url(target):
    if re.match(r"^https?://|^file://", target):
        return target
    p = Path(target)
    if p.exists():
        return p.resolve().as_uri()
    sys.exit(f"Not a URL and file not found: {target}")


def compare_images(before, after, diff_out):
    try:
        from PIL import Image, ImageChops
    except ImportError:
        return None
    a = Image.open(before).convert("RGB")
    b = Image.open(after).convert("RGB")
    w, h = min(a.width, b.width), min(a.height, b.height)
    mask = ImageChops.difference(a.crop((0, 0, w, h)), b.crop((0, 0, w, h))).convert("L").point(lambda p: 255 if p > 16 else 0)
    pct = 100.0 * mask.histogram()[255] / max(1, w * h)
    mask.save(diff_out)
    return {"changed_pct": round(pct, 2), "height_before": a.height, "height_after": b.height}


def run_page(browser, url, vw, vh, scheme, reduced, cookie, wait_ms):
    kw = dict(viewport={"width": vw, "height": vh}, color_scheme=scheme)
    if reduced:
        kw["reduced_motion"] = "reduce"
    ctx = browser.new_context(**kw)
    if cookie:
        name, _, value = cookie.partition("=")
        ctx.add_cookies([{"name": name, "value": value, "url": url}])
    page = ctx.new_page()
    logs = {"console": [], "pageerror": [], "failed": []}
    page.on("console", lambda m: logs["console"].append(m.text[:160]) if m.type == "error" else None)
    page.on("pageerror", lambda e: logs["pageerror"].append(str(e)[:160]))
    page.on("requestfailed", lambda r: logs["failed"].append(f"{r.url[:100]}"))
    try:
        page.goto(url, wait_until="networkidle", timeout=30000)
    except Exception:
        page.goto(url, wait_until="load", timeout=30000)
    try:
        page.evaluate("document.fonts && document.fonts.ready")
    except Exception:
        pass
    page.wait_for_timeout(wait_ms)
    return ctx, page, logs


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("target", help="URL or local .html file")
    ap.add_argument("--out", default="audit/run", help="output directory")
    ap.add_argument("--viewports", default="375x812,768x1024,1280x800,1536x864")
    ap.add_argument("--dark", action="store_true", help="also audit with prefers-color-scheme: dark")
    ap.add_argument("--baseline", help="directory of earlier screenshots to diff against")
    ap.add_argument("--cookie", help='cookie for authenticated pages, e.g. "session=abc123"')
    ap.add_argument("--wait", type=int, default=600, help="extra ms to wait after load (default 600)")
    ap.add_argument("--tabs", type=int, default=25, help="max Tab presses for the focus-indicator check")
    args = ap.parse_args()

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        sys.exit("Playwright missing. Run: pip install playwright && python -m playwright install chromium")

    url = to_url(args.target)
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    viewports = parse_viewports(args.viewports)
    schemes = ["light"] + (["dark"] if args.dark else [])
    merged = {}
    runtime = {"console": set(), "pageerror": set(), "failed": set()}
    shots = []
    metrics = {}

    with sync_playwright() as p:
        browser = p.chromium.launch()
        for scheme in schemes:
            for vw, vh in viewports:
                tag = f"{vw}-{scheme}"
                ctx, page, logs = run_page(browser, url, vw, vh, scheme, False, args.cookie, args.wait)
                res = page.evaluate(AUDIT_JS)
                shot = out / f"shot-{tag}.png"
                page.screenshot(path=str(shot), full_page=True)
                shots.append(shot.name)
                for k in runtime:
                    runtime[k].update(logs[k])
                if tag not in metrics:
                    metrics[tag] = res["metrics"]
                for f in res["findings"]:
                    key = (f["id"], f["title"], f["detail"])
                    m = merged.setdefault(key, {**f, "where": set(), "samples": []})
                    m["where"].add(tag)
                    for s in f["samples"]:
                        if s not in m["samples"] and len(m["samples"]) < 6:
                            m["samples"].append(s)
                # Focus indicators once per scheme at the widest viewport only
                if (vw, vh) == viewports[-1]:
                    n = page.evaluate(FOCUS_PREP_JS)
                    missing, seen = [], set()
                    for _ in range(min(args.tabs, n or 0)):
                        page.keyboard.press("Tab")
                        r = page.evaluate(FOCUS_CHECK_JS)
                        if not r:
                            break
                        if r["id"] in seen:
                            break
                        seen.add(r["id"])
                        if not r["changed"]:
                            missing.append(r["name"])
                    if missing:
                        key = ("focus-indicator", "No visible focus indicator on keyboard focus", "")
                        m = merged.setdefault(key, {"id": "focus-indicator", "sev": "P1", "title": key[1], "detail": "Add a :focus-visible outline/ring with >=3:1 contrast.",
                                                    "count": len(missing), "samples": missing[:6], "where": set()})
                        m["where"].add(tag)
                ctx.close()
        # Reduced motion check (first viewport, light)
        vw, vh = viewports[0]
        ctx, page, _ = run_page(browser, url, vw, vh, "light", True, args.cookie, args.wait)
        running = page.evaluate(RUNNING_ANIM_JS)
        if running:
            merged[("rm", "Looping/repeating animations still run under prefers-reduced-motion", "")] = {
                "id": "reduced-motion", "sev": "P2", "title": "Looping/repeating animations still run under prefers-reduced-motion",
                "detail": "Provide a reduced-motion variant (fade or none).", "count": len(running), "samples": running, "where": {"reduced-motion"}}
        ctx.close()
        browser.close()

    # Runtime issues
    for k, label, sev in (("pageerror", "JavaScript page errors", "P1"), ("console", "Console errors", "P2"), ("failed", "Failed network requests", "P2")):
        if runtime[k]:
            merged[(k, label, "")] = {"id": k, "sev": sev, "title": label, "detail": "", "count": len(runtime[k]),
                                      "samples": sorted(runtime[k])[:6], "where": {"runtime"}}

    findings = sorted(merged.values(), key=lambda f: (SEV_ORDER.get(f["sev"], 9), f["id"]))
    for f in findings:
        f["where"] = sorted(f["where"])

    diffs = {}
    if args.baseline:
        base = Path(args.baseline)
        (out / "diff").mkdir(exist_ok=True)
        for name in shots:
            b = base / name
            if b.exists():
                d = compare_images(b, out / name, out / "diff" / name)
                if d:
                    diffs[name] = d

    report = {"url": url, "viewports": [f"{w}x{h}" for w, h in viewports], "schemes": schemes,
              "findings": findings, "metrics": metrics, "screenshots": shots, "diffs": diffs}
    (out / "report.json").write_text(json.dumps(report, indent=2))

    counts = {s: sum(1 for f in findings if f["sev"] == s) for s in SEV_ORDER}
    lines = [f"# UI audit: {url}", "",
             f"Viewports: {', '.join(report['viewports'])} | Themes: {', '.join(schemes)}",
             f"Findings: P0={counts['P0']} P1={counts['P1']} P2={counts['P2']} P3={counts['P3']}", ""]
    for f in findings:
        lines.append(f"## [{f['sev']}] {f['title']}")
        if f["detail"]:
            lines.append(f["detail"])
        lines.append(f"Seen in: {', '.join(f['where'])}" + (f" | count: {f['count']}" if f["count"] else ""))
        for s in f["samples"]:
            lines.append(f"- {s}")
        lines.append("")
    first = next(iter(metrics.values()), {})
    if first:
        lines += ["## Consistency metrics (first viewport)",
                  f"- distinct font sizes: {first.get('fontSizes')} | families: {', '.join(first.get('fontFamilies', [])[:4])}",
                  f"- distinct text colors: {first.get('textColors')} | radii: {first.get('radii')} | shadows: {first.get('shadows')}", ""]
    if diffs:
        lines.append("## Screenshot diff vs baseline")
        for n, d in diffs.items():
            lines.append(f"- {n}: {d['changed_pct']}% pixels changed (page height {d['height_before']} -> {d['height_after']})")
        lines.append("")
    lines.append("Screenshots: " + ", ".join(shots))
    lines.append("Note: automated checks cover the measurable half. Review screenshots for hierarchy, rhythm, tone.")
    md = "\n".join(lines)
    (out / "report.md").write_text(md)
    print(md)


if __name__ == "__main__":
    main()
