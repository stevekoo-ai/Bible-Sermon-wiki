"""페르시아 왕 5명 아이콘 (SVG) — 에스라 7장 설교 PPT용. 사용: python scripts/make_king_icons.py <출력폴더>"""
import sys, pathlib
BG = ('<defs><linearGradient id="g" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8da0e0"/>'
      '<stop offset="1" stop-color="#2f3f94"/></linearGradient></defs>'
      '<circle cx="100" cy="100" r="96" fill="url(#g)" stroke="#e8edff" stroke-width="3"/>')
W, B, GOLD = '#ffffff', '#2f3f94', '#ffd98a'
ICONS = {
 '1_고레스_원통': f'''<ellipse cx="100" cy="58" rx="34" ry="11" fill="{W}"/>
<path d="M66 58v82a34 11 0 0 0 68 0V58a34 11 0 0 1-68 0z" fill="{W}" stroke="#cfd8ff" stroke-width="2"/>
<g stroke="{B}" stroke-width="3" stroke-linecap="round"><path d="M76 82h8m6 0h8m6 0h8m6 0h8M76 98h8m6 0h8m6 0h8m6 0h8M76 114h8m6 0h8m6 0h8m6 0h8"/></g>''',
 '2_캄비세스_피라미드': f'''<polygon points="100,50 154,140 46,140" fill="{W}"/><polygon points="100,50 154,140 112,140" fill="#dfe6ff"/>
<g stroke="{B}" stroke-width="2.5"><path d="M82 112h36M72 128h56"/></g>
<circle cx="150" cy="56" r="11" fill="{GOLD}"/><path d="M40 146h120" stroke="{W}" stroke-width="4" stroke-linecap="round"/>''',
 '3_다리오_칙령두루마리': f'''<rect x="62" y="56" width="76" height="88" rx="4" fill="{W}"/>
<rect x="54" y="50" width="92" height="12" rx="6" fill="#cfd8ff"/><rect x="54" y="138" width="92" height="12" rx="6" fill="#cfd8ff"/>
<g stroke="{B}" stroke-width="3" stroke-linecap="round"><path d="M74 78h52M74 92h52M74 106h34"/></g>
<circle cx="120" cy="120" r="11" fill="#e0453a"/><circle cx="120" cy="120" r="5" fill="#ff8a80"/>''',
 '4_아하수에로_왕관과홀': f'''<path d="M52 112l-8-40 30 22 26-36 26 36 30-22-8 40z" fill="{GOLD}"/>
<rect x="52" y="112" width="96" height="14" rx="3" fill="#f2b84b"/>
<circle cx="44" cy="70" r="5" fill="{W}"/><circle cx="100" cy="54" r="5" fill="{W}"/><circle cx="156" cy="70" r="5" fill="{W}"/>
<path d="M62 160L146 138" stroke="{W}" stroke-width="5" stroke-linecap="round"/><circle cx="150" cy="137" r="7" fill="{GOLD}"/>''',
 '5_아닥사스다_술잔': f'''<path d="M64 56h72c0 36-14 56-36 56S64 92 64 56z" fill="{W}"/>
<path d="M68 70h64c-2 14-8 24-14 30h-36c-6-6-12-16-14-30z" fill="#e0453a" opacity=".85"/>
<rect x="95" y="110" width="10" height="26" fill="{W}"/><ellipse cx="100" cy="142" rx="28" ry="7" fill="{W}"/>
<circle cx="146" cy="60" r="9" fill="none" stroke="{GOLD}" stroke-width="5"/><rect x="141" y="49" width="10" height="7" rx="2" fill="{GOLD}"/>''',
}
def svg(body, size=200):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" width="{size}" height="{size}">{BG}{body}</svg>'
out = pathlib.Path(sys.argv[1]); out.mkdir(parents=True, exist_ok=True)
for name, body in ICONS.items():
    (out / f'{name}.svg').write_text(svg(body), encoding='utf-8')
sheet = ''.join(f'<g transform="translate({i*210+5},5)">{BG}{b}</g>' for i, b in enumerate(ICONS.values()))
(out / '왕아이콘_모음.svg').write_text(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1060 210" width="1060" height="210">{sheet}</svg>', encoding='utf-8')
print('ok', len(ICONS))
