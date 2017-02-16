#!/bin/bash

echo 'Generate distr...'
sh distr.sh
echo 'Docker build...'
docker build -f Dockerfile_arm -t princip/crane:arm .
echo 'Docker push...'
docker push princip/crane:arm
