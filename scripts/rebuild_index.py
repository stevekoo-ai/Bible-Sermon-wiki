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
        "2026 Sermon Outlines": ROOT_DIR / "2_Sermon_Outlines" / "2026_Preaching",
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

    MOC_DIR.mkdir(parents=True, exist_ok=True)
    with open(INDEX_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(content))
    print(f"Master Index updated successfully at {INDEX_FILE}")

if __name__ == "__main__":
    scan_files()
