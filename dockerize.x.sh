#!/bin/bash

echo 'Generate distr...'
sh distr.sh
echo 'Docker build...'
docker build -f Dockerfile_x -t princip/crane:x .
echo 'Docker push...'
docker push princip/crane:x
