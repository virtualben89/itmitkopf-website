#!/usr/bin/env python3
"""IT mit Kopf logo v3: hand-painted look inspired by the original (stacked words, red/orange-yellow/teal,
drips + splatter). Text is converted to vector paths (Rubik Wet Paint, SIL OFL 1.1). Usage: make_logo2.py OUTDIR [font.ttf]"""
import os, random, sys
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen

OUT = sys.argv[1] if len(sys.argv) > 1 else "."
FONT = sys.argv[2] if len(sys.argv) > 2 else "RubikWetPaint-Regular.ttf"
RED, ORANGE, YELLOW, TEAL = "#D93A22", "#EE7B1B", "#FDB913", "#3E8F86"

font = TTFont(FONT)
gs = font.getGlyphSet()
cmap = font.getBestCmap()
upm = font["head"].unitsPerEm


PREC = 1


def fmt(v):
    t = ("%.*f" % (PREC, v))
    return t.rstrip("0").rstrip(".") if "." in t else t


def word(txt, size, x, y, tracking=0.0):
    s = size / upm
    d, cx = [], x
    bx0 = by0 = 1e9
    bx1 = by1 = -1e9
    for ch in txt:
        g = gs[cmap[ord(ch)]]
        pen = SVGPathPen(gs, ntos=fmt)
        g.draw(TransformPen(pen, (s, 0, 0, -s, cx, y)))
        d.append(pen.getCommands())
        bp = BoundsPen(gs)
        g.draw(TransformPen(bp, (s, 0, 0, -s, cx, y)))
        if bp.bounds:
            a, b, c, e = bp.bounds
            bx0, by0, bx1, by1 = min(bx0, a), min(by0, b), max(bx1, c), max(by1, e)
        cx += g.width * s + tracking * size
    return " ".join(d), (bx0, by0, bx1, by1)


def build(bg=None, bimi=False):
    # --- layout: line 1 "IT" + "MIT", line 2 "KOPF" scaled to the same width
    s1, s2 = 150, 205
    gap = 34
    d_it, b_it = word("IT", s1, 0, 0)
    w_it = b_it[2] - b_it[0]
    d_mit, b_mit = word("MIT", s1, 0, 0)
    d_kopf, b_kopf = word("KOPF", s2, 0, 0)
    line1_w = w_it + gap + (b_mit[2] - b_mit[0])
    line2_w = b_kopf[2] - b_kopf[0]
    k = line2_w / line1_w                       # scale line 1 so both lines have equal width
    s1 *= k
    d_it, b_it = word("IT", s1, 0, 0)
    d_mit, b_mit = word("MIT", s1, 0, 0)
    pad = 70
    x0 = pad
    base1 = pad + (-b_it[1])                    # baseline line 1 (b[1] is negative = above baseline)
    h1 = -b_it[1]
    base2 = base1 + 36 + (-b_kopf[1]) + 8
    d_it, b_it = word("IT", s1, x0 - b_it[0], base1)
    x_mit = x0 + (b_it[2] - b_it[0]) + gap
    d_mit, b_mit = word("MIT", s1, x_mit - word("MIT", s1, 0, 0)[1][0], base1)
    d_kopf, b_kopf = word("KOPF", s2, x0 - word("KOPF", s2, 0, 0)[1][0], base2)
    W = int(b_kopf[2] + pad)
    H = int(b_kopf[3] + 60)

    rnd = random.Random(7)

    def splat(box, color, n, rmin, rmax, spread=34):
        x0_, y0_, x1_, y1_ = box
        out = []
        for _ in range(n):
            # sample points in a band around the word box
            x = rnd.uniform(x0_ - spread, x1_ + spread)
            y = rnd.uniform(y0_ - spread, y1_ + spread)
            r = rnd.choice([rmin, rmin, (rmin + rmax) / 2, rmax])
            out.append(f'<circle cx="{fmt(x)}" cy="{fmt(y)}" r="{fmt(r)}"/>')
        return f'<g fill="{color}">' + "".join(out) + "</g>"

    blobs = (
        f'<g fill="{RED}"><circle cx="{pad-34}" cy="{base1-h1+8}" r="17"/><circle cx="{pad-48}" cy="{base1-h1*0.45}" r="22"/>'
        f'<path d="M{pad-52} {base1-h1*0.45+18} q4 24 0 34 q-6 -12 0 -34z"/></g>'
        f'<g fill="{YELLOW}"><circle cx="{W-pad+30}" cy="{base1+22}" r="15"/><circle cx="{W-pad+4}" cy="{base1+50}" r="21"/></g>'
        f'<g fill="{TEAL}"><circle cx="{pad-40}" cy="{base2-60}" r="14"/><circle cx="{pad-22}" cy="{base2-40}" r="12"/><circle cx="{pad-36}" cy="{base2-16}" r="16"/></g>'
    )
    box_it = (b_it[0], b_it[1], b_it[2], b_it[3])
    spl = (
        splat(box_it, RED, 22, 1.6, 5)
        + splat(b_mit, YELLOW, 14, 1.5, 4.5)
        + splat(b_kopf, TEAL, 30, 1.5, 5)
    )

    grad_id = "gm"
    if bimi:
        fill_mit = ORANGE
        defs = ""
    else:
        fill_mit = f"url(#{grad_id})"
        defs = (f'<defs><linearGradient id="{grad_id}" gradientUnits="userSpaceOnUse" x1="{fmt(b_mit[0])}" y1="0" '
                f'x2="{fmt(b_mit[2])}" y2="0"><stop offset="0" stop-color="{ORANGE}"/><stop offset="1" stop-color="{YELLOW}"/>'
                f'</linearGradient></defs>')
    rect = f'<rect width="{W}" height="{H}" fill="{bg}"/>' if bg else ""
    body = (f'{defs}{rect}{spl}{blobs}'
            f'<path d="{d_it}" fill="{RED}"/><path d="{d_mit}" fill="{fill_mit}"/><path d="{d_kopf}" fill="{TEAL}"/>')
    return W, H, body


def write(name, bg=None):
    W, H, body = build(bg)
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-labelledby="t">'
           f'<title id="t">IT mit Kopf</title>{body}</svg>\n')
    open(os.path.join(OUT, name), "w").write(svg)
    return W, H


print(write("logo-color.svg"))

# ---- icon (favicon / avatar): red "IT" with orange/yellow and teal paint dots
def icon(name, bg=None):
    size = 180
    d, b = word("IT", size, 0, 0)
    w, h = b[2] - b[0], -b[1]
    d, b = word("IT", size, 40 - b[0], 40 + h)
    W, H = int(w + 80), int(h + 150)
    rect = f'<rect width="{W}" height="{H}" rx="40" fill="{bg}"/>' if bg else ""
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}">{rect}'
           f'<path d="{d}" fill="{RED}"/>'
           f'<circle cx="{int(W*0.30)}" cy="{H-42}" r="26" fill="{ORANGE}"/>'
           f'<circle cx="{int(W*0.55)}" cy="{H-38}" r="20" fill="{YELLOW}"/>'
           f'<circle cx="{int(W*0.77)}" cy="{H-44}" r="24" fill="{TEAL}"/></svg>\n')
    open(os.path.join(OUT, name), "w").write(svg)
    return W, H

print(icon("favicon.svg"))

# ---- BIMI (SVG Tiny-PS style): square, solid white bg, solid fills only, wordmark inside circular safe area
PREC = 0   # integer coordinates keep the file under the 32 KB BIMI limit
Wb, Hb, body = build(None, bimi=True)
PREC = 1
sc = 0.135
tx, ty = (120 - Wb * sc) / 2, (120 - Hb * sc) / 2
bimi = ('<?xml version="1.0" encoding="UTF-8"?>\n'
        '<svg xmlns="http://www.w3.org/2000/svg" version="1.2" baseProfile="tiny-ps" viewBox="0 0 120 120">'
        '<title>IT mit Kopf</title><rect width="120" height="120" fill="#FFFFFF"/>'
        f'<g transform="translate({fmt(tx)} {fmt(ty)}) scale({sc})">{body}</g></svg>\n')
open(os.path.join(OUT, "bimi.svg"), "w").write(bimi)

