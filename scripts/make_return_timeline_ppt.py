# -*- coding: utf-8 -*-
"""이스라엘 귀환 마일스톤 연표 (에스라 · 느헤미야 · 학개 · 스가랴 · 에스더 · 말라기 · 다니엘) — BC 539–430.

1장: 계단식 마일스톤 연표 (유다멸망_마일스톤_연표와 같은 시각 언어, 에스라 458년 확대)
2장: 같은 시대의 성경 — 에스라서의 어느 대목을 비추나 (카드 표)

연대: 전통 연대(에스라 458, 느헤미야 445), 월일은 히브리력, 위치는 율리우스력 근사(Parker-Dubberstein).
사용: python scripts/make_return_timeline_ppt.py <출력.pptx>
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


def d(y, m=1, dd=1):
    """BC y년 m월 dd일(율리우스력 근사) → 연속 시간값."""
    return -y + (m - 1) / 12 + (dd - 1) / 365


RGB = RGBColor.from_string
C = {"ezra": RGB("FF4D4D"), "persia": RGB("E0C04F"), "ret": RGB("5CC98A"),
     "proph": RGB("C78BE8"), "neh": RGB("4FA3E0")}

# (분류, 시작, 끝, 추정, 제목, 정보)
ROWS = [
    # 1막
    ("persia", d(539, 10, 12), d(539, 10, 29), False, "고레스의 바벨론 입성", "539.10 · 바벨론 함락 (단 5:30-31, 고레스 원통)"),
    ("proph", d(539, 11, 1), d(538, 3, 1), True, "다니엘의 70년 기도", "다리오 원년 · '그 연수를 깨달았나니' (단 9:1-3)"),
    ("ret", d(538, 3, 24), d(538, 5, 1), True, "고레스 조서", "538 · '올라갈지어다' (스 1:1-4 = 대하 36:22-23)"),
    ("ret", d(538, 5, 1), d(538, 9, 1), True, "1차 귀환", "538 · 세스바살·스룹바벨·예수아, 42,360명 (스 1:11; 2:64)"),
    ("proph", d(538, 9, 1), d(537, 6, 1), True, "시편 126 — 귀환의 노래", "연대 추정 · '꿈꾸는 것 같았도다' (시 126:1)"),
    ("ret", d(537, 9, 15), d(537, 10, 15), True, "제단을 쌓고 초막절", "7월 · 기초 놓기 전 (스 3:1-6)"),
    ("ret", d(536, 4, 15), d(536, 5, 15), True, "성전 기초", "536 · 2월 · 통곡과 함성이 섞임 (스 3:8-13)"),
    ("proph", d(536, 4, 20), d(536, 5, 15), True, "다니엘의 마지막 환상", "고레스 3년 · 힛데겔 강가 (단 10:1-4)"),
    # 2막
    ("ret", d(536, 6, 1), d(520, 9, 21), True, "방해 — 공사 중단", "536~520 · 약 16년 (스 4:1-5, 24)"),
    ("proph", d(520, 8, 29), d(520, 9, 5), False, "학개의 첫 말씀", "520.6.1 · '너희의 행위를 살필지니라' (학 1:1-11)"),
    ("ret", d(520, 9, 21), d(520, 9, 28), False, "공사 재개", "520.6.24 · 스룹바벨·예수아 (학 1:14-15; 스 5:1-2)"),
    ("proph", d(520, 10, 27), d(520, 11, 10), True, "스가랴의 부름", "520.8 · '내게로 돌아오라' (슥 1:1-6)"),
    ("persia", d(520, 11, 1), d(519, 6, 1), True, "닷드내의 조사 → 다리오의 회신", "고레스 조서 발견 (스 5:3–6:12)"),
    ("proph", d(520, 12, 18), d(520, 12, 25), False, "학개의 마지막 말씀", "520.9.24 · '오늘부터는 내가 복을 주리라' (학 2:10-23)"),
    ("proph", d(519, 2, 15), d(519, 2, 25), False, "스가랴의 여덟 환상", "519.11.24 · '오직 나의 영으로' (슥 1:7–6:15; 4:6)"),
    ("proph", d(518, 12, 7), d(518, 12, 15), False, "스가랴 — 금식의 질문", "518.9.4 · 다리오 4년 (슥 7–8)"),
    ("ret", d(515, 3, 12), d(515, 3, 20), False, "성전 완공", "515.3 (516설) · 다리오 6년 아달월 3일 (스 6:15)"),
    ("ret", d(515, 4, 21), d(515, 4, 28), False, "봉헌과 유월절", "1월 14일 · '여호와께서 그들을 즐겁게 하시고' (스 6:16-22)"),
    # 3막
    ("persia", d(486, 12, 1), d(485, 3, 1), False, "아하수에로 즉위 · 고소장", "486 · (스 4:6)"),
    ("proph", d(483, 4, 1), d(483, 10, 1), True, "와스디 폐위", "483 · 왕 3년 잔치 (에 1)"),
    ("proph", d(479, 1, 1), d(478, 2, 1), True, "에스더 왕후", "479 · 왕 7년 10월 (에 2:16-17)"),
    ("proph", d(474, 4, 1), d(473, 3, 15), True, "하만의 음모 → 부림절", "474/473 · '이 때를 위함이 아닌지' (에 3:7; 4:14; 9)"),
    ("persia", d(465, 12, 1), d(464, 6, 1), True, "아닥사스다 즉위 · 고소 편지", "465 이후 · 성벽 공사 방해 (스 4:7-23)"),
    ("proph", d(460), d(430), True, "말라기의 외침 (연대 추정)", "~460–430 · 흠 있는 제물, '내가 너희를 사랑하였노라' (말 1)"),
    # 4막 — 에스라
    ("ezra", d(458, 3, 1), d(458, 4, 8), True, "아닥사스다의 조서", "458 · 왕 7년 · 아람어 원문 (스 7:11-26)"),
    ("ezra", d(458, 4, 8), d(458, 4, 12), False, "★ 1월 1일 바벨론 출발", "마음을 준비하여 — 연구·준행·가르침 (스 7:9-10)"),
    ("ezra", d(458, 4, 8), d(458, 4, 19), False, "아하와 강가 — 레위인 찾기·금식", "군대 대신 기도 (스 8:15-23)"),
    ("ezra", d(458, 4, 19), d(458, 4, 23), False, "1월 12일 강가 출발", "'하나님의 손이 우리를 도우사' (스 8:31)"),
    ("ezra", d(458, 4, 19), d(458, 8, 4), False, "넉 달의 여정", "약 1,500km · 아기·노인·금은과 함께 (스 7:9; 8:26-27)"),
    ("ezra", d(458, 8, 4), d(458, 8, 9), False, "★ 5월 1일 예루살렘 도착", "'선한 손이 그를 도우심' (스 7:9; 8:32-36)"),
    ("ezra", d(458, 8, 15), d(458, 12, 15), True, "이방 결혼 보고 · 에스라의 기도", "옷을 찢음, '우리'의 죄 (스 9)"),
    ("ezra", d(458, 12, 19), d(458, 12, 24), False, "빗속의 총회", "9월 20일 · 어린 아이까지 (스 10:1, 9)"),
    ("ezra", d(458, 12, 29), d(457, 3, 27), False, "조사와 결단", "10월 1일 → 이듬해 1월 1일 (스 10:16-17)"),
    # 5막 — 느헤미야
    ("neh", d(446, 12, 1), d(446, 12, 20), True, "하나니의 소식", "446 기슬르월 · 울고 금식하며 기도 (느 1)"),
    ("neh", d(445, 4, 1), d(445, 4, 15), True, "왕 앞의 묵도", "445 니산월 · '내 하나님의 선한 손이' (느 2:1-8)"),
    ("neh", d(445, 7, 1), d(445, 7, 20), True, "밤의 순찰", "'일어나 건축하자' (느 2:11-18)"),
    ("neh", d(445, 8, 11), d(445, 10, 2), False, "성벽 공사 52일", "엘룰월 25일 완공 · 한 손엔 연장 (느 4:17; 6:15)"),
    ("ezra", d(445, 10, 8), d(445, 10, 12), False, "★ 에스라의 율법 낭독", "7월 1일 · '기뻐하는 것이 너희의 힘' (느 8:1-12)"),
    ("neh", d(445, 10, 22), d(445, 10, 29), False, "초막절", "7월 15–22일 · 여호수아 이후 처음 (느 8:13-18)"),
    ("neh", d(445, 10, 31), d(445, 11, 6), False, "회개 기도 · 언약 서명", "7월 24일 (느 9–10)"),
    ("neh", d(445, 11, 15), d(445, 12, 31), True, "성벽 봉헌", "두 찬양대 · '즐거워하는 소리가 멀리' (느 12:27-43)"),
    ("neh", d(433), d(432, 6, 1), False, "느헤미야 귀국", "433 · 아닥사스다 32년 (느 13:6)"),
    ("neh", d(432), d(430), True, "다시 무너진 것들 — 2차 개혁", "~430 · '내 하나님이여 나를 기억하사' (느 13)"),
]
PHASES = [  # (시작 번호, 끝 번호, 이름, 부제, 연대, 배경색)
    (1, 8, "1막", "귀환과 성전 기초", "539–536", RGB("17261D")),
    (9, 18, "2막", "멈춘 공사, 다시 선 성전", "536–515", RGB("1B2A20")),
    (19, 24, "3막", "58년 — 에스더의 시대", "486–460", RGB("2A2418")),
    (25, 33, "4막", "★ 에스라", "458–457", RGB("361616")),
    (34, 43, "5막", "느헤미야와 말씀 앞의 백성", "446–430", RGB("18202C")),
]
LANES = [  # (이름, 색, [(라벨, 시작, 끝, 줄, 추정)])
    ("페르시아 왕", C["persia"], [("고레스", d(539, 10, 29), d(530, 8, 1), 0, False), ("캄비세스", d(530, 8, 1), d(522, 7, 1), 0, False),
                               ("다리오 1세", d(522, 9, 29), d(486, 11, 1), 0, False), ("아하수에로", d(486, 12, 1), d(465, 8, 1), 0, False),
                               ("아닥사스다 1세 (465–424)", d(465, 12, 1), d(429), 0, False)]),
    ("유다 지도자", C["neh"], [("세스바살 → 스룹바벨·예수아", d(538, 3, 24), d(515, 4, 21), 0, True),
                            ("에스라 (458~)", d(458, 4, 8), d(445, 12, 31), 0, True),
                            ("느헤미야 총독 1차 (445–433)", d(445, 4, 1), d(433), 1, False), ("2차", d(432), d(430), 1, True)]),
    ("같은 시대 성경", C["proph"], [("다니엘 (~536)", d(545), d(536, 5, 1), 0, False), ("에스더 (483–473)", d(483, 4, 1), d(473, 3, 15), 0, True),
                               ("말라기 (추정)", d(460), d(430), 2, True), ("학개 (520, 넉 달)", d(520, 8, 29), d(520, 12, 18), 1, False),
                               ("역대기 기록 (추정)", d(450), d(429), 1, True), ("스가랴 (520–518)", d(520, 10, 27), d(518, 12, 7), 2, False)]),
]
MILESTONES = [(d(539, 10, 12), "바벨론 함락"), (d(538, 3, 24), "고레스 조서"), (d(536, 4, 15), "성전 기초"),
              (d(520, 8, 29), "학개"), (d(515, 3, 12), "성전 완공"), (d(479), "에스더"),
              (d(458, 4, 8), "에스라 출발"), (d(458, 8, 4), "선한 손 · 도착"), (d(445, 10, 2), "성벽 완공"),
              (d(445, 10, 8), "말씀 낭독"), (d(433), "귀국")]
HIGHLIGHT = d(458, 8, 4)

BG, WHITE, GREY, DIM = RGB("141414"), RGB("FFFFFF"), RGB("9A9A9A"), RGB("555555")
RED = C["ezra"]

SW, SH = 13.333, 7.5
X0, X1 = 1.45, SW - 0.2
SEGS = [(d(540), d(534), 0.14, "539–535 귀환"), (d(534), d(514), 0.17, "534–515 중단과 재건"),
        (d(514), d(458, 1), 0.13, "514–459 · 58년, 에스더"), (d(458, 1), d(457, 6), 0.29, "★ BC 458–457 (확대)"),
        (d(457, 6), d(446, 10), 0.07, "457–447"), (d(446, 10), d(444, 1), 0.15, "BC 446–445 느헤미야 (확대)"),
        (d(444, 1), d(429), 0.05, "444–430")]
TOP, ROW_BOTTOM = 1.30, 6.02
PITCH = (ROW_BOTTOM - TOP) / len(ROWS)
BAR_H, TXT_H = 0.034, 0.08


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
s = None


def new_slide():
    global s
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


def text(x, y, w, h, t, size, color=WHITE, bold=False, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP, wrap=False):
    tb = s.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    tf.word_wrap = wrap; tf.vertical_anchor = anchor
    for i, line in enumerate(t.split("\n")):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        r = p.add_run(); r.text = line
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


# ════════════════ 1장: 연표 ════════════════
new_slide()
box(0.25, 0.12, 6.4, 0.42, fill=RGB("1E5C3A"), shape=MSO_SHAPE.ROUNDED_RECTANGLE)
text(0.4, 0.12, 6.2, 0.42, "이스라엘 귀환 사건 연대표 — 에스라·느헤미야와 그 시대", 15, bold=True, anchor=MSO_ANCHOR.MIDDLE)
text(6.85, 0.13, 6.3, 0.18, "네모: 왼쪽 변 = 시작, 오른쪽 변 = 끝 · 점선 = 추정 · 월일은 히브리력, 위치는 율리우스력 근사 · 전통 연대(에스라 458, 느헤미야 445)", 7, GREY)
leg = [("★ 11/15 본문·결론", C["ezra"]), ("페르시아", C["persia"]), ("귀환·성전", C["ret"]), ("같은 시대 성경", C["proph"]), ("느헤미야", C["neh"])]
lx = 6.85
for name, col in leg:
    box(lx, 0.37, 0.12, 0.1, fill=col)
    text(lx + 0.16, 0.34, 1.6, 0.16, name, 7.5, GREY)
    lx += 0.32 + len(name) * 0.085

for a, b, nm, sub, yrs, bg in PHASES:
    y0 = TOP + (a - 1) * PITCH - 0.02
    y1 = TOP + b * PITCH
    box(0.2, y0, SW - 0.35, y1 - y0, fill=bg)
    text(0.3, y0 + 0.03, 1.1, 0.2, nm, 11, RED if nm == "4막" else WHITE, bold=True)
    text(0.3, y0 + 0.24, 1.15, 0.14, sub, 6.5, GREY)
    text(0.3, y0 + 0.36, 1.15, 0.14, yrs, 6.5, GREY)

LANE_TOP = ROW_BOTTOM + 0.08
LANE_HS = [0.24, 0.34, 0.47]
LANE_Y = []
yy = LANE_TOP
for (nm, col, _), h in zip(LANES, LANE_HS):
    box(0.2, yy, SW - 0.35, h, fill=RGB("22201E"))
    box(0.2, yy, 0.06, h, fill=col)
    text(0.32, yy + h / 2 - 0.08, 1.1, 0.16, nm, 8, col, bold=True)
    LANE_Y.append(yy); yy += h + 0.01

AX_Y = 1.05
BOTTOM = yy
ax = s.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(X0), Inches(AX_Y), Inches(X1), Inches(AX_Y))
ax.line.color.rgb = GREY; ax.line.width = Pt(0.75)
for a, b, _, nm in SEGS:
    xa, xb = xpos(a), xpos(b)
    vline(xa, AX_Y - 0.08, BOTTOM, RGB("606060"), 1.0, dash=False)
    text(xa + 0.02, AX_Y + 0.11, xb - xa - 0.04, 0.12, nm, 5.5, RGB("B0B0B0"), align=PP_ALIGN.CENTER)
ticks = [(d(y), f"BC {y}") for y in (538, 536)] + [(d(y), str(y)) for y in (530, 525, 520, 515)] + \
        [(d(y), str(y)) for y in (500, 480)] + [(d(458, m), f"458.{m}") for m in (1, 4, 7, 10)] + \
        [(d(457, m), f"457.{m}") for m in (1, 4)] + [(d(450), "450")] + \
        [(d(445, m), f"445.{m}") for m in (1, 4, 7, 10)] + [(d(440), "440"), (d(430), "430")]
for t, lab in ticks:
    x = xpos(t)
    vline(x, AX_Y, ROW_BOTTOM, RGB("303030"), 0.4)
    text(x - 0.3, AX_Y + 0.0, 0.6, 0.11, lab, 5.5, GREY, align=PP_ALIGN.CENTER)
for i, (t, lab) in enumerate(MILESTONES):
    x = xpos(t)
    col = RED if t == HIGHLIGHT else WHITE
    box(x - 0.045, AX_Y - 0.045, 0.09, 0.09, fill=col, shape=MSO_SHAPE.DIAMOND)
    vline(x, AX_Y, BOTTOM, RED if t == HIGHLIGHT else DIM, 1.25 if t == HIGHLIGHT else 0.4)
    text(x - 0.5, AX_Y - (0.3, 0.19)[i % 2], 1.0, 0.11, lab, 6.5, col, bold=(t == HIGHLIGHT), align=PP_ALIGN.CENTER)

CHAR_W = 0.048
for i, (cat, a, b, est, title, info) in enumerate(ROWS):
    n = i + 1
    y = TOP + i * PITCH
    xa, xb = xpos(a), xpos(b)
    w = max(xb - xa, 0.045)
    if est:
        box(xa, y, w, BAR_H, line=C[cat], dash=True)
    else:
        box(xa, y, w, BAR_H, fill=C[cat])
    label = f"{n}. {title}  ·  {info}"
    tw = len(label) * CHAR_W + 0.1
    ty = y + BAR_H + 0.003
    col = C["ezra"] if cat == "ezra" else WHITE
    if xa + tw <= SW - 0.2:
        text(xa, ty, tw, TXT_H, label, 5.5, col, bold=(cat == "ezra"))
    else:
        right = min(xa + w, SW - 0.2)
        text(right - tw, ty, tw, TXT_H, label, 5.5, col, bold=(cat == "ezra"), align=PP_ALIGN.RIGHT)

for (nm, col, items), y in zip(LANES, LANE_Y):
    for lab, a, b, sub, est in items:
        lane_y = y + 0.04 + sub * 0.145
        xa, xb = max(xpos(a), X0), xpos(b)
        if est:
            box(xa, lane_y, max(xb - xa, 0.04), 0.035, line=col, dash=True)
        else:
            box(xa, lane_y, max(xb - xa, 0.04), 0.035, fill=col)
        tw = len(lab) * 0.05 + 0.1
        if xa + tw > SW - 0.2:
            text(SW - 0.2 - tw, lane_y + 0.04, tw, 0.09, lab, 5.5, col, align=PP_ALIGN.RIGHT)
        else:
            text(xa + 0.02, lane_y + 0.04, tw, 0.09, lab, 5.5, col)

# 11/15 강조 (3막 아래 빈 공간)
x = xpos(d(458, 1))
text(x - 4.6, TOP + 25 * PITCH + 0.05, 4.5, 0.14, "11/15 설교 본문 (스 7:6-10) — 마음을 준비한 사람, 선한 손 ▶", 7, RED, bold=True, align=PP_ALIGN.RIGHT)
text(x - 4.6, TOP + 25 * PITCH + 0.23, 4.5, 0.14, "빨간 글씨 = 본문 사건(25–33) · 결론 장면(38, 느 8)", 6, RED, align=PP_ALIGN.RIGHT)

# ════════════════ 2장: 같은 시대의 성경 ════════════════
new_slide()
box(0.25, 0.12, 7.4, 0.42, fill=RGB("1E5C3A"), shape=MSO_SHAPE.ROUNDED_RECTANGLE)
text(0.4, 0.12, 7.2, 0.42, "같은 시대의 성경 — 에스라·느헤미야의 어느 대목을 비추나", 15, bold=True, anchor=MSO_ANCHOR.MIDDLE)
text(7.85, 0.2, 5.3, 0.3, "연대는 전통 연대 · '추정'은 학설이 갈리는 연대(Opinion)\n인용은 개역개정", 7.5, GREY)

BOOKS = [  # (책, 시기, 겹치는 대목, 보여 주는 것, 핵심 구절, 색)
    ("역대하 36:22-23", "538 (기록 ~450–400 추정)", "스 1:1-3", "같은 문장으로 두 책이 이어진다 — 열왕기의 끝 뒤에 \"올라갈지어다\"", "\"그의 백성 된 자는 다 올라갈지어다\"", C["ret"]),
    ("다니엘 9–10장", "539–536", "스 1–3 직전·직후", "예레미야의 70년을 읽고 기도한 사람 · 바벨론에 남은 노인", "\"그 연수를 깨달았나니\" (단 9:2)", C["proph"]),
    ("시편 126", "귀환 후 (추정)", "스 1–3", "돌아온 기쁨과 아직 남은 눈물 — 스 3:13 통곡과 함성의 노래판", "\"눈물을 흘리며 씨를 뿌리는 자는 기쁨으로 거두리로다\" (126:5)", C["proph"]),
    ("학개", "520 (넉 달)", "스 4:24–5:2", "16년 멈춘 공사를 깨운 말씀 — \"너희 집은 판벽, 내 집은 황폐\"", "\"너희는 너희의 행위를 살필지니라\" (학 1:5)", C["proph"]),
    ("스가랴 1–8장", "520–518", "스 5–6", "밤의 여덟 환상으로 스룹바벨과 예수아를 격려", "\"오직 나의 영으로 되느니라\" (슥 4:6)", C["proph"]),
    ("에스더", "483–473", "스 6–7장 사이 58년", "돌아가지 않은 사람들 속에서 이름 없이 일하신 하나님", "\"이 때를 위함이 아닌지 누가 알겠느냐\" (에 4:14)", C["proph"]),
    ("말라기", "~460–430 (추정)", "스 9–10 · 느 13", "성전은 있는데 마음이 식은 백성 — 흠 있는 제물·이방 결혼·십일조", "\"내가 너희를 사랑하였노라\" (말 1:2)", C["proph"]),
    ("느헤미야", "446–430", "스 7–10에 이어", "성벽을 세운 뒤 에스라가 다시 말씀을 읽는다 (11/15 결론 장면)", "\"여호와로 인하여 기뻐하는 것이 너희의 힘이니라\" (느 8:10)", C["ezra"]),
]
COLS = [(0.35, 1.5, "성경"), (1.85, 1.6, "시기 (BC)"), (3.45, 1.6, "에스라·느헤미야의 대목"), (5.05, 4.3, "그 책이 보여 주는 것"), (9.35, 3.65, "핵심 구절")]
HY = 0.78
for x, w, h in COLS:
    text(x, HY, w, 0.2, h, 9, GREY, bold=True)
RH = 0.72
for i, (bk, yr, ez, what, verse, col) in enumerate(BOOKS):
    y = HY + 0.3 + i * (RH + 0.06)
    box(0.25, y, SW - 0.45, RH, fill=RGB("1F1F1F"), shape=MSO_SHAPE.ROUNDED_RECTANGLE)
    box(0.35, y + RH / 2 - 0.06, 0.12, 0.12, fill=col, shape=MSO_SHAPE.OVAL)
    vals = [bk, yr, ez, what, verse]
    for k, ((x, w, _), v) in enumerate(zip(COLS, vals)):
        xx, ww = (x + 0.18, w - 0.18) if k == 0 else (x, w - 0.1)
        text(xx, y + 0.08, ww, RH - 0.16, v, 10 if k == 0 else 9, col if k == 0 else WHITE,
             bold=(k == 0), anchor=MSO_ANCHOR.MIDDLE, wrap=True)

prs.save(OUT)
print("saved", OUT, "rows", len(ROWS), "pitch", round(PITCH, 3))
