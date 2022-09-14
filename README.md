## Описание
API социальной сети Yatube
##### API представляет следущие возможности:
* Подписываться/Отписываться на/от пользователя.
* Просматривать, создавать новые, удалять и изменять посты.
* Просматривать и создавать группы.
* Комментировать, смотреть, удалять и обновлять комментарии.
* Фильтровать выдачу.
## Установка 
Клонируем репозиторий на локальную машину:
### Как запустить проект:
Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/ssavboy/api_final_yatube.git
```

```
cd yatube_api
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv (GNU/Linux)
```

```
source venv/bin/activate (GNU/Linux)
source venv/Scripts/activate (Windows)
```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python3 manage.py migrate
```

Запустить проект:

```
python3 manage.py runserver
```
#### Документация API `http://localhost:8000/redoc/`