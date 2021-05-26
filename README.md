# Progetto Covid

## Setup

La prima cosa da fare è clonare la repository:

```sh
git https://github.com/massaroPietro/covid-italia.git
cd covid-italia
```

Crea un ambiente virtuale in cui installare le dipendenze e attivarlo:

```sh
python -m venv v_env
cd v_env/Scripts
activate
```

Adesso installare le dipendenze:

```sh
cd../..
pip install -r requirements.txt
```

Notare `(v_env)` davanti al prompt. Questo indica che questa sessione del terminale opera in un ambiente virtuale 
impostato da `python -m venv v_env` e tutti pacchetti che verranno scaricati saranno installati in quest'ultimo. In
questo modo non saranno installati globalmente sul pc, infatti, cancellando l'ambiente saranno cancellati i pacchetti. 


Quando `pip` avrà finito di scaricare le dipendenze crea le migrazioni:

```sh
python manage.py makemigrations
python manage.py migrate
```

Adesso puoi avviare il server di sviluppo:

```sh
python manage.py runserver
```
E segui il link sul browser `http://127.0.0.1:8000/`.

## Extra

Se vuoi accedere al database bisogna creare un super utente:

```sh
python manage.py createsuperuser
```

Avvia di nuovo il server di sviluppo, segui il link `http://127.0.0.1:8000/admin/` e inserisci le credenziali 
precedentemente immesse.





