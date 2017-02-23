#!/bin/bash

rm -rf ./distr
mkdir ./distr
mkdir ./distr/lib
cp ./lib/crane.py ./distr/sdk/lib/crane.py
cp ./lib/server.py ./distr/sdk/lib/server.py
cp ./lib/utils.py ./distr/sdk/lib/utils.py
cp ./lib/ftp.py ./distr/sdk/lib/ftp.py
cp ./lib/env.py ./distr/sdk/lib/env.py
cp ./main.py ./distr/sdk/main.py
cp ./requirements.txt ./distr/sdk/requirements.txt
cp ./setup.py ./distr/sdk/setup.py
cp ./run.sh ./distr/run.sh

# mkdir temp && cd temp
# git clone crane-client
# cd crane-client
# npm i
# npm run build
# cp dist ../../distr/ui
# cd ../..
# rm -rf temp
