#!/bin/bash

source ./env/bin/activate
gunicorn wedding_photo_roulette.wsgi -b 0.0.0.0:8081 -w 4
