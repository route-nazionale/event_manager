event_manager
==================
Gestione eventi della Route Nazionale 2014


Installazione
=============
Requisiti:

* virtualenv (consigliato ma non obbligatorio)
* python 2
* django 1.7
* recaptcha-client

Procedura di installazione:

```sh
sudo apt-get install virtualenvwrapper
mkvirtualenv rn-django17
git clone git@github.com:route-nazionale/event_manager.git
cd event_manager
pip install -r requirements.txt
cp event_manager/settings_dist.py event_manager/settings.py
```
inserite nel file event_manager/settings.py le vostre chiavi RECAPTCHA Google

https://www.google.com/recaptcha/admin#whyrecaptcha

Procedura di sviluppo/test:

```sh
# per entrare nel virtualenv
workon rn-django17
cd event_manager
python manage.py runserver

# per uscire dal virtualenv
deactivate
```

Il repository contiene un DB sqlite che ha dentro alcuni dati di test.

Per provare l'applicazione potete collegarvi a http://localhost:8000/
utilizando le credenziali nome utente 'admin' e password 'admin'

