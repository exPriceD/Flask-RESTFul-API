# RESTful API приложение
Проект сделан на основе лабораторной работы 0.4 по дисциплине программирование ИКТ 2023-2024

## Цель
Разработать RESTful API приложение, позволяющий принимать запросы и возвращать результаты работы. Приложение должно поддерживать операции GET/POST/PUT/PATCH/DELETE для большей части объектов/моделейя. 

## Ход работы
В ходе работы был создан API с использованием микрофреймворка Flask.
Были определены пути для работы с тремя моделями: Schedule, Personalities и Groups, 
а также разработаны методы GET, POST, PUT и DELETE для каждой модели.

## Модели
```
class Lessons(db.Model):
     id = db.Column(db.Integer, primary_key=True)
     group = db.Column(db.String(6))
     day = db.Column(db.String(16))
     even_week = db.Column(db.Boolean)
     subject = db.Column(db.String(64))
     type = db.Column(db.String(32))
     time_start = db.Column(db.String(5))
     time_end = db.Column(db.String(5))
     teacher_name = db.Column(db.String(128))
     room = db.Column(db.String(32))
     address = db.Column(db.String(512))
     zoom_url = db.Column(db.String(1024))
```
```
class Personalities(db.Model):
     id = db.Column(db.Integer, primary_key=True)
     fio = db.Column(db.String(256))
     gender = db.Column(db.String(32))
     phone = db.Column(db.String(32))
     email = db.Column(db.String(256))
     work = db.Column(db.String(512))
     education = db.Column(db.String(512))
```
```
class Groups(db.Model):
     id = db.Column(db.Integer, primary_key=True)
     name = db.Column(db.String(6))
     faculty = db.Column(db.String(512))
     direction = db.Column(db.String(512))
     people_count = db.Column(db.Integer)
```
## Маршруты и Эндпоинты
#### 1. Schedule
```GET /api/v1/schedule``` - возвращает список всех записей в модели Schedule.

```GET /api/v1/schedule/id/<int: id>``` - возвращает запись с указанным ID.

```GET /api/v1/schedule/name/<string: group_name>``` - возвращает список записей с указанным номером группы.

```GET /api/v1/schedule/name/<string: group>/<string: week_number>``` -
возвращает список записей по номеру группы c указанием номера недели
или четности недели.

```GET /api/v1/schedule/name/<string: group>/<string: week_number>/<day>``` -
возвращает список записей по номеру группы c указанием номера недели
или четности недели, а также дню недели (цифра от 1 до 7 или название
дня из набора ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday',
'sunday'] (регистр не важен)).

```POST /api/v1/schedule``` - создает новую запись в модели Schedule.

```PUT /api/v1/schedule/id/<int: id>``` - обновляет запись с указанным ID в
модели Schedule.

```DELETE /api/v1/schedule/<int: id>``` - удаляет запись с указанным ID из
модели Schedule.\

#### 2. Personalities
```GET /api/v1/personalities``` - возвращает список всех персоналий в модели
Personalities.

```GET /api/v1/personalities/id/<int: id>``` - возвращает запись с указанным ID.

```GET /api/v1/personalities/email/<string: email>``` - возвращает запись с
указанным email.

```GET /api/v1/personalities/phone/<string: phone>``` - возвращает запись с
указанным номером телефона.

```POST /api/v1/personalities``` - создает новую персону в модели Personalities.

```PUT /api/v1/personalities/id/<int: id>``` - обновляет персоналию с указанным
ID.

```PUT /api/v1/personalities/email/<string: email>``` - обновляет персоналию с
указанным email.

```PUT /api/v1/personalities/phone/<string: phone>``` - обновляет персоналию с
указанным номером телефона.

```DELETE /api/v1/personalities/<int: id>``` - удаляет персоналию с заданным ID
из модели Personalities.

#### 3. Groups
```GET /api/v1/groups``` - возвращает список всех групп в модели Groups.

```GET /api/v1/groups/id/<int: id>``` - возвращает запись с указанным ID.

```GET /api/v1/groups/name/<string: group_name>``` - возвращает запись с
указанным номером группы.

```POST /api/v1/groups``` - создает новую группу в модели Groups.

```PUT /api/v1/groups/id/<int: id>```- обновляет группу с указанным ID в модели
Groups.

```PUT /api/v1/groups/name/<string: group_name>``` - обновляет группу с
указанным номером в модели Groups.

```DELETE /api/v1/groups/<int: id>``` - удаляет группу с заданным ID из модели
Groups
