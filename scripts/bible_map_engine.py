# -*- coding: utf-8 -*-
"""성경 지도 연표 공용 엔진 — 사건 목록 → KML(구글 내 지도/Google Earth) + HTML(Leaflet 슬라이드쇼).

event dict 키:
  k      정렬·재생 단계 키(숫자). 같은 k = 같은 시기의 여러 갈래(화살표 여러 개)
  lab    지도에 표시할 번호 문자열
  cat    범례 분류 키 (cats 의 키)
  date, title, note(성경 구절), desc(상세 설명)
  where  장소명 또는 [출발, 경유..., 도착]
  folder (선택) KML 폴더 이름
"""
import math, os, json, html


def kml_color(hexcol, alpha="ff"):
    h = hexcol.lstrip("#")
    return alpha + h[4:6] + h[2:4] + h[0:2]


def curve(a, b, bend):
    (y1, x1), (y2, x2) = a, b
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
    dx, dy = x2 - x1, y2 - y1
    cx, cy = mx - dy * bend, my + dx * bend
    pts = []
    for i in range(21):
        t = i / 20
        x = (1 - t) ** 2 * x1 + 2 * (1 - t) * t * cx + t ** 2 * x2
        y = (1 - t) ** 2 * y1 + 2 * (1 - t) * t * cy + t ** 2 * y2
        pts.append((y, x))
    return pts


def arrowhead(p_prev, p_end, size):
    (y1, x1), (y2, x2) = p_prev, p_end
    ang = math.atan2(y2 - y1, (x2 - x1) * math.cos(math.radians(y2)))
    k = 1 / math.cos(math.radians(y2))
    pts = [p_end]
    for d in (152, -152):
        a = ang + math.radians(d)
        pts.append((y2 + size * math.sin(a), x2 + size * math.cos(a) * k))
    pts.append(p_end)
    return pts


def esc(t):
    return html.escape(str(t), quote=False)


def build_map(events, P, P_NOTE, cats, title, out_dir, basename,
              default_off=(), bounds=((27.5, 29), (37.5, 49)), kml_desc=""):
    color = {c[0]: c[2] for c in cats}
    missing = {w for e in events for w in (e["where"] if isinstance(e["where"], list) else [e["where"]]) if w not in P}
    assert not missing, missing
    missing = [p for p in P if p not in P_NOTE]
    assert not missing, missing

    visits, markers, paths = {}, [], []
    for idx, e in enumerate(events):
        route = e["where"] if isinstance(e["where"], list) else [e["where"]]
        end = route[-1]
        n = visits.get(end, 0); visits[end] = n + 1
        r = 0.018 * math.sqrt(n); th = n * 2.4
        col = color[e["cat"]]
        m = dict(n=e["k"], lab=e["lab"], cat=e["cat"], date=e["date"], title=e["title"], note=e["note"],
                 desc=e["desc"], place=end, pnote=P_NOTE[end], col=col,
                 route=" → ".join(route) if len(route) > 1 else "",
                 lat=P[end][0] + r * math.sin(th), lon=P[end][1] + r * math.cos(th),
                 folder=e.get("folder", ""))
        markers.append(m)
        if len(route) > 1:
            pts = []
            bend = 0.12 if idx % 2 == 0 else -0.12
            for a, b in zip(route[:-1], route[1:]):
                seg = curve(P[a], P[b], bend)
                pts += seg if not pts else seg[1:]
            seglen = math.hypot(P[route[-1]][0] - P[route[-2]][0], P[route[-1]][1] - P[route[-2]][1])
            head = arrowhead(pts[-3], pts[-1], max(0.012, min(0.06, seglen * 0.02)))
            paths.append(dict(n=e["k"], lab=e["lab"], cat=e["cat"], title=e["title"], col=col,
                              pts=pts, head=head, route=m["route"], folder=m["folder"]))

    # ---------------- KML ----------------
    k = ['<?xml version="1.0" encoding="UTF-8"?>',
         '<kml xmlns="http://www.opengis.net/kml/2.2"><Document>',
         f'<name>{esc(title)}</name>', f'<description>{esc(kml_desc)}</description>']
    for col in sorted(set(m["col"] for m in markers)):
        sid = col.lstrip("#")
        k.append(f'<Style id="p{sid}"><IconStyle><color>{kml_color(col)}</color><scale>0.9</scale>'
                 f'<Icon><href>http://maps.google.com/mapfiles/kml/shapes/placemark_circle.png</href></Icon></IconStyle>'
                 f'<LabelStyle><scale>0.8</scale></LabelStyle></Style>')
        k.append(f'<Style id="l{sid}"><LineStyle><color>{kml_color(col, "e6")}</color><width>3</width></LineStyle>'
                 f'<PolyStyle><color>{kml_color(col)}</color><fill>1</fill><outline>0</outline></PolyStyle></Style>')
    folders = []
    for m in markers:
        if m["folder"] not in folders:
            folders.append(m["folder"])
    for fd in folders:
        k.append(f"<Folder><name>{esc(fd or title)}</name>")
        for m in (x for x in markers if x["folder"] == fd):
            k.append(f'<Placemark><name>{esc(m["lab"])}. {esc(m["title"])}</name>'
                     f'<description>{esc(m["date"])} · {esc(m["desc"])} ({esc(m["note"])}) / 📍 {esc(m["place"])}: {esc(m["pnote"])}</description>'
                     f'<styleUrl>#p{m["col"].lstrip("#")}</styleUrl><Point><coordinates>{m["lon"]:.5f},{m["lat"]:.5f},0</coordinates></Point></Placemark>')
        for p in (x for x in paths if x["folder"] == fd):
            coords = " ".join(f"{x:.5f},{y:.5f},0" for y, x in p["pts"])
            hc = " ".join(f"{x:.5f},{y:.5f},0" for y, x in p["head"])
            k.append(f'<Placemark><name>{esc(p["lab"])} → {esc(p["route"])}</name><description>{esc(p["title"])}</description>'
                     f'<styleUrl>#l{p["col"].lstrip("#")}</styleUrl><MultiGeometry>'
                     f'<LineString><tessellate>1</tessellate><coordinates>{coords}</coordinates></LineString>'
                     f'<Polygon><outerBoundaryIs><LinearRing><coordinates>{hc}</coordinates></LinearRing></outerBoundaryIs></Polygon>'
                     f'</MultiGeometry></Placemark>')
        k.append("</Folder>")
    k.append("</Document></kml>")
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, basename + ".kml"), "w", encoding="utf-8") as f:
        f.write("\n".join(k))

    # ---------------- HTML ----------------
    ks = sorted(set(m["n"] for m in markers))
    kmin, kmax = int(math.floor(ks[0])), int(math.ceil(ks[-1]))
    data = dict(markers=markers, paths=[{x: p[x] for x in ("n", "lab", "cat", "title", "col", "pts", "route")} for p in paths])
    page = (PAGE.replace("__TITLE__", esc(title))
                .replace("__KMIN__", str(kmin)).replace("__KMAX__", str(kmax))
                .replace("__CATS__", json.dumps([list(c) for c in cats], ensure_ascii=False))
                .replace("__OFF__", json.dumps(list(default_off), ensure_ascii=False))
                .replace("__BOUNDS__", json.dumps([list(bounds[0]), list(bounds[1])]))
                .replace("__DATA__", json.dumps(data, ensure_ascii=False)))
    with open(os.path.join(out_dir, basename + "_미리보기.html"), "w", encoding="utf-8") as f:
        f.write(page)
    return dict(markers=len(markers), paths=len(paths), steps=len(ks))


PAGE = r"""<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>__TITLE__</title>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.css">
<script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.js"></script>
<style>
html,body{margin:0;height:100%;background:#141414;font-family:'Malgun Gothic',sans-serif}
#map{position:absolute;inset:0 0 0 320px}
#side{position:absolute;left:0;top:0;bottom:0;width:320px;display:flex;flex-direction:column;background:#1b1b1b;color:#ddd;font-size:12px}
#side h1{font-size:14px;margin:10px 10px 6px;color:#fff}
#lg{padding:0 8px 6px;display:flex;flex-wrap:wrap;gap:4px}
#lg .c{display:inline-flex;align-items:center;gap:5px;padding:3px 8px;border:1px solid #333;border-radius:12px;cursor:pointer;user-select:none;background:#222}
#lg .c i{width:10px;height:10px;border-radius:50%;display:inline-block}
#lg .c.off{opacity:.35;text-decoration:line-through}
#ctl{padding:8px 10px;border-top:1px solid #2a2a2a;border-bottom:1px solid #2a2a2a;background:#202020}
#ctl label{display:inline-block;margin-right:6px;color:#aaa}
#ctl input{width:52px;background:#111;color:#fff;border:1px solid #444;border-radius:4px;padding:2px 4px}
#ctl input#iv{width:62px}
#ctl .btns{margin-top:6px;display:flex;gap:6px}
#ctl button{flex:1;padding:5px 0;border:0;border-radius:5px;font-weight:700;cursor:pointer;color:#111}
#bPlay{background:#5CC98A}#bPause{background:#F2C14E}#bStop{background:#FF6B6B}#bPrev,#bNext{background:#9CC7F0}
#st{margin-top:5px;color:#aaa;font-size:11px}
#list{flex:1;overflow:auto}
#list .it{padding:4px 10px;border-bottom:1px solid #2a2a2a;cursor:pointer}
#list .it:hover{background:#2a2a2a}
#list .it.act{background:#3a2f12;color:#fff}
#list .it.hid{display:none}
.num{display:flex;align-items:center;justify-content:center;border-radius:11px;color:#111;font-weight:700;font-size:11px;border:1px solid #111;min-width:22px;height:22px;padding:0 3px;box-sizing:border-box;white-space:nowrap}
.num.cur{animation:pulse 1s ease-out infinite;transform-origin:center;box-shadow:0 0 0 0 rgba(255,255,255,.8)}
@keyframes pulse{0%{transform:scale(1.9);box-shadow:0 0 0 0 rgba(255,255,255,.9)}70%{transform:scale(1.5);box-shadow:0 0 0 14px rgba(255,255,255,0)}100%{transform:scale(1.5)}}
#cap{position:absolute;left:calc(320px + 50% - 160px);transform:translateX(-50%);bottom:28px;z-index:1000;min-width:420px;max-width:720px;
 background:rgba(15,15,15,.88);color:#fff;border-radius:14px;padding:14px 18px;display:none;box-shadow:0 8px 30px rgba(0,0,0,.5)}
#cap.show{display:flex;gap:14px;align-items:center;animation:rise .5s ease-out}
@keyframes rise{from{opacity:0;transform:translate(-50%,20px)}to{opacity:1;transform:translate(-50%,0)}}
#cap .big{flex:none;min-width:58px;height:58px;padding:0 6px;box-sizing:border-box;border-radius:29px;display:flex;align-items:center;justify-content:center;font-size:22px;font-weight:800;color:#111}
#cap .dt{color:#bbb;font-size:12px}#cap .tt{font-size:17px;font-weight:700;margin:4px 0 2px}#cap .ds{font-size:13.5px;line-height:1.55;color:#eee}#cap .nt{color:#999;font-size:11.5px;margin-top:6px}#cap .body{max-height:42vh;overflow:auto}#cap .pl{color:#9fd3ff;font-size:11.5px;margin-top:6px;line-height:1.5;border-top:1px solid #333;padding-top:6px}
#prog{position:absolute;left:320px;right:0;top:0;height:4px;z-index:1000;background:transparent}
#prog div{height:100%;width:0;background:#F2C14E;transition:width .3s}
@media (max-width:820px){#side{right:0;bottom:auto;width:auto;height:42%}#map{inset:42% 0 0 0}#prog{left:0;top:42%}#cap{left:50%;bottom:12px;min-width:0;width:calc(100% - 24px);padding:10px 12px}#cap .big{min-width:44px;height:44px;font-size:16px}#cap .tt{font-size:14px}#cap .ds{font-size:12.5px}}
</style></head><body>
<div id="side">
 <h1>__TITLE__</h1>
 <div id="lg"></div>
 <div id="ctl">
  <label>시작 <input id="s0" type="number" step="any" min="__KMIN__" max="__KMAX__" value="__KMIN__"></label>
  <label>끝 <input id="s1" type="number" step="any" min="__KMIN__" max="__KMAX__" value="__KMAX__"></label>
  <label>간격 <input id="iv" type="number" min="300" step="100" value="2500">ms</label>
  <label style="display:block;margin-top:6px">카메라 <select id="cam" style="background:#111;color:#fff;border:1px solid #444;border-radius:4px;padding:2px 4px"><option value="auto">자동 줌 (단계마다 확대·축소)</option><option value="cum">누적 범위 (지금까지 전체)</option><option value="fixed">화면 고정 (수동으로 이동)</option></select></label>
  <div class="btns"><button id="bPlay">▶ Play</button><button id="bPause">❚❚ Pause</button><button id="bStop">■ Stop</button></div><div class="btns"><button id="bPrev">◀ Prev</button><button id="bNext">Next ▶</button></div>
  <div id="st">정지 — 전체 보기</div>
 </div>
 <div id="list"></div>
</div>
<div id="map"></div><div id="prog"><div></div></div>
<div id="cap"><div class="big"></div><div class="body"><div class="dt"></div><div class="tx"></div><div class="nt"></div><div class="pl"></div></div></div>
<script>
const D=__DATA__;
const CATS=__CATS__, OFF=__OFF__, KMIN=__KMIN__, KMAX=__KMAX__;
const vis={};CATS.forEach(c=>vis[c[0]]=!OFF.includes(c[0]));
const map=L.map('map',{zoomSnap:0.25,minZoom:3}).setView([32.5,38],5);
const esri=L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}',{maxZoom:12,attribution:'Tiles © Esri'});
const topo=L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer/tile/{z}/{y}/{x}',{maxZoom:12,attribution:'Tiles © Esri'});
const sat=L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',{maxZoom:12,attribution:'Imagery © Esri'});
esri.addTo(map);L.control.layers({'도로 지도 (Esri)':esri,'지형 (Esri)':topo,'위성 (Esri)':sat}).addTo(map);
const items=[];const list=document.getElementById('list');
function arrowMk(p){const a=p.pts[p.pts.length-2],b=p.pts[p.pts.length-1];const A=map.project(a,6),B=map.project(b,6);const deg=Math.atan2(B.y-A.y,B.x-A.x)*180/Math.PI;return L.marker(b,{interactive:false,keyboard:false,icon:L.divIcon({className:'',iconSize:[14,14],iconAnchor:[7,7],html:`<svg width="14" height="14" viewBox="0 0 14 14" style="overflow:visible;transform:rotate(${deg}deg)"><polygon points="7,7 -2,2.5 -2,11.5" fill="${p.col}" stroke="#111" stroke-width=".6"/></svg>`})})}
function icon(m,cur){const w=m.lab.length>2?(m.lab.length>3?42:36):22;return L.divIcon({className:'',html:`<div class="num${cur?' cur':''}" style="background:${m.col}">${m.lab}</div>`,iconSize:[w,22],iconAnchor:[w/2,11]})}
D.paths.forEach(p=>{const g=L.layerGroup([L.polyline(p.pts,{color:p.col,weight:3,opacity:.9}).bindTooltip(p.lab+' → '+p.route),arrowMk(p)]);
  items.push({type:'p',n:p.n,cat:p.cat,layer:g,d:p,ll:p.pts});});
D.markers.forEach(m=>{const mk=L.marker([m.lat,m.lon],{icon:icon(m,false),zIndexOffset:Math.round(m.n*10)}).bindPopup(`<b>${m.lab}. ${m.title}</b><br><small>${m.date}</small><br>${m.desc}<br><small>📍 ${m.place}: ${m.pnote}<br>📖 ${m.note}</small>`,{maxWidth:340});
  const el=document.createElement('div');el.className='it';el.innerHTML=`<b style="color:${m.col}">${m.lab}</b> ${m.date} — ${m.title}`;
  el.onclick=()=>startFrom(m.n);list.appendChild(el);
  items.push({type:'m',n:m.n,cat:m.cat,layer:mk,d:m,ll:[[m.lat,m.lon]],el});});
const lg=document.getElementById('lg');
CATS.forEach(([k,name,col])=>{const b=document.createElement('span');b.className='c'+(vis[k]?'':' off');b.innerHTML=`<i style="background:${col}"></i>${name}`;
  b.onclick=()=>{vis[k]=!vis[k];b.classList.toggle('off',!vis[k]);if(mode==='play'){const keep=cur;seq=numbersInRange();si=Math.max(0,seq.indexOf(keep))+1;}render(false)};lg.appendChild(b);});
let mode='all', cur=0, s0=KMIN, s1=KMAX, timer=null, paused=false, anims=[], token=0, pending=null;
const $=id=>document.getElementById(id);
function shown(it){ if(!vis[it.cat])return false; if(mode==='all')return true; if(pending!==null&&it.n===pending)return false; return it.n>=s0 && it.n<=cur; }
function render(fit){
  items.forEach(it=>{const on=shown(it);if(on&&!map.hasLayer(it.layer))it.layer.addTo(map);if(!on&&map.hasLayer(it.layer))map.removeLayer(it.layer);
    if(it.type==='m'){it.el.classList.toggle('hid',!vis[it.cat]);it.layer.setIcon(icon(it.d,mode!=='all'&&it.n===cur));}});
  if(fit)fitShown();
}
function fitShown(dur){const pts=[];items.forEach(it=>{if(map.hasLayer(it.layer))pts.push(...it.ll)});
  if(!pts.length)return;const b=L.latLngBounds(pts);
  const z=Math.min(8.5,map.getBoundsZoom(b,false,L.point(140,140)));const c=b.getCenter();
  if(map.getCenter().distanceTo(c)<800&&Math.abs(map.getZoom()-z)<0.1)return;
  try{map.flyTo(c,z,{duration:dur||1.0})}catch(e){map.setView(c,z)}}
function stepBounds(n){const pts=[];items.forEach(it=>{if(it.n===n&&vis[it.cat])pts.push(...it.ll)});return pts.length?L.latLngBounds(pts):null}
function camTarget(n,i){const cm=$('cam').value;if(cm==='fixed')return null;let b;
  if(cm==='cum'){const pts=[];items.forEach(it=>{if(vis[it.cat]&&it.n>=s0&&it.n<=n)pts.push(...it.ll)});if(!pts.length)return null;b=L.latLngBounds(pts);}
  else{b=stepBounds(n);if(!b)return null;
    if(i>0){const pb=stepBounds(seq[i-1]);if(pb&&pb.getCenter().distanceTo(b.getCenter())<120000)b=L.latLngBounds([b.getSouthWest(),b.getNorthEast(),pb.getSouthWest(),pb.getNorthEast()]);}}
  const span=b.getNorthEast().distanceTo(b.getSouthWest());
  let z=span<20000?8.5:map.getBoundsZoom(b,false,L.point(170,230));z=Math.max(3.5,Math.min(8.5,z));
  const c=L.latLng(b.getCenter().lat-(span<20000?0:0.06*(b.getNorth()-b.getSouth())),b.getCenter().lng);
  return {c,z,b};}
function moveCam(t,dur){if(!t)return false;const cz=map.getZoom();
  if(map.getCenter().distanceTo(t.c)<800&&Math.abs(cz-t.z)<0.1)return false;
  if($('cam').value==='auto'&&map.getBounds().pad(-0.08).contains(t.b)&&Math.abs(t.z-cz)<0.75)return false;
  try{map.flyTo(t.c,t.z,{duration:dur})}catch(e){map.setView(t.c,t.z);return false}return true;}
function caption(n){const ms=items.filter(it=>it.type==='m'&&it.n===n&&vis[it.cat]).map(it=>it.d);const c=$('cap');
  if(!ms.length){c.classList.remove('show');return}
  const m0=ms[0];c.querySelector('.big').textContent=m0.lab;c.querySelector('.big').style.background=m0.col;
  c.querySelector('.dt').textContent=m0.date+' · '+[...new Set(ms.map(m=>m.place))].join(' / ');
  c.querySelector('.tx').innerHTML=ms.map(m=>`<div class="tt">${m.title}</div><div class="ds">${m.desc}</div>`).join('');
  c.querySelector('.nt').textContent='📖 '+[...new Set(ms.map(m=>m.note))].join(' · ');
  const seen=new Set();c.querySelector('.pl').innerHTML=ms.filter(m=>{const key=m.place+m.route;if(seen.has(key))return false;seen.add(key);return true}).map(m=>`📍 <b>${m.place}</b> — ${m.pnote}`+(m.route?`<br><span style="color:#888">경로: ${m.route}</span>`:'')).join('<br>');
  c.classList.remove('show');void c.offsetWidth;c.classList.add('show');}
function reveal(n,tk,pathMs){if(tk!==token)return;
  const ps=items.filter(it=>it.type==='p'&&it.n===n&&vis[it.cat]);let left=ps.length;
  const finish=()=>{if(tk!==token)return;pending=null;render(false);};
  if(!left){finish();return}
  ps.forEach(it=>{const pl=L.polyline([it.d.pts[0]],{color:it.d.col,weight:5,opacity:1}).addTo(map);anims.push(pl);
    const ms=pathMs*Math.min(1.6,Math.max(0.7,it.d.pts.length/21));const t0=performance.now();
    (function step(t){if(tk!==token){map.removeLayer(pl);return}
      const k=Math.min(1,(t-t0)/ms);const upto=Math.max(1,Math.round(k*(it.d.pts.length-1)));pl.setLatLngs(it.d.pts.slice(0,upto+1));
      if(k<1)requestAnimationFrame(step);else{map.removeLayer(pl);if(--left===0)finish();}})(t0);});}
function numbersInRange(){return [...new Set(items.filter(it=>vis[it.cat]&&it.n>=s0&&it.n<=s1).map(it=>it.n))].sort((a,b)=>a-b)}
let seq=[],si=0;
function LB(n){const m=items.find(it=>it.type==='m'&&it.n===n);return m?m.d.lab:n}
function showAt(i,manual){const n=seq[i];cur=n;si=i+1;const iv=Math.max(300,+$('iv').value||2500);
  const tk=++token;anims.forEach(a=>map.removeLayer(a));anims=[];pending=n;render(false);
  caption(n);
  items.forEach(it=>{if(it.type==='m')it.el.classList.toggle('act',it.n===n)});
  const a=items.find(it=>it.type==='m'&&it.n===n&&vis[it.cat]);if(a)a.el.scrollIntoView({block:'center',behavior:'smooth'});
  $('prog').firstChild.style.width=((i+1)/seq.length*100)+'%';
  $('st').textContent=`${manual?'수동':'재생 중'} — ${LB(n)} (${i+1}/${seq.length})`;
  const camDur=Math.min(1.4,Math.max(0.4,iv/1000*0.3)),pathMs=Math.min(1700,Math.max(250,iv*0.35));
  const moved=moveCam(camTarget(n,i),camDur);let done=false;const go=()=>{if(done)return;done=true;reveal(n,tk,pathMs)};
  if(moved){map.once('moveend',()=>setTimeout(go,120));setTimeout(go,camDur*1000+600)}else go();}
function tick(){if(paused)return;if(si>=seq.length){$('st').textContent=`완료 — ${LB(seq[0])}~${LB(seq[seq.length-1])}`;timer=null;return}
  const iv=Math.max(300,+$('iv').value||2500);showAt(si,false);timer=setTimeout(tick,iv);}
function initSeq(){s0=Math.max(KMIN,Math.min(KMAX,+$('s0').value||KMIN));s1=Math.max(KMIN,Math.min(KMAX,+$('s1').value||KMAX));if(s0>s1)[s0,s1]=[s1,s0];
  mode='play';seq=numbersInRange();si=0;cur=s0-1;}
function manualStep(dir){clearTimeout(timer);timer=null;
  if(mode!=='play'){initSeq();paused=true;if(!seq.length)return;showAt(dir>0?0:seq.length-1,true);return}
  paused=true;const curIdx=si-1;const t=curIdx+dir;
  if(t<0||t>=seq.length){$('st').textContent=`${t<0?'처음':'마지막'} 단계입니다 — ${LB(cur)}`;return}
  showAt(t,true);}
function startFrom(n){clearTimeout(timer);timer=null;$('s0').value=n;if((+$('s1').value||KMAX)<n)$('s1').value=KMAX;
  initSeq();paused=true;if(!seq.length)return;anims.forEach(a=>map.removeLayer(a));anims=[];showAt(0,true);
  $('st').textContent=`${LB(n)}번부터 시작 — Next ▶ 로 이어가기 (1/${seq.length})`;}
$('bNext').onclick=()=>manualStep(1);
$('bPrev').onclick=()=>manualStep(-1);
document.addEventListener('keydown',e=>{if(e.target.tagName==='INPUT')return;
  if(e.key==='ArrowRight'){manualStep(1);e.preventDefault()}else if(e.key==='ArrowLeft'){manualStep(-1);e.preventDefault()}
  else if(e.key===' '){(mode==='play'&&!paused)?$('bPause').click():$('bPlay').click();e.preventDefault()}});
$('bPlay').onclick=()=>{if(mode==='play'&&paused){paused=false;$('st').textContent='재생 재개';tick();return}
  if(mode==='play'&&timer)return;
  initSeq();paused=false;render(false);tick();};
$('bPause').onclick=()=>{if(mode!=='play')return;paused=true;clearTimeout(timer);timer=null;$('st').textContent=`일시정지 — ${LB(cur)}`};
$('bStop').onclick=()=>{clearTimeout(timer);timer=null;paused=false;mode='all';token++;pending=null;anims.forEach(a=>map.removeLayer(a));anims=[];
  $('cap').classList.remove('show');$('prog').firstChild.style.width='0';items.forEach(it=>it.el&&it.el.classList.remove('act'));
  render(true);$('st').textContent='정지 — 전체 보기';};
render(false);map.fitBounds(__BOUNDS__);
</script></body></html>"""
