"""Bible-Sermon-wiki 한방 스냅샷.

새 세션이 작업을 시작하기 전에 한 번 실행한다. 읽기 전용이며 아무 파일도 고치지 않는다.
    python scripts/wiki_snapshot.py          # 기본
    python scripts/wiki_snapshot.py --no-fetch   # 네트워크 없이
보여주는 것: git 동기화 상태 · 폴더별 문서 수 · 진행 중 인계 문서 · 다가오는/미정 설교 ·
최근 묵상 노트와 나눔 · PC 바깥 저장소(D:\\설교, E:\\GitHub\\Repo_name) 존재 여부.
"""
import re
import subprocess
import sys
from datetime import date
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

ROOT = Path(__file__).resolve().parent.parent
TODAY = date.today().isoformat()
DATE_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})_")

FOLDERS = [
    ("0_Index_MOC", "인덱스 · 스타일 가이드 · 인계 문서"),
    ("1_Bible_Exegesis/0_Study_Notes", "묵상·QT·성경공부 노트"),
    ("1_Bible_Exegesis/1_Old_Testament", "구약 정식 주해"),
    ("1_Bible_Exegesis/2_New_Testament", "신약 정식 주해"),
    ("2_Sermon_Outlines", "설교 아웃라인 · 구연 스크립트 · 시리즈"),
    ("3_Shared_Assets", "예화 · 신학용어 · 지도 · 연표 · 슬라이드"),
    ("4_Group_Sharing", "목장 나눔"),
    ("4_Reference_Research", "외부 자료 조사"),
    ("9_Archive", "콜드 아카이브 (설교 원문 · 대화 전문)"),
]

PC_PLACES = [
    (r"D:\설교\어린이지구설교", "설교 원본 docx/pptx (날짜_본문 폴더)"),
    (r"E:\GitHub\Repo_name", "경제·PEOS 위키 (오드리 브리핑 정의 wiki/concepts/)"),
]


def git(*args):
    try:
        r = subprocess.run(["git", "-C", str(ROOT), *args], capture_output=True,
                           text=True, encoding="utf-8", timeout=30)
        return r.stdout.strip()
    except Exception as e:  # noqa: BLE001
        return f"(git 실패: {e})"


def frontmatter(path):
    try:
        text = path.read_text(encoding="utf-8")
    except Exception:
        return {}
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    fm = {}
    for line in text[3:end].splitlines():
        m = re.match(r"^(\w[\w-]*):\s*(.*)$", line)
        if m:
            fm[m.group(1)] = m.group(2).strip().strip('"')
    return fm


def section(title):
    print(f"\n## {title}")


def main():
    print(f"# Bible-Sermon-wiki 스냅샷 — {TODAY}")
    print(f"루트: {ROOT}")

    # 1. git
    section("1. Git 동기화")
    if "--no-fetch" not in sys.argv:
        git("fetch", "-q", "origin")
    print(git("status", "-sb").splitlines()[0] if git("status", "-sb") else "(git 없음)")
    dirty = [l for l in git("status", "--porcelain").splitlines() if l]
    print(f"커밋 안 된 변경: {len(dirty)}개" + (" → " + ", ".join(l[3:] for l in dirty[:6]) if dirty else ""))
    print("최근 커밋:")
    for line in git("log", "--oneline", "-5").splitlines():
        print(f"  {line}")

    # 2. folders
    section("2. 폴더 지도 (md 문서 수)")
    for rel, desc in FOLDERS:
        p = ROOT / rel
        n = len(list(p.rglob("*.md"))) if p.exists() else 0
        print(f"  {rel:<34} {n:>3}  {desc}")

    # 3. handoff
    section("3. 진행 중 작업 인계 (0_Index_MOC/진행중_작업_인계.md)")
    handoff = ROOT / "0_Index_MOC" / "진행중_작업_인계.md"
    if handoff.exists():
        body = handoff.read_text(encoding="utf-8").split("\n---", 2)[-1]
        lines = [l for l in body.splitlines() if l.strip() and not l.startswith(">")]
        for l in lines[:28]:
            print(f"  {l}")
        if len(lines) > 28:
            print(f"  … (+{len(lines) - 28}줄, 파일에서 계속)")
    else:
        print("  (인계 문서 없음)")

    # 4. sermons
    section("4. 설교 — 다가오는 날짜 / 날짜 미정")
    sermon_root = ROOT / "2_Sermon_Outlines"
    groups = {}
    for f in sorted(sermon_root.rglob("*")):
        if f.is_dir() or f.suffix.lower() not in {".md", ".html", ".pptx"}:
            continue
        m = DATE_RE.match(f.name)
        key = m.group(1) if m else ("TBD" if f.name.startswith("TBD_") else None)
        if key and (key == "TBD" or key >= TODAY):
            groups.setdefault(key, []).append(f)
    if not groups:
        print("  (예정된 설교 파일 없음)")
    for key in sorted(groups, key=lambda k: (k == "TBD", k)):
        files = groups[key]
        outlines = [f for f in files if f.suffix == ".md" and frontmatter(f).get("type") == "sermon"]
        for o in outlines or files[:1]:
            fm = frontmatter(o)
            print(f"  [{key}] {fm.get('title', o.stem)}")
            if fm.get("status"):
                print(f"      상태: {fm['status']}")
        print("      파일: " + " · ".join(f.name.split("_", 1)[-1] if key != "TBD" else f.name for f in files))

    # 5. recent notes / nanum
    section("5. 최근 묵상 노트 5개")
    notes = sorted((ROOT / "1_Bible_Exegesis" / "0_Study_Notes").glob("*.md"), reverse=True)
    for f in notes[:5]:
        print(f"  {f.stem}")
    section("6. 목장 나눔 — 목장별 최신")
    gs = ROOT / "4_Group_Sharing"
    for d in sorted(p for p in gs.iterdir() if p.is_dir()) if gs.exists() else []:
        latest = sorted(d.glob("*.md"))
        print(f"  {d.name}: {len(latest)}편, 최신 {latest[-1].stem if latest else '-'}")

    # 7. outside places
    section("7. 위키 바깥 저장 위치 (PC)")
    for path, desc in PC_PLACES:
        p = Path(path)
        mark = "있음" if p.exists() else "없음(클라우드/다른 PC면 정상)"
        extra = ""
        if p.exists() and "설교" in path:
            subs = sorted(x.name for x in p.iterdir() if x.is_dir() and x.name[:1].isdigit())
            extra = f" · 최근 폴더: {', '.join(subs[-3:])}"
        print(f"  {path} — {mark} · {desc}{extra}")

    print("\n다음: SKILL.md의 '작업별 바로가기'에서 오늘 할 일을 골라 시작.")


if __name__ == "__main__":
    main()
