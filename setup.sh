#!/bin/bash

pip3 install virtualenv
virtualenv .
source ./bin/activate
pip3 install -r requrements.txt
