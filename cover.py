import math

W, H = 350, 516   # canvas size in pixels
N = 11              # number of ridges

THEMES = {
    "dark":  dict(bg="#0d1024", top="#3b3f9e", bot="#ff7a59", txt="#f4f1ff", sub="#a9aed6", edge="#ffffff"),
    "light": dict(bg="#f5f1ea", top="#2a7f86", bot="#d9902f", txt="#1d2430", sub="#5b6472", edge="#ffffff"),
}

TITLE = ["Exploratory Analysis", "of Bayesian Models"]
SUBTITLE = ["Visualization, diagnostics, model checking", "and comparison with ArviZ"]
AUTHORS = "OSVALDO A. MARTIN - ORIOL ABRIL-PLA - JORDAN DEKLERK"

SERIF = "Fraunces, 'Source Serif 4', Georgia, 'Times New Roman', serif"
SANS = "Inter, 'Helvetica Neue', Arial, sans-serif"


def lerp(a, b, t):
    return a + (b - a) * t


def smooth(t):
    t = max(0.0, min(1.0, t))
    return t * t * (3 - 2 * t)


def mix(c1, c2, t):
    a = [int(c1[i:i + 2], 16) for i in (1, 3, 5)]
    b = [int(c2[i:i + 2], 16) for i in (1, 3, 5)]
    return "#%02x%02x%02x" % tuple(round(lerp(a[i], b[i], t)) for i in range(3))


def ridge(i, n, W, H):
    """Return (filled path, outline path) for ridge i of n."""
    t = i / (n - 1)
    x0, x1 = 0.0875 * W, 0.9125 * W                     # side margins
    sigma = lerp(0.1875, 0.053, t ** 0.85) * W          # wide prior -> tight posterior
    height = lerp(0.043, 0.133, t ** 0.9) * H           # low -> tall
    center = W * (0.5 + lerp(-0.075, 0.056, t)) + 0.025 * W * math.sin(i * 1.7)
    skew = lerp(0.1125, 0.031, t) * W * (1 if i % 2 else -1)
    top, bottom = 0.461 * H, 0.883 * H                  # vertical extent of baselines
    base = lerp(top, bottom, t)
    taper_w = 0.0875 * W
    pts = []
    steps = 270
    for k in range(steps + 1):
        x = lerp(x0, x1, k / steps)
        g1 = math.exp(-0.5 * ((x - center) / sigma) ** 2)
        g2 = 0.45 * math.exp(-0.5 * ((x - center - skew) / (sigma * 0.7)) ** 2)
        taper = smooth((x - x0) / taper_w) * smooth((x1 - x) / taper_w)
        pts.append((x, base - height * (g1 + g2) / 1.3 * taper))
    line = "M" + " L".join("%.1f,%.1f" % p for p in pts)
    area = "M%.1f,%.1f L" % (x0, base) + " L".join("%.1f,%.1f" % p for p in pts) + " L%.1f,%.1f Z" % (x1, base)
    return area, line


def build(theme, W, H, n):
    colors = THEMES[theme]
    scale = min(W, H) / 1600
    left = 0.05 * W
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">',
           f'<rect width="{W}" height="{H}" fill="{colors["bg"]}"/>']

    for i in range(n):
        fill = mix(colors["top"], colors["bot"], i / (n - 1))
        stroke = mix(fill, colors["edge"], 0.55)
        area, line = ridge(i, n, W, H)
        out.append(f'<path d="{area}" fill="{fill}"/>')
        out.append(f'<path d="{line}" fill="none" stroke="{stroke}" stroke-width="{3 * scale:.2f}" stroke-linejoin="round"/>')

    y = 0.117 * H
    for line in TITLE:
        out.append(f'<text x="{left:.1f}" y="{y:.1f}" font-family="{SERIF}" font-size="{132 * scale:.1f}" '
                   f'font-weight="600" fill="{colors["txt"]}">{line}</text>')
        y += 140 * scale
    y += -140 * scale + 110 * scale
    for line in SUBTITLE:
        out.append(f'<text x="{left:.1f}" y="{y:.1f}" font-family="{SANS}" font-size="{65 * scale:.1f}" '
                   f'fill="{colors["sub"]}">{line}</text>')
        y += 65 * scale
    out.append(f'<text x="{left:.1f}" y="{0.953 * H:.1f}" font-family="{SANS}" font-size="{45 * scale:.1f}" '
               f'letter-spacing="{2 * scale:.1f}" fill="{colors["sub"]}">{AUTHORS}</text>')
    out.append("</svg>")
    return "\n".join(out)


with open(f"cover.svg", "w") as f:
    f.write(build("light", W, H, N))