#!/bin/sh

docker build --tag=meinsack-prod .
docker rm -f meinsack
docker run -d --volumes-from home --link meinsack-db:db -v `pwd`/meinsack/meinsack/settings/production.py:/opt/code/meinsack/meinsack/settings/production.py --restart=always -p 8010:8010  --name meinsack meinsack-prod
