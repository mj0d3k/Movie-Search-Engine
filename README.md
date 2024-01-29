# Movie-Search-Engine
University search engine for movies in Django Framework.
App runs with database in PostreSQL, but there is also JSON file "DATABASE".

HOW TO RUN APP (z pobranego zip):
- pobrać virtualenv
- aktywować venv załączone w zipie
    - Linux/macOS: source venv/bin/activate
    - Windows: venv\Scripts\activate
- LUB założyć własne środowisko wirtualne i zainstlować wymgania:
    - pip install -r requirements.txt
- pobrać PostreSQL (jeśli się nie posiada) 
    - Linux: sudo apt-get install postgresql
    - Windows: https://www.postgresql.org/download/windows/
    - macOS: https://www.postgresql.org/download/macosx/
- konfiguracja bazy danych (w razie zmianw w pliku settings.py):
    - można skorzystać z gotowych w 'settings.py', chyba że zmienia się usera, hasło i nazwe bazy danych, wtedy należy dokoanć migracji:
        - python manage.py migrate
- uruchamianie apliakcji w terminalu: 
    - python manage.py runserver uruchamia apliakcję


Dodatkowe informacje o podstawowych instalacjach:
- jeśli tworzysz własne środowisko wirtualne, a nie chcesz instlować wszytskiego z requirements, oto podstawowe biblioteki, które są konieczne:
    - Django==5.0.1
    - django-import-export==3.3.6
    - psycopg2-binary==2.9.9
    - scikit-learn==1.4.0
    - scipy==1.11.4
    - selenium==4.16.0
    - sqlparse==0.4.4
    - numpy==1.26.3

Hosting: tbc