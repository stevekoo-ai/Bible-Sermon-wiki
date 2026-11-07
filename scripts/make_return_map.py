# -*- coding: utf-8 -*-
"""포로 귀환 지도 연표 — (1) 단독판 BC 539–432, (2) 확장판(BC 740 이사야 ~ BC 432 느헤미야 · 신약)에 합치기.

사용: python scripts/make_return_map.py <출력폴더> [복사할 폴더 ...]
"""
import os, sys, shutil
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bible_map_engine import build_map
from bible_map_art import ART
from bible_map_micro import LANDMARKS, apply_fine_judah
from make_bible_map_kml import P as GP, P_NOTE as GPN
from judah_fall_events import PLACES as JP, PLACE_NOTES as JPN, EVENTS as JEV
import judah_fall_events_ext as X
import return_events as R

out = sys.argv[1] if len(sys.argv) > 1 else "."
P = {**GP, **JP, **X.EXT_PLACES, **R.PLACES}
PN = {**GPN, **JPN, **X.EXT_PLACE_NOTES, **R.PLACE_NOTES}
LM = LANDMARKS + R.landmarks()
BOUNDS = ((23.5, 22.0), (42.5, 53.5))
names = []

# (1) 단독판
evs, total = R.build()
folder = {c[0]: c[1] for c in R.CATS}
r1 = build_map([dict(e, folder=folder[e["cat"]]) for e in evs], P, PN, R.CATS,
               f"포로 귀환 지도 연표 (1–{total}) — 고레스부터 느헤미야까지, 에스라의 넉 달 (BC 539–432)",
               out, "귀환_지도연표", bounds=BOUNDS, landmarks=LM, art=ART,
               kml_desc=f"BC 539 바벨론 함락 ~ BC 432 느헤미야 2차 개혁 + 에필로그, {total}단계. 성경(스·느·에·학·슥·말·단·시) 전문 정독 + 페르시아 시대 역사서·고고학(등급 표기). "
                        "날짜는 Parker–Dubberstein 근사, 에스라 458·느헤미야 445 전통 연대. 경로·예루살렘 성문은 재구성(추정).")
print("standalone", total, r1); names.append("귀환_지도연표")

# (2) 확장판: 기존 순서표에서 539 이후 귀환 부분을 상세판으로 바꾸고 신약 에필로그는 뒤에 둔다
apply_fine_judah(JEV)
cut = next(i for i, it in enumerate(X.ORDER) if isinstance(it, dict) and it["date"].startswith("BC 539"))
nt = [it for it in X.ORDER[cut:] if isinstance(it, dict) and it["cat"] == "nt"]
by_lab = {}
for e in X.OLD:
    by_lab.setdefault(int(e["lab"]), []).append(e)
out_ev, n = [], 0
for item in X.ORDER[:cut]:
    n += 1
    for e in (by_lab[item] if isinstance(item, int) else [item]):
        out_ev.append(dict(e, k=float(n), lab=str(n)))
last = 0
for e in evs:
    if int(e["k"]) != last:
        n += 1; last = int(e["k"])
    out_ev.append(dict(e, k=float(n), lab=str(n)))
for e in nt:
    n += 1
    out_ev.append(dict(e, k=float(n), lab=str(n), act="신약 — 다시 들리는 소리"))
cats = X.CATS + [c for c in R.CATS if c[0] not in {k[0] for k in X.CATS}]
folder = {c[0]: c[1] for c in cats}
r2 = build_map([dict(e, folder=folder[e["cat"]]) for e in out_ev], P, PN, cats,
               f"유다 멸망과 귀환 지도 연표 확장판 (1–{n}) — 열왕기 흐름 + 선지서 + 귀환 (BC 740 ~ BC 432 · 신약)",
               out, "유다멸망_지도연표_확장판", bounds=BOUNDS, landmarks=LM, art=ART,
               kml_desc=f"BC 740 이사야 소명 ~ BC 432 느헤미야, 신약 에필로그까지 {n}단계. 539년 이후는 귀환 지도 연표 상세판으로 교체(2026-11-07).")
print("extended", n, r2); names.append("유다멸망_지도연표_확장판")

for dst in sys.argv[2:]:
    os.makedirs(dst, exist_ok=True)
    for nm in names:
        for ext in ("_미리보기.html", ".kml"):
            shutil.copy2(os.path.join(out, nm + ext), os.path.join(dst, nm + ext))
    print("copied →", dst)
