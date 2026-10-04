# -*- coding: utf-8 -*-
"""유다 멸망 지도 연표 — (1) 단독판, (2) 예수님 족보 지도 통합판 Rev2.

사용: python scripts/make_judah_fall_map.py <출력폴더>
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bible_map_engine import build_map
from make_bible_map_kml import P as GP, P_NOTE as GPN, GENEALOGY_CATS, genealogy_events
from judah_fall_events import PLACES, PLACE_NOTES, CATS, EVENTS
from bible_map_micro import LANDMARKS, apply_fine_judah, apply_fine_genealogy

apply_fine_judah(EVENTS)

out = sys.argv[1] if len(sys.argv) > 1 else "."
P = {**GP, **PLACES}
PN = {**GPN, **PLACE_NOTES}

# (1) 단독판
r1 = build_map([dict(e, folder=dict((c[0], c[1]) for c in CATS)[e["cat"]]) for e in EVENTS], P, PN, CATS,
               "유다 멸망 지도 연표 (1–38) — 왕하 24–25 · 렘 39–43 · 52", out, "유다멸망_지도연표",
               bounds=((29.5, 30.5), (37.2, 46)), landmarks=LANDMARKS,
               kml_desc="BC 605~561, 38개 사건. 날짜는 Thiele/Parker-Dubberstein 환산(함락 586년설), 율리우스력 근사. 좌표는 근사값.")
print("standalone", r1)

# (2) Rev2 — 족보 지도에 '유다 멸망 상세' 범례로 통합 (기본: 꺼짐)
detail = [dict(e, k=e["r2k"], lab="D" + e["lab"], cat="d", folder="유다 멸망 상세 (D1–D38)") for e in EVENTS]
cats2 = GENEALOGY_CATS + [("d", "유다 멸망 상세 D1–D38", "#FF8C42")]
r2 = build_map(apply_fine_genealogy(genealogy_events()) + detail, P, PN, cats2, "예수님 족보 지도 연표 Rev2 (1–74 + 유다 멸망 D1–D38)", out,
               "예수님족보_지도연표_Rev2", default_off=("d",), landmarks=LANDMARKS,
               kml_desc="예수님 족보 1~74 + 유다 멸망 상세 D1~D38(49~54번 사이에 시간순으로 끼워 넣음). 범례에서 켜고 끌 수 있음.")
print("rev2", r2)
