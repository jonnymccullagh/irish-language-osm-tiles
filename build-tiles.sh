#!/bin/bash
PATH_TO_NGINX_CONF=/etc/nginx/sites-available/learscail.openstreetmap.ie.conf
PATH_TO_WEB_FILES=/var/www/learscail.openstreetmap.ie
cd $PATH_TO_WEB_FILES
git clone https://github.com/openmaptiles/openmaptiles.git
cd openmaptiles
git checkout v3.14
sed -i 's/MAX_ZOOM=7/MAX_ZOOM=17/' .env
make remove-docker-images
make start-db
make import-data
make download area="ireland-and-northern-ireland"
make import-osm area=ireland-and-northern-ireland
make import-wikidata area=ireland-and-northern-ireland
cp ./mapping.yaml build/mapping.yaml
make import-sql 
make build-style
make generate-bbox-file area=ireland-and-northern-ireland
make generate-tiles-pg
# Copy files to web directory
cp -r ./data/tiles.mbtiles $PATH_TO_WEB_FILES/tiles.mbtiles



