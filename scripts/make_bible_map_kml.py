# -*- coding: utf-8 -*-
"""예수님 족보 연표 PPT의 인물·사건을 지도 위 번호 + 이동 화살표로 — KML(구글 내 지도/Google Earth) + HTML 미리보기.

사용: python scripts/make_bible_map_kml.py <출력폴더>
같은 번호 = 같은 시기에 여러 갈래로 일어난 일 (화살표 여러 개).
좌표는 전통적·학계 통용 위치의 근사값(일부 장소는 위치 논쟁 있음 — note 참고).
"""
import math, os, sys, json, html

OUT = sys.argv[1] if len(sys.argv) > 1 else "."

P = {  # 장소: (위도, 경도)
    "우르": (30.9626, 46.1031), "하란": (36.8650, 39.0310), "세겜": (32.2137, 35.2820),
    "벧엘": (31.9300, 35.2217), "애굽(멤피스)": (29.8446, 31.2502), "고센(라암셋)": (30.7990, 31.8340),
    "헤브론": (31.5326, 35.0998), "단": (33.2486, 35.6525), "예루살렘": (31.7781, 35.2354),
    "술 길 샘": (30.8500, 34.3500), "브엘세바": (31.2450, 34.8400), "브니엘(얍복)": (32.1800, 35.6700),
    "아둘람": (31.6500, 34.9900), "숙곳": (30.5540, 32.0990), "홍해": (29.9500, 32.5500),
    "시내산(호렙)": (28.5392, 33.9750), "가데스 바네아": (30.6450, 34.4230), "느보산": (31.7680, 35.7260),
    "여리고": (31.8711, 35.4440), "드빌": (31.4990, 34.9670), "다볼산": (32.6870, 35.3900),
    "오브라": (32.6070, 35.2890), "모압": (31.1800, 35.7000), "베들레헴": (31.7054, 35.2024),
    "실로": (32.0556, 35.2897), "소라": (31.7760, 34.9820), "길르앗 미스바": (32.3300, 35.8000),
    "라마": (31.8530, 35.2020), "사마리아": (32.2760, 35.1970), "갈멜산": (32.6700, 35.0500),
    "도단": (32.4130, 35.2380), "욥바": (32.0530, 34.7520), "니느웨": (36.3590, 43.1520),
    "드고아": (31.6140, 35.2260), "모레셋": (31.6000, 34.8900), "하볼 강(고산)": (36.5000, 40.7500),
    "라기스": (31.5650, 34.8490), "바벨론": (32.5364, 44.4209), "아나돗": (31.8130, 35.2640),
    "므깃도": (32.5850, 35.1850), "그발 강(델아빕)": (32.1300, 45.2300), "립나": (34.4800, 36.3800),
    "다바네스": (30.9720, 32.2000), "수산": (32.1890, 48.2580), "힛데겔(티그리스) 강가": (33.3000, 44.4000),
    "바사(파사르가대)": (30.2020, 53.1790), "펠라(마케도니아)": (40.7600, 22.5250),
    "알렉산드리아": (31.2001, 29.9187), "안디옥": (36.2021, 36.1604), "모데인": (31.9300, 34.9600),
    "로마": (41.8902, 12.4922), "나사렛": (32.6996, 35.3035), "요단강 베다니": (31.8370, 35.5510),
}

# (번호, 기, 종류, 연대, 제목, 설명, 장소 or [경로...])
#  종류: g=족보 인물/사건, k=왕, m=하나님이 보내신 사람(천사·선지자·사사·멜기세덱·세례요한), x=세계사
E = [
    (1, 1, "g", "BC 2166", "아브라함 출생 — 갈대아 우르", "창 11:27-28", "우르"),
    (2, 1, "g", "BC 2100경", "데라와 함께 하란으로", "창 11:31", ["우르", "하란"]),
    (3, 1, "g", "BC 2091", "부르심 — 가나안으로", "창 12:1-6 · 75세", ["하란", "세겜"]),
    (4, 1, "g", "BC 2090경", "기근으로 애굽에 내려감", "창 12:10", ["세겜", "벧엘", "애굽(멤피스)"]),
    (5, 1, "g", "BC 2089경", "애굽에서 올라와 헤브론 마므레에 거주", "창 13", ["애굽(멤피스)", "헤브론"]),
    (6, 1, "g", "BC 2085경", "롯을 구하러 단까지 추격", "창 14:14", ["헤브론", "단"]),
    (6, 1, "m", "BC 2085경", "멜기세덱 — 살렘 왕, 지극히 높은 하나님의 제사장", "창 14:18-20; 히 7", ["단", "예루살렘"]),
    (7, 1, "g", "BC 2085경", "횃불 언약", "창 15 · 400년 종살이 예고", "헤브론"),
    (8, 1, "m", "BC 2080", "여호와의 사자 — 도망친 하갈을 만남", "창 16:7 · 술 길 샘물", ["헤브론", "술 길 샘"]),
    (9, 1, "g", "BC 2066", "이삭 출생", "창 21 · 브엘세바 부근", "브엘세바"),
    (10, 1, "m", "BC 2050경", "모리아산 — 이삭을 바침, 여호와의 사자", "창 22 · 모리아 = 훗날 성전 터(대하 3:1)", ["브엘세바", "예루살렘"]),
    (11, 1, "g", "BC 1929경", "야곱, 에서를 피해 하란으로 (벧엘의 꿈)", "창 28", ["브엘세바", "벧엘", "하란"]),
    (12, 1, "g", "BC 1909경", "야곱 귀향 — 브니엘에서 '이스라엘'", "창 32-33", ["하란", "브니엘(얍복)", "세겜"]),
    (13, 1, "g", "BC 1900경", "유다와 다말 — 베레스·세라 출생", "창 38 · 족보 첫 여인", "아둘람"),
    (14, 1, "g", "BC 1876", "야곱 가족 70명 애굽 이주 (베레스·헤스론 포함)", "창 46:12", ["헤브론", "브엘세바", "고센(라암셋)"]),
    (15, 1, "g", "BC 1876–1446", "400년 종살이 — 람·아미나답 세대", "출 1 · 창 15:13 성취", "고센(라암셋)"),
    (16, 1, "m", "BC 1447", "떨기나무 — 여호와의 사자, 모세를 부르심", "출 3", "시내산(호렙)"),
    (17, 1, "g", "BC 1446", "출애굽 — 나손 세대", "출 12-14 · 홍해 도하 위치는 논쟁 중", ["고센(라암셋)", "숙곳", "홍해", "시내산(호렙)"]),
    (18, 1, "m", "BC 1446", "시내산 언약 · 십계명 — 선지자 모세", "출 19-20", "시내산(호렙)"),
    (19, 1, "g", "BC 1445–1406", "광야 40년", "민수기", ["시내산(호렙)", "가데스 바네아", "느보산"]),
    (20, 1, "g", "BC 1406", "가나안 입성 — 여리고, 살몬과 라합", "수 2, 6", ["느보산", "여리고"]),
    (21, 1, "m", "BC 1373–1334", "사사 옷니엘", "삿 1:13; 3:9", "드빌"),
    (22, 1, "m", "BC 1316–1236", "사사 에훗 — 모압 왕 에글론", "삿 3", "여리고"),
    (23, 1, "m", "BC 1216–1176", "사사 드보라·바락 — 다볼산", "삿 4-5", "다볼산"),
    (24, 1, "m", "BC 1169", "사사 기드온 — 여호와의 사자가 부름", "삿 6", "오브라"),
    (25, 1, "g", "BC 1140경", "룻이 나오미와 베들레헴으로 — 보아스·오벳", "룻 1-4 · 모압 여인", ["모압", "베들레헴"]),
    (26, 1, "m", "BC 1107–1067", "제사장·사사 엘리 — 실로 성막", "삼상 1-4", "실로"),
    (27, 1, "m", "BC 1095", "여호와의 사자 — 삼손의 부모", "삿 13", "소라"),
    (28, 1, "m", "BC 1086–1080", "사사 입다", "삿 11", "길르앗 미스바"),
    (29, 1, "m", "BC 1075–1055", "사사 삼손", "삿 14-16", "소라"),
    (30, 1, "m", "BC 1025경", "사무엘(마지막 사사·선지자)이 이새의 아들 다윗에게 기름부음", "삼상 16", ["라마", "베들레헴"]),
    (31, 1, "k", "BC 1010 → 1003", "다윗 — 헤브론에서 즉위, 예루살렘으로 / 나단의 다윗 언약", "삼하 2, 5, 7", ["헤브론", "예루살렘"]),
    (32, 2, "k", "BC 959", "솔로몬 성전 완공 — 하늘에서 불", "왕상 8; 대하 7:1", "예루살렘"),
    (33, 2, "k", "BC 931", "왕국 분열 — 르호보암이 세겜에 갔다가 거절당함", "왕상 12:1-19", ["예루살렘", "세겜"]),
    (33, 2, "k", "BC 931", "여로보암 — 벧엘과 단에 금송아지", "왕상 12:28-29", ["세겜", "벧엘"]),
    (33, 2, "k", "BC 931", "여로보암 — 단의 금송아지", "왕상 12:29", ["세겜", "단"]),
    (34, 2, "k", "BC 913–848", "남유다 아비야·아사·여호사밧", "왕상 15, 22", "예루살렘"),
    (35, 2, "m", "BC 860경", "엘리야 — 갈멜산 대결", "왕상 18", "갈멜산"),
    (36, 2, "m", "BC 860경", "엘리야 도피 — 로뎀나무 아래 천사, 호렙산", "왕상 19", ["갈멜산", "브엘세바", "시내산(호렙)"]),
    (37, 2, "k", "BC 853–841", "요람 — 아합의 딸 아달랴와 결혼", "왕하 8:16-18", "예루살렘"),
    (37, 2, "m", "BC 848–797", "엘리사 — 사마리아·도단", "왕하 2-13", ["사마리아", "도단"]),
    (38, 2, "m", "BC 785경", "요나 — 니느웨로", "욘 1-4", ["욥바", "니느웨"]),
    (39, 2, "m", "BC 760", "아모스 — 드고아에서 벧엘로", "암 1:1; 7:10-13", ["드고아", "벧엘"]),
    (39, 2, "m", "BC 755–715", "호세아 — 북이스라엘", "호 1", "사마리아"),
    (40, 2, "m", "BC 740", "이사야 소명 — 웃시야 왕이 죽던 해 (웃시야·요담)", "사 6", "예루살렘"),
    (40, 2, "m", "BC 735–700", "미가 — 모레셋", "미 1:1", "모레셋"),
    (41, 2, "k", "BC 722", "북이스라엘 멸망 — 앗수르로 포로 (아하스 재위 중)", "왕하 17:6", ["사마리아", "하볼 강(고산)"]),
    (42, 2, "k", "BC 701", "산헤립 — 라기스 함락 후 예루살렘 포위 (히스기야)", "왕하 18-19", ["니느웨", "라기스", "예루살렘"]),
    (42, 2, "m", "BC 701", "여호와의 사자 — 앗수르 군대 18만 5천", "왕하 19:35", "예루살렘"),
    (43, 2, "k", "BC 697–642", "므낫세 — 바벨론으로 끌려갔다가 회개하고 돌아옴 (아몬)", "왕하 21; 대하 33:11-13", ["예루살렘", "바벨론", "예루살렘"]),
    (44, 2, "m", "BC 650–630", "나훔 — 니느웨 멸망 예언 / 스바냐", "나 1; 습 1", "니느웨"),
    (45, 2, "m", "BC 627", "예레미야 소명 — 아나돗", "렘 1", "아나돗"),
    (46, 2, "k", "BC 622", "요시야 — 율법책 발견, 대개혁", "왕하 22-23", "예루살렘"),
    (47, 2, "k", "BC 609", "요시야 전사 — 므깃도", "왕하 23:29", ["예루살렘", "므깃도"]),
    (48, 2, "m", "BC 607경", "하박국", "합 1-3", "예루살렘"),
    (49, 2, "m", "BC 605", "1차 포로 — 다니엘", "단 1", ["예루살렘", "바벨론"]),
    (50, 2, "k", "BC 597", "여고냐(여호야긴)와 에스겔 포로", "왕하 24:12-16", ["예루살렘", "바벨론"]),
    (51, 2, "m", "BC 593", "에스겔 — 그발 강가의 환상", "겔 1:1-3", ["바벨론", "그발 강(델아빕)"]),
    (52, 2, "k", "BC 586", "★ 성전 불탐 — 예루살렘 멸망 (10/18 본문)", "왕하 25:8-10", "예루살렘"),
    (52, 2, "k", "BC 586", "시드기야 도주 — 여리고에서 잡혀 립나로", "왕하 25:4-7", ["예루살렘", "여리고", "립나"]),
    (52, 2, "k", "BC 586", "백성 포로 — 바벨론으로", "왕하 25:11, 21", ["립나", "바벨론"]),
    (53, 3, "m", "BC 582경", "예레미야 — 애굽 다바네스로 끌려감", "렘 43:7", ["예루살렘", "다바네스"]),
    (54, 3, "g", "BC 561", "여고냐 석방 — 왕의 식탁 (스알디엘 출생은 포로기)", "왕하 25:27-30", "바벨론"),
    (55, 3, "m", "BC 551–539", "가브리엘 — 다니엘에게 환상 해석 (수산 환상)", "단 8:2, 16; 9:21", "수산"),
    (56, 3, "x", "BC 539", "고레스 — 바벨론 정복, 귀환 칙령(538)", "스 1:1-4; 사 45:1", ["바사(파사르가대)", "바벨론"]),
    (57, 3, "m", "BC 536", "미가엘 — 힛데겔 강가의 다니엘", "단 10:4, 13, 21", "힛데겔(티그리스) 강가"),
    (58, 3, "g", "BC 538", "1차 귀환 — 스룹바벨·예수아", "스 1-2", ["바벨론", "예루살렘"]),
    (59, 3, "m", "BC 520–516", "학개·스가랴 — 성전 재건 완공(516)", "스 5-6; 학 1-2", "예루살렘"),
    (60, 3, "g", "BC 486–465", "에스더·모르드개 — 수산 궁 (아비훗 세대 추정)", "에 2:5-6", "수산"),
    (61, 3, "g", "BC 458", "에스라 귀환", "스 7-8", ["바벨론", "예루살렘"]),
    (62, 3, "g", "BC 445", "느헤미야 — 수산에서 예루살렘으로, 성벽 52일", "느 1-2, 6:15", ["수산", "예루살렘"]),
    (63, 3, "m", "BC 430경", "말라기 — 구약 마지막 선지자", "말 3:1; 4:5", "예루살렘"),
    (64, 3, "x", "BC 334–332", "알렉산더 대왕 — 동방 원정 (사독 세대 추정)", "단 8:5-8 해석 참고", ["펠라(마케도니아)", "예루살렘", "알렉산드리아"]),
    (65, 3, "x", "BC 3세기", "프톨레미 왕조 — 알렉산드리아에서 70인역 번역 (엘리웃 세대 추정)", "성경 밖 역사", "알렉산드리아"),
    (66, 3, "x", "BC 167", "안티오쿠스 4세 — 성전 모독 (엘르아살 세대 추정)", "단 11:31 해석 참고", ["안디옥", "예루살렘"]),
    (67, 3, "x", "BC 164", "마카비 — 성전 정화, 수전절(하누카)", "요 10:22", ["모데인", "예루살렘"]),
    (68, 3, "x", "BC 63", "로마 폼페이우스 — 예루살렘 점령 (야곱 세대 추정)", "성경 밖 역사", ["로마", "예루살렘"]),
    (69, 3, "k", "BC 37–4", "헤롯 대왕 — 성전 증축 (요셉 세대)", "요 2:20", "예루살렘"),
    (70, 3, "m", "BC 7경", "가브리엘 — 성전의 사가랴에게", "눅 1:11-19", "예루살렘"),
    (71, 3, "m", "BC 6경", "가브리엘 — 나사렛의 마리아에게", "눅 1:26-38", "나사렛"),
    (72, 3, "g", "BC 6–4", "요셉과 마리아, 베들레헴으로 — 예수 탄생", "눅 2:1-7; 마 1:18-25", ["나사렛", "베들레헴"]),
    (73, 3, "m", "AD 28–29", "세례 요한 — 요단강에서 주의 길을 예비", "마 3; 요 1:28", "요단강 베다니"),
    (74, 3, "g", "AD 30–33", "예수 그리스도 — 예루살렘, 십자가와 부활", "마 26-28", ["나사렛", "예루살렘"]),
]

COL = {  # 종류별 색 (KML은 aabbggrr)
    1: "#F2C14E", 2: "#4FA3E0", 3: "#5CC98A", "m": "#C78BE8", "x": "#9A9A9A", "red": "#FF4D4D",
}


def color_of(e):
    num, per, kind = e[0], e[1], e[2]
    if num == 52:
        return COL["red"]
    if kind in ("m", "x"):
        return COL[kind]
    return COL[per]


def kml_color(hexcol, alpha="ff"):
    h = hexcol.lstrip("#")
    return alpha + h[4:6] + h[2:4] + h[0:2]


def curve(a, b, bend):
    """a,b = (lat,lon). 곡선(2차 베지어)으로 왕복 경로가 겹치지 않게."""
    (y1, x1), (y2, x2) = a, b
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
    dx, dy = x2 - x1, y2 - y1
    L = math.hypot(dx, dy) or 1e-9
    cx, cy = mx - dy / L * L * bend, my + dx / L * L * bend
    pts = []
    for i in range(21):
        t = i / 20
        x = (1 - t) ** 2 * x1 + 2 * (1 - t) * t * cx + t ** 2 * x2
        y = (1 - t) ** 2 * y1 + 2 * (1 - t) * t * cy + t ** 2 * y2
        pts.append((y, x))
    return pts


def arrowhead(p_prev, p_end, size):
    (y1, x1), (y2, x2) = p_prev, p_end
    ang = math.atan2(y2 - y1, (x2 - x1) * math.cos(math.radians(y2)))
    left = ang + math.radians(152)
    right = ang - math.radians(152)
    k = 1 / math.cos(math.radians(y2))
    pL = (y2 + size * math.sin(left), x2 + size * math.cos(left) * k)
    pR = (y2 + size * math.sin(right), x2 + size * math.cos(right) * k)
    return [p_end, pL, pR, p_end]


# ---- 같은 장소에 여러 번호가 겹치지 않게 살짝 흩뿌림 ----
visits = {}
markers = []   # (num, per, kind, date, title, note, place, lat, lon, color)
paths = []     # (num, title, color, [(lat,lon)...], head)
for idx, e in enumerate(E):
    num, per, kind, date, title, note, where = e
    col = color_of(e)
    route = where if isinstance(where, list) else [where]
    end = route[-1]
    n = visits.get(end, 0); visits[end] = n + 1
    r = 0.045 * math.sqrt(n); th = n * 2.4
    lat, lon = P[end][0] + r * math.sin(th), P[end][1] + r * math.cos(th)
    markers.append((num, per, kind, date, title, note, end, lat, lon, col))
    if len(route) > 1:
        pts = []
        bend = 0.12 if idx % 2 == 0 else -0.12
        for a, b in zip(route[:-1], route[1:]):
            seg = curve(P[a], P[b], bend)
            pts += seg if not pts else seg[1:]
        seglen = math.hypot(P[route[-1]][0] - P[route[-2]][0], P[route[-1]][1] - P[route[-2]][1])
        head = arrowhead(pts[-3], pts[-1], max(0.035, min(0.18, seglen * 0.05)))
        paths.append((num, title, col, pts, head, " → ".join(route)))

# ---------------- KML ----------------
def esc(t):
    return html.escape(t, quote=False)

folders = {1: "1기 · 약속 (아브라함 → 다윗)", 2: "2기 · 왕국과 몰락 (다윗 → 바벨론 포로)", 3: "3기 · 회복 (포로 → 그리스도)"}
k = ['<?xml version="1.0" encoding="UTF-8"?>',
     '<kml xmlns="http://www.opengis.net/kml/2.2"><Document>',
     '<name>예수님 족보와 하나님이 보내신 사람들 — 지도 연표</name>',
     '<description>1~74 시간 순서. 같은 번호 = 같은 시기의 여러 갈래. 금색=1기, 파랑=2기, 초록=3기, 보라=천사·선지자·사사, 회색=세계사, 빨강=BC 586 성전 불탐. 좌표는 근사값.</description>']
for num_col in set(m[9] for m in markers):
    sid = num_col.lstrip("#")
    k.append(f'<Style id="p{sid}"><IconStyle><color>{kml_color(num_col)}</color><scale>0.9</scale>'
             f'<Icon><href>http://maps.google.com/mapfiles/kml/shapes/placemark_circle.png</href></Icon></IconStyle>'
             f'<LabelStyle><scale>0.8</scale></LabelStyle></Style>')
    k.append(f'<Style id="l{sid}"><LineStyle><color>{kml_color(num_col, "e6")}</color><width>3</width></LineStyle>'
             f'<PolyStyle><color>{kml_color(num_col)}</color><fill>1</fill><outline>0</outline></PolyStyle></Style>')
for per in (1, 2, 3):
    k.append(f"<Folder><name>{esc(folders[per])}</name>")
    for (num, pp, kind, date, title, note, place, lat, lon, col) in markers:
        if pp != per:
            continue
        k.append(f'<Placemark><name>{num}. {esc(title)}</name><description>{esc(date)} · {esc(place)} · {esc(note)}</description>'
                 f'<styleUrl>#p{col.lstrip("#")}</styleUrl><Point><coordinates>{lon:.5f},{lat:.5f},0</coordinates></Point></Placemark>')
    for (num, title, col, pts, head, route_txt) in paths:
        per_of = next(m[1] for m in markers if m[0] == num and m[4] == title)
        if per_of != per:
            continue
        coords = " ".join(f"{x:.5f},{y:.5f},0" for y, x in pts)
        hc = " ".join(f"{x:.5f},{y:.5f},0" for y, x in head)
        k.append(f'<Placemark><name>{num} → {esc(route_txt)}</name><description>{esc(title)}</description>'
                 f'<styleUrl>#l{col.lstrip("#")}</styleUrl><MultiGeometry>'
                 f'<LineString><tessellate>1</tessellate><coordinates>{coords}</coordinates></LineString>'
                 f'<Polygon><outerBoundaryIs><LinearRing><coordinates>{hc}</coordinates></LinearRing></outerBoundaryIs></Polygon>'
                 f'</MultiGeometry></Placemark>')
    k.append("</Folder>")
k.append("</Document></kml>")
os.makedirs(OUT, exist_ok=True)
with open(os.path.join(OUT, "예수님족보_지도연표.kml"), "w", encoding="utf-8") as f:
    f.write("\n".join(k))

# ---------------- HTML 미리보기 (Leaflet + OSM) ----------------
data = {
    "markers": [dict(n=m[0], per=m[1], kind=m[2], date=m[3], title=m[4], note=m[5], place=m[6], lat=m[7], lon=m[8], col=m[9]) for m in markers],
    "paths": [dict(n=p[0], title=p[1], col=p[2], pts=p[3], head=p[4], route=p[5]) for p in paths],
}
page = """<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>예수님 족보 지도 연표</title>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.css">
<script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.js"></script>
<style>html,body{margin:0;height:100%;background:#141414;font-family:'Malgun Gothic',sans-serif}#map{position:absolute;inset:0 0 0 300px}
#side{position:absolute;left:0;top:0;bottom:0;width:300px;overflow:auto;background:#1b1b1b;color:#ddd;font-size:12px}
#side h1{font-size:14px;margin:10px;color:#fff}#side .it{padding:4px 10px;border-bottom:1px solid #2a2a2a;cursor:pointer}#side .it:hover{background:#2a2a2a}
.num{display:flex;align-items:center;justify-content:center;border-radius:50%;color:#111;font-weight:700;font-size:11px;border:1px solid #111;width:22px;height:22px}
.lg span{display:inline-block;width:10px;height:10px;border-radius:50%;margin:0 4px 0 10px}</style></head><body>
<div id="side"><h1>예수님 족보 지도 연표 (1–74)</h1><div class="lg"><span style="background:#F2C14E"></span>1기<span style="background:#4FA3E0"></span>2기<span style="background:#5CC98A"></span>3기<br><span style="background:#C78BE8"></span>천사·선지자·사사<span style="background:#9A9A9A"></span>세계사<span style="background:#FF4D4D"></span>BC 586</div><div id="list"></div></div>
<div id="map"></div><script>
const D=__DATA__;
const map=L.map('map').setView([32.5,38],5);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',{maxZoom:12,attribution:'© OpenStreetMap'}).addTo(map);
D.paths.forEach(p=>{L.polyline(p.pts,{color:p.col,weight:3,opacity:.9}).addTo(map).bindTooltip(p.n+' → '+p.route);
 L.polygon(p.head,{color:p.col,fillColor:p.col,fillOpacity:1,weight:1}).addTo(map);});
const list=document.getElementById('list');
D.markers.forEach(m=>{const ic=L.divIcon({className:'',html:`<div class="num" style="background:${m.col}">${m.n}</div>`,iconSize:[22,22],iconAnchor:[11,11]});
 const mk=L.marker([m.lat,m.lon],{icon:ic}).addTo(map).bindPopup(`<b>${m.n}. ${m.title}</b><br>${m.date} · ${m.place}<br>${m.note}`);
 const d=document.createElement('div');d.className='it';d.innerHTML=`<b style="color:${m.col}">${m.n}</b> ${m.date} — ${m.title}`;d.onclick=()=>{map.setView([m.lat,m.lon],8);mk.openPopup()};list.appendChild(d);});
</script></body></html>"""
with open(os.path.join(OUT, "예수님족보_지도연표_미리보기.html"), "w", encoding="utf-8") as f:
    f.write(page.replace("__DATA__", json.dumps(data, ensure_ascii=False)))
print("markers", len(markers), "paths", len(paths), "numbers", len(set(m[0] for m in markers)))
