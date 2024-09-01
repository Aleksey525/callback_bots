# Боты-помощники с интегрированной нейросетью
Боты для Телеграм и ВКонтакте с [DialogFlow](https://dialogflow.cloud.google.com/#/getStarted).  
`Телеграм` - [ссылка](https://t.me/ACallbackBot)  
`ВКонтакте` - [ссылка](https://vk.com/im?sel=-82796087)


### Как установить

Python3 должен быть уже установлен. Затем используйте `pip` (или `pip3`, есть конфликт с Python2) для установки зависимостей:

```

pip install -r requirements.txt

```

Также нужно создать аккаунт [DialogFlow](https://dialogflow.cloud.google.com/#/getStarted) и проект в нем:  
- [Создать проект](https://cloud.google.com/dialogflow/es/docs/quick/setup) в `DialogFlow`
- [Создать агента](https://cloud.google.com/dialogflow/es/docs/quick/build-agent) в `DialogFlow`
- [Включить API](https://cloud.google.com/dialogflow/es/docs/quick/setup#api) `DialogFlow` на вашем Google-аккаунте
- [Получить файл с ключами от вашего Google-аккаунта](https://cloud.google.com/dialogflow/es/docs/quick/setup#sdk)
- [Создать токен](https://cloud.google.com/docs/authentication/api-keys) от `DialogFlow`

### Примеры запуска ботов и обучающего скрипта
Телеграм-бот:

```
python tg_bot.py 
```

ВКонтакте-бот:
```
python vk_bot.py 
```

Скрипт для обучения [DialogFlow](https://dialogflow.cloud.google.com/#/getStarted):
```
python df_learning_script.py "Устройство на работу" 
```
Скрипт скачивает `json` файл с темами для обучения по [ссылке](https://dvmn.org/media/filer_public/a7/db/a7db66c0-1259-4dac-9726-2d1fa9c44f20/questions.json) и взаимодействует с нейросетью по API.  
Доступные темы:
- Устройство на работу
- Забыл пароль
- Удаление аккаунта
- Вопросы от забаненных
- Вопросы от действующих партнеров

### Переменные окружения

Часть настроек проекта берётся из переменных окружения. Чтобы их определить, создайте файл `.env` в корневом каталоге проекта и 
запишите туда данные в таком формате: `ПЕРЕМЕННАЯ=значение`.

Доступны 6 переменных:
- `TG_BOT_TOKEN` — API-токен телеграм-бота 
- `VK_BOT_TOKEN` — API-токен ВКонтакте-бота
- `TG_LOGGER_BOT_TOKEN` — API-токен телеграм-бота для мониторинга
- `GOOGLE_APPLICATION_CREDENTIALS` — путь до файла с ключами от Google - [Документация](https://cloud.google.com/dialogflow/es/docs/quick/setup#sdk)
- `PROJECT_ID` — идентификатор Google проекта - [Документация](https://cloud.google.com/dialogflow/es/docs/quick/setup)
- `TG_CHAT_ID` — идентификатор чата

## Цели проекта

Код написан в учебных целях — это урок в курсе по Python и веб-разработке на сайте [Devman.org](https://dvmn.org).