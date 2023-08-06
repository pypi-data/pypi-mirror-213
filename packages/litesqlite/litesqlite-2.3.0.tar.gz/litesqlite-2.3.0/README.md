<h1 align="center">EasySqlite

<h3 align="center">Теперь вам не нужно каждый раз устанавливать соединение, писать sql-запрос и закрывать соединение. Данная библиотека сделает это за вас

Она поддерживает как синхронную, так и асинхронную работу

</h3>

```python

from easysqlite import Sqlite, AioSqlite, DataTypes

# Создаём объект класса Sqlite, передавая в него имя базы данных

db = Sqlite('database.db')

# Создаём таблицу users с столбцами id, name, age и sex

# В качестве альтернативы DataTypes вы можете просто передать тип текстом

db.create_table('users', {'id': DataTypes.INTEGER(autoincrement=True, primary_key=True), 'name': DataTypes.TEXT(not_null=True), 'age': DataTypes.INTEGER(), 'sex': DataTypes.TEXT(default='М')})

  

# Добавляем людей

db.insert_data('users', {'name': 'Анна', 'age': 20, 'sex': 'Ж'})

db.insert_data('users', {'name': 'Евгений', 'age': 31})

db.insert_data('users', {'name': 'Сергей', 'age': 17})

  

# Выбираем всех людей

# '*' указывается для того, чтоб выбрать все столбцы, а fetchall - для того чтобы получить все записи списком, без него будет первая попавшая запись

people = db.select_data('users', '*', fetchall=True)

print(people)

  

# Выбираем id и имена всех мужчин

# В where передаём уточнение, где ищем. В данном случае везде, где пол - мужской

men = db.select_data('users', ['id', 'name'], where={'sex': 'М'}, fetchall=True)

print(men)

  

# Прибавляем 2 года к текущему возрасту Анны

# Если не передавать аргумент sign, то значение обновится на 2. Но мы передаём знак '+', чтобы к текущему значению прибавить 2

db.update_data('users', {'age': 2} , where={'name': 'Анна'}, sign='+')

  

# Выбираем возраст Анны

anna = db.select_data('users', ['age'], where={'name': 'Анна'})

print(anna)

  

# Удаляем Сергея

db.delete_data('users', where={'name': 'Сергей'})

```

  

## Ну а для асинхронной работы всё то же самое, только использовать вместо Sqlite - Aiosqlite и во всех методах использовать ключевое слово 'await'. Ну, надеюсь, знаете, что такое асинхронность и как с ней работать:)

  

[![Typing SVG](https://readme-typing-svg.herokuapp.com?color=%2336BCF7&lines=Удачи😉)](https://git.io/typing-svg)
