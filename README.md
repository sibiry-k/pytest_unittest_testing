# <p align='center'> Pytest & Unittest</p>  
## Тесты для двух приложений (**ya_news** и **ya_note**):

```
Dev
 └── django_testing
     ├── ya_news
     │   ├── news
     │   │   ├── fixtures/
     │   │   ├── migrations/
     │   │   ├── pytest_tests/   <- Директория с вашими тестами pytest для проекта ya_news
     │   │   ├── __init__.py
     │   │   ├── admin.py
     │   │   ├── apps.py
     │   │   ├── forms.py
     │   │   ├── models.py
     │   │   ├── urls.py
     │   │   └── views.py
     │   ├── templates/
     │   ├── yanews/
     │   ├── manage.py
     │   └── pytest.ini
     ├── ya_note
     │   ├── notes
     │   │   ├── migrations/
     │   │   ├── tests/          <- Директория с вашими тестами unittest для проекта ya_note
     │   │   ├── __init__.py
     │   │   ├── admin.py
     │   │   ├── apps.py
     │   │   ├── forms.py
     │   │   ├── models.py
     │   │   ├── urls.py
     │   │   └── views.py
     │   ├── templates/
     │   ├── yanote/
     │   ├── manage.py
     │   └── pytest.ini
     ├── .gitignore
     ├── README.md
     ├── requirements.txt
     └── structure_test.py
```

## Для запуска тестов:
1. Создать и активировать виртуальное окружение; установить зависимости из файла `requirements.txt`;
2. Запустить скрипт для `run_tests.sh` из корневой директории проекта:
```sh
bash run_tests.sh
```
