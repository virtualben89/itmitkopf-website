import re, resvg_py, pathlib, sys
d = pathlib.Path(sys.argv[1])
def inner(n):
    s = (d/n).read_text()
    s = re.sub(r'<\?xml[^>]*\?>', '', s).strip()
    vb = re.search(r'viewBox="([^"]+)"', s).group(1)
    body = re.sub(r'^<svg[^>]*>', '', s); body = re.sub(r'</svg>\s*$', '', body)
    return vb, body
def nest(n, x, y, w, h, idsuffix, extra=''):
    vb, body = inner(n)
    body = body.replace('id="gm"', f'id="gm{idsuffix}"').replace('url(#gm)', f'url(#gm{idsuffix})')
    return f'<svg x="{x}" y="{y}" width="{w}" height="{h}" viewBox="{vb}" {extra}>{body}</svg>'
W, H = 1240, 760
parts = [f'<rect width="{W}" height="{H}" fill="#ffffff"/>',
 '<rect x="0" y="0" width="620" height="520" fill="#F8FAFC"/>', '<rect x="620" y="0" width="620" height="520" fill="#0B1220"/>',
 nest('logo-color.svg', 30, 20, 560, 480, 'a'), nest('logo-color.svg', 650, 20, 560, 480, 'b'),
 nest('favicon.svg', 40, 560, 92, 100, 'c'), nest('favicon.svg', 160, 590, 32, 35, 'd'), nest('favicon.svg', 220, 600, 16, 18, 'e'),
 '<clipPath id="cp"><circle cx="360" cy="630" r="80"/></clipPath>',
 '<g clip-path="url(#cp)">' + nest('bimi.svg', 280, 550, 160, 160, 'f') + '</g>',
 '<circle cx="360" cy="630" r="80" fill="none" stroke="#bbb"/>',
 nest('logo-color.svg', 500, 560, 200, 170, 'g'), nest('logo-color.svg', 740, 590, 110, 100, 'h')]
svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">' + ''.join(parts) + '</svg>'
png = resvg_py.svg_to_bytes(svg_string=svg)
(d/'preview.png').write_bytes(bytes(png))
print(len(png))
