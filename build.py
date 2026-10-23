#!/usr/bin/env python3
"""Osaka sights site (24-26.10.2026). Run: python3 build.py -> index.html + one page per place.
Data: places P, day plans DAYS, hours/prices in each place (checked 24.10.2026 night, see SRC)."""
import json, html
from urllib.parse import quote

E = html.escape
HOTEL = "Hotel Granvia Osaka"
H_LL = (34.701881, 135.496338)

def gm(q):
    return "https://www.google.com/maps/search/?api=1&query=" + quote(q)

def gdir(dst, mode="transit", origin=HOTEL):
    return (f"https://www.google.com/maps/dir/?api=1&origin={quote(origin)}"
            f"&destination={quote(dst)}&travelmode={mode}")

# ---------- photo credits ----------
CR = {k: f'{v["author"] or "автор на странице файла"}, {v["lic"]}' for k, v in json.load(open("credits.json")).items()}
PAGE = {k: v["page"] for k, v in json.load(open("credits.json")).items()}
REUSE = {
    "sky-1.jpg": ("Martin Falbisoner, CC BY-SA 4.0", "https://commons.wikimedia.org/wiki/File:Umeda_Sky_Building,_Osaka,_November_2016_-02.jpg"),
    "sky-2.jpg": ("DXR, CC BY-SA 4.0", "https://commons.wikimedia.org/wiki/File:View_of_Kita-Ku,_Osaka,_from_Umeda_Sky_Building_20190415_1.jpg"),
    "hozenji-1.jpg": ("Choi2451, CC BY-SA 3.0", "https://commons.wikimedia.org/wiki/Category:Hōzen-ji_(Osaka)"),
    "hozenji-2.jpg": ("Mr.ちゅらさん, CC BY-SA 4.0", "https://commons.wikimedia.org/wiki/Category:Hōzen-ji_(Osaka)"),
    "osk-1.jpg": ("32linesky, CC BY-SA 4.0", "https://commons.wikimedia.org/wiki/File:Osaka_Dotonbori_Canal.jpg"),
    "osk-6.jpg": ("Oilstreet, CC BY 2.5", "https://commons.wikimedia.org/wiki/File:Dotonbori_Osaka_Japan01-r.jpg"),
    "osk-8.jpg": ("Sakai Yayoi, CC0", "https://commons.wikimedia.org/wiki/File:Dotonbori_ao_02.jpg"),
    "osk-10.jpg": ("Martin Falbisoner, CC BY-SA 4.0", "https://commons.wikimedia.org/wiki/File:Osaka_Castle_Outer_Moat_and_Osaka_Business_Park,_November_2016.jpg"),
    "osk-11.jpg": ("663highland, CC BY 2.5", "https://commons.wikimedia.org/wiki/File:Osaka_Castle_02bs3200.jpg"),
    "himeji-1.jpg": ("Gorgo, Public domain", "https://commons.wikimedia.org/wiki/File:Himeji_Castle_0804_1.jpg"),
    "himeji-9.jpg": ("663highland, CC BY 2.5", "https://commons.wikimedia.org/wiki/File:Himeji_Castle_01s2048.jpg"),
    "himeji-3.jpg": ("Martin Falbisoner, CC BY-SA 4.0", "https://commons.wikimedia.org/wiki/File:Himeji_Castle,_November_2016_-02.jpg"),
    "himeji-7.jpg": ("Yasuo Hamashima, CC BY-SA 4.0", "https://commons.wikimedia.org/wiki/File:Himeji_castle_20241025-_YAS2703.jpg"),
}
for k, (a, u) in REUSE.items():
    CR[k] = a; PAGE[k] = u

CAP = {
    "castle-1.jpg": "Главная башня на каменном основании", "castle-2.jpg": "Башня снизу",
    "castle-3.jpg": "Золотой карп-сятихоко на крыше, внизу парк", "castle-4.jpg": "Ворота Otemon и башня Sengan-yagura",
    "castle-5.jpg": "Башня над стенами из огромных камней", "osk-11.jpg": "Замок, рвы и небоскрёбы Business Park",
    "osk-10.jpg": "Внешний ров", "takoishi-1.jpg": "Камень Tako-ishi у ворот Sakuramon - видно масштаб по людям",
    "nishinomaru-1.jpg": "Сад Nishinomaru: газон и гостевой дом", "nishinomaru-2.jpg": "Вид на башню из сада Nishinomaru",
    "history-1.jpg": "Музей истории (овальное здание) рядом с NHK", "history-2.jpg": "Вид из музея на раскопки дворца Naniwa",
    "history-3.jpg": "Верхний этаж: реконструкция зала дворца Naniwa с придворными",
    "tenjin-1.jpg": "Вход в Tenjinbashisuji", "tenjin-2.jpg": "Крытая улица тянется 2,6 км",
    "tenmangu-1.jpg": "Ворота Osaka Tenmangu", "tenmangu-2.jpg": "Главный зал Osaka Tenmangu",
    "nakazaki-1.jpg": "Старый деревянный дом в Nakazakicho",
    "kokaido-1.jpg": "Центральный общественный зал (1918) на острове Nakanoshima",
    "kokaido-2.jpg": "Зал заседаний внутри", "kokaido-3.jpg": "Фасад из красного кирпича",
    "sky-3.jpg": "Две башни, соединённые наверху", "sky-1.jpg": "Эскалатор в стеклянной трубе",
    "sky-2.jpg": "Вид с крыши на север: река Yodo",
    "yasaka-1.jpg": "Сцена в форме головы льва, 12 м", "yasaka-2.jpg": "Пасть льва - это сцена для обрядов",
    "yasaka-3.jpg": "Нос льва вблизи",
    "osk-8.jpg": "Вывеска Glico днём", "osk-1.jpg": "Канал Dotonbori днём", "osk-6.jpg": "Улица Dotonbori, краб Kani Doraku",
    "hozenji-1.jpg": "Переулок Hozenji Yokocho", "hozenji-2.jpg": "Статуя Mizukake Fudo во мху",
    "kuromon-1.jpg": "Крытый рынок Kuromon", "kuromon-2.jpg": "Морепродукты на гриле прямо на улице",
    "kuromon-3.jpg": "Вход на рынок",
    "shinsekai-1.jpg": "Shinsekai и башня Tsutenkaku вечером", "shinsekai-2.jpg": "Крытая улица Tsutenkaku-Hondori и башня",
    "shinsekai-3.jpg": "Вывески Shinsekai", "shinsekai-4.jpg": "Вид с Tsutenkaku на юг",
    "harukas-1.jpg": "Abeno Harukas и пагода Shitennoji в сумерках", "harukas-2.jpg": "Abeno Harukas (300 м), вид с Tsutenkaku",
    "harukas-3.jpg": "Смотровая на 60 этаже, окна от пола",
    "shitennoji-1.jpg": "Пятиярусная пагода Shitennoji", "shitennoji-2.jpg": "Центральный двор: пагода и главный зал",
    "shitennoji-3.jpg": "Территория храма сверху", "shitennoji-4.jpg": "Статуи дзидзо в шапочках",
    "sumiyoshi-1.jpg": "Арочный мост Sorihashi", "sumiyoshi-2.jpg": "Главные залы - стиль Sumiyoshi-zukuri",
    "sumiyoshi-3.jpg": "С моста на главную аллею", "sumiyoshi-4.jpg": "Каменные тории",
    "expo-1.jpg": "Башня Солнца (70 м), Taro Okamoto", "expo-2.jpg": "Золотое лицо башни - оригинал в павильоне",
    "minpaku-1.jpg": "Minpaku: зал Океании", "minpaku-2.jpg": "Minpaku: зал Европы",
    "nara-1.jpg": "Daibutsuden - зал Великого Будды", "nara-2.jpg": "Daibutsuden с главной аллеи",
    "nara-3.jpg": "Олень среди каменных фонарей", "nara-4.jpg": "Олени в Nara свободно ходят по городу",
    "himeji-1.jpg": "Замок Himeji", "himeji-9.jpg": "Главная башня и малые башни", "himeji-3.jpg": "Himeji в ноябре",
    "himeji-7.jpg": "Himeji, конец октября (25.10.2024)",
}

AREAS = {
    "kita": ("У отеля · Umeda и Kita", "Пешком или 1-2 остановки"),
    "castle": ("Замок Osaka", "6 мин на метро, весь район пешком"),
    "minami": ("Юг · Namba, Shinsekai, Tennoji", "9-17 мин по красной линии Midosuji"),
    "city": ("Ещё в городе", "Если останется время"),
    "out": ("За город на полдня", "35-60 мин на поезде"),
}
RAIN = {"roof": ("🏠 под крышей", "в дождь - да"), "covered": ("☂️ крытая улица", "в дождь - да"),
        "mixed": ("⛅ часть под крышей", "в дождь - частично"), "open": ("🌳 под открытым небом", "лучше без дождя")}

from places import P
BY = {p["id"]: p for p in P}

# hours / price / closed / source - filled from the verification pass (see HRS below)
from hours import HRS
for k, v in HRS.items():
    BY[k].update(v)

# ---------- day plans ----------
ST = {  # station points for drawing train legs (approximate)
 "HUME": (34.700595, 135.499818), "MMORI": (34.6978, 135.5114), "TENMA": (34.6902, 135.5165), "TANI4": (34.68255, 135.51775),
 "NAKAZ": (34.7072, 135.5056), "TEN6": (34.710291, 135.51085),
 "UME": (34.7025, 135.4982), "YODO": (34.6930, 135.5010), "HOMM": (34.6823, 135.5009), "SHINS": (34.6750, 135.5009),
 "NAMBA": (34.6664, 135.5008), "DAIK": (34.6527, 135.4983), "DOBU": (34.6465, 135.5059), "TENNO": (34.6467, 135.5134),
}
W = json.load(open("walk.json"))["legs"]
def walk(day, a, b):
    for l in W[day]:
        if l["a"] == a and l["b"] == b:
            return dict(kind="walk", coords=l["coords"])
    raise KeyError((day, a, b))
def train(color, *names):
    return dict(kind="train", color=color, coords=[list(ST[n]) for n in names])
PURPLE, RED = "#7c3aed", "#dc2626"

DAYS = [
 dict(key="sat", label="Сб 24.10", title="Суббота 24.10 · замок, пока сухо",
      wx="Дождь до ~12-13 ч, потом облачно и в основном сухо, 22-25°. Закат 17:13.",
      why="Суббота после обеда - единственное сухое окно за три дня, а замок и сад под открытым небом. Начинаем с музея под крышей, пока дождь заканчивается. И только в сб-вс пускают внутрь старых башен замка 1620 года.",
      steps=[
        ("12:00", None, "Из отеля 7 мин пешком до станции <b>Higashi-Umeda</b>, линия <b>Tanimachi (фиолетовая)</b>, платформа 1, поезд на <b>Yaominami (八尾南)</b>. Остановки: Minami-morimachi → Temmabashi → <b>Tanimachi 4-chome</b>, 6 мин, поезда каждые ~6 мин. Выход 9.",
         [("📍 Higashi-Umeda", gm("Higashi-Umeda Station")), ("🚇 Маршрут", gdir("Osaka Museum of History"))]),
        ("12:15", "history", "Музей истории, ~1 ч. Начни с верхнего этажа (дворец Naniwa), из окон - замок.", []),
        ("13:20", "castle", "6 мин до ворот <b>Otemon</b> → внутрь башен <b>Sengan и Tamon</b> (билет вместе с садом, продают до 15:30) → сад <b>Nishinomaru</b> (вход до 16:30) → ворота Sakuramon и камень <b>Tako-ishi</b> → главная башня (вход до 17:30).", []),
        ("16:10", None, "<b>На закат, вариант А:</b> ~20 мин пешком до <b>Temmabashi</b>, Tanimachi (фиолетовая) на Dainichi (大日), 2 остановки до <b>Higashi-Umeda</b> (~5 мин), оттуда ~18 мин пешком до Umeda Sky. Или такси от замка, ~15 мин. <b>Вариант Б</b>, без спешки: остаться в замке, смотровая на 8 этаже башни открыта до 18:00.",
         [("📍 Temmabashi", gm("Temmabashi Station Osaka Metro")), ("🚕 Такси до Umeda Sky", gdir("Umeda Sky Building", "driving", "Osaka Castle"))]),
        ("16:50", "umeda-sky", "Закат в <b>17:13</b> с открытой крыши. В субботу на закат может быть очередь к лифту.", []),
        ("17:40", None, "Обратно в отель пешком ~15 мин.", [("🚶 До отеля", gdir(HOTEL, "walking", "Umeda Sky Building"))]),
      ],
      legs=[walk("sat", "H", "HUME"), train(PURPLE, "HUME", "MMORI", "TENMA", "TANI4"), walk("sat", "TANI4", "HIST"),
            walk("sat", "HIST", "OTEMON"), walk("sat", "OTEMON", "TOWER"), walk("sat", "TOWER", "NISHI"), walk("sat", "NISHI", "TENMA"),
            train(PURPLE, "TENMA", "MMORI", "HUME"), walk("sat", "HUME", "SKY"), walk("sat", "SKY", "H")],
      pins=["history", "castle", "umeda-sky"]),
 dict(key="sun", label="Вс 25.10", title="Воскресенье 25.10 · юг города, к вечеру под крышу",
      wx="Тепло 25-29°, дождь с перерывами, с ~15-16 ч сильнее. Закат 17:11.",
      why="Дождливый день: крытый рынок, частично крытые улицы Shinsekai, а к сильному дождю - смотровая Harukas под крышей. Всё на одной красной линии метро.",
      steps=[
        ("12:00", None, "Из отеля 5 мин до станции <b>Umeda</b>, линия <b>Midosuji (красная)</b>, платформа 1, поезд на <b>Tennoji</b>: Yodoyabashi → Hommachi → Shinsaibashi → <b>Namba</b>, 9 мин.",
         [("📍 Umeda (Midosuji)", gm("Umeda Station Osaka Metro Midosuji Line")), ("🚇 Маршрут", gdir("Namba Yasaka Shrine"))]),
        ("12:25", "yasaka", "От Namba 11 мин пешком. Голова льва - 15-20 мин.", []),
        ("12:55", "dotonbori", "16 мин пешком до моста Ebisubashi: канал и вывески днём, рядом переулок Hozenji.", []),
        ("13:40", "kuromon", "12 мин пешком. Обед у прилавков.", []),
        ("14:40", "shinsekai", "~18 мин пешком на юг (или метро Sakaisuji от Nippombashi 1 остановка до Ebisucho). Башня Tsutenkaku (билет на время), кушикацу.", []),
        ("15:50", "harukas", "~19 мин пешком или метро Midosuji Dobutsuen-mae → Tennoji, 1 остановка. К сильному дождю ты уже под крышей. Закат в 17:11, если облака дадут.", []),
        ("17:30", None, "<b>Tennoji → Umeda</b>, Midosuji (красная), платформа 3, поезд на Minoh-kayano (箕面萱野), 16 мин.",
         [("🚇 До отеля", gdir(HOTEL, "transit", "Tennoji Station Osaka Metro"))]),
      ],
      legs=[walk("sun", "H", "UME"), train(RED, "UME", "YODO", "HOMM", "SHINS", "NAMBA"), walk("sun", "NAMBA", "YASAKA"),
            walk("sun", "YASAKA", "EBISU"), walk("sun", "EBISU", "HOZENJI"), walk("sun", "HOZENJI", "KUROMON"),
            walk("sun", "KUROMON", "TSUTEN"), walk("sun", "TSUTEN", "HARUKAS"),
            train(RED, "TENNO", "DOBU", "DAIK", "NAMBA", "SHINS", "HOMM", "YODO", "UME")],
      pins=["yasaka", "dotonbori", "kuromon", "shinsekai", "harukas"]),
 dict(key="mon", label="Пн 26.10", title="Понедельник 26.10 · после выезда, до поезда в аэропорт",
      wx="Дождь, днём местами сильный, ветер.",
      why="Короткое окно рядом с отелем и под крышей: самая длинная крытая улица Японии ведёт прямо к святилищу. Чемодан ждёт в отеле, поезд Haruka в аэропорт уходит из-под отеля.",
      steps=[
        ("12:00", None, "Выезд (по osaka-info - до 12:00), чемодан на хранение в отеле. 7 мин до <b>Higashi-Umeda</b>, <b>Tanimachi (фиолетовая)</b>, платформа 2, поезд на <b>Dainichi (大日)</b>: Nakazakicho → <b>Tenjimbashisuji 6-chome</b>, 3 мин.",
         [("🚇 Маршрут", gdir("Tenjimbashisuji 6-chome Station"))]),
        ("12:15", "tenjin", "Пешком на юг по крытой улице ~23 мин чистой ходьбы, с обедом - около часа, до святилища Osaka Tenmangu.", []),
        ("13:45", None, "4 мин до <b>Minami-morimachi</b>, Tanimachi 1 остановка до Higashi-Umeda, 7 мин до отеля, забрать чемодан.",
         [("📍 Minami-morimachi", gm("Minami-morimachi Station"))]),
        ("14:33", None, "<b>Haruka</b> со станции Osaka, <b>платформа 21</b>, каждые 30 мин: 14:33 → аэропорт 15:27, 15:03 → 15:57, 15:33 → 16:27 (Yahoo на 26.10). В непогоду лучше не позже 15:03.",
         [("📍 JR Osaka", gm("JR Osaka Station"))]),
      ],
      legs=[walk("mon", "H", "HUME"), train(PURPLE, "HUME", "NAKAZ", "TEN6"), walk("mon", "TEN6", "TENMANGU"),
            walk("mon", "TENMANGU", "MINAMIMORI"), train(PURPLE, "MMORI", "HUME")],
      pins=["tenjin"]),
]

from weather import WX, WX_NOTE, SRC_DATE

# ---------- HTML ----------
HEAD = '''<!doctype html><html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="robots" content="noindex,nofollow"><title>{t}</title>{extra}<link rel="stylesheet" href="style.css?v=2"></head><body><div class="wrap">'''
FOOT = '</div><script src="lightbox.js?v=4" defer></script></body></html>'

def cap(f):
    return f'{E(CAP.get(f, ""))}. <a href="{E(PAGE.get(f, "#"))}">{E(CR.get(f, ""))}</a>'

def strip_pics(p, n=4):
    return "".join(f'<figure><img src="t/{f}" data-full="img/{f}" alt="{E(CAP.get(f, p["name"]))}" loading="lazy"><figcaption>{cap(f)}</figcaption></figure>'
                   for f in p["photos"][:n])

def vids(vs):
    if not vs: return ""
    return '<div class="vids">' + "".join(
        f'<a class="vid" href="https://www.youtube.com/watch?v={v["id"]}" target="_blank" rel="noopener"><img src="https://i.ytimg.com/vi/{v["id"]}/mqdefault.jpg" alt="" loading="lazy"><span>{E(v["t"])}<br><small>{E(v["ch"])} · {E(v["m"])}</small></span></a>'
        for v in vs) + '</div>'

def facts_tbl(p):
    rows = [("Часы", p.get("hours")), ("Вход", p.get("price")), ("Выходные", p.get("closed")),
            ("Наши даты", p.get("dates")), ("На месте", p.get("time")), ("Дождь", RAIN[p["rain"]][0] + ", " + RAIN[p["rain"]][1])]
    return "<table>" + "".join(f"<tr><th>{k}</th><td>{v}</td></tr>" for k, v in rows if v) + "</table>"

def place_page(p):
    grid = "".join(f'<figure class="{"w" if i == 0 else ""}"><a href="img/{f}"><img src="img/{f}" alt="{E(CAP.get(f, ""))}" loading="lazy"></a><figcaption>{cap(f)}</figcaption></figure>'
                   for i, f in enumerate(p["photos"]))
    near = "".join(f'<a class="city" href="{q}.html"><img src="t/{BY[q]["photos"][0]}" alt="{E(BY[q]["name"])}" loading="lazy"><div><b>{BY[q]["n"]}. {E(BY[q]["name"])}</b><span class="n">{E(BY[q]["sub"])}</span></div></a>' for q in p["near"])
    how = "".join(f"<li>{s}</li>" for s in p["how"])
    days = [d["label"] for d in DAYS if p["id"] in d["pins"]]
    inplan = f'<div class="verdict">В плане на <b>{", ".join(days)}</b> - <a href="index.html#{[d["key"] for d in DAYS if p["id"] in d["pins"]][0]}">смотреть день</a></div>' if days else ""
    tip = f'<div class="alert">{p["tip"]}</div>' if p.get("tip") else ""
    body = f'''<a class="back" href="index.html">← ко всем местам</a>
<header><h1><span class="pin" style="display:inline-block;vertical-align:middle;margin-right:8px">{p["n"]}</span>{E(p["name"])}</h1><div class="sub">{E(p["ja"])} · {E(AREAS[p["area"]][0])}</div></header>
{inplan}
<div class="grid">{grid}</div>
{"".join(f"<p>{E(x)}</p>" for x in p["what"])}
{tip}
<div class="card">{facts_tbl(p)}<p class="hint">Источник часов и цен: {p.get("src", "не проверял")}</p></div>
<h3>Как добраться от отеля</h3><ul>{how}</ul>
<div class="btns"><a class="btn" href="{gm(p["q"])}" target="_blank" rel="noopener">📍 Google Maps</a><a class="btn o" href="{gdir(p["q"], p["mode"])}" target="_blank" rel="noopener">{"🚶" if p["mode"] == "walking" else "🚇"} Маршрут от отеля</a></div>
{"<h3>Видео</h3>" + vids(p["vids"]) if p["vids"] else ""}
{"<h3>Рядом</h3><div class='cities'>" + near + "</div>" if near else ""}
<p class="foot">Фото: Wikimedia Commons, автор и лицензия под каждым. Поезда: Yahoo!乗換案内 на 24-26.10.2026, пешие отрезки: OSRM. Часы и цены проверены {SRC_DATE}. <a href="index.html">← ко всем местам</a></p>'''
    open(f'{p["id"]}.html', "w").write(HEAD.format(t=E(p["name"]) + " - Osaka", extra="") + body + FOOT)

def day_card(d):
    rows = ""
    for t, pid, txt, btns in d["steps"]:
        if pid:
            p = BY[pid]
            head = f'<span class="pin">{p["n"]}</span> <a href="{pid}.html"><b>{E(p["name"])}</b></a>'
            b = [("📍 Google Maps", gm(p["q"])), ("Подробнее →", f"{pid}.html")]
            pics = f'<div class="pics sm">{strip_pics(p, 3)}</div>'
        else:
            head, b, pics = "", btns, ""
        bt = "".join(f'<a class="btn{" o" if "Подробнее" in l else ""}" href="{u}"{"" if u.endswith(".html") else " target=_blank rel=noopener"}>{l}</a>' for l, u in b)
        rows += f'<div class="day"><span class="dt">{t}</span> {head}<div class="d">{txt}</div>{pics}<div class="btns">{bt}</div></div>'
    return f'''<div class="card opt" id="{d["key"]}"><h2>{E(d["title"])}</h2><div class="wxl">🌦 {E(d["wx"])}</div><div class="why">{E(d["why"])}</div>{rows}
<div class="btns"><button class="btn o showday" data-k="{d["key"]}">🗺 Показать день на карте</button></div></div>'''

def tile(p):
    r = RAIN[p["rain"]][0]
    return f'''<div class="card pl"><div class="top"><span class="pin">{p["n"]}</span><div><h2><a href="{p["id"]}.html">{E(p["name"])}</a></h2><div class="hint">{E(p["sub"])}</div></div></div>
<div class="pics">{strip_pics(p, 4)}</div>
<div class="meta">{r} · {E(p.get("short", ""))}</div>
<div class="btns"><a class="btn" href="{p["id"]}.html">Подробнее →</a><a class="btn o" href="{gm(p["q"])}" target="_blank" rel="noopener">📍 Maps</a></div></div>'''

def index():
    wx = "".join(f'<tr><td><b>{E(a)}</b></td><td>{b}</td></tr>' for a, b in WX)
    areas = ""
    for a, (t, s) in AREAS.items():
        areas += f'<h3 id="a-{a}">{E(t)}</h3><div class="hint">{E(s)}</div>' + "".join(tile(p) for p in P if p["area"] == a)
    markers = json.dumps([dict(n=p["n"], id=p["id"], name=p["name"], lat=p["ll"][0], lng=p["ll"][1], area=p["area"]) for p in P], ensure_ascii=False)
    days = json.dumps({d["key"]: dict(legs=d["legs"], pins=d["pins"]) for d in DAYS}, ensure_ascii=False)
    body = f'''<header><h1>Osaka: что посмотреть</h1><div class="sub">Сб 24 - пн 26.10.2026 · отель Granvia (станция JR Osaka) · срез {SRC_DATE}</div></header>
<div class="alert"><b>Коротко.</b> Суббота после обеда - единственное сухое окно, поэтому <b>сб = замок</b> (музей истории → замок → сад → закат на Umeda Sky). <b>Вс = юг</b> под крышей: голова льва, Dotonbori днём, рынок Kuromon, Shinsekai, вечером смотровая Harukas. <b>Пн</b> после выезда - крытая улица Tenjinbashisuji до святилища Tenmangu рядом с отелем, потом Haruka в аэропорт. Музей быта эпохи Edo (Kurashi no Konjakukan) закрыт на ремонт до 05.01.2027, поэтому его нет.</div>
<div class="card"><h2>Погода</h2><table class="wxt">{wx}</table><p class="hint">{WX_NOTE}</p></div>
<div class="vsw" id="sw"><button data-k="all" class="on">Все места</button><button data-k="sat">Сб 24</button><button data-k="sun">Вс 25</button><button data-k="mon">Пн 26</button><button data-k="out">За город</button></div>
<div id="map"></div>
<div class="legend">Синяя H - отель. Сплошная линия - пешком, пунктир - метро (цвет линии). Нажми на номер - откроется место.</div>
<div class="btns"><button class="btn o" id="me">📍 Показать, где я</button></div>
<h3>По дням</h3>
{"".join(day_card(d) for d in DAYS)}
<h3>Все места</h3><div class="hint">Номера как на карте. В каждой карточке - фото, «Подробнее» с историей, часами, входом и дорогой от отеля.</div>
{areas}
<h3>Видео</h3>{vids([v for p in P for v in p["vids"]][:6])}
<p class="foot">Срез {SRC_DATE}. Погода: Японское метеоагентство JMA (прогноз Осаки от 23.10 17:00 JST) и Open-Meteo (модели JMA MSM, ECMWF, GFS, ICON). Поезда: Yahoo!乗換案内 на 24-26.10. Пешие отрезки: OSRM. Часы и цены: официальные сайты (источник на странице места). Фото: Wikimedia Commons, автор и лицензия под каждым. Ничего не бронировалось.</p>'''
    script = '''<script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.js"></script><script>
var M=%s, D=%s, H=[%f,%f];
var map=L.map('map',{scrollWheelZoom:false});
L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}',{attribution:'Tiles © Esri',maxZoom:18}).addTo(map);
var COL={kita:'#c2410c',castle:'#b45309',minami:'#be185d',city:'#0f766e',out:'#64748b'};
var mk={};
M.forEach(function(p){var ic=L.divIcon({className:'',html:'<div class="pin" style="background:'+COL[p.area]+'">'+p.n+'</div>',iconSize:[28,28],iconAnchor:[14,14]});
 var m=L.marker([p.lat,p.lng],{icon:ic}).bindTooltip(p.n+'. '+p.name,{direction:'top',offset:[0,-14]});m.on('click',function(){location.href=p.id+'.html'});mk[p.id]=m;});
var hm=L.marker(H,{icon:L.divIcon({className:'',html:'<div class="pin h">H</div>',iconSize:[28,28],iconAnchor:[14,14]}),zIndexOffset:1000}).bindTooltip('Hotel Granvia Osaka',{direction:'top',offset:[0,-14]}).addTo(map);
var layer=L.layerGroup().addTo(map);
function show(k){layer.clearLayers();var pts=[H];
 Object.keys(mk).forEach(function(id){map.removeLayer(mk[id])});
 if(k=='all'||k=='out'){M.forEach(function(p){var o=(p.area=='out');if((k=='out')==o||k=='all'&&!o){mk[p.id].addTo(map);pts.push([p.lat,p.lng]);}});}
 else{var d=D[k];d.pins.forEach(function(id){mk[id].addTo(map);var p=M.filter(function(x){return x.id==id})[0];pts.push([p.lat,p.lng]);});
  d.legs.forEach(function(l){var o=l.kind=='walk'?{color:'#1d4ed8',weight:4,opacity:.8}:{color:l.color,weight:5,opacity:.85,dashArray:'8 8'};L.polyline(l.coords,o).addTo(layer);l.coords.forEach(function(c){pts.push(c)});});}
 map.fitBounds(pts,{padding:[24,24]});
 document.querySelectorAll('#sw button').forEach(function(b){b.classList.toggle('on',b.dataset.k==k)});}
document.querySelectorAll('#sw button').forEach(function(b){b.onclick=function(){show(b.dataset.k)}});
document.querySelectorAll('.showday').forEach(function(b){b.onclick=function(){show(b.dataset.k);document.getElementById('sw').scrollIntoView({behavior:'smooth'})}});
var h=location.hash.replace('#','');show(D[h]?h:'all');
var me=null;document.getElementById('me').onclick=function(){if(!navigator.geolocation)return;navigator.geolocation.getCurrentPosition(function(p){var ll=[p.coords.latitude,p.coords.longitude];if(me)map.removeLayer(me);me=L.circleMarker(ll,{radius:8,color:'#fff',weight:3,fillColor:'#2563eb',fillOpacity:1}).addTo(map).bindTooltip('Ты здесь');map.setView(ll,15);document.getElementById('map').scrollIntoView({behavior:'smooth'});});};
</script>''' % (markers, days, H_LL[0], H_LL[1])
    extra = '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.css">'
    open("index.html", "w").write(HEAD.format(t="Osaka: что посмотреть", extra=extra) + body + "</div>" + script + '<script src="lightbox.js?v=4" defer></script></body></html>')

for p in P:
    place_page(p)
index()
print("ok", len(P), "places")
