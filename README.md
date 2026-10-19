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
resource-pack-sha1=b3daa3ac56b9cc97384b8e977207a638e654c4b7
```

Опционально можно задать сообщение при скачивании:

```properties
resource-pack-prompt={"text":"Установите KisserskPack для корректного отображения","color":"light_purple"}
```

> **Важно:** `resource-pack-sha1` — это SHA-1 **самого zip-файла**, который раздаётся клиентам. Если пересобрать/перепаковать архив, хеш изменится и его нужно обновить в `server.properties`, иначе клиенты отклонят скачанный пак. Текущий хеш соответствует коммиту с файлом `KisserskPack.zip` в этом репозитории.

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
