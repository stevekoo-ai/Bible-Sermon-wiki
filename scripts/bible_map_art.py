# -*- coding: utf-8 -*-
"""지도 연표 삽화 — 자막·팝업에 들어가는 단순한 선화(SVG, 직접 그림 · 저작권 없음).

모든 그림은 viewBox 0 0 120 90, 양피지 바탕(#f4ecd8)은 페이지 CSS가 깐다.
사건 dict 에 art="키" 를 넣으면 bible_map_engine.build_map(art=ART) 이 자막 왼쪽에 보여 준다.
"""

INK, GOLD, BLUE, RED, GREEN, STONE, SAND, WOOD = "#3b2f22", "#c9962b", "#4a7bb7", "#b94a3b", "#5a8f4e", "#a89a82", "#e2cfa3", "#9a6a3c"


def _svg(body, label=""):
    lab = (f'<rect x="{60-len(label)*4.2-4:.0f}" y="78" width="{len(label)*8.4+8:.0f}" height="11" rx="3" fill="#f4ecd8" opacity=".9"/>'
           f'<text x="60" y="86" text-anchor="middle" font-size="8" fill="{INK}" font-family="Malgun Gothic">{label}</text>') if label else ""
    return (f'<svg viewBox="0 0 120 90" xmlns="http://www.w3.org/2000/svg" stroke-linecap="round" stroke-linejoin="round">'
            f'{body}{lab}</svg>')


S = f'stroke="{INK}" stroke-width="1.6"'

ART = {
    # ---- 페르시아·바벨론 ----
    "cylinder": _svg(f'<ellipse cx="22" cy="40" rx="9" ry="20" fill="{SAND}" {S}/><rect x="22" y="20" width="74" height="40" fill="{SAND}" stroke="none"/>'
                     f'<path d="M22 20H96M22 60H96" {S}/><ellipse cx="96" cy="40" rx="9" ry="20" fill="#d6c08f" {S}/>'
                     + "".join(f'<path d="M{30+i*8} {27+(i%3)*2}l3 3m-3 6l3 3m-3 6l3 3m-3 6l3 3" stroke="{INK}" stroke-width="1"/>' for i in range(8)),
                     "고레스 원통 (BC 539)"),
    "tablet": _svg(f'<rect x="34" y="12" width="52" height="62" rx="8" fill="{SAND}" {S}/>'
                   + "".join(f'<path d="M{42+(j%4)*10} {22+(j//4)*9}l4 2-4 2" fill="none" stroke="{INK}" stroke-width="1.2"/>' for j in range(24)),
                   "쐐기문자 토판"),
    "crown": _svg(f'<path d="M30 62L26 28L44 44L60 20L76 44L94 28L90 62Z" fill="{GOLD}" {S}/><rect x="28" y="62" width="64" height="10" rx="2" fill="{GOLD}" {S}/>'
                  f'<circle cx="60" cy="52" r="4" fill="{RED}" {S}/><circle cx="42" cy="56" r="3" fill="{BLUE}" {S}/><circle cx="78" cy="56" r="3" fill="{BLUE}" {S}/>', "페르시아 왕"),
    "column": _svg(f'<path d="M30 20h60v8H30z" fill="{SAND}" {S}/><path d="M34 28c4 8 10 10 14 6M86 28c-4 8-10 10-14 6" fill="none" {S}/>'
                   f'<path d="M30 14c6-8 20-8 22 0M90 14c-6-8-20-8-22 0" fill="none" {S}/><circle cx="36" cy="12" r="5" fill="{SAND}" {S}/><circle cx="84" cy="12" r="5" fill="{SAND}" {S}/>'
                   f'<rect x="50" y="34" width="20" height="40" fill="{SAND}" {S}/><path d="M55 34v40M60 34v40M65 34v40" stroke="{INK}" stroke-width=".8"/><rect x="44" y="74" width="32" height="5" fill="{STONE}" {S}/>', "페르시아 궁전 기둥"),
    "decree": _svg(f'<rect x="28" y="16" width="64" height="56" rx="3" fill="#fbf6ea" {S}/>'
                   + "".join(f'<path d="M36 {26+i*7}h{48 - (i%3)*8}" stroke="{STONE}" stroke-width="2"/>' for i in range(6))
                   + f'<circle cx="80" cy="64" r="9" fill="{RED}" {S}/><path d="M76 64l3 3 5-6" fill="none" stroke="#fff" stroke-width="1.6"/>', "왕의 조서 · 인장"),
    "archive": _svg(f'<rect x="18" y="20" width="84" height="54" fill="{WOOD}" {S}/>' + "".join(
        f'<rect x="{24+c*26}" y="{26+r*16}" width="20" height="11" fill="{SAND}" {S}/>' for c in range(3) for r in range(3))
        + f'<path d="M64 42l6-5h10l6 5" fill="none" stroke="{RED}" stroke-width="2"/>', "악메다 문서 창고"),
    "letter": _svg(f'<path d="M24 26h72v44H24z" fill="#fbf6ea" {S}/><path d="M24 26l36 26 36-26" fill="none" {S}/>'
                   f'<path d="M30 76l10-6M90 76l-10-6" {S}/><circle cx="60" cy="52" r="5" fill="{RED}" {S}/>', "고소 편지"),
    "dice": _svg(f'<rect x="26" y="34" width="30" height="30" rx="5" fill="#fbf6ea" {S} transform="rotate(-12 41 49)"/><rect x="62" y="28" width="30" height="30" rx="5" fill="#fbf6ea" {S} transform="rotate(10 77 43)"/>'
                 f'<circle cx="35" cy="44" r="2.4" fill="{INK}"/><circle cx="47" cy="54" r="2.4" fill="{INK}"/><circle cx="41" cy="49" r="2.4" fill="{INK}"/>'
                 f'<circle cx="72" cy="36" r="2.4" fill="{RED}"/><circle cx="82" cy="50" r="2.4" fill="{RED}"/>', "부르(제비)"),
    "scepter": _svg(f'<path d="M24 76L84 22" stroke="{GOLD}" stroke-width="5"/><circle cx="87" cy="19" r="8" fill="{GOLD}" {S}/>'
                    f'<path d="M80 14l7-8 7 8" fill="none" stroke="{GOLD}" stroke-width="2"/><path d="M18 78h44" {S}/>', "금 홀 (에 5:2)"),
    "cup": _svg(f'<path d="M38 18h44c0 22-10 34-22 34S38 40 38 18z" fill="{GOLD}" {S}/><rect x="57" y="52" width="6" height="14" fill="{GOLD}" {S}/>'
                f'<path d="M44 66h32l-4 8H48z" fill="{GOLD}" {S}/><path d="M44 24h32" stroke="{RED}" stroke-width="3"/>', "왕의 술잔 (느 2:1)"),
    # ---- 길·여행 ----
    "caravan": _svg(f'<path d="M4 70h112" stroke="{SAND}" stroke-width="6"/>'
                    + "".join(f'<g transform="translate({x} 0)"><path d="M0 60c0-10 6-16 12-14 3-8 10-8 13 0 4-2 8 2 8 6l6-10 4 2-6 14v8M6 60v10M14 60v10M26 60v10M32 60v10" fill="{SAND}" {S}/></g>' for x in (8, 46))
                    + f'<g transform="translate(84 0)"><circle cx="8" cy="40" r="4" fill="{SAND}" {S}/><path d="M8 44v14M8 58l-5 12M8 58l5 12M8 48l-6 6M8 48l7 2l6-8" fill="none" {S}/></g>', "귀환 행렬"),
    "river_camp": _svg(f'<path d="M0 66c20-8 40 8 60 0s40-8 60 0v24H0z" fill="{BLUE}" opacity=".6"/>'
                       + "".join(f'<path d="M{x} 56l12-22 12 22z" fill="{SAND}" {S}/><path d="M{x+12} 34v22" {S}/>' for x in (12, 44, 76))
                       + f'<path d="M100 20a6 6 0 1 0 0.1 0" fill="none" stroke="{GOLD}" stroke-width="2"/>', "아하와 강가의 진"),
    "fasting": _svg(f'<circle cx="60" cy="26" r="9" fill="{SAND}" {S}/><path d="M42 74c0-26 8-38 18-38s18 12 18 38z" fill="{STONE}" {S}/>'
                    f'<path d="M54 50l6-10 6 10" fill="none" {S}/><path d="M24 76h72" {S}/><path d="M90 26c-4 4-4 8 0 12" fill="none" stroke="{BLUE}" stroke-width="1.4"/>', "금식하며 간구"),
    "scale": _svg(f'<path d="M60 14v56M40 74h40M30 26h60" {S}/><path d="M30 26l-12 22h24zM90 26l-12 22h24z" fill="none" {S}/>'
                  f'<path d="M18 48a12 6 0 0 0 24 0z" fill="{GOLD}" {S}/><path d="M78 48a12 6 0 0 0 24 0z" fill="#d9d9d9" {S}/>', "은과 금을 달아 넘김"),
    "horsemen": _svg(f'<path d="M20 66c0-14 10-22 26-22h18l10-10 6 4-6 10v18M30 66v12M60 66v12M46 44c0-8 4-14 10-14" fill="{WOOD}" {S}/>'
                     f'<circle cx="54" cy="22" r="5" fill="{SAND}" {S}/><path d="M54 27v12" {S}/><path d="M66 10v34" stroke="{INK}" stroke-width="1.6"/><path d="M66 10l8 4-8 4" fill="{RED}"/>', "군대 장관과 마병 (느 2:9)"),
    "cedar": _svg(f'<path d="M40 70V58M40 14l-18 20h10l-14 16h12l-12 12h44l-12-12h12L58 34h10z" fill="{GREEN}" {S}/>'
                  f'<path d="M64 74h48l-6 8H70z" fill="{WOOD}" {S}/><path d="M66 70h44" stroke="{WOOD}" stroke-width="4"/><path d="M0 82c20-4 40 4 60 0s40-4 60 0" fill="none" stroke="{BLUE}" stroke-width="2"/>', "백향목 · 욥바 바다"),
    # ---- 성전·예배 ----
    "vessels": _svg(f'<path d="M14 40h28l-4 22H18z" fill="{GOLD}" {S}/><path d="M50 30c0-6 20-6 20 0l-4 32H54z" fill="{GOLD}" {S}/>'
                    f'<path d="M78 46h28c0 12-6 18-14 18s-14-6-14-18z" fill="#d9d9d9" {S}/><path d="M56 30v-6h8v6" {S}/>', "돌아온 성전 그릇 5,400"),
    "altar": _svg(f'<rect x="32" y="42" width="56" height="32" fill="{STONE}" {S}/><path d="M32 42l-4-6h8zM88 42l4-6h-8z" fill="{STONE}" {S}/>'
                  f'<path d="M46 42c0-10 6-12 6-20 4 6 8 8 6 20M60 42c0-8 6-12 8-18 3 8 4 12 2 18" fill="{RED}" {S}/>'
                  + "".join(f'<path d="M32 {50+i*8}h56" stroke="{INK}" stroke-width=".8"/>' for i in range(3)), "다시 쌓은 제단"),
    "foundation": _svg(f'<path d="M10 70h100" {S}/>' + "".join(f'<rect x="{14+i*24}" y="54" width="22" height="16" fill="{STONE}" {S}/>' for i in range(4))
                       + f'<rect x="38" y="38" width="22" height="16" fill="{SAND}" {S}/><path d="M20 30q4-12 10 0M84 22q6-14 12 0" fill="none" stroke="{BLUE}" stroke-width="1.6"/>'
                       f'<path d="M86 30l2 4M94 30l-2 4" stroke="{BLUE}"/><text x="18" y="24" font-size="9" fill="{INK}">♪</text>', "기초석 · 함성과 통곡"),
    "temple": _svg(f'<path d="M22 74V36h76v38" fill="{SAND}" {S}/><path d="M16 36l44-20 44 20z" fill="{STONE}" {S}/>'
                   f'<rect x="50" y="48" width="20" height="26" fill="{WOOD}" {S}/><path d="M30 44v30M90 44v30" {S}/><path d="M12 74h96" {S}/>', "제2성전"),
    "tools": _svg(f'<path d="M30 74L66 28" stroke="{WOOD}" stroke-width="5"/><path d="M60 22l14 10-6 6-14-10z" fill="{STONE}" {S}/>'
                  f'<path d="M90 74L70 30" stroke="{INK}" stroke-width="3"/><path d="M66 20l8 14" stroke="#cfcfcf" stroke-width="5"/>', "한 손엔 연장, 한 손엔 병기"),
    "wall": _svg("".join(f'<rect x="{6+(i%5)*22 + (11 if (i//5)%2 else 0)}" y="{66-(i//5)*12}" width="22" height="12" fill="{STONE}" {S}/>' for i in range(20) if 6+(i%5)*22 + (11 if (i//5)%2 else 0) < 104)
                 + f'<path d="M6 30h12v-6h8v6h12v-6h8v6h12v-6h8v6h12v-6h8v6h12" fill="none" {S}/>', "다시 선 성벽"),
    "broken_wall": _svg(f'<path d="M6 78h108" {S}/><path d="M10 78V44h18v-8h10v14h8v28zM70 78V50h14v-10h12v18h12v20z" fill="{STONE}" {S}/>'
                        f'<path d="M46 78l6-10 8 4 6-8 4 14z" fill="{STONE}" {S}/><path d="M28 30c4-6 2-10 6-14 2 6 6 8 4 14M86 28c2-6 4-8 2-14 6 4 8 8 4 14" fill="none" stroke="{RED}" stroke-width="1.6"/>', "무너진 성벽 · 불탄 문"),
    "gate": _svg(f'<rect x="14" y="20" width="92" height="58" fill="{STONE}" {S}/><path d="M42 78V44a18 18 0 0 1 36 0v34" fill="{WOOD}" {S}/>'
                 f'<path d="M60 26v18M14 20h92M14 14h12v6M40 14h12v6M68 14h12v6M94 14h12v6" fill="none" {S}/><circle cx="66" cy="62" r="2" fill="{INK}"/>', "성문"),
    "night_ride": _svg(f'<rect width="120" height="90" fill="#26304a"/><circle cx="96" cy="18" r="9" fill="#f2e6a6"/><path d="M0 70h120v20H0z" fill="#3d3a33"/>'
                       f'<path d="M20 70V52h12v-6h8v24zM84 70V56h12v14z" fill="#5d574b"/>'
                       f'<path d="M48 68c0-8 6-12 14-12h8l6-6 4 3-4 7v8M54 68v8M70 68v8" fill="#8a7a62" stroke="#ddd" stroke-width="1"/><circle cx="62" cy="44" r="4" fill="#ddd"/><path d="M62 48v8" stroke="#ddd"/>', "밤의 성벽 순찰"),
    "pulpit": _svg(f'<path d="M20 76h80" {S}/><rect x="30" y="50" width="60" height="26" fill="{WOOD}" {S}/><path d="M30 58h60M30 66h60" stroke="{INK}" stroke-width=".8"/>'
                   f'<circle cx="60" cy="24" r="6" fill="{SAND}" {S}/><path d="M60 30v20" {S}/><path d="M44 40h32v-6H44z" fill="#fbf6ea" {S}/><path d="M44 37a3 3 0 0 0 0 6M76 37a3 3 0 0 1 0 6" fill="none" {S}/>'
                   f'<path d="M14 18l6 4M106 18l-6 4M60 8v6" stroke="{GOLD}" stroke-width="1.6"/>', "나무 강단 (느 8:4)"),
    "scroll": _svg(f'<rect x="30" y="20" width="60" height="50" fill="#fbf6ea" {S}/><rect x="22" y="14" width="10" height="62" rx="5" fill="{WOOD}" {S}/><rect x="88" y="14" width="10" height="62" rx="5" fill="{WOOD}" {S}/>'
                   + "".join(f'<path d="M38 {28+i*7}h44" stroke="{STONE}" stroke-width="2"/>' for i in range(6)), "율법책 두루마리"),
    "booth": _svg(f'<path d="M18 78V40h84v38" fill="none" {S}/><path d="M12 40c10-8 20 4 30-4s20 6 30-2 20 4 36 2" fill="none" stroke="{GREEN}" stroke-width="5"/>'
                  f'<path d="M24 36l4-10M50 34l2-10M76 34l4-10M96 36l2-10" stroke="{GREEN}" stroke-width="3"/><circle cx="46" cy="62" r="5" fill="{SAND}" {S}/><circle cx="70" cy="62" r="5" fill="{SAND}" {S}/><path d="M46 67v11M70 67v11" {S}/>', "초막절"),
    "choirs": _svg(f'<path d="M6 60h108" stroke="{STONE}" stroke-width="10"/>'
                   + "".join(f'<circle cx="{x}" cy="44" r="4" fill="{SAND}" {S}/><path d="M{x} 48v6" {S}/>' for x in (14, 26, 38, 82, 94, 106))
                   + f'<path d="M40 36l14-6v10zM80 36l-14-6v10z" fill="{GOLD}" {S}/><path d="M48 22l6 6-6 6M72 22l-6 6 6 6" fill="none" stroke="{RED}" stroke-width="2"/>', "두 찬양대 · 성벽 봉헌"),
    "covenant": _svg(f'<rect x="26" y="14" width="68" height="60" fill="#fbf6ea" {S}/>' + "".join(f'<path d="M34 {24+i*8}h{40 + (i%2)*12}" stroke="{STONE}" stroke-width="2"/>' for i in range(5))
                     + "".join(f'<circle cx="{40+i*14}" cy="66" r="5" fill="{RED}" {S}/>' for i in range(4)), "인봉한 언약 (느 9:38)"),
    "tears": _svg(f'<circle cx="60" cy="36" r="20" fill="{SAND}" {S}/><path d="M50 32h6M64 32h6M52 48q8-6 16 0" fill="none" {S}/>'
                  f'<path d="M52 38c-2 6-2 8 0 10 2-2 2-4 0-10zM68 38c-2 6-2 8 0 10 2-2 2-4 0-10z" fill="{BLUE}"/><path d="M30 78c10-14 50-14 60 0" fill="{STONE}" {S}/>', "말씀 앞의 눈물"),
    "joy": _svg(f'<circle cx="60" cy="36" r="20" fill="{SAND}" {S}/><path d="M50 30q3-4 6 0M64 30q3-4 6 0M48 42q12 12 24 0" fill="none" {S}/>'
                f'<path d="M30 78c10-14 50-14 60 0" fill="{GOLD}" {S}/><path d="M18 18l4 4M100 18l-4 4M14 40h6M100 40h6" stroke="{GOLD}" stroke-width="2"/>', "여호와로 인한 기쁨"),
    # ---- 선지자·말씀 ----
    "hand": _svg(f'<path d="M44 80V44c0-4 6-4 6 0v-22c0-4 6-4 6 0v18-24c0-4 6-4 6 0v24-20c0-4 6-4 6 0v26-12c0-4 6-4 6 0v22c0 14-8 24-20 24z" fill="{GOLD}" {S}/>'
                 f'<path d="M20 30l8 4M100 30l-8 4M24 54h8M88 54h8M60 6v6" stroke="{GOLD}" stroke-width="2"/>', "하나님의 선한 손"),
    "lamb": _svg(f'<ellipse cx="60" cy="46" rx="26" ry="16" fill="#fff" {S}/><circle cx="88" cy="38" r="8" fill="#fff" {S}/><path d="M86 36h.1" stroke="{INK}" stroke-width="2.4"/>'
                 f'<path d="M42 60v14M54 60v14M68 60v10l6 4M78 58v16" {S}/><path d="M64 70l10 4" stroke="{RED}" stroke-width="2"/><text x="20" y="28" font-size="14" fill="{RED}">?!</text>', "다리 저는 제물 (말 1:8)"),
    "book_remember": _svg(f'<path d="M60 24c-10-6-26-6-36 0v48c10-6 26-6 36 0 10-6 26-6 36 0V24c-10-6-26-6-36 0z" fill="#fbf6ea" {S}/><path d="M60 24v48" {S}/>'
                          + "".join(f'<path d="M30 {34+i*8}h22M68 {34+i*8}h22" stroke="{STONE}" stroke-width="1.6"/>' for i in range(4))
                          + f'<path d="M76 12l2 6 6 0-5 4 2 6-5-4-5 4 2-6-5-4h6z" fill="{GOLD}"/>', "기념책 (말 3:16)"),
    "sun_wings": _svg(f'<circle cx="60" cy="40" r="14" fill="{GOLD}" {S}/><path d="M46 40c-14-10-28-8-40-2 10 0 16 4 22 8-6 0-12 2-16 6 12-2 22-4 34-6M74 40c14-10 28-8 40-2-10 0-16 4-22 8 6 0 12 2 16 6-12-2-22-4-34-6" fill="{SAND}" {S}/>'
                      f'<path d="M60 18v-8M60 62v8M44 26l-4-4M76 26l4-4" stroke="{GOLD}" stroke-width="2"/>', "치료하는 광선 (말 4:2)"),
    "eyes_lamp": _svg(f'<rect x="54" y="30" width="12" height="44" fill="{GOLD}" {S}/><path d="M30 30h60" {S}/>'
                      + "".join(f'<path d="M{36+i*12} 30c0-8 4-10 4-14 2 4 4 6 2 14" fill="{RED}" stroke="none"/>' for i in range(5))
                      + f'<circle cx="18" cy="40" r="8" fill="{GREEN}" {S}/><circle cx="102" cy="40" r="8" fill="{GREEN}" {S}/><path d="M40 74h40" {S}/>', "금 등잔대와 두 감람나무 (슥 4)"),
    "prayer_window": _svg(f'<rect x="14" y="10" width="92" height="70" fill="{SAND}" {S}/><rect x="56" y="18" width="40" height="40" fill="#bfe0f5" {S}/><path d="M76 18v40M56 38h40" {S}/>'
                          f'<circle cx="36" cy="44" r="6" fill="#fff" {S}/><path d="M28 78c0-16 4-26 8-26s8 10 8 26z" fill="{STONE}" {S}/><path d="M40 48l10-4" {S}/>', "예루살렘 쪽 창문 (단 6:10)"),
    "dry_seed": _svg(f'<path d="M0 70h120v20H0z" fill="{WOOD}"/><path d="M20 70c0-10 4-16 8-20M28 50c4 0 8-4 8-8-6 0-8 4-8 8z" fill="{GREEN}" {S}/>'
                     f'<path d="M80 70v-24M80 52c-6 0-10-4-10-10 6 0 10 4 10 10zM80 46c6 0 10-4 10-10-6 0-10 4-10 10z" fill="{GREEN}" {S}/><path d="M50 20c-2 4-2 6 0 8 2-2 2-4 0-8z" fill="{BLUE}"/>', "눈물로 뿌린 씨 (시 126)"),
    # ---- 역사 자료 ----
    "papyrus": _svg(f'<path d="M26 16h68v58H26z" fill="#e9d9a8" {S}/>' + "".join(f'<path d="M26 {20+i*6}h68" stroke="#d2bf86" stroke-width="1"/>' for i in range(9))
                    + "".join(f'<path d="M34 {26+i*8}h{40+(i%2)*10}" stroke="{INK}" stroke-width="1.4" stroke-dasharray="3 2"/>' for i in range(5)), "파피루스 문서"),
    "silver_bowl": _svg(f'<path d="M16 40h88c0 20-20 30-44 30S16 60 16 40z" fill="#d9d9d9" {S}/><ellipse cx="60" cy="40" rx="44" ry="8" fill="#eeeeee" {S}/>'
                        f'<path d="M30 54h60" stroke="{INK}" stroke-width="1" stroke-dasharray="2 3"/>', "은그릇 비문"),
    "greek": _svg(f'<path d="M14 34l46-20 46 20z" fill="#eeeeee" {S}/><rect x="14" y="34" width="92" height="6" fill="#eeeeee" {S}/>'
                  + "".join(f'<rect x="{20+i*14}" y="40" width="8" height="32" fill="#f7f7f7" {S}/>' for i in range(6)) + f'<rect x="10" y="72" width="100" height="6" fill="#eeeeee" {S}/>', "아테네 (같은 시대 세계)"),
    "ship_war": _svg(f'<path d="M10 58h100l-14 14H22z" fill="{WOOD}" {S}/><path d="M60 58V16" {S}/><path d="M60 18l30 14-30 14z" fill="#f7f7f7" {S}/>'
                     + "".join(f'<path d="M{24+i*10} 62l-4 14" stroke="{INK}" stroke-width="1.2"/>' for i in range(8)) + f'<path d="M0 80c20-4 40 4 60 0s40-4 60 0" fill="none" stroke="{BLUE}" stroke-width="2"/>', "그리스와의 전쟁"),
    "inscription": _svg(f'<path d="M14 80V30l46-18 46 18v50z" fill="{STONE}" {S}/><rect x="30" y="40" width="60" height="32" fill="{SAND}" {S}/>'
                        + "".join(f'<path d="M36 {46+i*6}h48" stroke="{INK}" stroke-width="1" stroke-dasharray="2 2"/>' for i in range(5))
                        + f'<circle cx="60" cy="26" r="5" fill="{GOLD}" {S}/>', "바위 비문"),
    "statue": _svg(f'<rect x="40" y="70" width="40" height="10" fill="{STONE}" {S}/><path d="M46 70V36c0-8 28-8 28 0v34z" fill="#7c8a6b" {S}/><circle cx="60" cy="24" r="9" fill="#7c8a6b" {S}/>'
                   + "".join(f'<path d="M50 {44+i*6}h20" stroke="{INK}" stroke-width=".8" stroke-dasharray="2 2"/>' for i in range(4)) + f'<rect x="54" y="40" width="12" height="16" fill="{GOLD}" {S}/>', "우자호르레스넷 상"),
}
