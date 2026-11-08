# Builds assets/terminal-dark.svg and assets/terminal-light.svg for the profile README.
# Edit the `lines` list below, then run from the repository root:
#
#   python3 scripts/make_terminal.py
#
import sys, os
out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets")

THEMES = {
    "dark":  dict(bg="#0d1117", bar="#161b22", border="#30363d", text="#e6edf3", muted="#8b949e",
                  prompt="#3fb950", path="#58a6ff", accent="#d2a8ff", warm="#ffa657"),
    "light": dict(bg="#ffffff", bar="#f6f8fa", border="#d0d7de", text="#1f2328", muted="#59636e",
                  prompt="#1a7f37", path="#0969da", accent="#8250df", warm="#bc4c00"),
}

W, X0, LH, TOP = 720, 28, 23, 74

def esc(s): return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

# Each line: list of (x_offset_chars, text, color_key, bold). None = blank line. "prompt" lines get the prompt prefix.
P = "prompt"
lines = [
    (P, "whoami"),
    [(0, "Dinçer Tekin", "text", True), (13, "· Computer Engineering student · software developer", "muted", False)],
    [(0, "I build fast, private software that people actually use.", "text", False)],
    None,
    (P, "ls projects/"),
    [(0, "reclaimer/", "accent", True),      (17, "gets back deleted photos and files", "text", False), (60, "Rust", "muted", False)],
    [(0, "bloogla/", "accent", True),        (17, "a whole blog in one small program", "text", False),  (60, "Rust", "muted", False)],
    [(0, "pass1/", "accent", True),          (17, "passwords only you can read", "text", False),        (60, "TypeScript", "muted", False)],
    [(0, "theme-switcher/", "accent", True), (17, "Windows dark mode that follows the sun", "text", False), (60, "Rust", "muted", False)],
    [(0, "alaz/", "accent", True),           (17, "an operating system, from scratch", "text", False),  (60, "C · Assembly", "muted", False)],
    None,
    (P, "cat about.txt"),
    [(0, "languages", "warm", False), (12, "Rust · TypeScript · Python · C · C#", "text", False)],
    [(0, "focus", "warm", False),     (12, "security · systems programming · web apps", "text", False)],
    [(0, "teaching", "warm", False),  (12, "5,000+ subscribers learning to code on YouTube", "text", False)],
    [(0, "open to", "warm", False),   (12, "internships · junior software & security roles", "text", True)],
    None,
    (P, ""),
]

CW = 8.6  # approx. monospace advance at 14.5px
PROMPT = [("dincer", "prompt"), ("@", "muted"), ("github", "prompt"), (":", "muted"), ("~", "path"), ("$ ", "muted")]
PLEN = sum(len(t) for t, _ in PROMPT)

def build(name, c):
    H = TOP + LH * len(lines) + 10
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="t">',
         '<title id="t">Terminal: Dinçer Tekin, Computer Engineering student and software developer. Projects: Reclaimer, Bloogla, pass1, theme-switcher, Alaz. Open to internships and junior software and security engineer roles.</title>',
         '<style>',
         "text{font-family:ui-monospace,SFMono-Regular,'SF Mono',Menlo,Consolas,'Liberation Mono',monospace;font-size:14.5px;white-space:pre}",
         '.b{font-weight:700}',
         # Lines fade in one by one. Without animation support, everything is simply visible.
         '.l{animation:in .25s ease-out both}',
         '@keyframes in{from{opacity:0;transform:translateY(4px)}to{opacity:1;transform:none}}',
         '.cur{animation:blink 1.1s steps(1) infinite}',
         '@keyframes blink{50%{opacity:0}}',
         '@media (prefers-reduced-motion:reduce){.l,.cur{animation:none}}',
         '</style>',
         f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="12" fill="{c["bg"]}" stroke="{c["border"]}"/>',
         f'<path d="M.5 40V12.5a12 12 0 0 1 12-12h{W-25}a12 12 0 0 1 12 12V40z" fill="{c["bar"]}"/>',
         f'<line x1="0" y1="40.5" x2="{W}" y2="40.5" stroke="{c["border"]}"/>',
         '<circle cx="24" cy="20" r="6" fill="#ff5f57"/><circle cx="44" cy="20" r="6" fill="#febc2e"/><circle cx="64" cy="20" r="6" fill="#28c840"/>',
         f'<text x="{W/2}" y="25" text-anchor="middle" fill="{c["muted"]}" style="font-size:13px">dincer@github: ~</text>']
    delay = 0.2
    for i, ln in enumerate(lines):
        y = TOP + i * LH
        if ln is None:
            continue
        g = [f'<g class="l" style="animation-delay:{delay:.2f}s">']
        if ln[0] == P:
            spans = "".join(f'<tspan fill="{c[k]}">{esc(t)}</tspan>' for t, k in PROMPT)
            g.append(f'<text x="{X0}" y="{y}" class="b">{spans}</text>')
            cmd = ln[1]
            if cmd:
                g.append(f'<text x="{X0 + PLEN*CW:.1f}" y="{y}" fill="{c["text"]}">{esc(cmd)}</text>')
            else:
                g.append(f'<rect class="cur" x="{X0 + PLEN*CW:.1f}" y="{y-13}" width="9" height="17" fill="{c["text"]}"/>')
            delay += 0.55
        else:
            for off, t, k, bold in ln:
                cls = ' class="b"' if bold else ""
                g.append(f'<text x="{X0 + off*CW:.1f}" y="{y}" fill="{c[k]}"{cls}>{esc(t)}</text>')
            delay += 0.18
        g.append("</g>")
        o.append("".join(g))
    o.append("</svg>")
    with open(os.path.join(out, f"terminal-{name}.svg"), "w") as f:
        f.write("\n".join(o) + "\n")

for n, c in THEMES.items():
    build(n, c)
