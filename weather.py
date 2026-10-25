# Weather as of 24.10.2026 ~03:00 JST: JMA Osaka forecast issued 23.10 17:00, Open-Meteo models (JMA MSM, ECMWF, GFS, ICON),
# JMA typhoon track for No.30, tenki.jp forecaster note 23.10.
import subprocess
SRC_DATE = subprocess.run(["date", "+%d.%m.%Y %H:%M JST"], capture_output=True, text=True).stdout.strip()
WX = [
 ("Вс 25.10, сегодня", "Облачно, временами дождь, местами до вечера сильный с грозой (JMA 11:00). Вероятность дождя 80% до 18 ч, 50% вечером. Модель JMA MSM: после 13 ч почти сухо до ~20 ч, 21-22°. Закат 17:11. Зонт с собой."),
 ("Пн 26.10", "Дождь весь день, с полудня до вечера местами сильный с грозой (JMA), вероятность 80-90%, ветер до ~12 км/ч и выше. Рейс в 19:00 из KIX - утром проверь статус рейса и поездов Haruka."),
]
WX_NOTE = "Прогноз Японского метеоагентства JMA от 25.10 11:00 и модель JMA MSM (Open-Meteo). Замок и музеи закрываются, если объявят штормовое предупреждение."
