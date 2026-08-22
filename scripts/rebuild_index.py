import os
import re
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent
MOC_DIR = ROOT_DIR / "0_Index_MOC"
INDEX_FILE = MOC_DIR / "Master_Index.md"

def scan_files():
    categories = {
        "Old Testament Exegesis": ROOT_DIR / "1_Bible_Exegesis" / "1_Old_Testament",
        "New Testament Exegesis": ROOT_DIR / "1_Bible_Exegesis" / "2_New_Testament",
        "Illustrations": ROOT_DIR / "3_Shared_Assets" / "Illustrations",
        "Theology Terms": ROOT_DIR / "3_Shared_Assets" / "Theology_Terms",
    }

    content = ["# 🗺️ Master Index & Knowledge Graph (MOC)\n\n", "Automated index of all research, sermons, and shared assets.\n\n"]

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

if __name__ == "__main__":
    scan_files()
