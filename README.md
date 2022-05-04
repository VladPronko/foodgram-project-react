# Foodgram - сервис для публикации рецептов
## Доступен по адресу: **http://51.250.89.43/**
### Полный перечень эндпоинтов и примеры запросов к API можно посмотреть в документации к проекту: http://51.250.89.43/api/docs/

### Для ознакомления с проектом заведены два тестовых пользователя: ivan@yandex.ru/Qwerty1231 и lana@yandex.ru/1231231Aa


Сервис позволяет пользователям просматривать рецепты любимых блюд, а также публиковать собственные.
При регистрации пользователь указывает свой email, который будет использоваться при авторизации.
![foodgram-main](https://user-images.githubusercontent.com/74264747/130495494-1eb4c107-209a-40cd-a4ac-12f40762725b.jpg)
![foodgram-main2](https://user-images.githubusercontent.com/74264747/130495522-0bf86788-1c17-4186-af86-a2c6853262ad.jpg)

Зарегестрированные пользователи могут подписываться на авторов рецептов или добавлять рецепты в корзину, в избранное.
Есть возможность добавить понравившиеся рецепты в список покупок и затем скачать список со всеми необходимыми ингридиентами для похода в магазин.


![recipe-detail](https://user-images.githubusercontent.com/74264747/130495561-d3193e9d-c759-4b00-8562-0f2ef4e37ce3.jpg)


## Запуск проекта на виртуальном сервере:
- Склонировать проект и перейти в папку infra

```bash
git clone https://github.com/VladPronko/foodgram-project-react.git
cd infra
```
- Создайте файл `.env` командой `touch .env` и добавьте в него переменные окружения для работы с базой данных:

```
DB_NAME=postgres # имя базы данных
POSTGRES_USER=postgres # логин для подключения к базе данных
POSTGRES_PASSWORD=postgres # пароль для подключения к БД (установите свой)
DB_HOST=db # название сервиса (контейнера)
DB_POR
```bash
python3 -m venv venv
source venv\bin\activate
```
Вы можете сгенерировать ```DJANGO_SECRET_KEY``` следующим образом. 
Из директории проекта _/backend/_ выполнить:
```python
python manage.py shell
from django.core.management.utils import get_random_secret_key  
get_random_secret_key()
```
- Скопируйте файлы `docker-compose.yml`, `nginx.conf` и `.env` из папки `/infra/` на Ваш сервер:
```bash
scp <название файла> <username>@<server_ip>:/home/<username>/
```
- Далее зайдите на виртуальный сервер и подготовьте его к работе с проектом:
 
```
sudo apt update
sudo apt upgrade -y
sudo apt install python3-pip python3-venv git -y
sudo apt install curl
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh 
sudo apt install docker-compose
``` 

- Теперь можно развернуть проект с помощью Docker используя контейнеризацию:

```
sudo docker-compose up -d —build
``` 

При запуске создаются три контейнера:

```
 - контейнер базы данных **db**
 - контейнер приложения **backend**
 - контейнер web-сервера **nginx**
```

- Осталось выполнить миграции, подключить статику, создать суперюзера

```
sudo docker exec -it <name или id контейнера backend> python manage.py migrate
sudo docker exec -it <name или id контейнера backend> python manage.py collectstatic
sudo docker exec -it <name или id контейнера backend> python manage.py createsuperuser
```
- И финально подгрузить списки тегов и ингридиентов

```
sudo docker exec -it <name или id контейнера backend> python manage.py loadjson --path «recipes/data/ingredients.json"
sudo docker exec -it <name или id контейнера backend> python manage.py loadjson --path "recipes/data/tags.json"
```
