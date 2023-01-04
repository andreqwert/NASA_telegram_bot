# Телеграм-бот фото NASA

При помощи кода из этого репозитория можно:
1) Скачать фотографии NASA.   
Вы можете скачать фотографии NASA с трех источников: с сайта SpaceX, c самогó сайта NASA, а также избранные крупные фото от NASA (Earth Polychromatic Imaging Camera).
2) Постить фото из выбранной папки в какой-нибудь заданный tg-канал с заранее определенной периодичностью.


## Запуск
### Запуск парсинга фото
Установите библиотеки необходимых версий:      
```
pip3 install -r requirements.txt
```
Поменяйте параметры в переменной окружения `.env`:
- `API_TOKEN` -- токен к сайту NASA;
- `TELEGRAM_BOT_TOKEN` -- токен к боту Telegram;
- `TELEGRAM_CHAT_ID` -- ID чата, в котором требуется опубликовать фото;
- `PUBLICATION_FREQ_SECONDS` -- с какой частотой будут публиковаться фото (в секундах). По умолчанию это 14400 секунд (т.е. 4 часа).

Запустите парсинг для фото источников:        
```bash
python3 fetch_nasa_images.py --save_dir='./images/nasa_images/' --images_num=50
python3 fetch_epic_images.py --save_dir='./images/epic_images/' --images_num=5
python3 fetch_spacex_images.py --save_dir='./images/spacex_images/' --launch_id='5eb87d47ffd86e000604b38a'
```
`launch_id` -- идентификатор одного из запусков, на котором успешно сделали фото. Бывает, что при запуске фото не делали;          
`save_dir` -- папка, будут сохраняться спарсенные изображения.

### Запуск телеграм-бота
Запустите телеграм-бота:     
```bash
python3 nasa_photos_poster_bot.py './images/' --limit_mb=20.0 --user_image_path './nasa_apod1.jpg'
```
Здесь обязательным аргументом выступает папка, откуда берутся фото для публикации.           
`limit_mb` -- количество мегабайт, выше которого загрузка файла не осуществится (в связи с требованиями Telegram). Если фото превышает данную величину, то будет выбрано любое другое фото из папки `./images/` для публикации.    
`user_image_path` -- путь до специфичного фото юзера. Оно будет загружено в канал первым. Далее будут грузиться случайные фото из папки `./images`.


## Цели проекта
Код написан в учебных целях.