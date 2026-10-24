"""묵상 노트·주해 등 위키 md 문서를 읽기 편한 HTML로 변환한다.

사용법:
    python scripts/note_to_html.py <노트.md 또는 폴더> [...] [--stale]
같은 폴더에 같은 이름의 .html을 만든다. 폴더를 주면 하위 .md 전부(9_Archive 제외),
--stale 이면 md가 html보다 새로운 것만 다시 만든다.

원칙 (2026-10-24, Steve 지시): Claude는 md만 작성하고 HTML은 이 도구가 만든다
— HTML을 손으로 다시 쓰는 토큰 낭비를 막기 위함.

읽기 규칙 (Steve 요청, 2026-10-24):
- 문장이 끝나거나 문장 부호(. ? ! … , ; : — →)가 나오면 줄을 바꾼다.
- 단, 괄호·따옴표 안이거나 부호 뒤에 공백이 없으면(7:10, 1,400 등) 바꾸지 않는다.
"""
import html
import re
import sys
from pathlib import Path

BREAK_AFTER = set('.?!…,;:')
BREAK_BEFORE_TOKENS = ('→', '—')
OPEN = '(["“‘「『['
CLOSE = ')]”’」』]'
HEBREW = re.compile(r'([֐-׿][֐-׿\s\-־׃]*[֐-׿׃])')


B_OPEN, B_CLOSE = '\x01', '\x02'  # **굵게** 를 줄바꿈 전에 표시로 바꿔 두었다가 줄마다 다시 닫고 연다


def split_lines(text):
    """문장 부호 기준으로 줄을 나눈다 (괄호/따옴표 안은 제외)."""
    n = 0

    def mark(_):
        nonlocal n
        n += 1
        return B_OPEN if n % 2 else B_CLOSE
    text = re.sub(r'\*\*', mark, text)
    out, buf, depth, in_straight = [], '', 0, False
    for i, ch in enumerate(text):
        if ch == '"':
            in_straight = not in_straight
        elif ch in '([“‘「『':
            depth += 1
        elif ch in ')]”’」』' and depth > 0:
            depth -= 1
        free = depth == 0 and not in_straight
        # → 와 — 는 그 앞에서 줄을 바꾼다
        if ch in BREAK_BEFORE_TOKENS and free and buf.strip() and i > 0 and text[i - 1] == ' ':
            out.append(buf.strip())
            buf = ''
        # 공백을 만났을 때, 바로 앞(닫는 괄호·따옴표·굵게 표시 제외)이 문장 부호면 줄을 바꾼다
        if ch == ' ' and free:
            tail = buf.rstrip(')”"’' + B_CLOSE)
            if tail and tail[-1] in BREAK_AFTER and not re.fullmatch(r'\s*\d+\.', buf):
                out.append(buf.strip())
                buf = ''
                continue
        buf += ch
    if buf.strip():
        out.append(buf.strip())
    # 굵게가 줄을 넘어가면 줄 끝에서 닫고 다음 줄에서 다시 연다
    fixed, bold = [], False
    for ln in out:
        if bold:
            ln = B_OPEN + ln
        for c in ln:
            if c == B_OPEN:
                bold = True
            elif c == B_CLOSE:
                bold = False
        if bold:
            ln += B_CLOSE
        fixed.append(ln)
    return fixed


def inline(s):
    s = html.escape(s, quote=False)
    s = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', s)
    s = re.sub(r'(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])', r'<em>\1</em>', s)
    s = re.sub(r'`(.+?)`', r'<code>\1</code>', s)
    s = re.sub(r'\[\[([^\]|]+)(?:\|([^\]]+))?\]\]',
               lambda m: f'<span class="wl" title="{m.group(1)}">{m.group(2) or m.group(1)}</span>', s)
    s = HEBREW.sub(r'<span class="he" dir="rtl" lang="he">\1</span>', s)
    return s.replace(B_OPEN, '<strong>').replace(B_CLOSE, '</strong>')


def para(text):
    return '<br>'.join(inline(x) for x in split_lines(text))


def parse_frontmatter(lines):
    meta = {}
    if lines and lines[0].strip() == '---':
        for j in range(1, len(lines)):
            if lines[j].strip() == '---':
                for ln in lines[1:j]:
                    if ':' in ln:
                        k, v = ln.split(':', 1)
                        meta[k.strip()] = v.strip().strip('"')
                return meta, lines[j + 1:]
    return meta, lines


def render_body(lines):
    out = []
    i = 0
    list_stack = []  # (indent, tag)

    def close_lists(to_indent=-1):
        while list_stack and list_stack[-1][0] > to_indent:
            out.append(f'</li></{list_stack.pop()[1]}>')

    while i < len(lines):
        ln = lines[i].rstrip('\n')
        s = ln.strip()
        m_li = re.match(r'^(\s*)([-*]|\d+\.)\s+(.*)$', ln)
        if not s:
            i += 1
            continue
        if m_li:
            ind = len(m_li.group(1).replace('\t', '    '))
            tag = 'ol' if m_li.group(2)[0].isdigit() else 'ul'
            if list_stack and ind < list_stack[-1][0]:
                close_lists(ind)
            if not list_stack or ind > list_stack[-1][0]:
                out.append(f'<{tag}><li>')
                list_stack.append((ind, tag))
            else:
                out.append('</li><li>')
            body = m_li.group(3)
            cb = re.match(r'^\[( |x)\]\s*(.*)$', body)
            if cb:
                mark = '☑' if cb.group(1) == 'x' else '☐'
                out.append(f'<span class="cb">{mark}</span> ' + para(cb.group(2)))
            else:
                out.append(para(body))
            i += 1
            continue
        close_lists()
        if s.startswith('#'):
            lvl = len(s) - len(s.lstrip('#'))
            out.append(f'<h{lvl}>{inline(s[lvl:].strip())}</h{lvl}>')
        elif s.startswith('|'):
            rows = []
            while i < len(lines) and lines[i].strip().startswith('|'):
                rows.append([c.strip() for c in lines[i].strip().strip('|').split('|')])
                i += 1
            head, body = rows[0], [r for r in rows[1:] if not all(re.fullmatch(r':?-+:?', c) for c in r)]
            t = '<div class="tw"><table><thead><tr>' + ''.join(f'<th>{inline(c)}</th>' for c in head) + '</tr></thead><tbody>'
            t += ''.join('<tr>' + ''.join(f'<td>{inline(c)}</td>' for c in r) + '</tr>' for r in body)
            out.append(t + '</tbody></table></div>')
            continue
        elif s.startswith('>'):
            q = []
            while i < len(lines) and lines[i].strip().startswith('>'):
                q.append(lines[i].strip()[1:].strip())
                i += 1
            kind = ''
            if q and re.match(r'\[!(\w+)\]', q[0]):
                kind = re.match(r'\[!(\w+)\]', q[0]).group(1).lower()
                q[0] = re.sub(r'\[!\w+\]\s*', '', q[0])
            out.append(f'<blockquote class="{kind}">' + render_body(q) + '</blockquote>')
            continue
        elif re.fullmatch(r'-{3,}|\*{3,}', s):
            out.append('<hr>')
        else:
            out.append(f'<p>{para(s)}</p>')
        i += 1
    close_lists()
    return '\n'.join(out)


CSS = """
:root{--bg:#faf8f3;--fg:#24211c;--muted:#7a7266;--card:#fff;--line:#e6e0d4;--accent:#6b4f2a;--wl:#2f5d8a;--he:#5b3a7a;--qbg:#f3efe6;--fs:18px}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#1b1a17;--fg:#ebe6dc;--muted:#a59d90;--card:#24221e;--line:#3a3630;--accent:#d9b27c;--wl:#8db8e6;--he:#c9a7ea;--qbg:#2a2722}}
:root[data-theme="dark"]{--bg:#1b1a17;--fg:#ebe6dc;--muted:#a59d90;--card:#24221e;--line:#3a3630;--accent:#d9b27c;--wl:#8db8e6;--he:#c9a7ea;--qbg:#2a2722}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--fg);font-family:"Pretendard","Apple SD Gothic Neo","Malgun Gothic","맑은 고딕",sans-serif;font-size:var(--fs);line-height:1.85;word-break:keep-all;overflow-wrap:anywhere}
main{max-width:760px;margin:0 auto;padding:24px 16px 80px}
.bar{position:sticky;top:0;z-index:5;display:flex;gap:6px;justify-content:flex-end;padding:8px 16px;background:var(--bg);border-bottom:1px solid var(--line)}
.bar button{font:inherit;font-size:14px;padding:4px 10px;border:1px solid var(--line);border-radius:8px;background:var(--card);color:var(--fg);cursor:pointer}
.meta{font-size:.78em;color:var(--muted);background:var(--card);border:1px solid var(--line);border-radius:10px;padding:10px 14px;margin-bottom:18px}
.meta b{color:var(--fg);font-weight:600}
h1{font-size:1.45em;line-height:1.4;color:var(--accent);margin:.4em 0 .8em}
h2{font-size:1.2em;margin:1.8em 0 .6em;padding-bottom:.3em;border-bottom:2px solid var(--line)}
h3{font-size:1.05em;margin:1.4em 0 .4em}
p{margin:.2em 0 1em}
ul,ol{padding-left:1.3em;margin:.3em 0 1em}
li{margin:.55em 0}
li>ul,li>ol{margin:.3em 0}
strong{color:var(--accent)}
.wl{color:var(--wl);border-bottom:1px dotted var(--wl)}
.he{font-family:"SBL Hebrew","Ezra SIL","Times New Roman",serif;color:var(--he);font-size:1.08em;unicode-bidi:isolate}
code{font-size:.85em;background:var(--qbg);padding:1px 5px;border-radius:4px}
blockquote{margin:1em 0;padding:10px 16px;background:var(--qbg);border-left:4px solid var(--accent);border-radius:6px}
blockquote p{margin:.3em 0}
.tw{overflow-x:auto}
table{border-collapse:collapse;width:100%;font-size:.9em}
th,td{border:1px solid var(--line);padding:6px 8px;text-align:left;vertical-align:top}
th{background:var(--qbg)}
.cb{color:var(--accent)}
hr{border:0;border-top:1px solid var(--line);margin:2em 0}
"""

JS = """
const r=document.documentElement;let fs=18;
try{fs=+localStorage.getItem('note-fs')||18;r.style.setProperty('--fs',fs+'px');const t=localStorage.getItem('note-theme');if(t)r.dataset.theme=t}catch(e){}
function setFs(d){fs=Math.min(30,Math.max(13,fs+d));r.style.setProperty('--fs',fs+'px');try{localStorage.setItem('note-fs',fs)}catch(e){}}
function toggleTheme(){const dark=r.dataset.theme?r.dataset.theme==='dark':matchMedia('(prefers-color-scheme: dark)').matches;r.dataset.theme=dark?'light':'dark';try{localStorage.setItem('note-theme',r.dataset.theme)}catch(e){}}
"""

META_KEYS = [('date', '날짜'), ('related_passages', '관련 본문'), ('theological_themes', '주제'),
             ('linked_sermons', '연결 설교'), ('status', '상태')]


def convert(md_path):
    p = Path(md_path)
    lines = p.read_text(encoding='utf-8').split('\n')
    meta, body = parse_frontmatter(lines)
    title = meta.get('title') or p.stem
    meta_html = ''.join(
        f'<div><b>{label}</b> · {inline(re.sub(r"^\[|\]$", "", meta[k]).replace(chr(34), ""))}</div>'
        for k, label in META_KEYS if meta.get(k))
    doc = f"""<!doctype html>
<html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)}</title><style>{CSS}</style></head>
<body><div class="bar"><button onclick="setFs(-1)">가−</button><button onclick="setFs(1)">가+</button><button onclick="toggleTheme()">◐</button></div>
<main>{'<div class="meta">' + meta_html + '</div>' if meta_html else ''}
{render_body(body)}
</main><script>{JS}</script></body></html>"""
    out = p.with_suffix('.html')
    out.write_text(doc, encoding='utf-8')
    return out


def targets(args):
    """파일은 그대로, 폴더는 하위 .md 전부 (9_Archive 콜드 아카이브 제외)."""
    for a in args:
        p = Path(a)
        if p.is_dir():
            yield from (f for f in sorted(p.rglob('*.md')) if '9_Archive' not in f.parts)
        else:
            yield p


if __name__ == '__main__':
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    stale_only = '--stale' in sys.argv  # md가 html보다 새로울 때만 다시 만든다
    if not args:
        print(__doc__)
        sys.exit(1)
    for f in targets(args):
        h = f.with_suffix('.html')
        if stale_only and h.exists() and h.stat().st_mtime >= f.stat().st_mtime:
            continue
        print('saved', convert(f))
