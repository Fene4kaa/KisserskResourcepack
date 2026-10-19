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
| `minecraft` | Кастомный шрифт `safei.ttf`, иконка таба `tab-base.png`, дополнение `default` шрифта |

### Обновлённая форма ошейника

- Прямоугольная рамка заменена восьмигранным ремнём со скошенными углами. Передняя и задняя части опущены ниже головы, плоские боковые секции лежат поверх плеч с зазором 0,05 пикселя. Ступенчатые угловые переходы соединяют эти уровни снаружи головы и плеч.
- Сохранены исходные PNG и все пять расцветок; серебряная застёжка, заклёпки и золотое кольцо перенесены на новый контур.
- В ZIP изменён только `assets/meowdoggie/models/item/collar.json`. Остальные записи, включая ресурсы алтаря, звуки и метаданные, сохранены побайтно.
- Проверены целостность ZIP, допустимые повороты элементов и геометрический предпросмотр с четырёх ракурсов. Три регрессионные проверки подтверждают отсутствие пересечений с головой, плечами и торсом и прилегание боковин к плечам на базовой модели в прямой позе, без внешних слоёв скина и брони. Проверки в Minecraft-клиенте не было. Крепление остаётся к голове, поэтому при её наклонах и анимации тела посадка меняется.

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
resource-pack-sha1=30adf081f316960115d1a470b0dcb3084eb8d762
```

Перед использованием этой ссылки опубликуйте изменённый `KisserskPack.zip` в ветке `main`. Локальная правка сама по себе не обновляет архив на GitHub; новый SHA-1 нельзя применять к прежнему удалённому файлу.

Опционально можно задать сообщение при скачивании:

```properties
resource-pack-prompt={"text":"Установите KisserskPack для корректного отображения","color":"light_purple"}
```

> **Важно:** `resource-pack-sha1` — это SHA-1 **самого zip-файла**, который раздаётся клиентам. Если пересобрать/перепаковать архив, хеш изменится и его нужно обновить в `server.properties`, иначе клиенты отклонят скачанный пак. Указанный хеш относится к локальному ZIP с восьмигранным ошейником.

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
