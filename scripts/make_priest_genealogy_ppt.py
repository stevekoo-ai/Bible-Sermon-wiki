# -*- coding: utf-8 -*-
"""아론에서 예수님까지 — 대제사장·제사장 계보 조직도 (성경 본문만으로).

1장: 계보 조직도 (레위→아론 → 엘르아살 계열 ①② · 포로 이후 · 이다말/엘리 계열 · 계보 위치 미상 대제사장 · 신약 · 예수님)
2장: 읽는 법과 주의할 점 (Fact / Opinion)

박스 색: 금색 채움 = 본문이 '대제사장'·'우두머리 제사장'이라 부름 / 금색 테두리 = 직분은 맡았으나 칭호는 '제사장' /
회색 = 계보에만 등장 / 점선 = 본문이 직접 잇지 않고 추론으로 연결.
사용: python scripts/make_priest_genealogy_ppt.py <출력.pptx>
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
BG, WHITE, GREY, DIM = RGB("141414"), RGB("FFFFFF"), RGB("9A9A9A"), RGB("555555")
GOLD = RGB("E0C04F")
HEAD = {"el": RGB("5CC98A"), "post": RGB("4FA3E0"), "ith": RGB("C78BE8"), "unk": RGB("B0B0B0"), "nt": RGB("FF8C8C")}

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


def box(x, y, w, h, fill=None, line=None, dash=False, shape=MSO_SHAPE.ROUNDED_RECTANGLE, lw=0.75):
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


def text(x, y, w, h, runs, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP, wrap=True):
    """runs: [(문자열, 크기, 색, 굵게)] — 각 항목이 한 문단."""
    tb = s.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.margin_left = tf.margin_right = Inches(0.05); tf.margin_top = tf.margin_bottom = 0
    tf.word_wrap = wrap; tf.vertical_anchor = anchor
    for i, (t, size, color, bold) in enumerate(runs):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        r = p.add_run(); r.text = t
        _font(r, size, color, bold)
    return tb


def line(x0, y0, x1, y1, color=GREY, w=0.75, dash=False):
    ln = s.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(x0), Inches(y0), Inches(x1), Inches(y1))
    ln.line.color.rgb = color; ln.line.width = Pt(w)
    if dash:
        ln.line.dash_style = MSO_LINE.DASH
    return ln


STYLE = {  # fill, line, dash, name color, sub color
    "hp": (GOLD, None, False, RGB("141414"), RGB("3D3300")),
    "office": (RGB("2A2A2A"), GOLD, False, WHITE, RGB("B0B0B0")),
    "line": (RGB("262626"), None, False, RGB("D8D8D8"), RGB("8A8A8A")),
    "dead": (RGB("1C1C1C"), DIM, True, RGB("808080"), RGB("6A6A6A")),
    "est": (RGB("262626"), RGB("8A8A8A"), True, RGB("D8D8D8"), RGB("8A8A8A")),
}


def node(x, y, w, h, name, sub="", kind="line", size=8.5):
    fill, ln, dash, nc, sc = STYLE[kind]
    box(x, y, w, h, fill=fill, line=ln, dash=dash, lw=1.25 if kind == "office" else 0.75)
    runs = [(name, size, nc, True)]
    if sub:
        runs.append((sub, 6, sc, False))
    text(x, y + 0.02, w, h - 0.04, runs, anchor=MSO_ANCHOR.MIDDLE)
    return (x, y, w, h)


def down(a, b, dash=False, color=GREY):
    """a 박스 아래 가운데 → b 박스 위 가운데."""
    ax, ay, aw, ah = a; bx, by, bw, bh = b
    line(ax + aw / 2, ay + ah, bx + bw / 2, by, color, 0.75, dash)


def elbow(a, b, dash=False, color=GREY, mid=None):
    """a 아래 → (아래로 조금) → 옆으로 → b 위 (열을 건너가는 연결)."""
    ax, ay, aw, ah = a; bx, by, bw, bh = b
    x0, y0 = ax + aw / 2, ay + ah
    x1, y1 = bx + bw / 2, by
    ym = mid if mid is not None else y0 + 0.06
    line(x0, y0, x0, ym, color, 0.75, dash)
    line(x0, ym, x1, ym, color, 0.75, dash)
    line(x1, ym, x1, y1, color, 0.75, dash)


# ════════════════ 1장: 조직도 ════════════════
new_slide()
box(0.25, 0.1, 6.9, 0.42, fill=RGB("6B5410"))
text(0.35, 0.1, 6.8, 0.42, [("아론에서 예수님까지 — 대제사장·제사장 계보 (성경 본문만으로)", 15, WHITE, True)], anchor=MSO_ANCHOR.MIDDLE, wrap=False)
legend = [("hp", "본문이 '대제사장'·'우두머리 제사장'이라 부름"), ("office", "직분은 맡았으나 칭호는 '제사장'"),
          ("line", "계보에만 등장"), ("est", "점선 = 본문이 직접 잇지 않음(추론)")]
lx, ly = 7.4, 0.1
for i, (k, t) in enumerate(legend):
    fill, ln, dash, _, _ = STYLE[k]
    xx = lx + (i % 2) * 2.95
    yy = ly + (i // 2) * 0.22
    box(xx, yy + 0.03, 0.22, 0.13, fill=fill, line=ln, dash=dash, lw=1.0)
    text(xx + 0.25, yy, 2.7, 0.2, [(t, 7, GREY, False)], wrap=False)

# 레위 → 고핫 → 아므람 → 아론
TY, TH = 0.62, 0.4
lev = node(0.3, TY, 0.85, TH, "레위", "", "line")
koh = node(1.35, TY, 0.85, TH, "고핫", "", "line")
amr = node(2.4, TY, 0.85, TH, "아므람", "", "line")
aar = node(3.45, TY, 1.75, TH, "아론", "첫 대제사장 · 출 28–29; 레 8", "office", 10)
mos = node(5.45, TY, 1.15, TH, "모세", "아론의 동생 · 출 6:20", "dead")
for a, b in ((lev, koh), (koh, amr), (amr, aar)):
    line(a[0] + a[2], TY + TH / 2, b[0], TY + TH / 2, GREY, 0.75)
line(aar[0] + aar[2], TY + TH / 2, mos[0], TY + TH / 2, DIM, 0.75, True)
text(0.3, TY + TH + 0.01, 3.0, 0.15, [("출 6:16-23", 6, GREY, False)], wrap=False)

# 열 좌표
CW = 1.98
COLX = [0.3 + i * 2.15 for i in range(6)]
ROW0, PITCH, BH = 1.98, 0.447, 0.38


def R(i):
    return ROW0 + i * PITCH


# 아론의 네 아들
SY, SHH = 1.22, 0.42
ele = node(COLX[0], SY, CW, SHH, "엘르아살", "아론의 옷을 입음 · 민 20:28", "office")
nad = node(COLX[1], SY, CW, SHH, "나답 · 아비후", "다른 불 → 죽음, 아들 없음 · 레 10:1-2; 민 3:4", "dead")
ith = node(COLX[3], SY, CW, SHH, "이다말", "성막 일 감독 · 출 38:21", "line")
bus = 1.13
line(aar[0] + aar[2] / 2, TY + TH, aar[0] + aar[2] / 2, bus)
line(COLX[0] + CW / 2, bus, COLX[3] + CW / 2, bus)
for b in (ele, nad, ith):
    line(b[0] + b[2] / 2, bus, b[0] + b[2] / 2, b[1])

# 열 머리
heads = [("엘르아살 계열 ① 광야 ~ 다윗 · 대상 6:4-8", HEAD["el"]), ("엘르아살 계열 ② 성전 ~ 포로 · 대상 6:9-15", HEAD["el"]),
         ("포로 이후 · 느 12:10-11", HEAD["post"]), ("이다말 계열 — 엘리 가문", HEAD["ith"]),
         ("계보 위치 미상 (열왕기·역대기)", HEAD["unk"]), ("신약", HEAD["nt"])]

# C1 엘르아살 ①
C1 = [("비느하스", "영원한 제사장 언약 · 민 25:13; 삿 20:28", "office"), ("아비수아", "", "line"), ("북기", "", "line"),
      ("웃시", "", "line"), ("스라히야", "", "line"), ("므라욧", "", "line"), ("아마랴", "", "line"),
      ("아히둡", "삼하 8:17", "line"), ("사독", "다윗·솔로몬, 아비아달을 대신함 · 왕상 2:35", "office")]
c1 = [node(COLX[0], R(i), CW, BH, n, sb, k) for i, (n, sb, k) in enumerate(C1)]
down(ele, c1[0])
for a, b in zip(c1, c1[1:]):
    down(a, b)

# C2 엘르아살 ②
C2 = [("아히마아스", "사독의 아들 · 삼하 15:27", "line"), ("아사랴", "왕상 4:2 '사독의 아들'(후손)", "line"), ("요하난", "", "line"),
      ("아사랴", "솔로몬 성전에서 섬김 · 대상 6:10", "office"), ("아마랴", "", "line"), ("아히둡", "", "line"), ("사독", "", "line"),
      ("살룸", "= 므술람 · 대상 9:11", "line"), ("힐기야", "요시야 · 율법책 발견 · 왕하 22:4, 8", "hp"), ("아사랴", "", "line"),
      ("스라야", "립나에서 처형 · 왕하 25:18-21", "hp"), ("여호사닥", "바벨론 포로 · 대상 6:15", "line")]
c2 = [node(COLX[1], R(i), CW, BH, n, sb, k) for i, (n, sb, k) in enumerate(C2)]
for a, b in zip(c2, c2[1:]):
    down(a, b)
# 사독(C1 끝) → 아히마아스(C2 처음)
z = c1[-1]; a0 = c2[0]
line(z[0] + z[2], z[1] + z[3] / 2, z[0] + z[2] + 0.085, z[1] + z[3] / 2)
line(z[0] + z[2] + 0.085, z[1] + z[3] / 2, z[0] + z[2] + 0.085, a0[1] - 0.06)
line(z[0] + z[2] + 0.085, a0[1] - 0.06, a0[0] + a0[2] / 2, a0[1] - 0.06)
line(a0[0] + a0[2] / 2, a0[1] - 0.06, a0[0] + a0[2] / 2, a0[1])

# C3 포로 이후
C3 = [("예수아(여호수아)", "귀환·성전 재건 · 스 3:2; 학 1:1", "hp"), ("요야김", "느 12:10, 26", "line"),
      ("엘리아십", "성벽 재건 · 느 3:1; 13:4", "hp"), ("요야다", "아들이 산발랏의 사위 · 느 13:28", "line"),
      ("요나단(요하난)", "느 12:11, 22", "line"), ("얏두아", "구약에 이름이 나오는 마지막 대제사장 · 느 12:22", "line")]
c3 = [node(COLX[2], R(i), CW, BH, n, sb, k) for i, (n, sb, k) in enumerate(C3)]
for a, b in zip(c3, c3[1:]):
    down(a, b)
y_ = c2[-1]; j0 = c3[0]
line(y_[0] + y_[2], y_[1] + y_[3] / 2, y_[0] + y_[2] + 0.085, y_[1] + y_[3] / 2)
line(y_[0] + y_[2] + 0.085, y_[1] + y_[3] / 2, y_[0] + y_[2] + 0.085, j0[1] - 0.06)
line(y_[0] + y_[2] + 0.085, j0[1] - 0.06, j0[0] + j0[2] / 2, j0[1] - 0.06)
line(j0[0] + j0[2] / 2, j0[1] - 0.06, j0[0] + j0[2] / 2, j0[1])
ezr = node(COLX[2], R(8), CW, BH * 2 + 0.07, "에스라", "제사장 겸 학자 · 스 7:1-12\n대제사장 혈통, 그러나 대제사장은 아님\n스라야의 어느 줄인지 본문 침묵", "est", 9)
# 스라야 → 에스라 (점선)
sr = c2[10]
line(sr[0] + sr[2], sr[1] + sr[3] / 2, ezr[0], ezr[1] + 0.2, RGB("FF4D4D"), 1.0, True)

# C4 이다말 / 엘리
C4 = [("엘리", "실로의 제사장 · 삼상 1:9; 4:18", "office"), ("홉니 · 비느하스", "전사 · 삼상 2:12; 4:11", "line"),
      ("아히둡", "이가봇의 형 · 삼상 14:3", "line"), ("아히멜렉 (아히야?)", "놉의 제사장 학살 · 삼상 21:1; 22:9-19", "office"),
      ("아비아달", "다윗과 함께 · 솔로몬이 쫓아냄 · 왕상 2:26-27", "office"), ("아히멜렉 · 요나단", "아비아달의 아들들 · 삼하 8:17; 15:27", "line")]
c4 = [node(COLX[3], R(i), CW, BH, n, sb, k) for i, (n, sb, k) in enumerate(C4)]
down(ith, c4[0], dash=True, color=RGB("8A8A8A"))
for a, b in zip(c4, c4[1:]):
    down(a, b)
n1 = node(COLX[3], R(6) + 0.04, CW, BH * 2 + 0.03, "엘리 집 예언의 성취",
          "삼상 2:31-35 → 왕상 2:27\n이후 대제사장은 사독 계열로만", "est", 7.5)
n2 = node(COLX[3], R(8) + 0.04, CW, BH * 2 + 0.03, "다윗의 24반열 · 대상 24:1-19",
          "엘르아살 16 + 이다말 8 반열\n여덟째 제비 = 아비야 반열", "est", 7.5)

# C5 계보 위치 미상
C5 = [("아마랴", "여호사밧 · 대하 19:11", "hp"), ("여호야다", "요아스를 세움 · 왕하 11; 12:10", "hp"),
      ("스가랴", "여호야다의 아들 · 성전 뜰 순교 · 대하 24:20-22", "office"), ("아사랴", "웃시야의 분향을 막음 · 대하 26:17-20", "hp"),
      ("우리야", "아하스의 다메섹식 제단 · 왕하 16:10-16", "office"), ("아사랴", "사독의 족속 · 히스기야 · 대하 31:10", "hp"),
      ("스바냐", "둘째 제사장 · 왕하 25:18; 렘 29:25", "office")]
c5 = [node(COLX[4], R(i), CW, BH, n, sb, k) for i, (n, sb, k) in enumerate(C5)]
node(COLX[4], R(7) + 0.03, CW, BH + 0.05, "대상 6장 계보에 없는 이름들", "→ 계보는 대제사장 '명단'이 아니다", "est", 7.5)
mel = node(COLX[4], R(9) + 0.03, CW, BH * 2 + 0.05, "멜기세덱", "살렘 왕, 지극히 높은 하나님의 제사장\n창 14:18; 시 110:4 · 족보 없음(히 7:3)", "office", 9)

# C6 신약
gap = node(COLX[5], R(0), CW, BH * 2 + 0.05, "성경 침묵 · 약 400년", "얏두아 ~ 신약 · 마카비·하스몬 시대\n대제사장은 정경 밖이라 제외", "dead", 8)
zac = node(COLX[5], R(2), CW, BH, "사가랴", "아비야 반열 · 아내는 아론의 자손 · 눅 1:5", "office")
joh = node(COLX[5], R(3), CW, BH, "세례 요한", "제사장의 아들 · 눅 1:13", "line")
ann = node(COLX[5], R(4), CW, BH, "안나스", "눅 3:2; 요 18:13; 행 4:6", "hp")
cai = node(COLX[5], R(5), CW, BH, "가야바", "안나스의 사위 · 요 11:49; 18:13", "hp")
ana = node(COLX[5], R(6), CW, BH, "아나니아", "바울을 재판 · 행 23:2; 24:1", "hp")
down(zac, joh); down(ann, cai)
line(n2[0] + n2[2], n2[1] + n2[3] / 2, COLX[5] - 0.08, n2[1] + n2[3] / 2, RGB("8A8A8A"), 0.75, True)
line(COLX[5] - 0.08, n2[1] + n2[3] / 2, COLX[5] - 0.08, zac[1] + zac[3] / 2, RGB("8A8A8A"), 0.75, True)
line(COLX[5] - 0.08, zac[1] + zac[3] / 2, COLX[5], zac[1] + zac[3] / 2, RGB("8A8A8A"), 0.75, True)

# 예수님
jx, jy, jw, jh = COLX[5], R(7) + 0.05, CW, SH - (R(7) + 0.05) - 0.12
box(jx, jy, jw, jh, fill=RGB("3A2E0A"), line=GOLD, lw=2.25)
text(jx, jy + 0.06, jw, jh - 0.1, [
    ("예수님", 18, RGB("FFD966"), True),
    ("영원한 큰 대제사장 · 히 4:14", 8.5, WHITE, True),
    ("", 4, WHITE, False),
    ("유다 지파 — 레위 혈통이 아님 · 히 7:14", 7.5, RGB("E8D9A8"), False),
    ("멜기세덱의 반차를 따라 · 히 5:6; 7:17", 7.5, RGB("E8D9A8"), False),
    ("혈통의 법이 아니라", 7.5, RGB("E8D9A8"), False),
    ("'불멸의 생명의 능력'으로 · 히 7:16", 7.5, RGB("E8D9A8"), False),
    ("단번에 자기를 드림 · 히 7:27", 7.5, RGB("E8D9A8"), False),
], anchor=MSO_ANCHOR.TOP)
line(mel[0] + mel[2], mel[1] + mel[3] / 2, jx, mel[1] + mel[3] / 2, GOLD, 1.5, True)

# 열 머리 (연결선보다 위에)
for x, (h, c) in zip(COLX, heads):
    box(x, 1.74, min(len(h) * 0.072 + 0.15, CW + 0.12), 0.19, fill=BG, shape=MSO_SHAPE.RECTANGLE)
    text(x, 1.73, CW + 0.1, 0.2, [(h, 6.8, c, True)], wrap=False)

# ════════════════ 2장: 읽는 법과 주의할 점 ════════════════
new_slide()
box(0.25, 0.1, 6.9, 0.42, fill=RGB("6B5410"))
text(0.35, 0.1, 6.8, 0.42, [("계보를 읽는 법과 주의할 점", 15, WHITE, True)], anchor=MSO_ANCHOR.MIDDLE, wrap=False)
text(7.4, 0.16, 5.7, 0.35, [("Fact = 본문에서 바로 확인 · Opinion = 해석이나 학설이 갈리는 부분", 7.5, GREY, False)], wrap=False)
NOTES = [
    ("Fact", "대상 6:3-15는 '대제사장 명단'이 아니라 제사장 가문 계보다",
     "여호야다·우리야·히스기야 때 아사랴처럼 열왕기·역대기가 대제사장이라 부른 이름들이 이 계보에는 없다. 그래서 1장에서 따로 모았다."),
    ("Fact", "계보에는 생략이 있다",
     "스 7:1-5는 대상 6장보다 약 6명이 짧다. 왕상 4:2는 아사랴를 '사독의 아들'이라 하지만 대상 6:8-9에서는 손자다. 성경의 '아들'은 후손도 뜻한다."),
    ("Opinion", "엘리가 이다말 계열이라는 것은 추론이다",
     "엘리 → 비느하스 → 아히둡 → 아히멜렉 → 아비아달은 본문이 잇는다(삼상 14:3; 22:20). 그 아비아달의 아들 아히멜렉이 '이다말의 자손'이라는 대상 24:3에서 거꾸로 추론한 것이라 점선으로 그렸다."),
    ("Opinion", "아히야(삼상 14:3)와 아히멜렉(삼상 21–22)은 같은 사람일 수 있다",
     "둘 다 아히둡의 아들로 나온다. 같은 사람의 다른 이름으로 보는 견해가 많지만 본문이 단정하지 않는다."),
    ("Fact", "왕들이 대제사장을 바꾸기도 했다",
     "솔로몬이 아비아달을 쫓아내고 사독을 세웠다(왕상 2:27, 35). 엘리 집에 대한 예언(삼상 2:31-35)이 그렇게 이루어졌고, 그 뒤로는 사독 계열이 이어졌다(겔 44:15)."),
    ("Fact", "구약과 신약 사이 약 400년은 성경이 침묵한다",
     "얏두아(느 12:22) 이후 신약의 안나스까지 이어지는 대제사장들은 개신교 정경에 나오지 않아 넣지 않았다. 신약의 대제사장들은 계보가 적혀 있지 않다."),
    ("Fact", "예수님은 레위가 아니라 유다 지파다",
     "히 7:13-14. 그래서 히브리서는 예수님의 대제사장직을 아론의 혈통이 아니라 '족보도 없는' 멜기세덱의 반차에서 찾는다(히 7:3, 16)."),
]
for i, (tag, head, body) in enumerate(NOTES):
    y = 0.72 + i * 0.95
    box(0.25, y, SW - 0.5, 0.85, fill=RGB("1F1F1F"))
    tc = RGB("5CC98A") if tag == "Fact" else RGB("E0A04F")
    box(0.4, y + 0.3, 0.8, 0.26, fill=tc)
    text(0.4, y + 0.3, 0.8, 0.26, [(tag, 9, RGB("141414"), True)], align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, wrap=False)
    text(1.35, y + 0.08, SW - 1.8, 0.75, [(head, 11, WHITE, True), (body, 9, RGB("C8C8C8"), False)], anchor=MSO_ANCHOR.MIDDLE)

prs.save(OUT)
print("saved", OUT)
