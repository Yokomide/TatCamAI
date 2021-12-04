![Logo](https://github.com/Yokomide/TatCamAI/raw/main/logo_large.png)
__Реализованная функциональность__
- Отслеживание заполняемости мусорных баков
- Отслеживание горизонтального положения человека
- Поиск информации по базе данных
- Вывод обработаной картинки на страницу веб-приложения

__Особенность проекта в следующем__
- Уведомление служб помощи, при обнаружении человека, лежащего более 40 секунд на земле
- Рейтинг районов для отслеживания оперативности работы по вывозу мусора
- Система, отслеживающая скорость заполнения баков в районах, и на основе этого, формирующая рекомендации по установке доп.контейнеров и оптимизации пути мусоровозов.

__Основной стек технологий:__

- HTML, CSS, Bootstrap
- MySQL
- Flask
- OpenCV
- GitHub

## СРЕДА ЗАПУСКА
1. Требуется установленная СУБД MySQL
2. Требуется установленный фреймворк Flask для создания веб-приложения, пакет flask_mysqldb для совместной работы Flask с MySQL, OpenCV для обработки изображений при помощи компьютерного зрения, yaml для создания конфигурационных файлов

## УСТАНОВКА

Выполните

```
pip install Flask
pip install flask-mysqldb
pip install PyYAML
pip install opencv-python
```

### База данных
Необходимо импортировать базу данных 
```
tatcamapp.sql
```
Либо создать и заполнить свою, указав в файле конфигурации свои данные.



РАЗРАБОТЧИКИ
- Гречкин Иван: Fullstack
- Мацко Егор: Разработчик AI
- Мельников Владислав: Data scientist
- Бардадымов Даниил: Разработчик AI
