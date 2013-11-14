#!/bin/sh

# compile coffeescript
./node_modules/.bin/coffee --compile -o src/www/scripts/celestrium/core/ src/www/scripts/celestrium/core-coffee/ &&\
./node_modules/.bin/coffee --compile src/www/scripts/*.coffee &&\

# run server
# USAGE: python src/server.py <port>
python src/server.py 5000
