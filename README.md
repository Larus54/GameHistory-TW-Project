# GameHistory Project - Django Edition

Applicazione ri-adattata in django del progetto "GameHistory Project - C# Edition" per la compravendita di chiavi di videogiochi.

## Installazione del programma

1. Clona la repository corrente.
```
git clone <url_repository>
```
2. Entra nella cartella del progetto e verificare di avere installato una versione di python e le sue impostazioni (pip)
```
python --version # se funziona, allora vuol dire che è presente nel sistema una versione di python, in caso contrario, scaricare python.
```
3. Attivare la shell per creare un venv pip tramite:
```
pipenv shell
```
4. Installare l'estensione di django all'interno dell'venv creato tramite il comando di prima:
```
pip install django
```
5. Ora, entra nella cartella del progetto (GameHistory Project) ed esegui la migrazione per configurare tutti i database:
```
python manage.py migrate
```
6. (Facoltativo) Creare un superuser per accedere all'admin di Django:
```
python manage.py createsuperuser <nome>
```
7. Avvia il server:
```
python manage.py runserver
```


