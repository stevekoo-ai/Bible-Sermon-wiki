# -*- coding: utf-8 -*-
"""말라기와 에스라·느헤미야 — 시대 겹침 연대표 (BC 520–410), 2장.

1장: 시간축 + 왕 / 성전 / 에스라 / 느헤미야 / 말라기(학자 견해 3갈래 + 안전한 띠 470–430)
2장: 말라기가 지적한 문제 ↔ 에스라·느헤미야 본문 대응표

근거: 4_Reference_Research/에스라느헤미야_한권의이야기_관계와구조.md
사용: python scripts/make_malachi_overlap_ppt.py <출력.pptx>
"""
import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.dml import MSO_LINE

OUT = sys.argv[1]
FONT = "맑은 고딕"
RGB = RGBColor.from_string
BG, WHITE, GREY, DIM, CARD = RGB("141414"), RGB("FFFFFF"), RGB("9A9A9A"), RGB("555555"), RGB("1F1F1F")
PER, JUD, RET, RED, PRO, GOLD = RGB("E0C04F"), RGB("4FA3E0"), RGB("5CC98A"), RGB("FF4D4D"), RGB("C78BE8"), RGB("F2C14E")

SW, SH = 13.333, 7.5
prs = Presentation()
prs.slide_width, prs.slide_height = Inches(SW), Inches(SH)
s = None


def new_slide():
    global s
    s = prs.slides.add_slide(prs.slide_layouts[6])
    s.background.fill.solid(); s.background.fill.fore_color.rgb = BG


def _font(r, size, color, bold):
    r.font.size = Pt(size); r.font.bold = bold; r.font.name = FONT; r.font.color.rgb = color
    rPr = r._r.get_or_add_rPr()
    for tag in ("ea", "cs"):
        rPr.append(rPr.makeelement("{http://schemas.openxmlformats.org/drawingml/2006/main}" + tag, {"typeface": FONT}))


def box(x, y, w, h, fill=None, line=None, dash=False, shape=MSO_SHAPE.RECTANGLE, lw=0.75):
    sp = s.shapes.add_shape(shape, Inches(x), Inches(y), Inches(w), Inches(h))
    if shape == MSO_SHAPE.ROUNDED_RECTANGLE:
        sp.adjustments[0] = 0.2
    if fill is None:
        sp.fill.background()
    else:
        sp.fill.solid(); sp.fill.fore_color.rgb = fill
    if line is None:
        sp.line.fill.background()
    else:
        sp.line.color.rgb = line; sp.line.width = Pt(lw)
        if dash:
            sp.line.dash_style = MSO_LINE.DASH
    sp.shadow.inherit = False
    return sp


def text(x, y, w, h, runs, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP, wrap=True, bg=None):
    if isinstance(runs, str):
        runs = [(runs, 10, WHITE, False)]
    tb = s.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    if bg is not None:
        tb.fill.solid(); tb.fill.fore_color.rgb = bg
    tf = tb.text_frame
    tf.margin_left = tf.margin_right = Inches(0.04); tf.margin_top = tf.margin_bottom = 0
    tf.word_wrap = wrap; tf.vertical_anchor = anchor
    for i, (t, size, color, bold) in enumerate(runs):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        p._p.get_or_add_pPr().set("eaLnBrk", "0")
        r = p.add_run(); r.text = t
        _font(r, size, color, bold)
    return tb


def vline(x, y1, y2, color, dash=False, w=1.0):
    ln = s.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(x), Inches(y1), Inches(x), Inches(y2))
    ln.line.color.rgb = color; ln.line.width = Pt(w)
    if dash:
        ln.line.dash_style = MSO_LINE.DASH
    return ln


# ---------- 1장: 겹침 연대표 ----------
new_slide()
text(0.5, 0.3, 12.3, 0.6, [("말라기는 언제? — 에스라·느헤미야와 겹치는 시대", 26, WHITE, True)])
text(0.5, 0.88, 12.3, 0.4, [("성전 완공(515) 뒤, 총독이 있던 페르시아 시대 · 정확한 해는 학자마다 다르다 → 점이 아니라 띠로 본다", 13, GREY, False)])

X0, X1 = 2.3, 12.9          # 축 좌표
Y0, Y1 = 520, 410           # BC 연도 (큰 수 → 작은 수)


def X(year):
    return X0 + (Y0 - year) / (Y0 - Y1) * (X1 - X0)


LAB = 0.4
rows = {"king": 1.55, "temple": 2.35, "ezra": 3.05, "neh": 3.75, "mal": 4.55}
AXIS_Y = 6.6

# 안전한 띠 (470–430) — 맨 먼저 그려 뒤에 깔기
box(X(470), 1.45, X(430) - X(470), AXIS_Y - 1.45, fill=RGB("2A2440"))
LBL_470 = (X(470), 6.2, X(430) - X(470), 0.3)

# 주요 세로선
for yr, col, lab in [(515, RET, "515 성전 완공"), (458, JUD, "458 에스라 도착"), (445, GOLD, "445 느헤미야 도착"), (433, RED, "433 느헤미야 잠시 돌아감")]:
    vline(X(yr), 1.4, AXIS_Y, col, dash=True, w=0.9)

# 행 이름
for key, lab in [("king", "페르시아 왕"), ("temple", "성전"), ("ezra", "에스라"), ("neh", "느헤미야"), ("mal", "말라기\n(학자 견해)")]:
    text(LAB, rows[key], 1.8, 0.6, [(l, 14, WHITE, True) for l in lab.split("\n")])

# 왕
for a, b, name in [(520, 486, "다리오 1세"), (486, 465, "아하수에로"), (465, 424, "아닥사스다 1세"), (424, 410, "다리오 2세")]:
    box(X(a), rows["king"], X(b) - X(a) - 0.03, 0.45, fill=RGB("3A3420"), line=PER)
    text(X(a), rows["king"], X(b) - X(a), 0.45, [(name, 11, PER, True)], align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

# 성전
box(X(515), rows["temple"], X(410) - X(515), 0.4, fill=RGB("1E3326"), line=RET)
text(X(515), rows["temple"], X(410) - X(515), 0.4, [("성전에서 제사가 계속 드려짐 (약 57년 뒤 에스라)", 11, RET, False)], align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

# 에스라
box(X(458), rows["ezra"], X(445) - X(458), 0.45, fill=RGB("1B2E40"), line=JUD)
text(X(458) - 2.6, rows["ezra"], 2.55, 0.45, [("스 7–10 · 율법을 가르침", 11, JUD, True)], align=PP_ALIGN.RIGHT, anchor=MSO_ANCHOR.MIDDLE)
box(X(445), rows["ezra"], X(433) - X(445), 0.45, fill=None, line=JUD, dash=True)
text(X(445), rows["ezra"], X(433) - X(445), 0.45, [("느 8 · 12:36", 10, JUD, False)], align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

# 느헤미야
box(X(445), rows["neh"], X(433) - X(445), 0.45, fill=RGB("3A3016"), line=GOLD)
text(X(445), rows["neh"], X(433) - X(445), 0.45, [("총독 12년", 11, GOLD, True)], align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
box(X(431), rows["neh"], X(420) - X(431), 0.45, fill=None, line=GOLD, dash=True)
text(X(431), rows["neh"], X(420) - X(431), 0.45, [("2차 · 느 13", 10, GOLD, False)], align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

# 말라기 견해 3갈래
mal = [
    (500, 460, "ⓐ 에스라 이전 — Hill(약 500) · Stuart(약 460)", 0.0),
    (458, 445, "ⓑ 사이 — Harrison · Bright(약 450)", 0.5),
    (433, 420, "ⓒ 느헤미야 부재 중 — Verhoef(433 직후)", 1.0),
]
for a, b, lab, dy in mal:
    y = rows["mal"] + dy
    box(X(a), y + 0.05, X(b) - X(a), 0.32, fill=PRO, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
    if a == 500:
        text(X(b) + 0.08, y, 4.0, 0.42, [(lab, 11, WHITE, False)], anchor=MSO_ANCHOR.MIDDLE, bg=BG)
    else:
        text(X(a) - 4.3, y, 4.22, 0.42, [(lab, 11, WHITE, False)], align=PP_ALIGN.RIGHT, anchor=MSO_ANCHOR.MIDDLE, bg=BG)

text(*LBL_470, [("말라기: 약 470–430 (안전한 띠)", 11, PRO, True)], align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, bg=RGB("2A2440"))

# 축
ax =s.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(X0), Inches(AXIS_Y), Inches(X1), Inches(AXIS_Y))
ax.line.color.rgb = GREY; ax.line.width = Pt(1.5)
for yr in range(520, 409, -10):
    vline(X(yr), AXIS_Y - 0.06, AXIS_Y + 0.06, GREY)
    text(X(yr) - 0.4, AXIS_Y + 0.1, 0.8, 0.3, [(f"BC {yr}", 10, GREY, False)], align=PP_ALIGN.CENTER)
text(0.5, 7.0, 12.3, 0.35, [("어느 견해든: 말라기는 에스라·느헤미야의 앞뒤에서 같은 문제(이방 결혼·십일조·제사장·성전을 업신여김)를 다룬 선지자", 12, WHITE, False)])

# ---------- 2장: 대응표 ----------
new_slide()
text(0.5, 0.3, 12.3, 0.6, [("말라기가 지적한 문제 ↔ 에스라·느헤미야", 26, WHITE, True)])
text(0.5, 0.88, 12.3, 0.4, [("가장 많이 겹치는 곳은 느헤미야 13장", 13, GREY, False)])
rowsT = [
    ("이방 신의 딸과 결혼", "말 2:11", "스 9:2 · 10:3 · 느 10:30 · 13:23"),
    ("십일조와 봉헌물을 도둑질", "말 3:8-10", "느 10:37-38 · 13:10, 12"),
    ("하나님의 전을 업신여김", "말 1:7, 10", "느 10:39 · 13:11 \"전이 어찌하여 버린 바 되었느냐\""),
    ("제사장이 레위 언약을 깨뜨림", "말 2:4-8", "느 13:4-5 · 13:29 \"레위 사람에 대한 언약을 어겼사오니\""),
    ("형제를 학대함", "말 2:10 · 3:5", "느 5:5"),
    ("총독이 있음", "말 1:8", "느 5:14 (느헤미야 총독 12년)"),
]
cx = [0.6, 4.6, 6.6]
cw = [3.9, 1.9, 6.1]
y = 1.5
for i, h in enumerate(["말라기가 지적한 문제", "말라기", "에스라 · 느헤미야"]):
    text(cx[i], y, cw[i], 0.45, [(h, 14, PRO if i < 2 else GOLD, True)], anchor=MSO_ANCHOR.MIDDLE)
y += 0.55
for a, b, c in rowsT:
    box(0.5, y, 12.3, 0.68, fill=CARD)
    text(cx[0], y, cw[0], 0.68, [(a, 15, WHITE, True)], anchor=MSO_ANCHOR.MIDDLE)
    text(cx[1], y, cw[1], 0.68, [(b, 14, PRO, False)], anchor=MSO_ANCHOR.MIDDLE)
    text(cx[2], y, cw[2], 0.68, [(c, 13, WHITE, False)], anchor=MSO_ANCHOR.MIDDLE)
    y += 0.78
text(0.5, 6.85, 12.3, 0.4, [("말라기에는 에스라·느헤미야 이름이 나오지 않는다 — 연대는 이 겹침으로 추정한다", 12, GREY, False)])

prs.save(OUT)
print("saved", OUT)
