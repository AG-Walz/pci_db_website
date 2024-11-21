# The WebApp of the Peptides for Cancer Immunotherapy Database (PCI-DB)

The website can be accessed under: 
[https://pci-db.org](https://pci-db.org)



## Test setup:

Test setup:

1) Start the dev setup with:
```
docker compose -f docker-compose.yml up -d --build
```

1.1) If there is no database in the db folder you need to create one:
 a) 
 ```
 docker run --name <postgres-container> -e POSTGRES_PASSWORD=<mysecretpassword> -v /path/to/data/directory:/var/lib/postgresql/data -d <postgres container tag>
 ```

b) create db_users database in postgres
```
docker exec -it <container ID> bash
psql -U postgres -d postgres
CREATE database db_users;
```

c) migrate change in the webapp
```
docker exec -it <container ID> bash
python manage.py migrate
```

2) Add new database version to setup
Create the database locally (outside of the setup) and dump it into a file:
```
pg_dump --no-owner --no-privileges immuno_db > immuno_db_<version/date>.pgsql
```
Then put the .pgsql file in the mount volume (here: transfer)

Connect into the container using:
```
docker exec -it <CONTAINER ID> bash
```
and locate the .pgsql file. e.g. /var/lib/transfer


Connect to the postgres and if necessary create the database.
```
psql -d immuno_db -U postgres
```

if there is already a database with the same name, drop it first:
```
DROP SCHEMA public CASCADE;
CREATE SCHEMA public;
CREATE DATABASE immuno_db;
```

Then import the database dump.
```
psql -U postgres immuno_db < dump_name.sql
```
Add the database in the settings.py

Optional:
Uf there are no models in the models.py file (which shouldn't be the case), then inspect the database and add the models to the models.py
```
python manage.py inspectdb --include-views --database <database_name>
```

## Production setup:

1) Start docker compose:
```
docker compose -f docker-compose.prod.yml up -d --build
```

2) Collect static files
```
docker compose -f docker-compose.prod.yml exec web python manage.py collectstatic --no-input --clear
```

3) Download dummy certificate and replace by actual certificate. For this port 80 and 443 needs to be open all CIDR ranges

```
chmod +x init-letsencrypt.sh
sudo ./init-letsencrypt.sh
```