
Istruzioni per il DEPLOY
========================

Assestamento
-------------

- Si va sul server di deploy <nome server>
- cd /var/www/event_manager
- git branch 

ci devono essere 2 rami: 

 * master: clone del master GitHub; 
 * deploy: modifiche solo in fase di deploy se necessarie, al volo. Dovrebbe essere il branch corrente

Aggiornamento
-------------

- sudo -i (diventa root in modo interattivo)

- cd /var/www/event_manager
- git checkout master
- git pull origin master
- git checkout deploy
- git rebase master
- ./manage.py migrate
- ./manage.py collectstatic --noinput

se dovessero essere stati aggiornati i requirements.txt 
si può fare anche un 

- pip install -r requirements.txt

CONFIGURAZIONE APACHE
---------------------

<VirtualHost *:80>
    ServerAdmin <email contatto apache2>
    ServerName <nome server>

    DocumentRoot /var/www/event_manager/
    <Directory />
        Options -FollowSymLinks
        AllowOverride None
        Order deny,allow
        Deny from all
    </Directory>

    WSGIScriptAlias / /var/www/event_manager/event_manager/wsgi_local.py
    Alias /static /var/www/event_manager_static

    <Directory /var/www/event_manager_static/>
        Order allow,deny
        Allow from all
    </Directory>

    <Directory /var/www/event_manager/>
        Order allow,deny
        Allow from all
        <Files event_manager/wsgi_local.py>
            Require all granted
        </Files>
    </Directory>

    ErrorLog ${APACHE_LOG_DIR}/event_manager_error.log

    # Possible values include: debug, info, notice, warn, error, crit,
    # alert, emerg.
    LogLevel warn

    CustomLog ${APACHE_LOG_DIR}/event_manager_access.log combined


</VirtualHost>

NOTE
----

Ho installato un po'' di pacchetti

$ sudo apt-get install python-pip ipython vim python-mysqldb ipython-doc python-distribute libapache2-mod-wsgi git libmysqlclient-dev


e seguendo la guida

$ sudo pip install -r requirements.txt (Django + recaptcha)

e anche la localizzazione italiana it_IT.UTF-8

$ sudo dpkg-reconfigure locales 

