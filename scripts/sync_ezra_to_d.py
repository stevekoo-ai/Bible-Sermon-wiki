"""에스라 11/15 설교 관련 md를 D:\\설교\\어린이지구설교\\20261115_에스라 7장 으로 복사한다.

    python scripts/sync_ezra_to_d.py            # 복사 (원본이 더 새로울 때만 덮어씀)
    python scripts/sync_ezra_to_d.py --dry-run  # 무엇을 복사할지만 보기

규칙 (Steve, 2026-11-14): 에스라 설교 관련 산출물은 위키 저장과 함께 이 폴더에도 복사본을 둔다.
새 에스라 관련 md를 만들면 아래 EZRA_FILES에 경로를 한 줄 추가하고 다시 실행한다.
원본은 위키(E:\\Claude_Local)이고 D: 쪽은 복사본이다 — 복사본을 고치지 않는다.
"""
import shutil
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

ROOT = Path(__file__).resolve().parent.parent
DEST = Path(r"D:\설교\어린이지구설교\20261115_에스라 7장")

EZRA_FILES = [
    # 설교 아웃라인 · 구연 스크립트
    "2_Sermon_Outlines/2026_Preaching/2026-11-15_에스라_말씀을준비하고가르치는사람.md",
    "2_Sermon_Outlines/2026_Preaching/2026-11-15_에스라_말씀을준비하고가르치는사람_script.md",
    "2_Sermon_Outlines/2026_Preaching/2026-11-15_에스라_말씀을준비하고가르치는사람_script_R2.md",
    "2_Sermon_Outlines/2026_Preaching/2026-11-15_에스라_R3흐름_하나님의두진심.md",
    # 정식 주해
    "1_Bible_Exegesis/1_Old_Testament/에스라1_3-6장_성전재건과칠십년예언.md",
    "1_Bible_Exegesis/1_Old_Testament/에스라7장6-10절_에스라의결심과선한손.md",
    # 묵상·공부 노트
    "1_Bible_Exegesis/0_Study_Notes/2026-10-24_에스라7장정독_스라야의후손과마음을준비한사람.md",
    "1_Bible_Exegesis/0_Study_Notes/2026-10-24_열왕기이후에스라까지_에스라7장의역사적정황.md",
    "1_Bible_Exegesis/0_Study_Notes/2026-11-07_에스라7장설교구상_조상열거와선한손의의미.md",
    "1_Bible_Exegesis/0_Study_Notes/2026-11-08_대제사장계승_엘리의집에서사독까지.md",
    "1_Bible_Exegesis/0_Study_Notes/2026-11-08_에스라8장21절_아하와강가의우리는누구인가.md",
    "1_Bible_Exegesis/0_Study_Notes/2026-11-08_에스라9장이방결혼_말라기에도있는가.md",
    "1_Bible_Exegesis/0_Study_Notes/2026-11-13_고레스이후성전재건_관련성경모음.md",
    "1_Bible_Exegesis/0_Study_Notes/2026-11-13_귀환과성전_하나님의마음지도.md",
    "1_Bible_Exegesis/0_Study_Notes/2026-11-13_바벨론포로생활_어떤취급을받았나.md",
    "1_Bible_Exegesis/0_Study_Notes/2026-11-13_에스라가와야했던이유_하나님의관점.md",
    "1_Bible_Exegesis/0_Study_Notes/2026-11-13_학개스가랴와에스라_시간순표.md",
    "1_Bible_Exegesis/0_Study_Notes/2026-11-14_레위의언약_말2장8절과느13장29절.md",
    "1_Bible_Exegesis/0_Study_Notes/2026-11-14_에스라설교_논리사슬과하나님의뜻.md",
    "1_Bible_Exegesis/0_Study_Notes/2026-11-14_에스라설교방향재설정_성전재건이후의에스라.md",
    "1_Bible_Exegesis/0_Study_Notes/2026-11-14_율법주의란_하나님없이복과구원을얻으려는것.md",
    "1_Bible_Exegesis/0_Study_Notes/2026-11-14_하나님이먼저정하신규칙_성령으로즐거이따름.md",
    # 예화
    "3_Shared_Assets/Illustrations/엄마가찾으면나온다_찾고또찾기.md",
    "3_Shared_Assets/Illustrations/자전거설명서_읽기만해서는못타요.md",
    # 외부 자료 조사
    "4_Reference_Research/2026-11-07_페르시아시대_귀환사_역사자료.md",
    "4_Reference_Research/귀환과성전_하나님의의도_약속과현실_본문조사.md",
    "4_Reference_Research/마음을정하다_용례와결단인물.md",
    "4_Reference_Research/성전재건_예언전수표.md",
    "4_Reference_Research/에스라느헤미야_숲과나무.md",
    "4_Reference_Research/에스라느헤미야_숲과나무_오드리브리핑.md",
    "4_Reference_Research/에스라느헤미야_한권의이야기_관계와구조.md",
    "4_Reference_Research/에스라파송의배경_이미율법대로예배하던공동체에왜.md",
]


def main():
    dry = "--dry-run" in sys.argv
    if not DEST.parent.exists():
        print(f"D: 폴더 없음({DEST.parent}) — 이 PC가 아니면 정상. 건너뜀.")
        return
    DEST.mkdir(parents=True, exist_ok=True)
    copied = skipped = missing = 0
    for rel in EZRA_FILES:
        src = ROOT / rel
        dst = DEST / src.name
        if not src.exists():
            print(f"  ✗ 원본 없음: {rel}")
            missing += 1
            continue
        if dst.exists() and dst.stat().st_mtime >= src.stat().st_mtime:
            skipped += 1
            continue
        print(f"  {'(예정)' if dry else '복사'} {src.name}")
        if not dry:
            shutil.copy2(src, dst)
        copied += 1
    print(f"\n복사 {copied} · 최신이라 건너뜀 {skipped} · 원본 없음 {missing} → {DEST}")


if __name__ == "__main__":
    main()
