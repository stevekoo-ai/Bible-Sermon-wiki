# -*- coding: utf-8 -*-
"""포로에서 귀환까지 — 나라와 왕들의 연대표 (BC 610–420), 3장.

1장: 제국·바벨론 왕·페르시아 왕·포로들이 사는 땅·사건·인물·70년 레인 연표
2장: 왜 '바벨론에서' 올라왔나? (스 7:6) — 나라 이름과 땅 이름
3장: 왜 왕 세 명이 함께 나오나? (스 6:14) — 미니 연표 + 이름 대조표

연대: 바벨론 연대기·페르시아 왕명록 기준 관례 연대.
사용: python scripts/make_exile_kings_timeline_ppt.py <출력.pptx>
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
INK = RGB("141414")
BAB, PER, JUD, RET, RED, PRO = RGB("E8955F"), RGB("E0C04F"), RGB("4FA3E0"), RGB("5CC98A"), RGB("FF4D4D"), RGB("C78BE8")

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
        sp.adjustments[0] = 0.12
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


def text(x, y, w, h, runs, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP, wrap=True, margin=0.04, bg=None):
    if isinstance(runs, str):
        runs = [(runs, 8, WHITE, False)]
    tb = s.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    if bg is not None:
        tb.fill.solid(); tb.fill.fore_color.rgb = bg
    tf = tb.text_frame
    tf.margin_left = tf.margin_right = Inches(margin); tf.margin_top = tf.margin_bottom = 0
    tf.word_wrap = wrap; tf.vertical_anchor = anchor
    for i, (t, size, color, bold) in enumerate(runs):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        p._p.get_or_add_pPr().set("eaLnBrk", "0")  # 한글은 단어 단위로 줄바꿈
        r = p.add_run(); r.text = t
        _font(r, size, color, bold)
    return tb


def line(x0, y0, x1, y1, color=GREY, w=0.75, dash=False):
    ln = s.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(x0), Inches(y0), Inches(x1), Inches(y1))
    ln.line.color.rgb = color; ln.line.width = Pt(w)
    if dash:
        ln.line.dash_style = MSO_LINE.DASH
    return ln


def title(t, sub=""):
    box(0.25, 0.1, 7.4, 0.42, fill=RGB("1E5C3A"), shape=MSO_SHAPE.ROUNDED_RECTANGLE)
    text(0.35, 0.1, 7.3, 0.42, [(t, 15, WHITE, True)], anchor=MSO_ANCHOR.MIDDLE, wrap=False)
    if sub:
        text(7.85, 0.12, 5.3, 0.4, [(sub, 7.5, GREY, False)])


# ════════════════ 1장: 나라와 왕들의 연대표 ════════════════
new_slide()
title("포로에서 귀환까지 — 나라와 왕들의 연대표", "BC 610–420 · 연대는 바벨론 연대기·페르시아 왕명록 기준 관례 연대\n괄호 안 이름 = 현대인의성경·역사 교과서 표기 · 점선 = 추정/논쟁")
Y0, Y1 = 610, 420
X0, X1 = 1.55, SW - 0.25


def X(bc):
    bc = min(max(bc, Y1), Y0)
    return X0 + (Y0 - bc) / (Y0 - Y1) * (X1 - X0)


AX = 0.98
line(X0, AX, X1, AX, GREY, 0.75)
for y in range(610, 419, -10):
    x = X(y)
    line(x, AX, x, 6.6, RGB("2C2C2C"), 0.4, True)
    text(x - 0.3, AX - 0.17, 0.6, 0.14, [(f"BC {y}" if y in (610, 420) else str(y), 6.5, GREY, False)], align=PP_ALIGN.CENTER, wrap=False, margin=0)

LANES = [("제국", 1.08, 0.32), ("바벨론 왕", 1.46, 0.72), ("페르시아 왕", 2.24, 0.72), ("포로들이\n사는 땅", 3.02, 0.6),
         ("사건", 3.68, 1.35), ("인물", 5.09, 0.9), ("70년", 6.05, 0.55)]
for nm, y, h in LANES:
    box(0.2, y, SW - 0.4, h, fill=RGB("1B1B1B"))
    text(0.28, y, 1.2, h, [(nm, 8.5, GREY, True)], anchor=MSO_ANCHOR.MIDDLE)

# 제국 띠
box(X(626), 1.12, X(539) - X(626), 0.24, fill=BAB)
text(X(610), 1.12, X(539) - X(610), 0.24, [("신바벨론 제국 (626–539)", 8, INK, True)], anchor=MSO_ANCHOR.MIDDLE, wrap=False)
box(X(539), 1.12, X1 - X(539), 0.24, fill=PER)
text(X(539), 1.12, X1 - X(539), 0.24, [("페르시아 제국 (바사, 539–330) — 바벨론은 제국의 한 지방·왕궁 도시로 남음", 8, INK, True)], anchor=MSO_ANCHOR.MIDDLE, wrap=False)

# 바벨론 왕
BK = [("나보폴라살", 626, 605), ("느부갓네살 2세 (네부카드네자르) 605–562", 605, 562), ("", 562, 560), ("", 560, 556), ("", 556, 555.6),
      ("나보니두스 556–539", 556, 539)]
for lab, a, b in BK:
    box(X(a), 1.52, max(X(b) - X(a), 0.03), 0.24, fill=BAB, line=BG, lw=0.5)
    if lab and X(b) - X(a) > 0.9:
        text(X(a), 1.52, X(b) - X(a), 0.24, [(lab, 7, INK, True)], anchor=MSO_ANCHOR.MIDDLE, wrap=False)
text(X(610), 1.79, 1.2, 0.14, [("나보폴라살 (~605)", 6, BAB, False)], wrap=False, margin=0)
box(X(553), 1.8, X(539) - X(553), 0.1, fill=BAB, line=None)
text(X(539) + 0.05, 1.77, 2.2, 0.14, [("◀ 벨사살 공동 통치 ~553–539 (단 5)", 6, BAB, False)], wrap=False, margin=0)
text(X(556) - 3.0, 1.93, 3.0, 0.3, [("에윌므로닥 562–560 · 여호야긴 석방 (왕하 25:27)", 6, BAB, False),
                                    ("네리글리살 560–556 · 라바시마르둑 556", 6, BAB, False)], align=PP_ALIGN.RIGHT, wrap=False, margin=0)
line(X(561), 1.76, X(561), 1.95, BAB, 0.5)

# 페르시아 왕
PK = [("고레스", "키루스 2세", 539, 530), ("캄비세스", "", 530, 522), ("다리오 1세", "다리우스", 522, 486),
      ("아하수에로", "크세르크세스", 486, 465), ("아닥사스다 1세", "아르타크세르크세스", 465, 424)]
for nm, gk, a, b in PK:
    box(X(a), 2.3, X(b) - X(a), 0.26, fill=PER, line=BG, lw=0.5)
    w_ = X(b) - X(a)
    lab = (f"{nm} ({gk}) {a}–{b}" if gk else f"{nm} {a}–{b}") if w_ > 2.0 else (f"{nm} {a}–{b}" if w_ > 1.0 else nm)
    text(X(a), 2.3, X(b) - X(a), 0.26, [(lab, 7 if X(b) - X(a) > 0.6 else 6, INK, True)], anchor=MSO_ANCHOR.MIDDLE, wrap=False, margin=0.02)
text(X(539), 2.6, 1.6, 0.14, [("고레스 (키루스) 539–530", 6, PER, False)], wrap=False, margin=0)
text(X(530) + 0.05, 2.74, 1.6, 0.14, [("캄비세스 530–522 (성경에 안 나옴)", 6, PER, False)], wrap=False, margin=0)
box(X(539) - 0.02, 2.82, 0.12, 0.1, line=PER, dash=True)
text(X(539) - 1.45, 2.78, 1.4, 0.14, [("메대 사람 다리오 (단 5:31) · 정체 논쟁", 6, PER, False)], align=PP_ALIGN.RIGHT, wrap=False, margin=0)

# 포로들이 사는 땅
box(X(597), 3.1, X(539) - X(597), 0.2, fill=RGB("5A3A24"))
box(X(539), 3.1, X1 - X(539), 0.2, fill=RGB("5A4E1E"))
text(X(597), 3.1, X1 - X(597), 0.2, [("바벨론 땅 — 그발 강 델아빕(겔 3:15) · 아하와 강(스 8:15) · 나라 주인은 바벨론 → 페르시아로 바뀌어도 땅 이름은 '바벨론'", 7, WHITE, True)], anchor=MSO_ANCHOR.MIDDLE, wrap=False)
box(X(572), 3.36, X(477) - X(572), 0.08, fill=RGB("A0A0A0"))
text(X(572), 3.45, 4.5, 0.14, [("'유다 마을'(알야후두) 토판 572–477 — 바벨론 시대부터 아하수에로 시대까지 한 마을 기록 (10/18 설교)", 6, GREY, False)], wrap=False, margin=0)

# 사건
EV = [(605, "1차 포로 · 다니엘 (단 1:1)", JUD, 0), (597, "2차 포로 · 여호야긴·에스겔 (왕하 24:12-16)", JUD, 1),
      (586, "★ 성전이 불탐 (왕하 25:8-9)", RED, 2), (561, "여호야긴 석방 (왕하 25:27)", JUD, 0),
      (539, "바벨론 함락 (단 5:30)", PER, 1), (538, "고레스 조서 · 1차 귀환 (스 1)", RET, 2),
      (536, "성전 기초 (스 3)", RET, 3), (520, "공사 재개 · 학개·스가랴 (스 5:1)", RET, 0),
      (515, "★ 성전 완공 · 다리오 6년 (스 6:15)", RET, 1), (479, "에스더 왕후 (에 2:16)", PRO, 0),
      (458, "★ 에스라 · 2차 귀환 (스 7)", RED, 1), (445, "느헤미야 · 3차 귀환, 성벽 (느 2)", RET, 2)]
EY = 3.78
line(X0, EY, X1, EY, RGB("444444"), 0.75)
for bc, lab, col, lv in EV:
    x = X(bc)
    line(x, EY + 0.05, x, EY + 0.12 + lv * 0.27 + 0.07, col, 0.5)
for bc, lab, col, lv in EV:
    x = X(bc)
    box(x - 0.055, EY - 0.055, 0.11, 0.11, fill=col, shape=MSO_SHAPE.DIAMOND)
    ly = EY + 0.12 + lv * 0.27
    tw = len(lab) * 0.072 + 0.15
    if x + tw > X1:
        text(x - tw, ly, tw, 0.18, [(lab, 7, col, lab.startswith("★"))], align=PP_ALIGN.RIGHT, wrap=False, margin=0.02, bg=RGB("1B1B1B"))
    else:
        text(x, ly, tw, 0.18, [(lab, 7, col, lab.startswith("★"))], wrap=False, margin=0.02, bg=RGB("1B1B1B"))
# 제국 교체선
line(X(539), 1.08, X(539), 6.6, PER, 1.25, True)

# 인물
PP = [("다니엘 (단 1:21; 10:1)", 605, 536, 0, PRO, False), ("에스겔 (겔 1:2; 29:17)", 593, 571, 1, PRO, False),
      ("예레미야 → 애굽", 627, 582, 2, PRO, False), ("스룹바벨·예수아", 538, 515, 0, RET, False),
      ("학개·스가랴", 520, 518, 1, PRO, False), ("에스더·모르드개 (수산 궁)", 483, 473, 0, PRO, True),
      ("말라기 (추정)", 460, 430, 2, PRO, True), ("에스라 (바벨론에서)", 458, 445, 0, RED, False),
      ("느헤미야 (수산 궁에서)", 445, 433, 1, RET, False)]
for lab, a, b, row, col, est in PP:
    y = 5.15 + row * 0.28
    box(X(a), y, max(X(b) - X(a), 0.05), 0.08, fill=None if est else col, line=col if est else None, dash=est)
    text(X(a), y + 0.08, 2.4, 0.15, [(lab, 6.5, col, False)], wrap=False, margin=0)

# 70년
box(X(605), 6.12, X(536) - X(605), 0.12, line=JUD, dash=True)
text(X(605), 6.24, 5.0, 0.14, [("70년 ① 바벨론을 섬긴 기간 605→536 (렘 25:11; 단 9:2)", 6.5, JUD, False)], wrap=False, margin=0)
box(X(586), 6.38, X(515) - X(586), 0.12, line=RED, dash=True)
text(X(515) + 0.05, 6.36, 5.0, 0.14, [("70년 ② 성전이 황폐했던 기간 586→515 (슥 1:12; 7:5) · [견해] 계산 방식 두 가지", 6.5, RED, False)], wrap=False, margin=0)

text(0.25, 6.75, SW - 0.5, 0.6, [
    ("한 줄 정리: 유다는 바벨론에 망했고, 바벨론은 539년 페르시아에 망했다. 포로들은 그 뒤에도 '바벨론 땅'에 살았고, 페르시아 왕들의 허락으로 세 번에 나눠 돌아왔다 — 538(스룹바벨) · 458(에스라) · 445(느헤미야).", 8.5, WHITE, True)])

# ════════════════ 2장: 왜 '바벨론에서'? ════════════════
new_slide()
title("왜 '바벨론에서' 올라왔다고 할까? (스 7:6)", "\"이 에스라가 바벨론에서 올라왔으니\"(7:6) · \"바사 왕 아닥사스다가 왕위에 있을 때\"(7:1)\n→ 바벨론 = 출발한 땅, 바사(페르시아) = 그때 다스린 나라")
# 왼쪽 그림: 제국 안의 지방
big = box(0.35, 0.8, 5.6, 6.2, fill=RGB("2A2410"), line=PER, lw=1.5, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
big.adjustments[0] = 0.03
text(0.5, 0.88, 5.3, 0.3, [("페르시아 제국 (바사) — 나라", 12, PER, True)])
text(0.5, 1.2, 5.3, 0.25, [("왕궁 도시: 수산(수사) · 바벨론 · 악메다(에그바다나) · 페르세폴리스", 8, RGB("D8C88A"), False)])
box(0.7, 1.65, 2.7, 2.6, fill=RGB("3A2618"), line=BAB, lw=1.25, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
text(0.8, 1.72, 2.5, 0.3, [("바벨론 — 지방·도시 이름", 10, BAB, True)])
text(0.8, 2.05, 2.5, 2.1, [("539년 고레스가 성을 차지했지만 도시는 그대로 남음", 8, WHITE, False),
                            ("", 4, WHITE, False),
                            ("포로들의 마을", 8, WHITE, True), ("그발 강 델아빕 (겔 3:15)", 8, WHITE, False), ("아하와 강 (스 8:15)", 8, WHITE, False), ("'유다 마을' 토판 (572–477)", 8, WHITE, False),
                            ("", 4, WHITE, False),
                            ("★ 에스라가 출발한 곳 (스 7:6, 9)", 8.5, RED, True)])
box(3.65, 1.65, 2.1, 1.2, fill=RGB("33301A"), line=PER, lw=1.0, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
text(3.72, 1.72, 2.0, 1.1, [("수산 궁 (수사)", 10, PER, True), ("에스더가 왕후로 산 곳 (에 1:2)", 7.5, WHITE, False),
                             ("느헤미야가 일하던 곳 (느 1:1)", 7.5, WHITE, False)])
box(3.65, 3.05, 2.1, 1.2, fill=RGB("1E2A33"), line=JUD, lw=1.0, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
text(3.72, 3.12, 2.0, 1.1, [("예후드 (유다 지방)", 10, JUD, True), ("페르시아의 작은 지방", 7.5, WHITE, False),
                             ("총독(페하)이 다스림 (학 1:1; 말 1:8)", 7.5, WHITE, False)])
line(3.4, 3.6, 3.65, 3.6, RED, 2.0)
text(0.7, 4.45, 5.1, 0.3, [("에스라의 길: 바벨론 → 아하와 강 → 예루살렘 · 넉 달 · 약 1,500km", 9, RED, True)])
text(0.7, 4.85, 5.1, 2.0, [("아이들에게", 9, GREY, True),
                            ("\"바벨론이라는 나라는 망했어.", 9.5, WHITE, False), ("그런데 바벨론이라는 동네는 그대로 있었어.", 9.5, WHITE, False),
                            ("주인만 페르시아로 바뀐 거야.", 9.5, WHITE, False), ("그래서 에스라는 페르시아 왕의 허락을 받고,", 9.5, WHITE, False),
                            ("바벨론 동네에서 출발한 거지!\"", 9.5, WHITE, False)])

CARDS2 = [
    ("Fact", "539년, 바벨론은 무너지지 않고 '주인'만 바뀌었다",
     "고레스는 바벨론 성을 큰 전투 없이 차지했다(단 5:30-31; 고레스 원통 ★★★). 도시와 이름은 그대로 남았고 페르시아의 지방이자 왕궁 도시가 되었다."),
    ("Fact", "포로들은 그 뒤에도 바벨론 땅에 마을을 이루고 살았다",
     "그발 강 델아빕(겔 3:15), 아하와 강(스 8:15). '유다 마을' 토판은 572년부터 477년까지, 바벨론 왕 시대에서 페르시아 아하수에로 시대까지 한 마을을 기록한다."),
    ("Fact", "성경은 '나라'와 '땅'을 구별해서 쓴다",
     "\"바사 왕 아닥사스다가 왕위에 있을 때에\"(7:1)는 나라, \"바벨론에서 올라왔으니\"(7:6)는 땅. 고레스도 \"바벨론 왕 고레스\"라 불린다(스 5:13)."),
    ("Fact", "모두가 바벨론에 있었던 것은 아니다",
     "에스더와 느헤미야는 페르시아의 왕궁 도시 수산에 있었다(에 1:2; 느 1:1). 그래서 느헤미야는 '수산 궁에서', 에스라는 '바벨론에서' 올라온다."),
]
for i, (tag, head, body) in enumerate(CARDS2):
    y = 0.8 + i * 1.55
    box(6.2, y, SW - 6.45, 1.42, fill=CARD, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
    box(6.35, y + 0.15, 0.7, 0.24, fill=RET, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
    text(6.35, y + 0.15, 0.7, 0.24, [(tag, 8.5, INK, True)], align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, wrap=False)
    text(7.15, y + 0.1, SW - 7.55, 1.25, [(head, 11, WHITE, True), (body, 9, RGB("C8C8C8"), False)])

# ════════════════ 3장: 왜 왕 세 명? ════════════════
new_slide()
title("왜 성전 완공에 왕 세 명이 나올까? (스 6:14)", "\"…바사 왕 고레스와 다리오와 아닥사스다의 조서를 따라 성전을 건축하며 일을 끝내되\"(6:14)\n\"다리오 왕 제육년 아달월 삼일에 성전 일을 끝내니라\"(6:15)")
M0, M1 = 545, 450
MX0, MX1 = 1.3, SW - 0.5


def MX(bc):
    return MX0 + (M0 - bc) / (M0 - M1) * (MX1 - MX0)


line(MX0, 1.05, MX1, 1.05, GREY, 0.75)
for y in range(545, 449, -5):
    x = MX(y)
    line(x, 1.05, x, 3.95, RGB("2C2C2C"), 0.4, True)
    if y % 10 == 5 or y in (545, 450):
        text(x - 0.3, 0.88, 0.6, 0.14, [(str(y), 6.5, GREY, False)], align=PP_ALIGN.CENTER, wrap=False, margin=0)
for nm, gk, a, b in PK:
    if b > M1 or a < M0:
        aa, bb = min(a, M0), max(b, M1)
        box(MX(aa), 1.15, MX(bb) - MX(aa), 0.32, fill=PER, line=BG, lw=0.5)
        text(MX(aa), 1.15, MX(bb) - MX(aa), 0.32, [(nm, 8, INK, True)], anchor=MSO_ANCHOR.MIDDLE, wrap=False, margin=0.03)
DEC = [(538, "① 고레스 조서", "성전을 지어라, 비용은 왕실이 (스 1:2-4; 6:3-5)", RET, 0),
       (519, "② 다리오 조서", "고레스 조서 확인, 방해 금지, 비용 지원 (스 6:6-12)", RET, 1),
       (515, "★ 성전 완공", "다리오 6년 아달월 3일 (스 6:15)", RED, 2),
       (458, "③ 아닥사스다 조서", "성전 기구·제사 비용·일꾼 세금 면제 (스 7:19-24, 27)", RET, 0)]
for bc, h, b, col, lv in DEC:
    line(MX(bc), 1.66, MX(bc), 1.8 + lv * 0.62, col, 0.75)
for bc, h, b, col, lv in DEC:
    x = MX(bc)
    box(x - 0.07, 1.6 - 0.07, 0.14, 0.14, fill=col, shape=MSO_SHAPE.DIAMOND)
    y = 1.8 + lv * 0.62
    w = 3.6
    xx = x if x + w < SW - 0.3 else x - w
    text(xx, y, w, 0.5, [(h, 10, col, True), (b, 8, WHITE, False)], align=PP_ALIGN.LEFT if xx == x else PP_ALIGN.RIGHT, bg=BG)
# 515 → 465 간격
gy = 3.65
line(MX(515), gy, MX(465), gy, RED, 1.5)
box(MX(465) - 0.05, gy - 0.05, 0.1, 0.1, fill=RED, shape=MSO_SHAPE.OVAL)
box(MX(515) - 0.05, gy - 0.05, 0.1, 0.1, fill=RED, shape=MSO_SHAPE.OVAL)
text(MX(515), gy - 0.25, MX(465) - MX(515), 0.2, [("성전 완공 → 아닥사스다 즉위: 50년 뒤", 8.5, RED, True)], align=PP_ALIGN.CENTER, wrap=False)

CARDS3 = [
    ("Fact", "성전은 다리오 때 이미 끝났다 — 아닥사스다는 50년 뒤의 왕이다",
     "6:15가 완공일을 다리오 6년(515)으로 못 박는다. 아닥사스다는 465년에 왕이 되었으니 건물 공사에는 참여할 수 없었다."),
    ("Fact", "아닥사스다가 한 일은 '건물'이 아니라 성전의 '섬김'을 채운 것이다",
     "성전 기구(7:19), 제사 비용(7:17, 20-22), 성전 일꾼 세금 면제(7:24).\n그래서 에스라는 \"성전을 아름답게 하려 하는 뜻을 왕의 마음에 두신\" 하나님을 찬송한다(7:27)."),
    ("Opinion", "6:14는 '세 왕이 함께 지었다'가 아니라 '하나님의 집을 도운 페르시아 왕들'을 한 줄로 모은 요약이다",
     "다수 학자의 견해. 4:6-23도 훗날 왕들의 방해를 성전 이야기 안에 모아 놓았다.\n6:14는 7장의 아닥사스다·에스라 이야기로 넘어가는 다리이기도 하다."),
    ("핵심", "그래서 6:14의 첫머리가 중요하다 — \"이스라엘 하나님의 명령과\"",
     "왕이 셋이어도 명령은 하나다. 세 왕은 서로 다른 시대에 조서를 냈지만, 모두 한 분 하나님의 명령을 따라 움직였다.\n에스라가 말한 하나님의 손(7:6, 9, 28)이 바로 이것이다."),
]
for i, (tag, head, body) in enumerate(CARDS3):
    y = 4.08 + i * 0.83
    box(0.25, y, 8.6, 0.76, fill=CARD, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
    tc = {"Fact": RET, "Opinion": RGB("E0A04F"), "핵심": RED}[tag]
    box(0.38, y + 0.25, 0.72, 0.24, fill=tc, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
    text(0.38, y + 0.25, 0.72, 0.24, [(tag, 8, INK, True)], align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, wrap=False)
    text(1.2, y + 0.04, 7.55, 0.7, [(head, 9, WHITE, True)] + [(b, 7.5, RGB("C8C8C8"), False) for b in body.split("\n")], anchor=MSO_ANCHOR.MIDDLE)

# 이름 대조표
TX, TY = 9.05, 4.08
box(TX, TY, SW - TX - 0.25, 3.27, fill=CARD, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
text(TX + 0.12, TY + 0.06, 3.8, 0.25, [("왕 이름 대조표", 10, PER, True)], wrap=False)
NAMES = [("개역개정", "현대인의성경·역사", "재위(BC)"),
         ("느부갓네살", "네부카드네자르 2세", "605–562"),
         ("에윌므로닥", "아멜마르둑", "562–560"),
         ("벨사살", "벨샤르우수르", "~553–539"),
         ("고레스", "키루스 2세", "539–530"),
         ("(성경에 없음)", "캄비세스 2세", "530–522"),
         ("다리오", "다리우스 1세", "522–486"),
         ("아하수에로", "크세르크세스 1세", "486–465"),
         ("아닥사스다", "아르타크세르크세스 1세", "465–424")]
for i, (a, b, c) in enumerate(NAMES):
    y = TY + 0.38 + i * 0.315
    col = GREY if i == 0 else WHITE
    bold = i == 0
    text(TX + 0.12, y, 1.1, 0.26, [(a, 8, PER if i else GREY, True)], wrap=False)
    text(TX + 1.22, y, 1.85, 0.26, [(b, 8, col, bold)], wrap=False)
    text(TX + 3.1, y, 1.0, 0.26, [(c, 8, col, bold)], wrap=False)
    if i == 0:
        line(TX + 0.12, y + 0.26, SW - 0.4, y + 0.26, DIM, 0.5)

prs.save(OUT)
print("saved", OUT)
