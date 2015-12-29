# meinsack - gelber Sack API

## run testsuite

``docker exec -ti meinsack_web_1 py.test --nomigrations -s --pdb``


## deploy on production

```
# database
docker run -d --restart=always -v /opt/meinsack/postgres:/var/lib/postgresql --name meinsack-db postgres:9.4

# home
docker run -d --name home -v /opt/dockerhome/data/meinsack:/home/uid1000/meinsack aexea/aexea-base

# on first run:
docker run --rm -ti --volumes-from home -v `pwd`/meinsack/meinsack/settings/production.py:/opt/code/meinsack/meinsack/settings/production.py --link meinsack-db:db -e DJANGO_SETTINGS_MODULE=meinsack.settings.production --entrypoint python3 meinsack-prod manage.py reset_db
docker run --rm -ti --volumes-from home -v `pwd`/meinsack/meinsack/settings/production.py:/opt/code/meinsack/meinsack/settings/production.py --link meinsack-db:db -e DJANGO_SETTINGS_MODULE=meinsack.settings.production --entrypoint python3 meinsack-prod manage.py migrate
docker run --rm -ti --volumes-from home -v `pwd`/meinsack/meinsack/settings/production.py:/opt/code/meinsack/meinsack/settings/production.py --link meinsack-db:db -e DJANGO_SETTINGS_MODULE=meinsack.settings.production --entrypoint python3 meinsack-prod manage.py createsuperuser
## get data
docker run --rm -ti --volumes-from home -v `pwd`/meinsack/meinsack/settings/production.py:/opt/code/meinsack/meinsack/settings/production.py --link meinsack-db:db -e DJANGO_SETTINGS_MODULE=meinsack.settings.production --entrypoint python3 meinsack-prod manage.py get_streets
docker run --rm -ti --volumes-from home -v `pwd`/meinsack/meinsack/settings/production.py:/opt/code/meinsack/meinsack/settings/production.py --link meinsack-db:db -e DJANGO_SETTINGS_MODULE=meinsack.settings.production --entrypoint python3 meinsack-prod manage.py schaalundmueller
docker run --rm -ti --volumes-from home -v `pwd`/meinsack/meinsack/settings/production.py:/opt/code/meinsack/meinsack/settings/production.py --link meinsack-db:db -e DJANGO_SETTINGS_MODULE=meinsack.settings.production --entrypoint python3 meinsack-prod manage.py schaalundmueller_districts

# python
./update.sh
```