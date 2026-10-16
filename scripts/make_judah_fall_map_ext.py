# -*- coding: utf-8 -*-
"""유다 멸망 지도 연표 확장판 — 요시야 시대(BC 627)부터 귀환·스가랴(BC 518)와 신약 에필로그까지,
열왕기 흐름에 예레미야·에스겔·애가 등 선지서의 말씀을 시간순으로 끼워 넣은 판.

사용: python scripts/make_judah_fall_map_ext.py <출력폴더>
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bible_map_engine import build_map
from make_bible_map_kml import P as GP, P_NOTE as GPN
from judah_fall_events import PLACES, PLACE_NOTES, EVENTS
from judah_fall_events_ext import CATS, EXT_PLACES, EXT_PLACE_NOTES, build_events
from bible_map_micro import LANDMARKS, apply_fine_judah

apply_fine_judah(EVENTS)          # 기존 38개 사건의 정밀 위치(확장판에도 그대로 이어짐)
events, total = build_events()

out = sys.argv[1] if len(sys.argv) > 1 else "."
P = {**GP, **PLACES, **EXT_PLACES}
PN = {**GPN, **PLACE_NOTES, **EXT_PLACE_NOTES}
folder = dict((c[0], c[1]) for c in CATS)

r = build_map([dict(e, folder=folder[e["cat"]]) for e in events], P, PN, CATS,
              f"유다 멸망 지도 연표 확장판 (1–{total}) — 열왕기 흐름 + 선지서의 말씀 (BC 740 ~ BC 518 · 신약)",
              out, "유다멸망_지도연표_확장판", bounds=((29.5, 30.5), (37.2, 46)), landmarks=LANDMARKS,
              kml_desc=f"BC 740 이사야 소명 ~ BC 518 스가랴, 신약 에필로그까지 {total}단계. 기존 38개 사건 + 예레미야·에스겔·애가·하박국·스바냐·오바댜·다니엘·시편·학개·스가랴의 말씀. "
                       "날짜는 Thiele/Parker-Dubberstein 환산(함락 586년설), 율리우스력 근사. 근거: 2026-10-16 선지서 시간순 재배열 노트.")
print(total, r)
