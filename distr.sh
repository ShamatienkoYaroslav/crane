#!/bin/bash

rm -rf ./distr
mkdir ./distr
mkdir ./distr/lib
cp ./lib/crane.py ./distr/lib/crane.py
cp ./lib/server.py ./distr/lib/server.py
cp ./lib/utils.py ./distr/lib/utils.py
cp ./lib/ftp.py ./distr/lib/ftp.py
cp ./lib/env.py ./distr/lib/env.py
cp ./main.py ./distr/main.py
cp ./requirements.txt ./distr/requirements.txt
cp ./setup.py ./distr/setup.py
cp ./run.sh ./distr/run.sh

# mkdir temp && cd temp
# git clone crane-client
# cd crane-client
# npm i
# npm run build
# cp dist ../../distr/ui
# cd ../..
# rm -rf temp
