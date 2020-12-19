Setup-DATABASE

    CREATE DATABASE classifieds;

    CREATE USER classifieds_admin WITH PASSWORD '=mK7Y[UJnSg5z^~8';

    ALTER ROLE classifieds_admin SET client_encoding TO 'utf8';
    ALTER ROLE classifieds_admin SET default_transaction_isolation TO 'read committed';
    ALTER ROLE classifieds_admin SET timezone TO 'UTC';

    GRANT ALL PRIVILEGES ON DATABASE classifieds TO classifieds_admin;

Python3 and Django Setup

    - VirtualEnv
         - sudo -H pip3 install --upgrade pip - (upgrade pip)
         - sudo -H pip3 install virtualenv - (install VirtualENV)

         - mkdir ~/classified - (Create a project Directory)
         - cd classified - (cd into project)
         - virtualenv classifiedenv (Create a VirtualENV)
         - source classifiedenv/bin/activate (to activate VirtualENV)
         - pip3 install gunicorn psycopg2 - (Make sure Ubuntu/OS build-tools have been installed)

    - Setup - Gunicorn
        - sudo nano /etc/systemd/system/gunicorn.service
        - sudo systemctl daemon-reload
        - sudo systemctl restart gunicorn
        - sudo systemctl status gunicorn
        - sudo journalctl -u gunicorn (to check gunicorn logs)
    
    - Setup - nginx 
        - sudo nano /etc/nginx/sites-available/classified
        - sudo nginx -t
        - sudo systemctl restart nginx