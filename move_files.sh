#!/bin/bash

#Change import path as needed
IMPORT_PATH="/var/lib/neo4j/import"

sudo mv clean_edge.tsv "$IMPORT_PATH"
sudo cp nodes.tsv "$IMPORT_PATH"
