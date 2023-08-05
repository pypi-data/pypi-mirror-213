#!/bin/sh

pyrcc5 -o ../emid/qrc_resources.py ../resources.qrc
pylupdate5 -verbose emid.pro
lrelease -verbose emid.pro

mv *.qm ../translations/
