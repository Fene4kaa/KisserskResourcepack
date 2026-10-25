# KisserskResourcepack

Ресурспак для Minecraft Java Edition (Kissersk + MeowGuild Altar).

- **Версия игры:** 1.21.9 – 1.21.10 (pack format 88.0, `min_format`/`max_format`)
- **Формат:** `.zip`, структура с `pack.mcmeta` в корне
- **Авторы:** Feni4ka, ItsKitsuRai

## Содержимое

| Namespace | Что внутри |
|---|---|
| `judgmentnight` | Звуки события: `intro_start`, `intro_mid`, `intro_end`, `kill`, `victory`, `active_start`, `reveal_glow` |
| `meowdoggie` | Ошейники (collar): модели, item-определения и текстуры (black, blue, green, purple, red, gold, silver, leather) |
| `meowguild` | Алтарь: модели `altar_core` и `runic_pedestal`, текстуры, шрифт `altar_schemes`, локализация `ru_ru`/`en_us` |
| `minecraft` | Кастомный шрифт `safei.ttf`, иконка таба `tab-base.png`, дополнение `default` шрифта; **скрытие тоста «не удалось скачать пак»**: пустые `download.pack.failed` и `download.pack.title` в 143 языках и прозрачный `textures/gui/sprites/toast/system.png` (см. ниже) |

### Обновлённая форма ошейника

- Восьмигранная форма со скошенными углами сохранена. Для плотной посадки надетый ошейник сужен на 8% по ширине и на 2% в глубину. Передняя и задняя секции с фурнитурой подняты на 0,2 пикселя: верх ремня находится на 0,06 пикселя ниже головы. Плоские боковины остаются на 0,05 пикселя над плечами; угловые переходы подогнаны без пересечений.
- Сохранены исходные PNG и все пять расцветок; серебряная застёжка, заклёпки и золотое кольцо перенесены на новый контур.
- В ZIP изменён только `assets/meowdoggie/models/item/collar.json`. Остальные записи, включая ресурсы алтаря, звуки и метаданные, сохранены побайтно.
- Проверены целостность ZIP, допустимые повороты элементов и геометрический предпросмотр с четырёх ракурсов. Пять регрессионных проверок контролируют пересечения с головой, плечами и торсом, опору боковин на плечи и небольшие зазоры под головой и по бокам. Проверки относятся к базовой модели в прямой позе, без внешних слоёв скина и брони. В Minecraft-клиенте не проверялось; при наклонах головы и анимации тела посадка меняется.

### Скрытие тоста «не удалось скачать пак» (для плагина MeowAntiXray)

Плагин [MeowAntiXray](https://github.com/Fene4kaa/MeowAntiXray) (модуль защиты от обхода бана) при входе игрока предлагает клиенту десятки служебных паков с недоступным адресом; клиент показывает по тосту «не удалось скачать» на каждый. Чтобы игрок их не видел, в этот пак добавлены 144 записи (содержимое остальных 46 записей и `pack.mcmeta` не менялось, сверено при сборке):

- `assets/minecraft/lang/<язык>.json` для 143 языков клиента с двумя пустыми ключами `download.pack.failed` и `download.pack.title`;
- `assets/minecraft/textures/gui/sprites/toast/system.png`: полностью прозрачный спрайт 160x32.

Побочный эффект: текст этих двух тостов пуст всегда, а фон «системного» тоста прозрачен у всех системных уведомлений клиента (его используют и другие тосты). Если вам это не нужно, верните архив с тега `pre-evasion-pack` (хеш в таблице ниже). В Minecraft-клиенте 26.2 скрытие не проверялось.

Проверка готового ZIP из корня этого репозитория (Python 3, без сторонних зависимостей):

```bash
python -B -m unittest discover -s tests -v
```

## Установка (клиент)

1. Скачайте [`KisserskPack.zip`](KisserskPack.zip).
2. Положите файл в `.minecraft/resourcepacks/`.
3. В игре: **Настройки → Наборы ресурсов** → включите `KisserskPack`.
4. Нажмите **Готово**.

## Установка (сервер)

Загрузите `KisserskPack.zip` на любой HTTPS-хостинг, доступный игрокам, и укажите его в `server.properties`.

### Вариант с GitHub (raw)

```properties
resource-pack=https://raw.githubusercontent.com/Fene4kaa/KisserskResourcepack/main/KisserskPack.zip
resource-pack-sha1=2571cda5d8f0da5a2d258ed251b2480557115273
```

Архив в ветке `main` содержит текущую версию; указанный SHA-1 соответствует опубликованному `KisserskPack.zip`. После замены архива пересчитайте хеш и обновите `server.properties`, иначе клиенты отклонят скачанный пак.

Опционально можно задать сообщение при скачивании:

```properties
resource-pack-prompt={"text":"Установите KisserskPack для корректного отображения","color":"light_purple"}
```

> **Важно:** `resource-pack-sha1` — это SHA-1 **самого zip-файла**, который раздаётся клиентам. Если пересобрать/перепаковать архив, хеш изменится и его нужно обновить в `server.properties`, иначе клиенты отклонят скачанный пак. Указанный хеш относится к опубликованному ZIP с восьмигранным ошейником и скрытием тоста. Файлы GitHub raw кэшируются на несколько минут: после замены архива подождите, прежде чем менять хеш на сервере.

### История хешей (для отката)

| Тег / коммит | `KisserskPack.zip` SHA-1 | Что изменилось |
|---|---|---|
| `pre-evasion-pack` (`fafb4d6`) | `517453c16593d2777a8054339fdf94a29d47080d` | Версия до скрытия тоста |
| `1f7e93b` «Hide the failed-download toast» | `2571cda5d8f0da5a2d258ed251b2480557115273` | + 144 записи для скрытия тоста |

Откат: `git checkout pre-evasion-pack -- KisserskPack.zip`, затем вернуть `resource-pack-sha1=517453c16593d2777a8054339fdf94a29d47080d`.

Актуальный хеш можно проверить так:

```bash
sha1sum KisserskPack.zip
# Windows PowerShell:
Get-FileHash .\KisserskPack.zip -Algorithm SHA1
```

## Обновление пака

1. Замените `KisserskPack.zip` в репозитории.
2. Пересчитайте SHA-1.
3. Обновите `resource-pack-sha1` в `server.properties`.
4. Перезапустите сервер (или выполните `reload`, если плагин/ядро поддерживает перечитывание настроек).

## Служебные паки для MeowAntiXray (`evasion-packs/`)

Папка `evasion-packs/` содержит файлы, которые плагин [MeowAntiXray](https://github.com/Fene4kaa/MeowAntiXray) выдаёт клиентам при определении повторного входа (защита от обхода бана): `1.zip` ... `62.zip` (проб-паки, по ~190 байт) и `hide.zip` (то же скрытие тоста отдельным паком, 48 КБ). **Игрокам их скачивать вручную не нужно.**

Файлы построены плагином (`PackFactory`, `track: 62`, `pack-format.min: 88`, `pack-format.max: 1000`) побайтно воспроизводимо, а клиент сверяет их SHA-1. Поэтому **не меняйте и не перепаковывайте их вручную**: плагин при старте и после `/axray reload` скачивает `1.zip` и сверяет хеш. Если вы поменяли `evasion.track` или `evasion.pack-format.*` в конфиге плагина, пересоздайте файлы (плагин экспортирует их в `plugins/MeowAntiXray/evasion/packs/`) и замените папку.

Конфиг плагина для этого репозитория:

```yaml
evasion:
  enabled: true
  public-url: "https://raw.githubusercontent.com/Fene4kaa/KisserskResourcepack/main/evasion-packs"
  hide-toast-pack: false   # скрытие тоста уже внутри KisserskPack.zip
```

Подробности: `docs/EVASION_GUIDE.md` и `docs/EVASION_INTERNALS.md` в репозитории плагина.
