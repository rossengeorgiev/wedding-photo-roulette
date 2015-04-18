#!/bin/bash

# create virtual py enviroment and activate
virtualenv --clear env
source ./env/bin/activate

# install deps
pip install -r requirements.txt

# generate secret_key
python -c "from random import SystemRandom; r=SystemRandom(); print ''.join([r.choice('abcdefghipqrstuvwxyz0123456789@#$%^&*(-_=+)') for i in range(50)])" > secret_key.txt

# init database
python manage.py migrate
