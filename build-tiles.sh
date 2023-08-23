#!/bin/bash
echo "Start Time: $(date)"
git clone https://github.com/openmaptiles/openmaptiles.git
cd openmaptiles
git checkout v3.14
sed -i 's/MAX_ZOOM=7/MAX_ZOOM=17/' .env
make remove-docker-images
echo "**** Starting DB container ****"
make start-db
echo "**** Import Data ****"
make import-data
echo "**** Download Area ****"
make download area="ireland-and-northern-ireland"
echo "**** Import ****"
make import-osm area=ireland-and-northern-ireland
make import-wikidata area=ireland-and-northern-ireland
echo "**** Copy mapping file ****"
cp ../mapping.yaml build/mapping.yaml
echo "**** Import SQL ****"
make import-sql 
echo "**** Build Style ****"
make build-style
make generate-bbox-file area=ireland-and-northern-ireland
echo "**** Generate Tiles ****"
make generate-tiles-pg
ls -alh
echo "End Time: $(date)"
