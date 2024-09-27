#!/bin/env sh

! test -f data.db && touch data.db
! test -d images && mkdir images

cat down.sql | sqlite3 data.db
cat up.sql | sqlite3 data.db

rm -rf images/*