#!/usr/bin/env bash

# get enmapbox project
rm -rf context/enmapbox
git clone https://bitbucket.org/hu-geomatics/enmap-box.git ./context/enmapbox
# git clone https://bitbucket.org/hu-geomatics/enmap-box.git --branch develop --single-branch ./context/enmapbox
cd ./context/enmapbox/ || exit
git checkout a337c182  # checkout EnMAP-Box 3.7 as 3.8 is not compatible to QGIS 3.16
cd ../..
