# -*- coding: utf-8 -*-
"""유다 멸망 사건 연대표(왕하 24–25 · 렘 39–43 · 52) — 1장짜리 계단식 마일스톤 PPT.
시간축은 구간별 축척(BC 586년 7–12월 확대). 사용: python scripts/make_judah_fall_timeline_ppt.py <출력.pptx>"""
import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.dml import MSO_LINE

OUT = sys.argv[1]
FONT = "맑은 고딕"


def d(y, m=1, dd=1):
    """BC y년 m월 dd일 → 연속 시간값 (BC는 음수, 연 안에서는 증가)."""
    return -y + (m - 1) / 12 + (dd - 1) / 365


C = {"text": RGBColor(0xFF, 0x4D, 0x4D), "bab": RGBColor(0xE8, 0x95, 0x5F), "king": RGBColor(0x4F, 0xA3, 0xE0),
     "jer": RGBColor(0xC7, 0x8B, 0xE8), "rem": RGBColor(0x5C, 0xC9, 0x8A)}
# (번호, 분류, 시작, 끝, 추정, 제목, 정보)
ROWS = [
    (1, "bab", d(605, 5, 15), d(605, 6, 30), False, "갈그미스 전투", "605.5~6 · 느부갓네살이 애굽 격파 (왕하 24:7)"),
    (2, "bab", d(605, 9, 7), d(605, 9, 20), False, "느부갓네살 즉위", "605.9.7 · 바벨론 왕 (바벨론 연대기)"),
    (3, "king", d(604, 12, 1), d(601, 11, 1), False, "여호야김 항복·조공", "604~601 · 3년 조공 (왕하 24:1)"),
    (4, "king", d(601, 11, 1), d(601, 12, 31), False, "여호야김의 배반", "601.11~12 · 바벨론–애굽 충돌 후 (24:1)"),
    (5, "bab", d(599, 1, 1), d(598, 12, 1), True, "약탈대의 침공", "599~598 · 바벨론·아람·모압·암몬 (24:2-4)"),
    (6, "king", d(598, 12, 9), d(597, 3, 16), False, "여호야김 사망 → 여호야긴", "598.12.9경 · 18세 즉위, 3개월 (24:6-9)"),
    (7, "king", d(597, 3, 16), d(597, 3, 22), False, "여호야긴 항복", "597.3.16 · 날짜가 바벨론 연대기에 기록 (24:12)"),
    (8, "bab", d(597, 4, 22), d(597, 5, 20), False, "1차 대규모 포로", "597.4.22경 · 여호야긴·1만 명·에스겔 (24:13-16)"),
    (9, "king", d(597, 4, 22), d(586, 7, 18), False, "시드기야 통치", "597~586 · 21세 즉위, 11년 (24:17-19)"),
    (10, "king", d(589, 6, 1), d(589, 9, 1), True, "시드기야의 배반", "589경 · 애굽을 의지 (24:20)"),
    (11, "text", d(588, 1, 15), d(586, 7, 18), False, "예루살렘 포위", "588.1.15 → 586.7.18 · 18개월, 토성 (25:1)"),
    (12, "jer", d(587, 6, 1), d(586, 7, 10), True, "에벳멜렉 구원 약속", "포위 중 · '네가 나를 신뢰하였음이라' (렘 39:15-18)"),
    (13, "text", d(586, 7, 18), d(586, 7, 20), False, "성벽이 뚫림", "586.7.18 · 기근 끝에 (25:2-4)"),
    (14, "text", d(586, 7, 18), d(586, 7, 21), False, "야간 도주", "586.7.18 밤 · 두 성벽 사이 문 (25:4)"),
    (15, "text", d(586, 7, 21), d(586, 7, 28), True, "여리고 평지 생포", "7월 하순 · 군대는 흩어짐 (25:5)"),
    (16, "text", d(586, 7, 28), d(586, 8, 8), True, "립나의 심판", "두 눈 뽑힘 → 바벨론 감옥 (25:6-7; 렘 52:11)"),
    (17, "text", d(586, 8, 14), d(586, 8, 17), False, "★ 성전이 불타던 날", "586.8.14 (렘 8.17) · 성전·왕궁·성벽 (25:8-10)"),
    (18, "bab", d(586, 8, 15), d(586, 8, 31), True, "성전 기구 약탈", "8월 · 놋기둥·놋바다·놋소 12 (25:13-17)"),
    (19, "text", d(586, 8, 17), d(586, 9, 12), True, "남은 백성 포로", "8월 · 라마 집결 → 바벨론, 832명 (25:11-12)"),
    (20, "jer", d(586, 8, 15), d(586, 8, 21), True, "예레미야 감옥에서 풀림", "8월 · 에벳멜렉도 구원 (렘 39:11-14)"),
    (21, "jer", d(586, 8, 25), d(586, 9, 2), True, "라마에서 사슬이 풀림", "8월 · 라마 → 미스바 (렘 40:1-6)"),
    (22, "text", d(586, 8, 20), d(586, 9, 5), True, "지도자들 처형", "립나 · '본토에서 떠났더라' (25:18-21)"),
    (23, "rem", d(586, 9, 1), d(586, 10, 3), False, "그달랴 총독", "586 · 미스바 (25:22)"),
    (24, "rem", d(586, 9, 5), d(586, 9, 25), True, "지휘관들과 그달랴의 맹세", "바벨론 왕을 섬기라 (25:23-24)"),
    (25, "rem", d(586, 9, 1), d(586, 10, 1), True, "흩어진 자들의 귀환·수확", "모압·암몬·에돔에서 (렘 40:11-12)"),
    (26, "rem", d(586, 9, 20), d(586, 9, 30), True, "요하난의 경고", "바알리스의 음모 (렘 40:13-16)"),
    (27, "rem", d(586, 10, 3), d(586, 10, 5), False, "그달랴 암살", "586.10경 식사 중 · 582년설 (25:25)"),
    (28, "rem", d(586, 10, 5), d(586, 10, 7), False, "순례자 80명 학살", "다음 날 · 세겜·실로·사마리아 (렘 41:4-9)"),
    (29, "rem", d(586, 10, 7), d(586, 10, 10), True, "이스마엘의 납치", "암몬으로 (렘 41:10)"),
    (30, "rem", d(586, 10, 10), d(586, 10, 13), True, "기브온 큰 못 구출", "이스마엘은 도주 (렘 41:11-15)"),
    (31, "rem", d(586, 10, 13), d(586, 11, 2), True, "게룻김함에 머묾", "베들레헴 근처 (렘 41:16-18)"),
    (32, "jer", d(586, 10, 20), d(586, 10, 22), True, "기도 요청·순종 맹세", "(렘 42:1-6)"),
    (33, "jer", d(586, 10, 22), d(586, 11, 1), True, "10일 후의 응답", "이 땅에 머물라 (렘 42:7-22)"),
    (34, "rem", d(586, 11, 2), d(586, 12, 1), True, "말씀 거부, 애굽행", "586 말(582설) · 다바네스 (렘 43:1-7)"),
    (35, "jer", d(586, 12, 1), d(586, 12, 20), True, "다바네스의 돌 예언", "(렘 43:8-13)"),
    (36, "bab", d(582, 1, 1), d(581, 3, 1), False, "3차 포로", "582/581 · 745명, 합계 4,600 (렘 52:28-30)"),
    (37, "bab", d(568, 1, 1), d(567, 12, 1), False, "느부갓네살의 애굽 원정", "568/567 · 예언 성취 (BM 33041)"),
    (38, "king", d(561, 3, 25), d(561, 4, 10), False, "여호야긴 석방", "561.3말~4초 · 왕의 식탁 (25:27-30)"),
]
PHASES = [  # (시작 번호, 끝 번호, 이름, 부제, 배경색)
    (1, 9, "1막", "바벨론의 등장과 1차 포로 · 605–597", RGBColor(0x2A, 0x22, 0x18)),
    (10, 16, "2막", "시드기야와 18개월 포위 · 589–586.7", RGBColor(0x2C, 0x18, 0x18)),
    (17, 22, "3막", "성전이 불타던 날 · 586.8", RGBColor(0x36, 0x16, 0x16)),
    (23, 35, "4막", "그달랴와 남은 자들 · 586 가을–말", RGBColor(0x17, 0x26, 0x1D)),
    (36, 38, "5막", "그 후 · 582–561", RGBColor(0x18, 0x20, 0x2C)),
]
LANES = [  # (이름, 색, [(라벨, 시작, 끝)])
    ("유다 왕·총독", C["king"], [("여호야김 → 여호야긴(3개월)", d(609), d(598, 12, 9)), ("", d(598, 12, 9), d(597, 3, 16)),
                                 ("시드기야", d(597, 4, 22), d(586, 7, 18)), ("그달랴", d(586, 9, 1), d(586, 10, 3)),
                                 ("여호야긴 포로 37년", d(597, 4, 22), d(561, 3, 25))]),
    ("바벨론 왕", C["bab"], [("느부갓네살 (43년)", d(605, 9, 7), d(562, 10, 1)), ("에윌므로닥", d(562, 10, 1), d(560, 8, 1))]),
    ("선지자", C["jer"], [("예레미야 (627~)", d(627), d(582)), ("에스겔 (593–571)", d(593, 7, 1), d(571)),
                          ("다니엘 (605–536)", d(605, 8, 1), d(536))]),
]
MILESTONES = [(d(605, 6, 1), "갈그미스"), (d(597, 3, 16), "1차 함락"), (d(588, 1, 15), "포위"),
              (d(586, 7, 18), "성벽"), (d(586, 8, 14), "성전 불탐"), (d(586, 10, 3), "그달랴 암살"),
              (d(582), "3차 포로"), (d(561, 3, 25), "석방")]
HIGHLIGHT = d(586, 8, 14)

BG, WHITE, GREY, DIM = RGBColor(0x14, 0x14, 0x14), RGBColor(0xFF, 0xFF, 0xFF), RGBColor(0x9A, 0x9A, 0x9A), RGBColor(0x55, 0x55, 0x55)
RED = RGBColor(0xFF, 0x4D, 0x4D)

SW, SH = 13.333, 7.5
X0, X1 = 1.45, SW - 0.2
# 구간별 축척: (시간 시작, 시간 끝, 화면 폭 비율)
SEGS = [(d(606), d(590), 0.22, "1년 간격"), (d(590), d(586, 7, 1), 0.17, "포위 기간"),
        (d(586, 7, 1), d(586, 12, 31), 0.45, "BC 586년 7–12월 (확대)"), (d(586, 12, 31), d(559), 0.16, "585–561")]
TOP, ROW_BOTTOM = 1.30, 6.02
PITCH = (ROW_BOTTOM - TOP) / len(ROWS)
BAR_H, TXT_H = 0.036, 0.085


def xpos(t):
    x = X0
    W = X1 - X0
    for a, b, frac, _ in SEGS:
        w = W * frac
        if t <= b:
            return x + max(0.0, (t - a) / (b - a)) * w
        x += w
    return X1


prs = Presentation()
prs.slide_width, prs.slide_height = Inches(SW), Inches(SH)
s = prs.slides.add_slide(prs.slide_layouts[6])
s.background.fill.solid(); s.background.fill.fore_color.rgb = BG


def box(x, y, w, h, fill=None, line=None, dash=False, shape=MSO_SHAPE.RECTANGLE, lw=0.75):
    sp = s.shapes.add_shape(shape, Inches(x), Inches(y), Inches(w), Inches(h))
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


def text(x, y, w, h, t, size, color=WHITE, bold=False, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP):
    tb = s.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    tf.word_wrap = False; tf.vertical_anchor = anchor
    p = tf.paragraphs[0]; p.alignment = align
    r = p.add_run(); r.text = t
    r.font.size = Pt(size); r.font.bold = bold; r.font.name = FONT; r.font.color.rgb = color
    rPr = r._r.get_or_add_rPr()
    for tag in ("ea", "cs"):
        rPr.append(rPr.makeelement("{http://schemas.openxmlformats.org/drawingml/2006/main}" + tag, {"typeface": FONT}))
    return tb


def vline(x, y0, y1, color, w=0.5, dash=True):
    ln = s.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(x), Inches(y0), Inches(x), Inches(y1))
    ln.line.color.rgb = color; ln.line.width = Pt(w)
    if dash:
        ln.line.dash_style = MSO_LINE.DASH
    return ln


# ---- 제목 ----
box(0.25, 0.12, 6.4, 0.42, fill=RGBColor(0x8B, 0x1E, 0x1E), shape=MSO_SHAPE.ROUNDED_RECTANGLE)
text(0.4, 0.12, 6.2, 0.42, "유다 멸망 사건 연대표 — 열왕기하 24–25 · 예레미야 39–43, 52", 15, bold=True, anchor=MSO_ANCHOR.MIDDLE)
text(6.85, 0.13, 6.3, 0.18, "네모: 왼쪽 변 = 시작, 오른쪽 변 = 끝 · 점선 = 날짜 추정 · 날짜는 율리우스력 근사(Thiele/Parker-Dubberstein, 함락 586년설)", 7.5, GREY)
leg = [("★ 10/18 본문", C["text"]), ("바벨론", C["bab"]), ("유다 왕실", C["king"]), ("예레미야·에벳멜렉", C["jer"]), ("그달랴와 남은 자들", C["rem"])]
lx = 6.85
for name, col in leg:
    box(lx, 0.37, 0.12, 0.1, fill=col)
    text(lx + 0.16, 0.34, 1.6, 0.16, name, 7.5, GREY)
    lx += 0.28 + len(name) * 0.085

# ---- 막(phase) 배경 ----
for a, b, nm, sub, bg in PHASES:
    y0 = TOP + (a - 1) * PITCH - 0.02
    y1 = TOP + b * PITCH
    box(0.2, y0, SW - 0.35, y1 - y0, fill=bg)
    text(0.3, y0 + 0.03, 1.1, 0.2, nm, 11, WHITE, bold=True)
    text(0.3, y0 + 0.24, 1.15, 0.5, sub.split(" · ")[0], 6.5, GREY)
    text(0.3, y0 + 0.36, 1.15, 0.2, sub.split(" · ")[1], 6.5, GREY)

# ---- 하단 레인 배경 ----
LANE_TOP = ROW_BOTTOM + 0.08
LANE_HS = [0.34, 0.26, 0.46]
LANE_Y = []
yy = LANE_TOP
for (nm, col, _), h in zip(LANES, LANE_HS):
    box(0.2, yy, SW - 0.35, h, fill=RGBColor(0x22, 0x1E, 0x28))
    box(0.2, yy, 0.06, h, fill=col)
    text(0.32, yy + h / 2 - 0.08, 1.1, 0.16, nm, 8, col, bold=True)
    LANE_Y.append(yy); yy += h + 0.01

# ---- 시간축 · 구간 표시 ----
AX_Y = 1.05
BOTTOM = yy
ax = s.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(X0), Inches(AX_Y), Inches(X1), Inches(AX_Y))
ax.line.color.rgb = GREY; ax.line.width = Pt(0.75)
for a, b, _, nm in SEGS:
    xa, xb = xpos(a), xpos(b)
    vline(xa, AX_Y - 0.08, BOTTOM, RGBColor(0x60, 0x60, 0x60), 1.0, dash=False)
    text(xa + 0.04, AX_Y + 0.11, xb - xa - 0.08, 0.12, nm, 6, RGBColor(0xB0, 0xB0, 0xB0), align=PP_ALIGN.CENTER)
ticks = [(d(y), f"BC {y}") for y in (605, 600, 595)] + [(d(y), str(y)) for y in (590, 588, 587)] + \
        [(d(586, m), f"586.{m}") for m in (7, 8, 9, 10, 11, 12)] + [(d(y), str(y)) for y in (585, 580, 575, 570, 565, 561)]
for t, lab in ticks:
    x = xpos(t)
    vline(x, AX_Y, ROW_BOTTOM, RGBColor(0x30, 0x30, 0x30), 0.4)
    text(x - 0.3, AX_Y + 0.0, 0.6, 0.11, lab, 5.5, GREY, align=PP_ALIGN.CENTER)
for i, (t, lab) in enumerate(MILESTONES):
    x = xpos(t)
    col = RED if t == HIGHLIGHT else WHITE
    box(x - 0.045, AX_Y - 0.045, 0.09, 0.09, fill=col, shape=MSO_SHAPE.DIAMOND)
    vline(x, AX_Y, BOTTOM, RED if t == HIGHLIGHT else DIM, 1.25 if t == HIGHLIGHT else 0.4)
    text(x - 0.45, AX_Y - (0.3, 0.19)[i % 2], 0.9, 0.11, lab, 6.5, col, bold=(t == HIGHLIGHT), align=PP_ALIGN.CENTER)

# ---- 사건 행 (계단) ----
CHAR_W = 0.05
for i, (n, cat, a, b, est, title, info) in enumerate(ROWS):
    y = TOP + i * PITCH
    xa, xb = xpos(a), xpos(b)
    w = max(xb - xa, 0.045)
    if est:
        box(xa, y, w, BAR_H, line=C[cat], dash=True)
    else:
        box(xa, y, w, BAR_H, fill=C[cat])
    label = f"{n}. {title}  ·  {info}"
    tw = len(label) * CHAR_W + 0.1
    ty = y + BAR_H + 0.004
    col = C["text"] if cat == "text" else WHITE
    if xa + tw <= SW - 0.2:
        text(xa, ty, tw, TXT_H, label, 5.5, col, bold=(cat == "text"))
    else:
        right = min(xa + w, SW - 0.2)
        text(right - tw, ty, tw, TXT_H, label, 5.5, col, bold=(cat == "text"), align=PP_ALIGN.RIGHT)

# ---- 하단 레인 막대 ----
for (nm, col, items), y in zip(LANES, LANE_Y):
    for k, (lab, a, b) in enumerate(items):
        if nm == "선지자":
            sub = k
        elif nm == "유다 왕·총독":
            sub = 1 if lab.startswith("여호야긴 포로") else 0
        else:
            sub = 0
        lane_y = y + 0.05 + sub * 0.145
        xa, xb = max(xpos(a), X0), xpos(b)
        box(xa, lane_y, max(xb - xa, 0.04), 0.035, fill=col)
        if not lab:
            continue
        tw = len(lab) * 0.05 + 0.1
        if xa + tw > SW - 0.2:
            text(SW - 0.2 - tw, lane_y + 0.04, tw, 0.09, lab, 5.5, col, align=PP_ALIGN.RIGHT)
        else:
            text(xa + 0.02, lane_y + 0.04, tw, 0.09, lab, 5.5, col)

# ---- 10/18 강조 ----
x = xpos(HIGHLIGHT)
text(x - 4.3, TOP + 2.2, 4.2, 0.14, "10/18 설교 본문 (왕하 25:1-12, 21) — 성전이 불타던 날 ▶", 7, RED, bold=True, align=PP_ALIGN.RIGHT)
text(x - 4.3, TOP + 2.38, 4.2, 0.14, "빨간 글씨 = 본문 사건 (11, 13–17, 19, 22)", 6, RED, align=PP_ALIGN.RIGHT)

prs.save(OUT)
print("saved", OUT, "rows", len(ROWS), "pitch", round(PITCH, 3))
