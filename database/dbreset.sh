#!/bin/env sh

echo "" > data.db
cat schema.sql | sqlite3 data.db

rm -rf images
mkdir images
