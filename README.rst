.. role:: shell(code)
   :language: shell

Тестовый проект для ШБР 2022.

.. image:: https://github.com/iriskis/enrollment2022/workflows/CI/badge.svg?branch=master&event=push
    :target: https://github.com/iriskis/enrollment2022/actions?query=workflow%3ACI

Что внутри?
===========
Приложение упаковано в Docker-контейнер и разворачивается с помощью Ansible.

Внутри Docker-контейнера доступны две команды: :shell:`disk-db` — утилита
для управления состоянием базы данных и :shell:`disk-api` — утилита для 
запуска REST API сервиса.

Как использовать?
=================
Как применить миграции:

.. code-block:: shell

    docker run -it \
        -e DISK_PG_URL=postgresql://user:hackme@localhost/disk \
        iriskis/enrollment2022 disk-db upgrade head

Как запустить REST API сервис локально на порту 8081:

.. code-block:: shell

    docker run -it -p 8081:8081 \
        -e DISK_PG_URL=postgresql://user:hackme@localhost/disk \
        iriskis/enrollment2022

Все доступные опции запуска любой команды можно получить с помощью
аргумента :shell:`--help`:

.. code-block:: shell

    docker run iriskis/enrollment2022 disk-db --help
    docker run iriskis/enrollment2022 disk-api --help

Опции для запуска можно указывать как аргументами командной строки, так и
переменными окружения с префиксом :shell:`DISK` (например: вместо аргумента
:shell:`--pg-url` можно воспользоваться :shell:`DISK_PG_URL`).

Как развернуть?
---------------
Чтобы развернуть и запустить сервис на серверах, добавьте список серверов в файл
deploy/hosts.ini (с установленной Ubuntu) и выполните команды:

.. code-block:: shell

    cd deploy
    ansible-playbook -i hosts.ini --user=ubuntu deploy.yml

Разработка
==========

Быстрые команды
---------------
* :shell:`make` Отобразить список доступных команд
* :shell:`make devenv` Создать и настроить виртуальное окружение для разработки
* :shell:`make postgres` Поднять Docker-контейнер с PostgreSQL
* :shell:`make lint` Проверить синтаксис и стиль кода с помощью `pylama`_
* :shell:`make clean` Удалить файлы, созданные модулем `distutils`_
* :shell:`make test` Запустить тесты
* :shell:`make sdist` Создать `source distribution`_
* :shell:`make docker` Собрать Docker-образ
* :shell:`make upload` Загрузить Docker-образ на hub.docker.com

.. _pylama: https://github.com/klen/pylama
.. _distutils: https://docs.python.org/3/library/distutils.html
.. _source distribution: https://packaging.python.org/glossary/

Как подготовить окружение для разработки?
-----------------------------------------
.. code-block:: shell

    make devenv
    make postgres
    source env/bin/activate
    disk-db upgrade head
    disk-api

После запуска команд приложение начнет слушать запросы на 0.0.0.0:8081.
