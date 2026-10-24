#!/usr/bin/env python3
"""Today page (Sat 24.10.2026): Dotonbori walk + where the castle is. Run after build.py."""
import json, html, subprocess
from urllib.parse import quote
from build import gm, gdir, cap, HOTEL, H_LL, HEAD, FOOT, CR, PAGE, CAP
E = html.escape
CR.update({"shinsaibashi-1.jpg": "そらみみ, CC BY-SA 4.0", "shinsaibashi-2.jpg": "そらみみ, CC BY-SA 4.0",
           "amemura-1.jpg": "BradBeattie, CC BY-SA 3.0", "glico-2.jpg": "Martin Falbisoner, CC BY-SA 4.0"})
for k in ["shinsaibashi-1.jpg", "shinsaibashi-2.jpg", "amemura-1.jpg", "glico-2.jpg"]:
    PAGE[k] = "https://commons.wikimedia.org/wiki/Special:Search?search=" + quote(k)
CAP.update({"shinsaibashi-1.jpg": "Крытая улица Shinsaibashi-suji", "shinsaibashi-2.jpg": "Shinsaibashi-suji ведёт прямо к каналу",
            "amemura-1.jpg": "Amerikamura", "glico-2.jpg": "Мост Ebisubashi и Glico"})
NOW = subprocess.run(["date", "+%d.%m.%Y %H:%M JST"], capture_output=True, text=True).stdout.strip()
W = json.load(open("today_walk.json"))
CASTLE = (34.687183, 135.525396); OTEMON = (34.685079, 135.523035)
ST = [(34.7025, 135.4982), (34.6930, 135.5010), (34.6823, 135.5009), (34.6750, 135.5009)]  # Umeda -> Shinsaibashi

S = [
 dict(n=1, ll=(34.6750, 135.5009), name="Shinsaibashi-suji - крытая улица к каналу", q="Shinsaibashi-suji Shopping Street",
      pics=["shinsaibashi-1.jpg", "shinsaibashi-2.jpg"],
      t="Из метро Shinsaibashi выход к крытой улице и ~9 мин пешком на юг (700 м) прямо к мосту через канал. Улица пешеходная, под крышей."),
 dict(n=2, ll=(34.669067, 135.501305), name="Ebisubashi, Glico и набережная канала", q="Ebisubashi Bridge Glico Sign Osaka",
      pics=["osk-8.jpg", "glico-2.jpg", "osk-1.jpg"],
      t="Та самая главная улица вдоль канала Dotonbori: мост, бегущий Glico, вдоль воды пешеходная набережная Tombori River Walk. Отсюда иди по улице Dotonbori на восток."),
 dict(n=3, ll=(34.668181, 135.50267), name="Улица Dotonbori и переулок Hozenji Yokocho", q="Hozenji Yokocho Osaka",
      pics=["osk-6.jpg", "hozenji-1.jpg", "hozenji-2.jpg"],
      t="Улица еды: огромные вывески (краб, осьминог), такояки, кушикацу, рамен. Через 3 мин на юг - тихий каменный переулок Hozenji Yokocho и статуя во мху (храм открыт круглосуточно)."),
 dict(n=4, ll=(34.66371, 135.506932), name="Рынок Kuromon", q="Kuromon Market Osaka",
      pics=["kuromon-1.jpg", "kuromon-2.jpg"],
      t="12 мин на восток. Крытый рынок ~580 м: морепродукты на гриле, вагю на шпажках. Лавки к вечеру закрываются, поэтому до ~17:00. Цены туристические."),
 dict(n=5, ll=(34.661482, 135.496733), name="Namba Yasaka - голова льва", q="Namba Yasaka Shrine",
      pics=["yasaka-1.jpg", "yasaka-2.jpg"],
      t="16 мин на юго-запад. Сцена в виде головы льва высотой 12 м. Ворота открыты до 17:00 (osaka-info), поэтому до пяти. Оттуда 16 мин обратно к каналу - как раз к закату (17:13) и включению неона."),
]
A = dict(ll=(34.6725, 135.4985), name="Amerikamura (по желанию)", q="Amerikamura Osaka Triangle Park",
         pics=["amemura-1.jpg"], t="Молодёжный квартал к западу от Shinsaibashi-suji, 5 мин в сторону: уличная мода, кафе, треугольная площадь.")

def pics(fs):
    return "".join(f'<figure><img src="t/{f}" data-full="img/{f}" alt="{E(CAP.get(f, ""))}" loading="lazy"><figcaption>{cap(f)}</figcaption></figure>' for f in fs)

stops = ""
for s in S + [A]:
    num = f'<span class="pin">{s["n"]}</span>' if "n" in s else '<span class="pin g">A</span>'
    stops += f'''<div class="card"><div class="top">{num}<h2>{E(s["name"])}</h2></div><div class="pics">{pics(s["pics"])}</div><p>{E(s["t"])}</p>
<div class="btns"><a class="btn" href="{gm(s["q"])}" target="_blank" rel="noopener">📍 Google Maps</a></div></div>'''

walk_all = gdir("Namba Yasaka Shrine", "walking", "Shinsaibashi Station Osaka Metro") + "&waypoints=" + quote("Ebisubashi Bridge Osaka|Hozenji Yokocho Osaka|Kuromon Market Osaka")
body = f'''<a class="back" href="index.html">← ко всем местам Осаки</a>
<header><h1>Сегодня: Dotonbori и центр Minami</h1><div class="sub">Сб 24.10 · выход ~14:15 · срез {NOW}</div></header>
<div class="alert"><b>Погода:</b> после обеда облачно, дождь маловероятен - 30% днём, 20% вечером (метеоагентство JMA, 11:00); модель JMA MSM до ночи 0 мм, 21-24°. Закат 17:13. Завтра с обеда дождь - сегодня лучший вечер для улицы.</div>
<div class="vsw" id="sw"><button data-k="walk" class="on">Прогулка</button><button data-k="castle">Где замок</button><button data-k="all">Всё с отелем</button></div>
<div id="map"></div>
<div class="legend">H - отель. Красный пунктир - метро Midosuji. Синяя линия - пешком по порядку 1→5→2. Серый пунктир - расстояние до замка.</div>

<h3>Дорога туда</h3>
<div class="card"><p><b>14:16</b> от отеля ~5 мин до станции <b>Umeda</b>, линия <b>Midosuji (красная)</b>, платформа 1, поезд на <b>Tennoji</b>. Остановки: Yodoyabashi → Hommachi → <b>Shinsaibashi</b> (14:23, 7 мин). Поезда каждые несколько минут, следующий тоже подойдёт. Выход к Shinsaibashi-suji.</p>
<div class="btns"><a class="btn" href="{gm("Umeda Station Osaka Metro Midosuji Line")}" target="_blank" rel="noopener">📍 Umeda (Midosuji)</a><a class="btn o" href="{gdir("Shinsaibashi Station Osaka Metro")}" target="_blank" rel="noopener">🚇 Маршрут от отеля</a></div></div>

<h3>Прогулка: ~3,8 км, ~55 мин чистой ходьбы</h3>
<div class="btns"><a class="btn t" href="{walk_all}" target="_blank" rel="noopener">🚶 Вся прогулка в Google Maps</a></div>
{stops}

<h3>Где замок (Osaka Castle)</h3>
<div class="card"><p><b>Пешком не близко:</b> от моста Ebisubashi до ворот замка Otemon <b>3,6 км, ~50 мин</b>, до главной башни 4,3 км, ~1 ч (OSRM). На карте серый пунктир.</p>
<p><b>Метро ~15-20 мин:</b> из Namba красная Midosuji 2 остановки до <b>Hommachi</b>, пересадка на <b>Chuo line (зелёная)</b> 2 остановки до <b>Tanimachi 4-chome</b> (пример по Yahoo: 16:40 → 16:53). От станции 6 мин до ворот Otemon.</p>
<p><b>Сегодня открыто:</b> главная башня до 18:00, вход до 17:30. Сад Nishinomaru до 17:00, вход до 16:30. Билеты в старые башни Sengan и Tamon продают до 15:30.</p>
<div class="verdict"><b>Два варианта:</b><br>
<b>А, спокойно (советую):</b> сегодня только Minami, а вечером решаешь, оставаться ли. Замок завтра в 12:00: башня - музей под крышей, но по прогнозу дождь с обеда.<br>
<b>Б, всё сегодня:</b> пункты 1-3 до ~16:30 → метро → замок в ~16:55: башня (вход до 17:30), закат в парке в 17:13 → назад в Namba к 18:10 (17:49 → 18:00, Tanimachi + Sennichimae, Yahoo) на вечерний неон. Минус: бегом, Kuromon и голову льва пропускаешь, сад уже закрыт.</div>
<div class="btns"><a class="btn" href="castle.html">Замок: фото и история →</a><a class="btn o" href="{gdir("Osaka Castle Main Tower", "transit", "Namba Station Osaka")}" target="_blank" rel="noopener">🚇 Из Namba к замку</a></div></div>

<h3>Если решишь остаться вечером</h3>
<div class="card"><p>Вечером Dotonbori с неоном, рядом бары и руфтопы. Карта мест с часами - на <a href="https://malexeym24.github.io/osaka-night-27d94d/">странице про вечер в Осаке</a> (раздел Minami).</p>
<p><b>Обратно:</b> красная Midosuji из Namba или Shinsaibashi в сторону Shin-Osaka / Minoh-kayano до Umeda, 8-9 мин. <b>Последний вариант по Yahoo на сегодня - в Umeda в 00:19.</b> Позже - такси, ~4 км; водителю показать: ホテルグランヴィア大阪.</p>
<div class="btns"><a class="btn o" href="{gdir(HOTEL, "transit", "Namba Station Osaka Metro")}" target="_blank" rel="noopener">🚇 В отель</a><a class="btn o" href="{gdir(HOTEL, "driving", "Ebisubashi Bridge Osaka")}" target="_blank" rel="noopener">🚕 Такси в отель</a></div></div>
<p class="foot">Поезда: Yahoo!乗換案内 на 24.10. Пешие отрезки: OSRM. Погода: JMA (11:00) и Open-Meteo. Часы: офиц. сайты и osaka-info, см. страницы мест. Фото: Wikimedia Commons.</p>'''

pts = [dict(n=s["n"], lat=s["ll"][0], lng=s["ll"][1], name=s["name"]) for s in S]
js = '''<script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.js"></script><script>
var P=%s, W=%s, H=[%f,%f], C=[%f,%f], A=[%f,%f], ST=%s;
var map=L.map('map',{scrollWheelZoom:false});
L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}',{attribution:'Tiles © Esri',maxZoom:18}).addTo(map);
function pin(t,c){return L.divIcon({className:'',html:'<div class="pin" style="background:'+c+'">'+t+'</div>',iconSize:[28,28],iconAnchor:[14,14]})}
L.marker(H,{icon:pin('H','#1d4ed8'),zIndexOffset:900}).addTo(map).bindTooltip('Hotel Granvia Osaka',{direction:'top',offset:[0,-14]});
L.polyline(ST,{color:'#dc2626',weight:5,opacity:.85,dashArray:'8 8'}).addTo(map);
W.forEach(function(l){L.polyline(l.coords,{color:'#1d4ed8',weight:4,opacity:.8}).addTo(map)});
P.forEach(function(p){L.marker([p.lat,p.lng],{icon:pin(p.n,'#be185d')}).addTo(map).bindTooltip(p.n+'. '+p.name,{direction:'top',offset:[0,-14]})});
L.marker(A,{icon:pin('A','#64748b')}).addTo(map).bindTooltip('Amerikamura',{direction:'top',offset:[0,-14]});
var cm=L.marker(C,{icon:pin('🏯','#b45309')}).addTo(map).bindTooltip('Замок Osaka',{direction:'top',offset:[0,-14]});cm.on('click',function(){location.href='castle.html'});
L.polyline([[34.669067,135.501305],C],{color:'#475569',weight:3,dashArray:'4 8'}).addTo(map).bindTooltip('до замка 3,6-4,3 км, ~50-60 мин пешком',{permanent:true,direction:'center',className:'dist'});
var walk=P.map(function(p){return [p.lat,p.lng]});
var Z={walk:walk,castle:walk.concat([C]),all:walk.concat([C,H])};
function show(k){map.fitBounds(Z[k],{padding:[28,28]});document.querySelectorAll('#sw button').forEach(function(b){b.classList.toggle('on',b.dataset.k==k)})}
document.querySelectorAll('#sw button').forEach(function(b){b.onclick=function(){show(b.dataset.k)}});show('walk');
</script>''' % (json.dumps(pts, ensure_ascii=False), json.dumps(W), H_LL[0], H_LL[1], CASTLE[0], CASTLE[1], A["ll"][0], A["ll"][1], json.dumps([list(x) for x in ST]))
extra = '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.css"><style>.dist{font:600 12px -apple-system,sans-serif;background:#fff;border:1px solid #475569}</style>'
open("today.html", "w").write(HEAD.format(t="Сегодня: Dotonbori - Osaka", extra=extra) + body + "</div>" + js + '<script src="lightbox.js?v=4" defer></script></body></html>')
print("today ok", NOW)
s = open("index.html").read()
b = '<div class="alert" style="border-color:#be185d"><b style="color:#be185d">Сегодня, сб 24.10:</b> прогулка по Dotonbori и центру + где замок → <a href="today.html"><b>открыть</b></a></div>'
if "today.html" not in s:
    open("index.html", "w").write(s.replace('</header>', '</header>' + b, 1))
