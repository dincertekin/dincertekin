# Builds the README badges in assets/badges/ (a dark and a light version of each).
# Add or change a badge in BADGES below, then run from the repository root:
#
#   python3 scripts/make_badges.py
#
# Use one in a README (swap "rust" for the badge name):
#
#   <picture>
#     <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/dincertekin/dincertekin/main/assets/badges/rust-dark.svg">
#     <img src="https://raw.githubusercontent.com/dincertekin/dincertekin/main/assets/badges/rust-light.svg" alt="Rust" height="28">
#   </picture>
import os, re

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
ICONS = os.path.join(ROOT, "scripts", "badge-icons")
OUT = os.path.join(ROOT, "assets", "badges")

# Simple line icons drawn on a 24x24 grid, for things without a brand logo.
LINE_ICONS = {
    "license":  "M12 4v16M6 20h12M4 7h16M7 7l-3 7a3 3 0 0 0 6 0zM17 7l-3 7a3 3 0 0 0 6 0z",
    "download": "M12 3v12M7 10l5 5 5-5M4 20h16",
    "chip":     "M7 7h10v10H7zM10 3v4M14 3v4M10 17v4M14 17v4M3 10h4M3 14h4M17 10h4M17 14h4",
    "terminal": "M3 5h18v14H3zM7 9l3 3-3 3M13 15h4",
    "sprout":   "M12 21v-9M12 12C12 8 9 6 5 6c0 4 3 6 7 6zM12 10c0-3 2-5 6-5 0 3-2 5-6 5z",
}

# name: (icons, text, style)
BADGES = {
    "rust":            (["rust"], "Rust", None),
    "typescript":      (["typescript"], "TypeScript", None),
    "react":           (["react"], "React", None),
    "python":          (["python"], "Python 3", None),
    "python-313":      (["python"], "Python 3.13+", None),
    "vue":             (["vuedotjs"], "Vue 3", None),
    "textual":         (["terminal"], "Textual", None),
    "c-assembly":      (["c"], "C · Assembly", None),
    "x86-64":          (["chip"], "x86_64", None),
    "early-days":      (["sprout"], "Early days", None),
    "self-hosted":     (["docker"], "Self-hosted", None),
    "mit":             (["license"], "MIT license", None),
    "download":        (["download"], "Download", "accent"),
    "macos-windows-linux": (["apple", "windows", "linux"], "macOS · Windows · Linux", None),
    "linux-windows-docker": (["linux", "windows", "docker"], "Linux · Windows · Docker", None),
    "windows":         (["windows"], "Windows 10 · 11", None),
}

THEMES = {
    "dark":  {"bg": "#161b22", "border": "#30363d", "fg": "#e6edf3"},
    "light": {"bg": "#f6f8fa", "border": "#d0d7de", "fg": "#1f2328"},
}
ACCENT = {"bg": "#1f883d", "border": "#1a7f37", "fg": "#ffffff"}

H, PAD, ICON, GAP, ICON_GAP, CHAR = 28, 11, 14, 7, 5, 7.25

def brand_path(name):
    with open(os.path.join(ICONS, f"{name}.svg")) as f:
        return re.search(r'<path d="([^"]+)"', f.read()).group(1)

def icon(name, x, color):
    s = ICON / 24
    y = (H - ICON) / 2
    if name in LINE_ICONS:
        return (f'<path transform="translate({x:.1f} {y:.1f}) scale({s:.4f})" d="{LINE_ICONS[name]}" '
                f'fill="none" stroke="{color}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>')
    return f'<path transform="translate({x:.1f} {y:.1f}) scale({s:.4f})" d="{brand_path(name)}" fill="{color}"/>'

def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;")

def badge(icons, text, c):
    icons_w = len(icons) * ICON + (len(icons) - 1) * ICON_GAP
    w = round(PAD + icons_w + GAP + len(text) * CHAR + PAD)
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{H}" viewBox="0 0 {w} {H}" role="img" aria-label="{esc(text)}">',
             f'<title>{esc(text)}</title>',
             f'<rect x=".5" y=".5" width="{w-1}" height="{H-1}" rx="8" fill="{c["bg"]}" stroke="{c["border"]}"/>']
    x = PAD
    for name in icons:
        parts.append(icon(name, x, c["fg"]))
        x += ICON + ICON_GAP
    x += GAP - ICON_GAP
    parts.append(f'<text x="{x:.1f}" y="18.5" fill="{c["fg"]}" font-family="ui-monospace,SFMono-Regular,\'SF Mono\',Menlo,Consolas,\'Liberation Mono\',monospace" font-size="12" font-weight="600">{esc(text)}</text>')
    parts.append("</svg>")
    return "".join(parts) + "\n"

os.makedirs(OUT, exist_ok=True)
for name, (icons, text, style) in BADGES.items():
    for theme, colors in THEMES.items():
        with open(os.path.join(OUT, f"{name}-{theme}.svg"), "w") as f:
            f.write(badge(icons, text, ACCENT if style == "accent" else colors))
print(f"{len(BADGES)} badges written to {os.path.relpath(OUT, ROOT)}/")
