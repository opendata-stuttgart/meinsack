# meinsack - gelber Sack API

This version is unmaintained!

The new version is using Datasette + SQLite:
- Site: https://meinsack.click/
- Code: https://github.com/mfa/meinsack-datasette


## run testsuite

``docker exec -ti meinsack_web_1 py.test --nomigrations -s --pdb``


## deploy on production

```
# database
docker run -d --restart=always --name meinsack-db postgres:10

# home
docker run -d --name home -v /home/meinsack/data:/home/uid1000/meinsack aexea/aexea-base

## build container
docker build --tag=meinsack-prod .

# on first run:
docker run --rm -ti --volumes-from home -v `pwd`/sack/sack/settings/production.py:/opt/code/sack/sack/settings/production.py --link meinsack-db:db -e DJANGO_SETTINGS_MODULE=sack.settings.production --entrypoint python3 meinsack-prod manage.py reset_db
docker run --rm -ti --volumes-from home -v `pwd`/sack/sack/settings/production.py:/opt/code/sack/sack/settings/production.py --link meinsack-db:db -e DJANGO_SETTINGS_MODULE=sack.settings.production --entrypoint python3 meinsack-prod manage.py migrate
docker run --rm -ti --volumes-from home -v `pwd`/sack/sack/settings/production.py:/opt/code/sack/sack/settings/production.py --link meinsack-db:db -e DJANGO_SETTINGS_MODULE=sack.settings.production --entrypoint python3 meinsack-prod manage.py createsuperuser

## get data (or use backup)
docker run --rm -ti --volumes-from home -v `pwd`/sack/sack/settings/production.py:/opt/code/sack/sack/settings/production.py --link meinsack-db:db -e DJANGO_SETTINGS_MODULE=sack.settings.production --entrypoint python3 meinsack-prod manage.py get_streets
docker run --rm -ti --volumes-from home -v `pwd`/sack/sack/settings/production.py:/opt/code/sack/sack/settings/production.py --link meinsack-db:db -e DJANGO_SETTINGS_MODULE=sack.settings.production --entrypoint python3 meinsack-prod manage.py schaalundmueller
docker run --rm -ti --volumes-from home -v `pwd`/sack/sack/settings/production.py:/opt/code/sack/sack/settings/production.py --link meinsack-db:db -e DJANGO_SETTINGS_MODULE=sack.settings.production --entrypoint python3 meinsack-prod manage.py schaalundmueller_districts

# python
./update.sh
```


### import database dump

```
cat meinsack.pgdump | docker exec -i meinsack-db pg_restore -U postgres -d meinsack
```

### add new data for a year on production server

example for stuttgart 2020

```
docker run --rm --link meinsack-db:db -e DJANGO_SETTINGS_MODULE=sack.settings.production --entrypoint "python" meinsack-prod manage.py schaalundmueller_datafile_parsing --filename /opt/code/sack/main/data/stuttgart_2020.txt --year 2020
```
