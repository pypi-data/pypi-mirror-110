#!/bin/bash
trap ctrl_c INT

function ctrl_c() {
    rm -rf ./django_regiment;
}

rm -rf ./django_regiment
cp -r ../django_regiment .

sed -i -e 's/PROTOCOL = "https"/PROTOCOL = "http"/; s/DOMAIN = "ingest.regiment.tech"/DOMAIN = "localhost:5002"/' ./django_regiment/bulletlog/middleware.py;

python manage.py runserver

rm -rf ./django_regiment