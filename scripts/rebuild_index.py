import os
import re
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent
MOC_DIR = ROOT_DIR / "0_Index_MOC"
INDEX_FILE = MOC_DIR / "Master_Index.md"
BY_THEME_FILE = MOC_DIR / "Index_by_Theme.md"
BY_BOOK_FILE = MOC_DIR / "Index_by_Book.md"

# Folders that carry findable (non-cold) content. 9_Archive is intentionally
# excluded — see CLAUDE.md 4.5 (cold archive, reachable only via hot-summary links).
META_SCAN_ROOTS = [
    ROOT_DIR / "1_Bible_Exegesis",
    ROOT_DIR / "2_Sermon_Outlines",
    ROOT_DIR / "3_Shared_Assets",
    ROOT_DIR / "4_Reference_Research",
]

TYPE_ICON = {
    "exegesis": "📖",
    "study_note": "📝",
    "sermon": "📢",
    "sermon_script": "🎙️",
    "illustration": "🧱",
    "research_note": "🔎",
    "theology_term": "📚",
}

# 66-book canon, Korean standard names. Order matters for matching (longest/most
# specific first) so e.g. "열왕기상" isn't swallowed by a shorter false match.
BOOKS = [
    "창세기", "출애굽기", "레위기", "민수기", "신명기", "여호수아", "사사기", "룻기",
    "사무엘상", "사무엘하", "열왕기상", "열왕기하", "역대상", "역대하", "에스라",
    "느헤미야", "에스더", "욥기", "시편", "잠언", "전도서", "아가", "이사야",
    "예레미야애가", "예레미야", "에스겔", "다니엘", "호세아", "요엘", "아모스",
    "오바댜", "요나", "미가", "나훔", "하박국", "스바냐", "학개", "스가랴", "말라기",
    "마태복음", "마가복음", "누가복음", "요한복음", "사도행전", "로마서",
    "고린도전서", "고린도후서", "갈라디아서", "에베소서", "빌립보서", "골로새서",
    "데살로니가전서", "데살로니가후서", "디모데전서", "디모데후서", "디도서",
    "빌레몬서", "히브리서", "야고보서", "베드로전서", "베드로후서", "요한일서",
    "요한이서", "요한삼서", "유다서", "요한계시록",
]
BOOKS_SORTED = sorted(BOOKS, key=len, reverse=True)

# Short book names that collide with common Korean words as substrings
# (e.g. "아가" inside "돌아가다/올라가다/찾아가다") — for these, only match
# inside frontmatter (structured, short fields), never the free-form body text.
AMBIGUOUS_SHORT_BOOKS = {"아가"}


def parse_frontmatter(text):
    """Minimal, dependency-free frontmatter reader (no PyYAML) — this repo's
    frontmatter is flat key: value / key: [list, items], no nested blocks."""
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.DOTALL)
    if not m:
        return {}, ""
    raw = m.group(1)
    fields = {}
    for line in raw.split("\n"):
        line_match = re.match(r"^([A-Za-z_]+):\s*(.*)$", line)
        if not line_match:
            continue
        key, val = line_match.group(1), line_match.group(2).strip()
        if val.startswith("[") and val.endswith("]"):
            items = re.findall(r'"([^"]*)"|([^,\[\]]+)', val[1:-1])
            fields[key] = [a or b for a, b in items if (a or b).strip()]
            fields[key] = [v.strip().strip('"') for v in fields[key] if v.strip()]
        else:
            fields[key] = val.strip('"')
    return fields, raw


def collect_documents():
    docs = []
    for root in META_SCAN_ROOTS:
        if not root.exists():
            continue
        for f in sorted(root.rglob("*.md")):
            if ".claude" in f.parts:
                continue
            text = f.read_text(encoding="utf-8")
            fields, raw_frontmatter = parse_frontmatter(text)
            if not fields:
                continue
            docs.append({
                "path": f,
                "stem": f.stem,
                "type": fields.get("type", ""),
                "title": fields.get("title", f.stem),
                "tags": fields.get("tags", []),
                "themes": fields.get("theological_themes", []),
                "raw": raw_frontmatter,
                "full_text": text,
            })
    return docs


def find_books(doc):
    # Scan the whole document (frontmatter + body), not just frontmatter —
    # cross-reference lists ("교차 참조") often live in the body, and skipping
    # them would silently under-connect the very links this index exists for.
    # Exception: AMBIGUOUS_SHORT_BOOKS collide with common Korean words in free
    # text, so those are checked against frontmatter only.
    hits = []
    full_haystack = doc["full_text"] + " " + doc["stem"]
    narrow_haystack = doc["raw"] + " " + doc["stem"]
    for book in BOOKS_SORTED:
        haystack = narrow_haystack if book in AMBIGUOUS_SHORT_BOOKS else full_haystack
        if book in haystack:
            hits.append(book)
    return hits


def scan_files():
    categories = {
        "Study Notes": ROOT_DIR / "1_Bible_Exegesis" / "0_Study_Notes",
        "Old Testament Exegesis": ROOT_DIR / "1_Bible_Exegesis" / "1_Old_Testament",
        "New Testament Exegesis": ROOT_DIR / "1_Bible_Exegesis" / "2_New_Testament",
        "Illustrations": ROOT_DIR / "3_Shared_Assets" / "Illustrations",
        "Theology Terms": ROOT_DIR / "3_Shared_Assets" / "Theology_Terms",
        "Reference Research": ROOT_DIR / "4_Reference_Research",
    }

    content = ["# 🗺️ Master Index & Knowledge Graph (MOC)\n\n", "Automated index of all research, sermons, and shared assets.\n\n"]
    content.append("**메타데이터로 찾기:** [[Index_by_Theme]] (주제별) · [[Index_by_Book]] (성경책별)\n\n")

    for cat_name, cat_path in categories.items():
        content.append(f"## {cat_name}\n")
        if cat_path.exists():
            files = sorted(list(cat_path.glob("*.md")))
            if files:
                for f in files:
                    rel_path = f.stem
                    content.append(f"- [[{rel_path}]]")
            else:
                content.append("- *(No entries found)*")
        content.append("\n")

    # Sermon Outlines: scan every year-folder under 2_Sermon_Outlines dynamically
    sermon_root = ROOT_DIR / "2_Sermon_Outlines"
    content.append("## Sermon Outlines\n")
    if sermon_root.exists():
        year_dirs = sorted([d for d in sermon_root.iterdir() if d.is_dir()])
        any_found = False
        for year_dir in year_dirs:
            files = sorted(list(year_dir.glob("*.md")))
            if files:
                any_found = True
                content.append(f"### {year_dir.name}\n")
                for f in files:
                    content.append(f"- [[{f.stem}]]")
                content.append("\n")
        if not any_found:
            content.append("- *(No entries found)*\n")

    MOC_DIR.mkdir(parents=True, exist_ok=True)
    with open(INDEX_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(content))
    print(f"Master Index updated successfully at {INDEX_FILE}")


def build_meta_indexes():
    docs = collect_documents()

    # ---- Index by Theme (tags + theological_themes merged) ----
    theme_map = {}
    for doc in docs:
        for theme in doc["tags"] + doc["themes"]:
            theme_map.setdefault(theme, []).append(doc)

    lines = [
        "# 🏷️ 주제별 인덱스 (Index by Theme)\n\n",
        "`tags`·`theological_themes` frontmatter를 자동 집계한 것입니다. "
        "같은 개념이 다른 이름으로 쓰였을 수 있습니다(예: 은혜/구원/값없이) — "
        "동의어 통합은 아직 하지 않았으니 관련어로 한 번 더 찾아보세요.\n\n",
        f"*(자동 생성 — `scripts/rebuild_index.py`가 갱신합니다. 총 {len(theme_map)}개 주제)*\n\n",
    ]
    for theme in sorted(theme_map.keys()):
        lines.append(f"## {theme}\n")
        for doc in sorted(theme_map[theme], key=lambda d: d["stem"]):
            icon = TYPE_ICON.get(doc["type"], "📄")
            lines.append(f"- {icon} [[{doc['stem']}]]")
        lines.append("\n")
    BY_THEME_FILE.write_text("\n".join(lines), encoding="utf-8")
    print(f"Theme index updated successfully at {BY_THEME_FILE} ({len(theme_map)} themes)")

    # ---- Index by Book (66-book canon order) ----
    book_map = {}
    for doc in docs:
        for book in find_books(doc):
            book_map.setdefault(book, []).append(doc)

    lines = [
        "# 📚 성경책별 인덱스 (Index by Book)\n\n",
        "주해·설교·예화·묵상 노트·외부 자료 조사에서 언급된 성경책을 자동 스캔하여 "
        "묶은 것입니다(본문 또는 교차 참조 모두 포함). 콜드 아카이브(`9_Archive/`)는 "
        "제외됩니다 — 요약본을 통해 링크를 따라가서 열람하십시오.\n\n",
        f"*(자동 생성 — `scripts/rebuild_index.py`가 갱신합니다. 총 {len(book_map)}권 등장)*\n\n",
    ]
    for book in BOOKS:  # canonical order, not alphabetical
        if book not in book_map:
            continue
        lines.append(f"## {book}\n")
        for doc in sorted(book_map[book], key=lambda d: d["stem"]):
            icon = TYPE_ICON.get(doc["type"], "📄")
            lines.append(f"- {icon} [[{doc['stem']}]]")
        lines.append("\n")
    BY_BOOK_FILE.write_text("\n".join(lines), encoding="utf-8")
    print(f"Book index updated successfully at {BY_BOOK_FILE} ({len(book_map)} books)")


if __name__ == "__main__":
    scan_files()
    build_meta_indexes()
