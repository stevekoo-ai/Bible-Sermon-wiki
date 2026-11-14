"""설교 구연 스크립트 md → docx (슬라이드마다 새 페이지 + 작은 슬라이드 그림).

    python scripts/sermon_script_to_docx.py <script.md> <slides.pptx> <out.docx> [--img-cm 8]

md 형식 (10/18 R5 · 11/15 R3과 같음):
    ## [슬라이드 N] 제목       → 새 페이지 + 제목 + 슬라이드 N 그림
    **➜ ...**                 → 다음 장 전환 멘트 (굵게, 파란색)
    *▸ ...*                   → 동작·메모 (기울임, 회색)
    > ...                     → 머리 안내 (작은 회색)
    ---  이후                 → 위키 링크 꼬리말이므로 넣지 않음
슬라이드 그림은 PowerPoint(COM)로 PNG를 뽑아 쓴다 (Windows + PowerPoint 필요).
내용 수정은 항상 md에서 하고 docx는 다시 만든다.
"""
import re
import subprocess
import sys
import tempfile
from pathlib import Path

from docx import Document
from docx.enum.text import WD_BREAK
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

FONT = "맑은 고딕"


def office_running() -> bool:
    r = subprocess.run(["tasklist", "/FI", "IMAGENAME eq POWERPNT.EXE", "/NH"], capture_output=True, text=True)
    return "POWERPNT.EXE" in r.stdout.upper()


def export_slides(pptx: Path, out_dir: Path) -> dict:
    # ⚠️ 2026-11-14 사고: PowerPoint는 한 프로그램만 뜨기 때문에 COM으로 붙으면 Steve가 작업 중인 창에 붙고,
    # Quit()이 저장 안 된 작업까지 닫아 버렸다. 그래서 PowerPoint가 켜져 있으면 절대 실행하지 않는다.
    if office_running():
        sys.exit("PowerPoint가 켜져 있어 중단합니다 (작업 중인 파일 보호). PowerPoint를 다 닫은 뒤 실행하거나, "
                 "--slides-dir <PNG 폴더>로 미리 뽑아 둔 그림을 쓰세요.")
    ps = f"""
$app = New-Object -ComObject PowerPoint.Application
$p = $app.Presentations.Open('{pptx}', $true, $false, $false)
$i = 1
foreach ($s in $p.Slides) {{ $s.Export('{out_dir}\\slide' + $i + '.png', 'PNG', 1280, 720); $i++ }}
$p.Close(); $app.Quit()
"""
    subprocess.run(["powershell", "-NoProfile", "-Command", ps], check=True)
    return {int(re.search(r"\d+", f.stem).group()): f for f in out_dir.glob("slide*.png")}


def set_font(run, size=None, bold=None, italic=None, color=None):
    run.font.name = FONT
    run._element.rPr.rFonts.set(qn("w:eastAsia"), FONT)
    if size:
        run.font.size = Pt(size)
    if bold is not None:
        run.bold = bold
    if italic is not None:
        run.italic = italic
    if color:
        run.font.color.rgb = RGBColor(*color)


def add_line(doc, text, **fmt):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.line_spacing = 1.3
    set_font(p.add_run(text), **fmt)
    return p


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if len(args) != 3:
        sys.exit(__doc__)
    md, pptx, out = Path(args[0]), Path(args[1]).resolve(), Path(args[2])
    img_cm = float(sys.argv[sys.argv.index("--img-cm") + 1]) if "--img-cm" in sys.argv else 8.0

    text = md.read_text(encoding="utf-8")
    if text.startswith("---"):
        text = text.split("---", 2)[2]
    text = text.split("\n---\n")[0]  # 꼬리말(관련 링크) 제외

    if "--slides-dir" in sys.argv:
        d = Path(sys.argv[sys.argv.index("--slides-dir") + 1])
        slides = {int(re.search(r"\d+", f.stem).group()): f for f in d.glob("slide*.png")}
    else:
        slides = export_slides(pptx, Path(tempfile.mkdtemp(prefix="slides_")))

    doc = Document()
    sec = doc.sections[0]
    sec.page_height, sec.page_width = Cm(29.7), Cm(21.0)
    for side in ("left_margin", "right_margin"):
        setattr(sec, side, Cm(2.0))
    sec.top_margin = sec.bottom_margin = Cm(1.8)

    first_slide = True
    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            continue
        if line.startswith("# "):
            add_line(doc, line[2:], size=18, bold=True)
        elif line.startswith(">"):
            add_line(doc, line.lstrip("> ").strip(), size=9, color=(110, 110, 110))
        elif m := re.match(r"## \[슬라이드 (\d+)\]\s*(.*)", line):
            n = int(m.group(1))
            if not first_slide:
                doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)
            first_slide = False
            h = add_line(doc, f"[슬라이드 {n}] {m.group(2)}", size=14, bold=True, color=(31, 56, 100))
            h.paragraph_format.space_before = Pt(6)
            if n in slides:
                doc.add_paragraph().add_run().add_picture(str(slides[n]), width=Cm(img_cm))
        elif line.startswith("**➜"):
            add_line(doc, line.strip("*").strip(), size=12, bold=True, color=(0, 90, 170))
        elif line.startswith("*▸"):
            add_line(doc, line.strip("*").strip(), size=10, italic=True, color=(120, 120, 120))
        else:
            add_line(doc, line.replace("**", ""), size=12)

    doc.save(out)
    print(f"저장: {out}  (슬라이드 그림 {len(slides)}장, {img_cm}cm)")


if __name__ == "__main__":
    main()
